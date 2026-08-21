"""Select entity for the Rekuperator MCB integration: system mode."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import const as c
from .coordinator import RekuperatorDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: RekuperatorDataUpdateCoordinator = hass.data[c.DOMAIN][entry.entry_id]
    async_add_entities([RekuperatorModeSelect(coordinator, entry)])


class RekuperatorModeSelect(CoordinatorEntity[RekuperatorDataUpdateCoordinator], SelectEntity):
    _attr_has_entity_name = True
    entity_description = SelectEntityDescription(
        key="mode",
        translation_key="mode",
        name="Режим работы",
        icon="mdi:fan-auto",
    )

    def __init__(self, coordinator: RekuperatorDataUpdateCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_mode"
        self._attr_options = c.MODE_OPTIONS
        self._attr_device_info = DeviceInfo(
            identifiers={(c.DOMAIN, entry.entry_id)},
            name=entry.data.get("name", c.DEFAULT_NAME),
            manufacturer="Komfovent/MCB",
            model="MCB-1.27 Modbus AHU",
        )

    @property
    def current_option(self) -> str | None:
        mode_value = self.coordinator.data.get("holding", {}).get(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE
        )
        if mode_value is None:
            return None
        return c.HR_VALUE_TO_MODE_OPTION.get(mode_value)

    async def async_select_option(self, option: str) -> None:
        client = self.coordinator.client

        if option == c.MODE_OPTION_INTENSIVE:
            ok = await client.write_coil(c.COIL_INTENSIVE_AIR_FLOW_BOOST, True)
            if not ok:
                _LOGGER.warning(
                    "Failed to activate intensive air flow boost (coil %s)",
                    c.COIL_INTENSIVE_AIR_FLOW_BOOST,
                )
            await self.coordinator.async_request_refresh()
            return

        hr_value = c.MODE_OPTION_TO_HR_VALUE.get(option)
        if hr_value is None:
            _LOGGER.warning("Unknown mode option selected: %s", option)
            return

        ok = await client.write_holding_register(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE, hr_value
        )
        if not ok:
            _LOGGER.warning(
                "Failed to write system mode %s to HR %s",
                hr_value,
                c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE,
            )
        await self.coordinator.async_request_refresh()
