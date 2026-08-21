"""Number entities for the Rekuperator MCB integration."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import const as c
from .coordinator import RekuperatorDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class RekuperatorNumberDescription(NumberEntityDescription):
    address: int = 0
    scale: float = 1.0


NUMBER_DESCRIPTIONS: tuple[RekuperatorNumberDescription, ...] = (
    RekuperatorNumberDescription(
        key="night_cooling_start_hours",
        translation_key="night_cooling_start_hours",
        name="Ночное охлаждение: час старта",
        address=c.HR_NIGHT_COOLING_START_HOURS,
        native_min_value=0,
        native_max_value=23,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:clock-start",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_start_mins",
        translation_key="night_cooling_start_mins",
        name="Ночное охлаждение: минута старта",
        address=c.HR_NIGHT_COOLING_START_MINS,
        native_min_value=0,
        native_max_value=59,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:clock-start",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_stop_hours",
        translation_key="night_cooling_stop_hours",
        name="Ночное охлаждение: час окончания",
        address=c.HR_NIGHT_COOLING_STOP_HOURS,
        native_min_value=0,
        native_max_value=23,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:clock-end",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_stop_mins",
        translation_key="night_cooling_stop_mins",
        name="Ночное охлаждение: минута окончания",
        address=c.HR_NIGHT_COOLING_STOP_MINS,
        native_min_value=0,
        native_max_value=59,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:clock-end",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_start_extract",
        translation_key="night_cooling_start_extract",
        name="Ночное охлаждение: t\u00b0 вытяжки старт",
        address=c.HR_NIGHT_COOLING_START_EXTRACT,
        scale=0.1,
        native_min_value=13.0,
        native_max_value=30.0,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_stop_extract",
        translation_key="night_cooling_stop_extract",
        name="Ночное охлаждение: t\u00b0 вытяжки стоп",
        address=c.HR_NIGHT_COOLING_STOP_EXTRACT,
        scale=0.1,
        native_min_value=13.0,
        native_max_value=30.0,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_start_outdoor",
        translation_key="night_cooling_start_outdoor",
        name="Ночное охлаждение: t\u00b0 наружного воздуха",
        address=c.HR_NIGHT_COOLING_START_OUTDOOR,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=30.0,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    ),
    RekuperatorNumberDescription(
        key="night_cooling_setpoint",
        translation_key="night_cooling_setpoint",
        name="Ночное охлаждение: заданная t\u00b0 притока",
        address=c.HR_NIGHT_COOLING_SETPOINT,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=30.0,
        native_step=0.1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    ),
    RekuperatorNumberDescription(
        key="extract_flow_setpoint_1",
        translation_key="extract_flow_setpoint_1",
        name="Расход вытяжка, факт. ступень 1",
        address=c.HR_AIR_FLOW_1_EXTRACT,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-1",
    ),
    RekuperatorNumberDescription(
        key="extract_flow_setpoint_2",
        translation_key="extract_flow_setpoint_2",
        name="Расход вытяжка, факт. ступень 2",
        address=c.HR_AIR_FLOW_2_EXTRACT,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-2",
    ),
    RekuperatorNumberDescription(
        key="extract_flow_setpoint_3",
        translation_key="extract_flow_setpoint_3",
        name="Расход вытяжка, факт. ступень 3",
        address=c.HR_AIR_FLOW_3_EXTRACT,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-3",
    ),
    RekuperatorNumberDescription(
        key="extract_flow_setpoint_4",
        translation_key="extract_flow_setpoint_4",
        name="Расход вытяжка, факт. ступень 4",
        address=c.HR_AIR_FLOW_4_EXTRACT,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-4",
    ),
    RekuperatorNumberDescription(
        key="supply_flow_setpoint_1",
        translation_key="supply_flow_setpoint_1",
        name="Расход приток, факт. ступень 1",
        address=c.HR_AIR_FLOW_1_SUPPLY,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-1",
    ),
    RekuperatorNumberDescription(
        key="supply_flow_setpoint_2",
        translation_key="supply_flow_setpoint_2",
        name="Расход приток, факт. ступень 2",
        address=c.HR_AIR_FLOW_2_SUPPLY,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-2",
    ),
    RekuperatorNumberDescription(
        key="supply_flow_setpoint_3",
        translation_key="supply_flow_setpoint_3",
        name="Расход приток, факт. ступень 3",
        address=c.HR_AIR_FLOW_3_SUPPLY,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-3",
    ),
    RekuperatorNumberDescription(
        key="supply_flow_setpoint_4",
        translation_key="supply_flow_setpoint_4",
        name="Расход приток, факт. ступень 4",
        address=c.HR_AIR_FLOW_4_SUPPLY,
        scale=0.1,
        native_min_value=0.0,
        native_max_value=100.0,
        native_step=0.1,
        native_unit_of_measurement="%",
        mode=NumberMode.BOX,
        icon="mdi:fan-speed-4",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: RekuperatorDataUpdateCoordinator = hass.data[c.DOMAIN][entry.entry_id]
    entities: list[NumberEntity] = [
        RekuperatorNumber(coordinator, entry, description)
        for description in NUMBER_DESCRIPTIONS
    ]
    entities.append(RekuperatorTargetTemperatureNumber(coordinator, entry))
    async_add_entities(entities)


class _BaseRekuperatorNumber(CoordinatorEntity[RekuperatorDataUpdateCoordinator], NumberEntity):
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


class RekuperatorNumber(_BaseRekuperatorNumber):
    entity_description: RekuperatorNumberDescription

    def __init__(
        self,
        coordinator: RekuperatorDataUpdateCoordinator,
        entry: ConfigEntry,
        description: RekuperatorNumberDescription,
    ) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        raw = self.coordinator.data.get("holding", {}).get(self.entity_description.address)
        if raw is None:
            return None
        return round(raw * self.entity_description.scale, 2)

    async def async_set_native_value(self, value: float) -> None:
        raw_value = round(value / self.entity_description.scale)
        ok = await self.coordinator.client.write_holding_register(
            self.entity_description.address, raw_value
        )
        if not ok:
            _LOGGER.warning(
                "Failed to write %s to HR %s",
                raw_value,
                self.entity_description.address,
            )
        await self.coordinator.async_request_refresh()


class RekuperatorTargetTemperatureNumber(_BaseRekuperatorNumber):
    entity_description = NumberEntityDescription(
        key="target_temperature",
        translation_key="target_temperature",
        name="Целевая температура",
        native_min_value=c.TEMPERATURE_MIN,
        native_max_value=c.TEMPERATURE_MAX,
        native_step=c.TEMPERATURE_STEP,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    )

    def __init__(self, coordinator: RekuperatorDataUpdateCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_target_temperature"

    def _current_mode(self) -> int | None:
        return self.coordinator.data.get("holding", {}).get(
            c.HR_USER_CONFIG_CURRENT_SYSTEM_MODE
        )

    def _target_register(self) -> int | None:
        mode = self._current_mode()
        if mode is None:
            return None
        return c.MODE_TO_TEMPERATURE_REGISTER.get(mode)

    @property
    def native_value(self) -> float | None:
        register = self._target_register()
        if register is None:
            return None
        raw = self.coordinator.data.get("holding", {}).get(register)
        if raw is None or raw < 0:
            return None
        return round(raw * c.TEMPERATURE_SCALE, 1)

    @property
    def available(self) -> bool:
        return super().available and self._target_register() is not None

    async def async_set_native_value(self, value: float) -> None:
        register = self._target_register()
        if register is None:
            _LOGGER.warning(
                "Cannot write target temperature: unit is in Standby or mode is unknown"
            )
            return
        raw_value = round(value / c.TEMPERATURE_SCALE)
        ok = await self.coordinator.client.write_holding_register(register, raw_value)
        if not ok:
            _LOGGER.warning("Failed to write target temperature to HR %s", register)
        await self.coordinator.async_request_refresh()
