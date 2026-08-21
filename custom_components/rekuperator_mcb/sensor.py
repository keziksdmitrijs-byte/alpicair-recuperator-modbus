"""Sensor entities for the Rekuperator MCB integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import const as c
from .coordinator import RekuperatorDataUpdateCoordinator

SYSTEM_MODE_LABELS = {
    0: "Standby",
    1: "Защита здания",
    2: "Эконом",
    3: "Комфорт",
    4: "Emergency run",
    5: "Preparing",
    6: "Opening dampers",
    7: "Boost",
    8: "Cooling heaters",
    9: "Closing dampers",
    10: "Night Cooling",
    11: "Critical alarm",
    12: "Fire alarm",
    13: "Heat exchanger frost protection",
    14: "Change filters",
}


@dataclass(frozen=True, kw_only=True)
class RekuperatorSensorDescription(SensorEntityDescription):
    register_group: str = "input"
    address: int = 0
    scale: float = 1.0
    value_fn: Callable[[Any], Any] | None = None


SENSOR_DESCRIPTIONS: tuple[RekuperatorSensorDescription, ...] = (
    RekuperatorSensorDescription(
        key="heat_exchanger_efficiency",
        translation_key="heat_exchanger_efficiency",
        name="КПД теплообменника",
        register_group="input",
        address=c.IR_TEMP_TRANSFER_EFFICIENCY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:heat-wave",
    ),
    RekuperatorSensorDescription(
        key="filter_days_left",
        translation_key="filter_days_left",
        name="Осталось дней до замены фильтров",
        register_group="input",
        address=c.IR_FILTERS_TIMER_DAYS_LEFT,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="current_air_flow",
        translation_key="current_air_flow",
        name="Скорость воздушного потока",
        register_group="input",
        address=c.IR_CURRENT_AIR_FLOW,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    RekuperatorSensorDescription(
        key="system_mode",
        translation_key="system_mode",
        name="Режим системы",
        register_group="input",
        address=c.IR_CURRENT_SYSTEM_MODE,
        value_fn=lambda v: SYSTEM_MODE_LABELS.get(v, f"Unknown ({v})"),
        icon="mdi:state-machine",
    ),
    RekuperatorSensorDescription(
        key="active_alarms_count",
        translation_key="active_alarms_count",
        name="Текущие ошибки вентиляции",
        register_group="input",
        address=c.IR_ACTIVE_ALARMS_COUNT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:alert-circle-outline",
    ),
    RekuperatorSensorDescription(
        key="exhaust_air_temperature",
        translation_key="exhaust_air_temperature",
        name="Температура выброса",
        register_group="input",
        address=c.IR_EXHAUST_AIR_TEMPERATURE,
        scale=0.1,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    RekuperatorSensorDescription(
        key="extract_air_temperature",
        translation_key="extract_air_temperature",
        name="Температура вытяжки",
        register_group="input",
        address=c.IR_EXTRACT_AIR_TEMPERATURE,
        scale=0.1,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    RekuperatorSensorDescription(
        key="outdoor_air_temperature",
        translation_key="outdoor_air_temperature",
        name="Температура наружного воздуха",
        register_group="input",
        address=c.IR_OUTDOOR_AIR_TEMPERATURE,
        scale=0.1,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    RekuperatorSensorDescription(
        key="supply_air_temperature",
        translation_key="supply_air_temperature",
        name="Температура притока",
        register_group="input",
        address=c.IR_SUPPLY_AIR_TEMPERATURE,
        scale=0.1,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    RekuperatorSensorDescription(
        key="extract_flow_stage_1",
        translation_key="extract_flow_stage_1",
        name="Расход вытяжка, факт. ступень 1",
        register_group="input",
        address=c.IR_1_EXTRACT_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="extract_flow_stage_2",
        translation_key="extract_flow_stage_2",
        name="Расход вытяжка, факт. ступень 2",
        register_group="input",
        address=c.IR_2_EXTRACT_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="extract_flow_stage_3",
        translation_key="extract_flow_stage_3",
        name="Расход вытяжка, факт. ступень 3",
        register_group="input",
        address=c.IR_3_EXTRACT_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="extract_flow_stage_4",
        translation_key="extract_flow_stage_4",
        name="Расход вытяжка, факт. ступень 4",
        register_group="input",
        address=c.IR_4_EXTRACT_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="supply_flow_stage_1",
        translation_key="supply_flow_stage_1",
        name="Расход приток, факт. ступень 1",
        register_group="input",
        address=c.IR_1_SUPPLY_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="supply_flow_stage_2",
        translation_key="supply_flow_stage_2",
        name="Расход приток, факт. ступень 2",
        register_group="input",
        address=c.IR_2_SUPPLY_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="supply_flow_stage_3",
        translation_key="supply_flow_stage_3",
        name="Расход приток, факт. ступень 3",
        register_group="input",
        address=c.IR_3_SUPPLY_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    RekuperatorSensorDescription(
        key="supply_flow_stage_4",
        translation_key="supply_flow_stage_4",
        name="Расход приток, факт. ступень 4",
        register_group="input",
        address=c.IR_4_SUPPLY_AIR_FLOW_M3H,
        native_unit_of_measurement="m\u00b3/h",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: RekuperatorDataUpdateCoordinator = hass.data[c.DOMAIN][entry.entry_id]
    entities = [
        RekuperatorSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)


class RekuperatorSensor(CoordinatorEntity[RekuperatorDataUpdateCoordinator], SensorEntity):
    entity_description: RekuperatorSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RekuperatorDataUpdateCoordinator,
        entry: ConfigEntry,
        description: RekuperatorSensorDescription,
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

    @property
    def native_value(self) -> Any:
        group = self.coordinator.data.get(self.entity_description.register_group, {})
        raw = group.get(self.entity_description.address)
        if raw is None:
            return None
        if self.entity_description.value_fn is not None:
            return self.entity_description.value_fn(raw)
        return round(raw * self.entity_description.scale, 2)
