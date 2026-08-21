"""Config flow for the Rekuperator MCB Modbus integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_SLAVE_ID, DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DEFAULT_SLAVE, DOMAIN
from .modbus_client import RekuperatorModbusClient

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE): int,
        vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
    }
)


async def _validate_connection(host: str, port: int, slave_id: int) -> bool:
    client = RekuperatorModbusClient(host=host, port=port, slave_id=slave_id)
    try:
        value = await client.read_holding_register(1)
        return value is not None
    finally:
        await client.close()


class RekuperatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Rekuperator MCB Modbus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            valid = await _validate_connection(
                user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_SLAVE_ID]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return RekuperatorOptionsFlow(config_entry)


class RekuperatorOptionsFlow(config_entries.OptionsFlow):
    """Handle options for the Rekuperator MCB Modbus integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options.get(
            "scan_interval",
            self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Optional("scan_interval", default=current): int}
            ),
        )
