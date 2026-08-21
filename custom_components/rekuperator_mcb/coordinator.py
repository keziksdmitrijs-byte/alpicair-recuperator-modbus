"""DataUpdateCoordinator for the Rekuperator MCB integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from . import const as c
from .modbus_client import RekuperatorModbusClient

_LOGGER = logging.getLogger(__name__)

HOLDING_REGISTERS_TO_POLL: list[int] = [
    c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE,
    c.HR_USER_CONFIG_COMFORT_MODE_TEMPERATURE_SET_POINT,
    c.HR_USER_CONFIG_ECONOMY_MODE_TEMPERATURE_SET_POINT,
    c.HR_USER_CONFIG_BUILDING_PROTECTION_MODE_TEMPERATURE_SET_POINT,
    c.HR_NIGHT_COOLING_START_HOURS,
    c.HR_NIGHT_COOLING_START_MINS,
    c.HR_NIGHT_COOLING_STOP_HOURS,
    c.HR_NIGHT_COOLING_STOP_MINS,
    c.HR_NIGHT_COOLING_START_EXTRACT,
    c.HR_NIGHT_COOLING_STOP_EXTRACT,
    c.HR_NIGHT_COOLING_START_OUTDOOR,
    c.HR_NIGHT_COOLING_SETPOINT,
    c.HR_AIR_FLOW_1_SUPPLY,
    c.HR_AIR_FLOW_2_SUPPLY,
    c.HR_AIR_FLOW_3_SUPPLY,
    c.HR_AIR_FLOW_4_SUPPLY,
    c.HR_AIR_FLOW_1_EXTRACT,
    c.HR_AIR_FLOW_2_EXTRACT,
    c.HR_AIR_FLOW_3_EXTRACT,
    c.HR_AIR_FLOW_4_EXTRACT,
]

INPUT_REGISTERS_TO_POLL: list[int] = [
    c.IR_CURRENT_SYSTEM_MODE,
    c.IR_CURRENT_AIR_FLOW,
    c.IR_SUPPLY_AIR_TEMPERATURE,
    c.IR_EXTRACT_AIR_TEMPERATURE,
    c.IR_EXHAUST_AIR_TEMPERATURE,
    c.IR_OUTDOOR_AIR_TEMPERATURE,
    c.IR_ACTIVE_ALARMS_COUNT,
    c.IR_FILTERS_TIMER_DAYS_LEFT,
    c.IR_TEMP_TRANSFER_EFFICIENCY,
    c.IR_CURRENT_SUPPLY_AIR_FLOW_M3H,
    c.IR_CURRENT_EXTRACT_AIR_FLOW_M3H,
    c.IR_1_SUPPLY_AIR_FLOW_M3H,
    c.IR_2_SUPPLY_AIR_FLOW_M3H,
    c.IR_3_SUPPLY_AIR_FLOW_M3H,
    c.IR_4_SUPPLY_AIR_FLOW_M3H,
    c.IR_1_EXTRACT_AIR_FLOW_M3H,
    c.IR_2_EXTRACT_AIR_FLOW_M3H,
    c.IR_3_EXTRACT_AIR_FLOW_M3H,
    c.IR_4_EXTRACT_AIR_FLOW_M3H,
]

COILS_TO_POLL: list[int] = [
    c.COIL_NIGHT_COOLING_FUNCTION,
]


class RekuperatorDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Polls the AHU controller over Modbus TCP on a fixed interval."""

    def __init__(
        self, hass: HomeAssistant, client: RekuperatorModbusClient, entry: ConfigEntry
    ) -> None:
        self.client = client
        self.entry = entry
        scan_interval = entry.options.get(
            "scan_interval", entry.data.get("scan_interval", c.DEFAULT_SCAN_INTERVAL)
        )
        super().__init__(
            hass,
            _LOGGER,
            name=c.DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            holding = await self.client.read_holding_registers_bulk(
                HOLDING_REGISTERS_TO_POLL
            )
            input_regs = await self.client.read_input_registers_bulk(
                INPUT_REGISTERS_TO_POLL
            )
            coils = await self.client.read_coils_bulk(COILS_TO_POLL)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Error communicating with AHU: {err}") from err

        return {"holding": holding, "input": input_regs, "coils": coils}
