"""Switch entities for the Rekuperator MCB integration."""
from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
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
    async_add_entities(
        [
            RekuperatorNightCoolingSwitch(coordinator, entry),
            RekuperatorStandbySwitch(coordinator, entry),
        ]
    )


class _BaseRekuperatorSwitch(CoordinatorEntity[RekuperatorDataUpdateCoordinator], SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: RekuperatorDataUpdateCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(c.DOMAIN, entry.entry_id)},
            name=entry.data.get("name", c.DEFAULT_NAME),
            manufacturer="Komfovent/MCB",
            model="MCB-1.27 Modbus AHU",
        )


class RekuperatorNightCoolingSwitch(_BaseRekuperatorSwitch):
    entity_description = SwitchEntityDescription(
        key="night_cooling",
        translation_key="night_cooling",
        name="Ночное охлаждение",
        icon="mdi:weather-night",
    )

    def __init__(self, coordinator: RekuperatorDataUpdateCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_night_cooling"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get("coils", {}).get(c.COIL_NIGHT_COOLING_FUNCTION)

    async def async_turn_on(self, **kwargs) -> None:
        ok = await self.coordinator.client.write_coil(c.COIL_NIGHT_COOLING_FUNCTION, True)
        if not ok:
            _LOGGER.warning("Failed to enable night cooling (coil %s)", c.COIL_NIGHT_COOLING_FUNCTION)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        ok = await self.coordinator.client.write_coil(c.COIL_NIGHT_COOLING_FUNCTION, False)
        if not ok:
            _LOGGER.warning("Failed to disable night cooling (coil %s)", c.COIL_NIGHT_COOLING_FUNCTION)
        await self.coordinator.async_request_refresh()


class RekuperatorStandbySwitch(_BaseRekuperatorSwitch):
    entity_description = SwitchEntityDescription(
        key="power",
        translation_key="power",
        name="Питание (Standby)",
        icon="mdi:power",
    )

    def __init__(self, coordinator: RekuperatorDataUpdateCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_standby_power"
        self._last_mode = c.MODE_COMFORT

    @property
    def is_on(self) -> bool | None:
        mode = self.coordinator.data.get("holding", {}).get(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE
        )
        if mode is None:
            return None
        if mode != c.MODE_STANDBY:
            self._last_mode = mode
        return mode != c.MODE_STANDBY

    async def async_turn_on(self, **kwargs) -> None:
        target_mode = self._last_mode if self._last_mode != c.MODE_STANDBY else c.MODE_COMFORT
        ok = await self.coordinator.client.write_holding_register(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE, target_mode
        )
        if not ok:
            _LOGGER.warning("Failed to leave standby (HR %s)", c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        ok = await self.coordinator.client.write_holding_register(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE, c.MODE_STANDBY
        )
        if not ok:
            _LOGGER.warning("Failed to enter standby (HR %s)", c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE)
        await self.coordinator.async_request_refresh()
