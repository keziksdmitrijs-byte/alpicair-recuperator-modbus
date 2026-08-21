"""Button entities for the Rekuperator MCB integration."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import const as c
from .coordinator import RekuperatorDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


BUTTON_DESCRIPTIONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="reset_errors",
        translation_key="reset_errors",
        name="Сброс ошибок",
        icon="mdi:restart-alert",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: RekuperatorDataUpdateCoordinator = hass.data[c.DOMAIN][entry.entry_id]
    async_add_entities(
        [RekuperatorResetErrorsButton(coordinator, entry, BUTTON_DESCRIPTIONS[0])]
    )


class RekuperatorResetErrorsButton(
    CoordinatorEntity[RekuperatorDataUpdateCoordinator], ButtonEntity
):
    """Pulses HR_ALARMS_RESET (address 202) to clear active alarms."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RekuperatorDataUpdateCoordinator,
        entry: ConfigEntry,
        description: ButtonEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(c.DOMAIN, entry.entry_id)},
            name=entry.data.get("name", c.DEFAULT_NAME),
            manufacturer="Komfovent/MCB",
            model="MCB-1.27 Modbus AHU",
        )

    async def async_press(self) -> None:
        client = self.coordinator.client
        ok = await client.write_holding_register(c.HR_ALARMS_RESET, 1)
        if not ok:
            _LOGGER.warning("Failed to write HR_ALARMS_RESET (address %s)", c.HR_ALARMS_RESET)
        await self.coordinator.async_request_refresh()
