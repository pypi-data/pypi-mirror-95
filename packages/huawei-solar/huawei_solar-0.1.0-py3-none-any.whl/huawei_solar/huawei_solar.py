"""
Get production and status information from the Huawei Inverter using Modbus over TCP
"""
import asyncio
import logging
import time
from collections import namedtuple
from datetime import datetime

import pytz
from pymodbus.client.asynchronous import schedulers
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException as ModbusConnectionException

LOGGER = logging.getLogger(__name__)

RegisterDefinitions = namedtuple(
    "RegisterDefinitions", "type unit gain register length"
)
GridCode = namedtuple("GridCode", "standard country")
Result = namedtuple("Result", "value unit")
Alarm = namedtuple("Alarm", "name id level")


# pylint: disable=too-few-public-methods
class HuaweiSolar:
    """Interface to the Huawei solar inverter"""

    def __init__(self, host, port="502", timeout=5, wait=2):
        self.client = ModbusTcpClient(host, port=port, timeout=timeout)
        self._time_offset = None
        self.connected = False
        self.wait = wait

    # pylint: disable=too-many-branches, too-many-statements
    def get(self, name):
        """get named register from device"""
        reg = REGISTERS[name]
        response = self.read_register(reg.register, reg.length)

        if reg.type == "str":
            result = response.decode("utf-8", "replace").strip("\0")

        elif reg.type == "u16" and reg.unit == "status_enum":
            result = DEVICE_STATUS_DEFINITIONS.get(response.hex(), "unknown/invalid")

        elif reg.type == "u16" and reg.unit == "storage_status_enum":
            result = STORAGE_STATUS_DEFINITIONS.get(response.hex(), "unknown/invalid")

        elif reg.type == "u16" and reg.unit == "storage_working_mode_enum":
            result = STORAGE_WORKING_MODES.get(response.hex(), "unknown/invalid")

        elif reg.type == "u16" and reg.unit == "storage_time_of_use_price_enum":
            result = STORAGE_TOU_PRICE.get(response.hex(), "unknown/invalid")

        elif reg.type == "u16" and reg.unit == "grid_enum":
            tmp = int.from_bytes(response, byteorder="big")
            result = GRID_CODES.get(
                tmp, GridCode("unknown/not implemented", "unknown/not implemented")
            )

        elif reg.type == "u32" and reg.unit == "epoch":
            tmp = int.from_bytes(response, byteorder="big")
            if self._time_offset is None:
                self._time_offset = self.get("time_zone").value
            try:
                tmp2 = datetime.utcfromtimestamp(tmp - 60 * self._time_offset)
            except OverflowError:
                tmp2 = datetime.utcfromtimestamp(0)
                LOGGER.debug(
                    "Received invalid time value: %s (time_offset = %s)",
                    tmp,
                    self._time_offset,
                )

            # don't use local time information and use UTC time
            # which we got from systemtime - time zone offset.
            # not yet sure about the is_dst setting
            result = pytz.utc.normalize(pytz.utc.localize(tmp2, is_dst=True))

        elif reg.type == "u16" or reg.type == "u32":
            tmp = int.from_bytes(response, byteorder="big")
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "i16":
            tmp = int.from_bytes(response, byteorder="big")
            if (tmp & 0x8000) == 0x8000:
                # result is actually negative
                tmp = -((tmp ^ 0xFFFF) + 1)
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "i32":
            tmp = int.from_bytes(response, byteorder="big")
            if (tmp & 0x80000000) == 0x80000000:
                # result is actually negative
                tmp = -((tmp ^ 0xFFFFFFFF) + 1)
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "alarm_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            alarm_codes = ALARM_CODES[name]
            for key in alarm_codes:
                if key & code:
                    result.append(alarm_codes[key])

        elif reg.type == "state_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_1:
                if key & code:
                    result.append(STATE_CODES_1[key])

        elif reg.type == "state_opt_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_2:
                bit = key & code
                if bit:
                    result.append(STATE_CODES_2[key][1])
                else:
                    result.append(STATE_CODES_2[key][0])

        elif reg.type == "state_opt_bitfield32":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_3:
                bit = key & code
                if bit:
                    result.append(STATE_CODES_3[key][1])
                else:
                    result.append(STATE_CODES_3[key][0])

        else:
            result = int.from_bytes(response, byteorder="big")

        return Result(result, reg.unit)

    def close_connection(self):
        self.client.close()
        self.connected = False

    def read_register(self, register, length):
        """
        Read register from device
        5 tries and then we give up.
        Consistently works after 3 tries if we haven't made requests for a while;
        for sequential requests 1 try is enough from the second request.
        With faster timeout it goes faster, but also fails more than 3 times.
        It seems to only support connections from one device at the same time.
        """
        i = 0
        if not self.connected:
            self.client.connect()
            self.connected = True
            time.sleep(self.wait)
        while i < 5:
            try:
                response = self.client.read_holding_registers(register, length)
            except ModbusConnectionException as ex:
                LOGGER.exception("failed to connect to device, is the host correct?")
                raise ConnectionException(ex)
            if not response.isError():
                break
            self.client.close()
            self.client.connect()
            time.sleep(self.wait)

            LOGGER.debug("Failed reading register %s time(s)", i)
            i = i + 1
        else:
            message = (
                "could not read register value, is an other device already connected?"
            )
            LOGGER.error(message)
            raise ReadException(message)
        return response.encode()[1:]


class AsyncHuaweiSolar:
    """Async interface to the Huawei solar inverter"""

    def __init__(self, host, port="502", timeout=5, loop=None):
        # pylint: disable=unpacking-non-sequence
        LOGGER.debug("creating loop and client")
        self.loop, self.client = AsyncModbusTCPClient(
            schedulers.ASYNC_IO, port=port, host=host, loop=loop
        )
        LOGGER.debug("created loop and client")
        self.timeout = timeout
        self._time_offset = None

    # pylint: disable=too-many-branches, too-many-statements
    async def get(self, name):
        """get named register from device"""
        reg = REGISTERS[name]
        response = await self.read_register(self.client, reg.register, reg.length)

        if reg.type == "str":
            result = response.decode("utf-8").strip("\0")

        elif reg.type == "u16" and reg.unit == "status_enum":
            result = DEVICE_STATUS_DEFINITIONS[response.hex()]

        elif reg.type == "u16" and reg.unit == "grid_enum":
            tmp = int.from_bytes(response, byteorder="big")
            result = GRID_CODES[tmp]

        elif reg.type == "u32" and reg.unit == "epoch":
            tmp = int.from_bytes(response, byteorder="big")
            if self._time_offset is None:
                self._time_offset = self.get("time_zone").value
            tmp2 = datetime.utcfromtimestamp(tmp - 60 * self._time_offset)
            # don't use local time information and use UTC time
            # which we got from systemtime - time zone offset.
            # not yet sure about the is_dst setting
            result = pytz.utc.normalize(pytz.utc.localize(tmp2, is_dst=True))

        elif reg.type == "u16" or reg.type == "u32":
            tmp = int.from_bytes(response, byteorder="big")
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "i16":
            tmp = int.from_bytes(response, byteorder="big")
            if (tmp & 0x8000) == 0x8000:
                # result is actually negative
                tmp = -((tmp ^ 0xFFFF) + 1)
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "i32":
            tmp = int.from_bytes(response, byteorder="big")
            if (tmp & 0x80000000) == 0x80000000:
                # result is actually negative
                tmp = -((tmp ^ 0xFFFFFFFF) + 1)
            if reg.gain == 1:
                result = tmp
            else:
                result = tmp / reg.gain

        elif reg.type == "alarm_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            alarm_codes = ALARM_CODES[name]
            for key in alarm_codes:
                if key & code:
                    result.append(alarm_codes[key])

        elif reg.type == "state_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_1:
                if key & code:
                    result.append(STATE_CODES_1[key])

        elif reg.type == "state_opt_bitfield16":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_2:
                bit = key & code
                if bit:
                    result.append(STATE_CODES_2[key][1])
                else:
                    result.append(STATE_CODES_2[key][0])

        elif reg.type == "state_opt_bitfield32":
            code = int.from_bytes(response, byteorder="big")
            result = []
            for key in STATE_CODES_3:
                bit = key & code
                if bit:
                    result.append(STATE_CODES_3[key][1])
                else:
                    result.append(STATE_CODES_3[key][0])

        else:
            result = int.from_bytes(response, byteorder="big")

        return Result(result, reg.unit)

    async def read_register(self, client, register, length):
        """
        Async read register from device
        5 tries and then we give up.
        Consistently works after 3 tries if we haven't made requests for a while;
        for sequential requests 1 try is enough from the second request.
        With faster timeout it goes faster, but also fails more than 3 times.
        It seems to only support connections from one device at the same time.
        """
        for i in range(1, 6):
            if not client.connected:
                message = "failed to connect to device, is the host correct?"
                LOGGER.exception(message)
                raise ConnectionException(message)
            try:
                response = await asyncio.wait_for(
                    client.protocol.read_holding_registers(register, length),
                    timeout=self.timeout,
                )
                return response.encode()[1:]
            except asyncio.TimeoutError:
                LOGGER.debug("Failed reading register %s time(s)", i)
            except ModbusConnectionException:
                message = (
                    "could not read register value, "
                    "is an other device already connected?"
                )
                LOGGER.error(message)
                raise ReadException(message)
        # errors are different with async pymodbus,
        # we should not be able to reach this code. Keep it for debugging
        message = "could not read register value for unknown reason"
        LOGGER.error(message)
        raise ReadException(message)


class ConnectionException(Exception):
    """Exception connecting to device"""


class ReadException(Exception):
    """Exception reading register from device"""


REGISTERS = {
    "model_name": RegisterDefinitions("str", None, 1, 30000, 15),
    "serial_number": RegisterDefinitions("str", None, 1, 30015, 10),
    "model_id": RegisterDefinitions("u16", None, 1, 30070, 1),
    "nb_pv_strings": RegisterDefinitions("u16", None, 1, 30071, 1),
    "nb_mpp_tracks": RegisterDefinitions("u16", None, 1, 30072, 1),
    "rated_power": RegisterDefinitions("u32", "W", 1, 30073, 2),
    "P_max": RegisterDefinitions("u32", "W", 1, 30075, 2),
    "S_max": RegisterDefinitions("u32", "VA", 1, 30077, 2),
    "Q_max_out": RegisterDefinitions("i32", "VAr", 1, 30079, 2),
    "Q_max_in": RegisterDefinitions("i32", "VAr", 1, 30081, 2),
    "state_1": RegisterDefinitions("state_bitfield16", None, 1, 32000, 1),
    "state_2": RegisterDefinitions("state_opt_bitfield16", None, 1, 32002, 1),
    "state_3": RegisterDefinitions("state_opt_bitfield32", None, 1, 32003, 2),
    "alarm_1": RegisterDefinitions("alarm_bitfield16", None, 1, 32008, 1),
    "alarm_2": RegisterDefinitions("alarm_bitfield16", None, 1, 32009, 1),
    "alarm_3": RegisterDefinitions("alarm_bitfield16", None, 1, 32010, 1),
    "pv_01_voltage": RegisterDefinitions("i16", "V", 10, 32016, 1),
    "pv_01_current": RegisterDefinitions("i16", "A", 100, 32017, 1),
    "pv_02_voltage": RegisterDefinitions("i16", "V", 10, 32018, 1),
    "pv_02_current": RegisterDefinitions("i16", "A", 100, 32019, 1),
    "pv_03_voltage": RegisterDefinitions("i16", "V", 10, 32020, 1),
    "pv_03_current": RegisterDefinitions("i16", "A", 100, 32021, 1),
    "pv_04_voltage": RegisterDefinitions("i16", "V", 10, 32022, 1),
    "pv_04_current": RegisterDefinitions("i16", "A", 100, 32023, 1),
    "pv_05_voltage": RegisterDefinitions("i16", "V", 10, 32024, 1),
    "pv_05_current": RegisterDefinitions("i16", "A", 100, 32025, 1),
    "pv_06_voltage": RegisterDefinitions("i16", "V", 10, 32026, 1),
    "pv_06_current": RegisterDefinitions("i16", "A", 100, 32027, 1),
    "pv_07_voltage": RegisterDefinitions("i16", "V", 10, 32028, 1),
    "pv_07_current": RegisterDefinitions("i16", "A", 100, 32029, 1),
    "pv_08_voltage": RegisterDefinitions("i16", "V", 10, 32030, 1),
    "pv_08_current": RegisterDefinitions("i16", "A", 100, 32031, 1),
    "pv_09_voltage": RegisterDefinitions("i16", "V", 10, 32032, 1),
    "pv_09_current": RegisterDefinitions("i16", "A", 100, 32033, 1),
    "pv_10_voltage": RegisterDefinitions("i16", "V", 10, 32034, 1),
    "pv_10_current": RegisterDefinitions("i16", "A", 100, 32035, 1),
    "pv_11_voltage": RegisterDefinitions("i16", "V", 10, 32036, 1),
    "pv_11_current": RegisterDefinitions("i16", "A", 100, 32037, 1),
    "pv_12_voltage": RegisterDefinitions("i16", "V", 10, 32038, 1),
    "pv_12_current": RegisterDefinitions("i16", "A", 100, 32039, 1),
    "pv_13_voltage": RegisterDefinitions("i16", "V", 10, 32040, 1),
    "pv_13_current": RegisterDefinitions("i16", "A", 100, 32041, 1),
    "pv_14_voltage": RegisterDefinitions("i16", "V", 10, 32042, 1),
    "pv_14_current": RegisterDefinitions("i16", "A", 100, 32043, 1),
    "pv_15_voltage": RegisterDefinitions("i16", "V", 10, 32044, 1),
    "pv_15_current": RegisterDefinitions("i16", "A", 100, 32045, 1),
    "pv_16_voltage": RegisterDefinitions("i16", "V", 10, 32046, 1),
    "pv_16_current": RegisterDefinitions("i16", "A", 100, 32047, 1),
    "pv_17_voltage": RegisterDefinitions("i16", "V", 10, 32048, 1),
    "pv_17_current": RegisterDefinitions("i16", "A", 100, 32049, 1),
    "pv_18_voltage": RegisterDefinitions("i16", "V", 10, 32050, 1),
    "pv_18_current": RegisterDefinitions("i16", "A", 100, 32051, 1),
    "pv_19_voltage": RegisterDefinitions("i16", "V", 10, 32052, 1),
    "pv_19_current": RegisterDefinitions("i16", "A", 100, 32053, 1),
    "pv_20_voltage": RegisterDefinitions("i16", "V", 10, 32054, 1),
    "pv_20_current": RegisterDefinitions("i16", "A", 100, 32055, 1),
    "pv_21_voltage": RegisterDefinitions("i16", "V", 10, 32056, 1),
    "pv_21_current": RegisterDefinitions("i16", "A", 100, 32057, 1),
    "pv_22_voltage": RegisterDefinitions("i16", "V", 10, 32058, 1),
    "pv_22_current": RegisterDefinitions("i16", "A", 100, 32059, 1),
    "pv_23_voltage": RegisterDefinitions("i16", "V", 10, 32060, 1),
    "pv_23_current": RegisterDefinitions("i16", "A", 100, 32061, 1),
    "pv_24_voltage": RegisterDefinitions("i16", "V", 10, 32062, 1),
    "pv_24_current": RegisterDefinitions("i16", "A", 100, 32063, 1),
    "input_power": RegisterDefinitions("i32", "W", 1, 32064, 2),
    "grid_voltage": RegisterDefinitions("u16", "V", 10, 32066, 1),
    "line_voltage_A_B": RegisterDefinitions("u16", "V", 10, 32066, 1),
    "line_voltage_B_C": RegisterDefinitions("u16", "V", 10, 32067, 1),
    "line_voltage_C_A": RegisterDefinitions("u16", "V", 10, 32068, 1),
    "phase_A_voltage": RegisterDefinitions("u16", "V", 10, 32069, 1),
    "phase_B_voltage": RegisterDefinitions("u16", "V", 10, 32070, 1),
    "phase_C_voltage": RegisterDefinitions("u16", "V", 10, 32071, 1),
    "grid_current": RegisterDefinitions("i32", "A", 1000, 32072, 2),
    "phase_A_current": RegisterDefinitions("i32", "A", 1000, 32072, 2),
    "phase_B_current": RegisterDefinitions("i32", "A", 1000, 32074, 2),
    "phase_C_current": RegisterDefinitions("i32", "A", 1000, 32076, 2),
    "day_active_power_peak": RegisterDefinitions("i32", "W", 1, 32078, 2),
    "active_power": RegisterDefinitions("i32", "W", 1, 32080, 2),
    "reactive_power": RegisterDefinitions("i32", "VA", 1, 32082, 2),
    "power_factor": RegisterDefinitions("i16", None, 1000, 32084, 1),
    "grid_frequency": RegisterDefinitions("u16", "Hz", 100, 32085, 1),
    "efficiency": RegisterDefinitions("u16", "%", 100, 32086, 1),
    "internal_temperature": RegisterDefinitions("i16", "°C", 10, 32087, 1),
    "insulation_resistance": RegisterDefinitions("u16", "MOhm", 100, 32088, 1),
    "device_status": RegisterDefinitions("u16", "status_enum", 1, 32089, 1),
    "fault_code": RegisterDefinitions("u16", None, 1, 32090, 1),
    "startup_time": RegisterDefinitions("u32", "epoch", 1, 32091, 2),
    "shutdown_time": RegisterDefinitions("u32", "epoch", 1, 32093, 2),
    "accumulated_yield_energy": RegisterDefinitions("u32", "kWh", 100, 32106, 2),
    # last contact with server?
    "unknown_time_1": RegisterDefinitions("u32", "epoch", 1, 32110, 2),
    # something todo with startup time?
    "unknown_time_2": RegisterDefinitions("u32", "epoch", 1, 32156, 2),
    # something todo with shutdown time?
    "unknown_time_3": RegisterDefinitions("u32", "epoch", 1, 32160, 2),
    # installation time?
    "unknown_time_4": RegisterDefinitions("u32", "epoch", 1, 35113, 2),
    "storage_status": RegisterDefinitions("i16", "storage_status_enum", 1, 37000, 1),
    "storage_charge_discharge_power": RegisterDefinitions("i32", "W", 1, 37001, 2),
    "storage_current_day_charge_capacity": RegisterDefinitions(
        "u32", "kWh", 100, 37015, 2
    ),
    "storage_current_day_discharge_capacity": RegisterDefinitions(
        "u32", "kWh", 100, 37017, 2
    ),
    "power_meter_active_power": RegisterDefinitions("i32", "W", 1, 37113, 2),
    "grid_A_voltage": RegisterDefinitions("i32", "V", 10, 37101, 2),
    "grid_B_voltage": RegisterDefinitions("i32", "V", 10, 37103, 2),
    "grid_C_voltage": RegisterDefinitions("i32", "V", 10, 37105, 2),
    "active_grid_A_current": RegisterDefinitions("i32", "I", 100, 37107, 2),
    "active_grid_B_current": RegisterDefinitions("i32", "I", 100, 37109, 2),
    "active_grid_C_current": RegisterDefinitions("i32", "I", 100, 37111, 2),
    "active_grid_power_factor": RegisterDefinitions("i16", None, 1000, 37117, 1),
    "active_grid_frequency": RegisterDefinitions("i16", "Hz", 100, 37118, 1),
    "grid_exporterd_energy": RegisterDefinitions("i32", "kWh", 100, 37119, 2),
    "grid_accumulated_energy": RegisterDefinitions("u32", "kWh", 100, 37121, 2),
    "active_grid_A_B_voltage": RegisterDefinitions("i32", "V", 10, 37126, 2),
    "active_grid_B_C_voltage": RegisterDefinitions("i32", "V", 10, 37128, 2),
    "active_grid_C_A_voltage": RegisterDefinitions("i32", "V", 10, 37130, 2),
    "active_grid_A_power": RegisterDefinitions("i32", "W", 1, 37132, 2),
    "active_grid_B_power": RegisterDefinitions("i32", "W", 1, 37134, 2),
    "active_grid_C_power": RegisterDefinitions("i32", "W", 1, 37136, 2),
    "daily_yield_energy": RegisterDefinitions("u32", "kWh", 100, 32114, 2),
    "nb_optimizers": RegisterDefinitions("u16", None, 1, 37200, 1),
    "nb_online_optimizers": RegisterDefinitions("u16", None, 1, 37201, 1),
    "system_time": RegisterDefinitions("u32", "epoch", 1, 40000, 2),
    # seems to be the same as unknown_time_4
    "unknown_time_5": RegisterDefinitions("u32", "epoch", 1, 40500, 2),
    "grid_code": RegisterDefinitions("u16", "grid_enum", 1, 42000, 1),
    "time_zone": RegisterDefinitions("i16", "min", 1, 43006, 1),
    "storage_working_mode": RegisterDefinitions(
        "i16", "storage_working_mode_enum", 1, 47004, 1
    ),
    "storage_time_of_use_price": RegisterDefinitions(
        "i16", "storage_tou_price_enum", 1, 47027, 1
    ),
    "storage_lcoe": RegisterDefinitions("u32", None, 1000, 47069, 2),
    "storage_maximum_charging_power": RegisterDefinitions("u32", "W", 1, 47075, 2),
    "storage_maximum_discharging_power": RegisterDefinitions("u32", "W", 1, 47077, 2),
    "storage_power_limit_grid_tied_point": RegisterDefinitions("i32", "W", 1, 47079, 2),
    "storage_charging_cutoff_capacity": RegisterDefinitions("u16", "%", 10, 47081, 1),
    "storage_discharging_cutoff_capacity": RegisterDefinitions(
        "u16", "%", 10, 47082, 1
    ),
    "storage_forced_charging_and_discharging_period": RegisterDefinitions(
        "u16", "min", 1, 47083, 1
    ),
    "storage_forced_charging_and_discharging_power": RegisterDefinitions(
        "i32", "min", 1, 47084, 2
    ),
}


DEVICE_STATUS_DEFINITIONS = {
    "0000": "Standby: initializing",
    "0001": "Standby: detecting insulation resistance",
    "0002": "Standby: detecting irradiation",
    "0003": "Standby: grid detecting",
    "0100": "Starting",
    "0200": "On-grid",
    "0201": "Grid Connection: power limited",
    "0202": "Grid Connection: self-derating",
    "0300": "Shutdown: fault",
    "0301": "Shutdown: command",
    "0302": "Shutdown: OVGR",
    "0303": "Shutdown: communication disconnected",
    "0304": "Shutdown: power limited",
    "0305": "Shutdown: manual startup required",
    "0306": "Shutdown: DC switches disconnected",
    "0307": "Shutdown: rapid cutoff",
    "0308": "Shutdown: input underpowered",
    "0401": "Grid scheduling: cosphi-P curve",
    "0402": "Grid scheduling: Q-U curve",
    "0403": "Grid scheduling: PF-U curve",
    "0404": "Grid scheduling: dry contact",
    "0405": "Grid scheduling: Q-P curve",
    "0500": "Spot-check ready",
    "0501": "Spot-checking",
    "0600": "Inspecting",
    "0700": "AFCI self check",
    "0800": "I-V scanning",
    "0900": "DC input detection",
    "0a00": "Running: off-grid charging",
    "a000": "Standby: no irradiation",
}

STORAGE_STATUS_DEFINITIONS = {
    "0": "offline",
    "1": "standby",
    "2": "running",
    "3": "fault",
    "4": "sleep mode",
}

STORAGE_WORKING_MODES = {
    "0": "unlimited",
    "1": "grid connection with zero power",
    "2": "grid connection with limited power",
}

STORAGE_TOU_PRICE = {"0": "disable", "1": "enable"}

# pylint: disable=fixme
GRID_CODES = {
    0: GridCode("VDE-AR-N-4105", "Germany"),
    1: GridCode("NB/T 32004", "China"),
    2: GridCode("UTE C 15-712-1(A)", "France"),
    3: GridCode("UTE C 15-712-1(B)", "France"),
    4: GridCode("UTE C 15-712-1(C)", "France"),
    5: GridCode("VDE 0126-1-1-BU", "Bulgary"),
    6: GridCode("VDE 0126-1-1-GR(A)", "Greece"),
    7: GridCode("VDE 0126-1-1-GR(B)", "Greece"),
    8: GridCode("BDEW-MV", "Germany"),
    9: GridCode("G59-England", "UK"),
    10: GridCode("G59-Scotland", "UK"),
    11: GridCode("G83-England", "UK"),
    12: GridCode("G83-Scotland", "UK"),
    13: GridCode("CEI0-21", "Italy"),
    14: GridCode("EN50438-CZ", "Czech Republic"),
    15: GridCode("RD1699/661", "Spain"),
    16: GridCode("RD1699/661-MV480", "Spain"),
    17: GridCode("EN50438-NL", "Netherlands"),
    18: GridCode("C10/11", "Belgium"),
    19: GridCode("AS4777", "Australia"),
    20: GridCode("IEC61727", "General"),
    21: GridCode("Custom (50 Hz)", "Custom"),
    22: GridCode("Custom (60 Hz)", "Custom"),
    23: GridCode("CEI0-16", "Italy"),
    24: GridCode("CHINA-MV480", "China"),
    25: GridCode("CHINA-MV", "China"),
    26: GridCode("TAI-PEA", "Thailand"),
    27: GridCode("TAI-MEA", "Thailand"),
    28: GridCode("BDEW-MV480", "Germany"),
    29: GridCode("Custom MV480 (50 Hz)", "Custom"),
    30: GridCode("Custom MV480 (60 Hz)", "Custom"),
    31: GridCode("G59-England-MV480", "UK"),
    32: GridCode("IEC61727-MV480", "General"),
    33: GridCode("UTE C 15-712-1-MV480", "France"),
    34: GridCode("TAI-PEA-MV480", "Thailand"),
    35: GridCode("TAI-MEA-MV480", "Thailand"),
    36: GridCode("EN50438-DK-MV480", "Denmark"),
    37: GridCode("Japan standard (50 Hz)", "Japan"),
    38: GridCode("Japan standard (60 Hz)", "Japan"),
    39: GridCode("EN50438-TR-MV480", "Turkey"),
    40: GridCode("EN50438-TR", "Turkey"),
    41: GridCode("C11/C10-MV480", "Belgium"),
    42: GridCode("Philippines", "Philippines"),
    43: GridCode("Philippines-MV480", "Philippines"),
    44: GridCode("AS4777-MV480", "Australia"),
    45: GridCode("NRS-097-2-1", "South Africa"),
    46: GridCode("NRS-097-2-1-MV480", "South Africa"),
    47: GridCode("KOREA", "South Korea"),
    48: GridCode("IEEE 1547-MV480", "USA"),
    49: GridCode("IEC61727-60Hz", "General"),
    50: GridCode("IEC61727-60Hz-MV480", "General"),
    51: GridCode("CHINA_MV500", "China"),
    52: GridCode("ANRE", "Romania"),
    53: GridCode("ANRE-MV480", "Romania"),
    54: GridCode("ELECTRIC RULE NO.21-MV480", "California, USA"),
    55: GridCode("HECO-MV480", "Hawaii, USA"),
    56: GridCode("PRC_024_Eastern-MV480", "Eastern USA"),
    57: GridCode("PRC_024_Western-MV480", "Western USA"),
    58: GridCode("PRC_024_Quebec-MV480", "Quebec, Canada"),
    59: GridCode("PRC_024_ERCOT-MV480", "Texas, USA"),
    60: GridCode("PO12.3-MV480", "Spain"),
    61: GridCode("EN50438_IE-MV480", "Ireland"),
    62: GridCode("EN50438_IE", "Ireland"),
    63: GridCode("IEEE 1547a-MV480", "USA"),
    64: GridCode("Japan standard (MV420-50 Hz)", "Japan"),
    65: GridCode("Japan standard (MV420-60 Hz)", "Japan"),
    66: GridCode("Japan standard (MV440-50 Hz)", "Japan"),
    67: GridCode("Japan standard (MV440-60 Hz)", "Japan"),
    68: GridCode("IEC61727-50Hz-MV500", "General"),
    70: GridCode("CEI0-16-MV480", "Italy"),
    71: GridCode("PO12.3", "Spain"),
    72: GridCode("Japan standard (MV400-50 Hz)", "Japan"),
    73: GridCode("Japan standard (MV400-60 Hz)", "Japan"),
    74: GridCode("CEI0-21-MV480", "Italy"),
    75: GridCode("KOREA-MV480", "South Korea"),
    76: GridCode("Egypt ETEC", "Egypt"),
    77: GridCode("Egypt ETEC-MV480", "Egypt"),
    78: GridCode("CHINA_MV800", "China"),
    79: GridCode("IEEE 1547-MV600", "USA"),
    80: GridCode("ELECTRIC RULE NO.21-MV600", "California, USA"),
    81: GridCode("HECO-MV600", "Hawaii, USA"),
    82: GridCode("PRC_024_Eastern-MV600", "Eastern USA"),
    83: GridCode("PRC_024_Western-MV600", "Western USA"),
    84: GridCode("PRC_024_Quebec-MV600", "Quebec, Canada"),
    85: GridCode("PRC_024_ERCOT-MV600", "Texas, USA"),
    86: GridCode("IEEE 1547a-MV600", "USA"),
    87: GridCode("EN50549-LV", "Ireland"),
    88: GridCode("EN50549-MV480", "Ireland"),
    89: GridCode("Jordan-Transmission", "Jordan"),
    90: GridCode("Jordan-Transmission-MV480", "Jordan"),
    91: GridCode("NAMIBIA", "Namibia"),
    92: GridCode("ABNT NBR 16149", "Brazil"),
    93: GridCode("ABNT NBR 16149-MV480", "Brazil"),
    94: GridCode("SA_RPPs", "South Africa"),
    95: GridCode("SA_RPPs-MV480", "South Africa"),
    96: GridCode("INDIA", "India"),
    97: GridCode("INDIA-MV500", "India"),
    98: GridCode("ZAMBIA", "Zambia"),
    99: GridCode("ZAMBIA-MV480", "Zambia"),
    100: GridCode("Chile", "Chile"),
    101: GridCode("Chile-MV480", "Chile"),
    102: GridCode("CHINA-MV500-STD", "China"),
    103: GridCode("CHINA-MV480-STD", "China"),
    104: GridCode("Mexico-MV480", "Mexico"),
    105: GridCode("Malaysian", "Malaysia"),
    106: GridCode("Malaysian-MV480", "Malaysia"),
    107: GridCode("KENYA_ETHIOPIA", "East Africa"),
    108: GridCode("KENYA_ETHIOPIA-MV480", "East Africa"),
    109: GridCode("G59-England-MV800", "UK"),
    110: GridCode("NEGERIA", "Negeria"),
    111: GridCode("NEGERIA-MV480", "Negeria"),
    112: GridCode("DUBAI", "Dubai"),
    113: GridCode("DUBAI-MV480", "Dubai"),
    114: GridCode("Northern Ireland", "Northern Ireland"),
    115: GridCode("Northern Ireland-MV480", "Northern Ireland"),
    116: GridCode("Cameroon", "Cameroon"),
    117: GridCode("Cameroon-MV480", "Cameroon"),
    118: GridCode("Jordan Distribution", "Jordan"),
    119: GridCode("Jordan Distribution-MV480", "Jordan"),
    120: GridCode("Custom MV600-50 Hz", "Custom"),
    121: GridCode("AS4777-MV800", "Australia"),
    122: GridCode("INDIA-MV800", "India"),
    123: GridCode("IEC61727-MV800", "General"),
    124: GridCode("BDEW-MV800", "Germany"),
    125: GridCode("ABNT NBR 16149-MV800", "Brazil"),
    126: GridCode("UTE C 15-712-1-MV800", "France"),
    127: GridCode("Chile-MV800", "Chile"),
    128: GridCode("Mexico-MV800", "Mexico"),
    129: GridCode("EN50438-TR-MV800", "Turkey"),
    130: GridCode("TAI-PEA-MV800", "Thailand"),
    133: GridCode("NRS-097-2-1-MV800", "South Africa"),
    134: GridCode("SA_RPPs-MV800", "South Africa"),
    135: GridCode("Jordan-Transmission-MV800", "Jordan"),
    136: GridCode("Jordan-Distribution-MV800", "Jordan"),
    137: GridCode("Egypt ETEC-MV800", "Egypt"),
    138: GridCode("DUBAI-MV800", "Dubai"),
    139: GridCode("SAUDI-MV800", "Saudi Arabia"),
    140: GridCode("EN50438_IE-MV800", "Ireland"),
    141: GridCode("EN50549-MV800", "Ireland"),
    142: GridCode("Northern Ireland-MV800", "Northern Ireland"),
    143: GridCode("CEI0-21-MV800", "Italy"),
    144: GridCode("IEC 61727-MV800-60Hz", "General"),
    145: GridCode("NAMIBIA_MV480", "Namibia"),
    146: GridCode("Japan (LV202-50 Hz)", "Japan"),
    147: GridCode("Japan (LV202-60 Hz)", "Japan"),
    148: GridCode("Pakistan-MV800", "Pakistan"),
    149: GridCode("BRASIL-ANEEL-MV800", "Brazil"),
    150: GridCode("Israel-MV800", "Israel"),
    151: GridCode("CEI0-16-MV800", "Italy"),
    152: GridCode("ZAMBIA-MV800", "Zambia"),
    153: GridCode("KENYA_ETHIOPIA-MV800", "East Africa"),
    154: GridCode("NAMIBIA_MV800", "Namibia"),
    155: GridCode("Cameroon-MV800", "Cameroon"),
    156: GridCode("NIGERIA-MV800", "Nigeria"),
    157: GridCode("ABUDHABI-MV800", "Abu Dhabi"),
    158: GridCode("LEBANON", "Lebanon"),
    159: GridCode("LEBANON-MV480", "Lebanon"),
    160: GridCode("LEBANON-MV800", "Lebanon"),
    161: GridCode("ARGENTINA-MV800", "Argentina"),
    162: GridCode("ARGENTINA-MV500", "Argentina"),
    163: GridCode("Jordan-Transmission-HV", "Jordan"),
    164: GridCode("Jordan-Transmission-HV480", "Jordan"),
    165: GridCode("Jordan-Transmission-HV800", "Jordan"),
    166: GridCode("TUNISIA", "Tunisia"),
    167: GridCode("TUNISIA-MV480", "Tunisia"),
    168: GridCode("TUNISIA-MV800", "Tunisia"),
    169: GridCode("JAMAICA-MV800", "Jamaica"),
    170: GridCode("AUSTRALIA-NER", "Australia"),
    171: GridCode("AUSTRALIA-NER-MV480", "Australia"),
    172: GridCode("AUSTRALIA-NER-MV800", "Australia"),
    173: GridCode("SAUDI", "Saudi Arabia"),
    174: GridCode("SAUDI-MV480", "Saudi Arabia"),
    175: GridCode("Ghana-MV480", "Ghana"),
    176: GridCode("Israel", "Israel"),
    177: GridCode("Israel-MV480", "Israel"),
    178: GridCode("Chile-PMGD", "Chile"),
    179: GridCode("Chile-PMGD-MV480", "Chile"),
    180: GridCode("VDE-AR-N4120-HV", "Germany"),
    181: GridCode("VDE-AR-N4120-HV480", "Germany"),
    182: GridCode("VDE-AR-N4120-HV800", "Germany"),
    183: GridCode("IEEE 1547-MV800", "USA"),
    184: GridCode("Nicaragua-MV800", "Nicaragua"),
    185: GridCode("IEEE 1547a-MV800", "USA"),
    186: GridCode("ELECTRIC RULE NO.21-MV800", "California, USA"),
    187: GridCode("HECO-MV800", "Hawaii, USA"),
    188: GridCode("PRC_024_Eastern-MV800", "Eastern USA"),
    189: GridCode("PRC_024_Western-MV800", "Western USA"),
    190: GridCode("PRC_024_Quebec-MV800", "Quebec, Canada"),
    191: GridCode("PRC_024_ERCOT-MV800", "Texas, USA"),
    192: GridCode("Custom-MV800-50Hz", "Custom"),
    193: GridCode("RD1699/661-MV800", "Spain"),
    194: GridCode("PO12.3-MV800", "Spain"),
    195: GridCode("Mexico-MV600", "Mexico"),
    196: GridCode("Vietnam-MV800", "Vietnam"),
    197: GridCode("CHINA-LV220/380", "China"),
    198: GridCode("SVG-LV", "Dedicated"),
    199: GridCode("Vietnam", "Vietnam"),
    200: GridCode("Vietnam-MV480", "Vietnam"),
    201: GridCode("Chile-PMGD-MV800", "Chile"),
    202: GridCode("Ghana-MV800", "Ghana"),
    203: GridCode("TAIPOWER", "Taiwan"),
    204: GridCode("TAIPOWER-MV480", "Taiwan"),
    205: GridCode("TAIPOWER-MV800", "Taiwan"),
    206: GridCode("IEEE 1547-LV208", "USA"),
    207: GridCode("IEEE 1547-LV240", "USA"),
    208: GridCode("IEEE 1547a-LV208", "USA"),
    209: GridCode("IEEE 1547a-LV240", "USA"),
    210: GridCode("ELECTRIC RULE NO.21-LV208", "USA"),
    211: GridCode("ELECTRIC RULE NO.21-LV240", "USA"),
    212: GridCode("HECO-O+M+H-LV208", "USA"),
    213: GridCode("HECO-O+M+H-LV240", "USA"),
    214: GridCode("PRC_024_Eastern-LV208", "USA"),
    215: GridCode("PRC_024_Eastern-LV240", "USA"),
    216: GridCode("PRC_024_Western-LV208", "USA"),
    217: GridCode("PRC_024_Western-LV240", "USA"),
    218: GridCode("PRC_024_ERCOT-LV208", "USA"),
    219: GridCode("PRC_024_ERCOT-LV240", "USA"),
    220: GridCode("PRC_024_Quebec-LV208", "USA"),
    221: GridCode("PRC_024_Quebec-LV240", "USA"),
    222: GridCode("ARGENTINA-MV480", "Argentina"),
    223: GridCode("Oman", "Oman"),
    224: GridCode("Oman-MV480", "Oman"),
    225: GridCode("Oman-MV800", "Oman"),
    226: GridCode("Kuwait", "Kuwait"),
    227: GridCode("Kuwait-MV480", "Kuwait"),
    228: GridCode("Kuwait-MV800", "Kuwait"),
    229: GridCode("Bangladesh", "Bangladesh"),
    230: GridCode("Bangladesh-MV480", "Bangladesh"),
    231: GridCode("Bangladesh-MV800", "Bangladesh"),
    232: GridCode("Chile-Net_Billing", "Chile"),
    233: GridCode("EN50438-NL-MV480", "Netherlands"),
    234: GridCode("Bahrain", "Bahrain"),
    235: GridCode("Bahrain-MV480", "Bahrain"),
    236: GridCode("Bahrain-MV800", "Bahrain"),
    238: GridCode("Japan-MV550-50Hz", "Japan"),
    239: GridCode("Japan-MV550-60Hz", "Japan"),
    241: GridCode("ARGENTINA", "Argentina"),
    242: GridCode("KAZAKHSTAN-MV800", "Kazakhstan"),
    243: GridCode("Mauritius", "Mauritius"),
    244: GridCode("Mauritius-MV480", "Mauritius"),
    245: GridCode("Mauritius-MV800", "Mauritius"),
    246: GridCode("Oman-PDO-MV800", "Oman"),
    247: GridCode("EN50438-SE", "Sweden"),
    248: GridCode("TAI-MEA-MV800", "Thailand"),
    249: GridCode("Pakistan", "Pakistan"),
    250: GridCode("Pakistan-MV480", "Pakistan"),
    251: GridCode("PORTUGAL-MV800", "Portugal"),
    252: GridCode("HECO-L+M-LV208", "USA"),
    253: GridCode("HECO-L+M-LV240", "USA"),
    254: GridCode("C10/11-MV800", "Belgium"),
    255: GridCode("Austria", "Austria"),
    256: GridCode("Austria-MV480", "Austria"),
    257: GridCode("G98", "UK"),
    258: GridCode("G99-TYPEA-LV", "UK"),
    259: GridCode("G99-TYPEB-LV", "UK"),
    260: GridCode("G99-TYPEB-HV", "UK"),
    261: GridCode("G99-TYPEB-HV-MV480", "UK"),
    262: GridCode("G99-TYPEB-HV-MV800", "UK"),
    263: GridCode("G99-TYPEC-HV-MV800", "UK"),
    264: GridCode("G99-TYPED-MV800", "UK"),
    265: GridCode("G99-TYPEA-HV", "UK"),
    266: GridCode("CEA-MV800", "India"),
    267: GridCode("EN50549-MV400", "Europe"),
    268: GridCode("VDE-AR-N4110", "Germany"),
    269: GridCode("VDE-AR-N4110-MV480", "Germany"),
    270: GridCode("VDE-AR-N4110-MV800", "Germany"),
    271: GridCode("Panama-MV800", "Panama"),
    272: GridCode("North Macedonia-MV800", "North Macedonia"),
    273: GridCode("NTS", "Spain"),
    274: GridCode("NTS-MV480", "Spain"),
    275: GridCode("NTS-MV800", "Spain"),
}

STATE_CODES_1 = {
    0b0000_0000_0000_0001: "standby",
    0b0000_0000_0000_0010: "grid-connected",
    0b0000_0000_0000_0100: "grid-connected normally",
    0b0000_0000_0000_1000: "grid connection with derating due to power rationing",
    0b0000_0000_0001_0000: (
        "grid connection with derating due to internalcauses" "of the solar inverter"
    ),
    0b0000_0000_0010_0000: "normal stop",
    0b0000_0000_0100_0000: "stop due to faults",
    0b0000_0000_1000_0000: "stop due to power rationing",
    0b0000_0001_0000_0000: "shutdown",
    0b0000_0010_0000_0000: "spot check",
}

STATE_CODES_2 = {
    0b0000_0000_0000_0001: ("locked", "unlocked"),
    0b0000_0000_0000_0010: ("PV disconnected", "PV connected"),
    0b0000_0000_0000_0100: ("no DSP data collection", "DSP data collection"),
}

STATE_CODES_3 = {
    0b0000_0000_0000_0000_0000_0000_0000_0001: ("on-grid", "off-grid"),
    0b0000_0000_0000_0000_0000_0000_0000_0010: (
        "off-grid switch disabled",
        "off-grid switch enabled",
    ),
}

ALARM_CODES_1 = {
    0b0000_0000_0000_0001: Alarm("High String Input Voltage", 2001, "Major"),
    0b0000_0000_0000_0010: Alarm("DC Arc Fault", 2002, "Major"),
    0b0000_0000_0000_0100: Alarm("String Reverse Connection", 2011, "Major"),
    0b0000_0000_0000_1000: Alarm("String Current Backfeed", 2012, "Warning"),
    0b0000_0000_0001_0000: Alarm("Abnormal String Power", 2013, "Warning"),
    0b0000_0000_0010_0000: Alarm("AFCI Self-Check Fail", 2021, "Major"),
    0b0000_0000_0100_0000: Alarm("Phase Wire Short-Circuited to PE", 2031, "Major"),
    0b0000_0000_1000_0000: Alarm("Grid Loss", 2032, "Major"),
    0b0000_0001_0000_0000: Alarm("Grid Undervoltage", 2033, "Major"),
    0b0000_0010_0000_0000: Alarm("Grid Overvoltage", 2034, "Major"),
    0b0000_0100_0000_0000: Alarm("Grid Volt. Imbalance", 2035, "Major"),
    0b0000_1000_0000_0000: Alarm("Grid Overfrequency", 2036, "Major"),
    0b0001_0000_0000_0000: Alarm("Grid Underfrequency", 2037, "Major"),
    0b0010_0000_0000_0000: Alarm("Unstable Grid Frequency", 2038, "Major"),
    0b0100_0000_0000_0000: Alarm("Output Overcurrent", 2039, "Major"),
    0b1000_0000_0000_0000: Alarm("Output DC Component Overhigh", 2040, "Major"),
}

ALARM_CODES_2 = {
    0b0000_0000_0000_0001: Alarm("Abnormal Residual Current", 2051, "Major"),
    0b0000_0000_0000_0010: Alarm("Abnormal Grounding", 2061, "Major"),
    0b0000_0000_0000_0100: Alarm("Low Insulation Resistance", 2062, "Major"),
    0b0000_0000_0000_1000: Alarm("Overtemperature", 2063, "Minor"),
    0b0000_0000_0001_0000: Alarm("Device Fault", 2064, "Major"),
    0b0000_0000_0010_0000: Alarm("Upgrade Failed or Version Mismatch", 2065, "Minor"),
    0b0000_0000_0100_0000: Alarm("License Expired", 2066, "Warning"),
    0b0000_0000_1000_0000: Alarm("Faulty Monitoring Unit", 61440, "Minor"),
    0b0000_0001_0000_0000: Alarm("Faulty Power Collector", 2067, "Major"),
    0b0000_0010_0000_0000: Alarm("Battery abnormal", 2068, "Minor"),
    0b0000_0100_0000_0000: Alarm("Active Islanding", 2070, "Major"),
    0b0000_1000_0000_0000: Alarm("Passive Islanding", 2071, "Major"),
    0b0001_0000_0000_0000: Alarm("Transient AC Overvoltage", 2072, "Major"),
    0b0010_0000_0000_0000: Alarm("Peripheral port short circuit", 2075, "Warning"),
    0b0100_0000_0000_0000: Alarm("Churn output overload", 2077, "Major"),
    0b1000_0000_0000_0000: Alarm("Abnormal PV module configuration", 2080, "Major"),
}

ALARM_CODES_3 = {
    0b0000_0000_0000_0001: Alarm("Optimizer fault", 2081, "Warning"),
    0b0000_0000_0000_0010: Alarm("Built-in PID operation abnormal", 2085, "Minor"),
    0b0000_0000_0000_0100: Alarm("High input string voltage to ground", 2014, "Major"),
    0b0000_0000_0000_1000: Alarm("External Fan Abnormal", 2086, "Major"),
    0b0000_0000_0001_0000: Alarm("Battery Reverse Connection", 2069, "Major"),
    0b0000_0000_0010_0000: Alarm("On-grid/Off-grid controller abnormal", 2082, "Major"),
    0b0000_0000_0100_0000: Alarm("PV String Loss", 2015, "Warning"),
    0b0000_0000_1000_0000: Alarm("Internal Fan Abnormal", 2087, "Major"),
    0b0000_0001_0000_0000: Alarm("DC Protection Unit Abnormal", 2088, "Major"),
}

ALARM_CODES = {
    "alarm_1": ALARM_CODES_1,
    "alarm_2": ALARM_CODES_2,
    "alarm_3": ALARM_CODES_3,
}
