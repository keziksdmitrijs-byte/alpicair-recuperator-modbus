"""Constants for the Rekuperator MCB Modbus integration."""

DOMAIN = "rekuperator_mcb"

DEFAULT_NAME = "Rekuperator"
DEFAULT_SCAN_INTERVAL = 15
DEFAULT_PORT = 502
DEFAULT_SLAVE = 1

CONF_SLAVE_ID = "slave_id"

# ---------------------------------------------------------------------------
# Modbus function-code register maps, based on:
# "MCB-1.27-Modbus-table-2019-06-18-1.xlsx"
#
# Holding registers  -> function code 0x03/0x06/0x10 (read/write)
# Coils              -> function code 0x01/0x05       (read/write, 1 bit)
# Input registers    -> function code 0x04             (read only)
# Discrete inputs    -> function code 0x02             (read only, 1 bit)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# COILS (address is 0-based coil number, as printed in the "Coils" sheet)
# ---------------------------------------------------------------------------
COIL_NIGHT_COOLING_FUNCTION = 4          # 0: Disabled, 1: Enabled -> also used as ON/OFF switch
COIL_INTENSIVE_AIR_FLOW_BOOST = 5        # 0: Nothing, 1: Activate (pulse -> "Intensive air flow" / boost)

# ---------------------------------------------------------------------------
# HOLDING REGISTERS
# ---------------------------------------------------------------------------
HR_USER_CONFIG_CURRENT_SYSTEM_MODE = 1                 # 0 Standby,1 Building protection,2 Economy,3 Comfort
HR_USER_CONFIG_COMFORT_MODE_TEMPERATURE_SET_POINT = 2  # 160..300 *0.1C
HR_USER_CONFIG_ECONOMY_MODE_TEMPERATURE_SET_POINT = 4  # 0:Energy saving,160..300*0.1C
HR_USER_CONFIG_BUILDING_PROTECTION_MODE_TEMPERATURE_SET_POINT = 6  # 0:Energy saving,160..300*0.1C

HR_NIGHT_COOLING_START_HOURS = 25
HR_NIGHT_COOLING_START_MINS = 26
HR_NIGHT_COOLING_STOP_HOURS = 27
HR_NIGHT_COOLING_STOP_MINS = 28
HR_NIGHT_COOLING_START_EXTRACT = 29     # 130-300 *0.1C
HR_NIGHT_COOLING_STOP_EXTRACT = 30      # 130-300 *0.1C
HR_NIGHT_COOLING_START_OUTDOOR = 31     # 0-300 *0.1C  (named "outdoor temp for stop" in table, kept as-is)
HR_NIGHT_COOLING_SETPOINT = 32          # 0-300 *0.1C  supply air setpoint

HR_ALARMS_RESET = 202                   # 0 Nothing, 1 Activate -> "reset errors" button

# Air flow steps (percent *0.1 %), stage 1..4
HR_AIR_FLOW_1_SUPPLY = 450
HR_AIR_FLOW_2_SUPPLY = 451
HR_AIR_FLOW_3_SUPPLY = 452
HR_AIR_FLOW_4_SUPPLY = 453
HR_AIR_FLOW_1_EXTRACT = 456
HR_AIR_FLOW_2_EXTRACT = 457
HR_AIR_FLOW_3_EXTRACT = 458
HR_AIR_FLOW_4_EXTRACT = 459

# ---------------------------------------------------------------------------
# INPUT REGISTERS (read only, function code 0x04)
# ---------------------------------------------------------------------------
IR_CURRENT_SYSTEM_MODE = 15             # 0..4 -> mirrors HR1 but read-only / includes transitional states
IR_CURRENT_AIR_FLOW = 16                # 0..100 %
IR_REQUIRED_SUPPLY_TEMPERATURE = 17     # *0.1C
IR_SUPPLY_AIR_TEMPERATURE = 18          # T1 *0.1C
IR_EXTRACT_AIR_TEMPERATURE = 19         # T2 *0.1C
IR_EXHAUST_AIR_TEMPERATURE = 20         # T3 *0.1C
IR_OUTDOOR_AIR_TEMPERATURE = 21         # T4 *0.1C
IR_ACTIVE_ALARMS_COUNT = 28             # 0-100
IR_FILTERS_TIMER_DAYS_LEFT = 30         # 1-365 days

IR_CURRENT_SUPPLY_AIR_FLOW_PCT = 58     # *0.1 %
IR_CURRENT_SUPPLY_AIR_FLOW_M3H = 60     # m3/h
IR_CURRENT_EXTRACT_AIR_FLOW_PCT = 62    # *0.1 %
IR_CURRENT_EXTRACT_AIR_FLOW_M3H = 64    # m3/h

# Air flow per stage, actual value, m3/h (Adjuster level registers)
IR_1_SUPPLY_AIR_FLOW_M3H = 77
IR_2_SUPPLY_AIR_FLOW_M3H = 78
IR_3_SUPPLY_AIR_FLOW_M3H = 79
IR_4_SUPPLY_AIR_FLOW_M3H = 80
IR_1_EXTRACT_AIR_FLOW_M3H = 83
IR_2_EXTRACT_AIR_FLOW_M3H = 84
IR_3_EXTRACT_AIR_FLOW_M3H = 85
IR_4_EXTRACT_AIR_FLOW_M3H = 86

IR_TEMP_TRANSFER_EFFICIENCY = 125       # 0-100 % -> "КПД теплообменника"

# ---------------------------------------------------------------------------
# System mode values shared between HR1 (write) and IR15 (read)
# ---------------------------------------------------------------------------
MODE_STANDBY = 0
MODE_BUILDING_PROTECTION = 1
MODE_ECONOMY = 2
MODE_COMFORT = 3
# "Intensive air flow" (boost) is not a persistent mode in the controller -
# it is a coil pulse (COIL_INTENSIVE_AIR_FLOW_BOOST) layered on top of the
# current mode. It is exposed as an extra option in select.rekuperator_mode.

MODE_NAMES = {
    MODE_STANDBY: "standby",
    MODE_BUILDING_PROTECTION: "building_protection",
    MODE_ECONOMY: "economy",
    MODE_COMFORT: "comfort",
}

MODE_LABELS_RU = {
    MODE_STANDBY: "Защита здания",  # placeholder, overwritten below intentionally left out
}

# Human-readable (RU) labels used for the select.rekuperator_mode entity.
MODE_OPTION_BUILDING_PROTECTION = "Защита здания"
MODE_OPTION_ECONOMY = "Эконом"
MODE_OPTION_COMFORT = "Комфорт"
MODE_OPTION_INTENSIVE = "Интенсивный обдув"

MODE_OPTIONS = [
    MODE_OPTION_BUILDING_PROTECTION,
    MODE_OPTION_ECONOMY,
    MODE_OPTION_COMFORT,
    MODE_OPTION_INTENSIVE,
]

# Maps select option -> HR1 value to write (Intensive uses a coil pulse instead)
MODE_OPTION_TO_HR_VALUE = {
    MODE_OPTION_BUILDING_PROTECTION: MODE_BUILDING_PROTECTION,
    MODE_OPTION_ECONOMY: MODE_ECONOMY,
    MODE_OPTION_COMFORT: MODE_COMFORT,
}

HR_VALUE_TO_MODE_OPTION = {
    MODE_BUILDING_PROTECTION: MODE_OPTION_BUILDING_PROTECTION,
    MODE_ECONOMY: MODE_OPTION_ECONOMY,
    MODE_COMFORT: MODE_OPTION_COMFORT,
    MODE_STANDBY: MODE_OPTION_BUILDING_PROTECTION,  # standby has no direct select option; falls back
}

# Maps current mode (HR1 value) -> the Holding register that stores its
# temperature setpoint. Used by the single "Целевая температура" entity so
# that writes always land in the register of the *currently selected* mode.
MODE_TO_TEMPERATURE_REGISTER = {
    MODE_BUILDING_PROTECTION: HR_USER_CONFIG_BUILDING_PROTECTION_MODE_TEMPERATURE_SET_POINT,
    MODE_ECONOMY: HR_USER_CONFIG_ECONOMY_MODE_TEMPERATURE_SET_POINT,
    MODE_COMFORT: HR_USER_CONFIG_COMFORT_MODE_TEMPERATURE_SET_POINT,
}

TEMPERATURE_SCALE = 0.1
TEMPERATURE_MIN = 16.0
TEMPERATURE_MAX = 30.0
TEMPERATURE_STEP = 0.5
