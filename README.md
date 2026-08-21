# Rekuperator MCB Modbus — интеграция для Home Assistant (HACS)

Кастомная интеграция Home Assistant для приточно-вытяжной установки (рекуператора)
на контроллере **MCB** (Modbus-таблица `MCB-1.27-Modbus-table-2019-06-18-1`).
Работает по **Modbus TCP** (например, через Wi-Fi/Ethernet шлюз RS-485 ↔ TCP).

## Возможности

### Кнопки (`button`)
| Сущность | Регистр | Описание |
|---|---|---|
| Сброс ошибок | `HR_ALARMS_RESET` (Holding, адрес **202**) | Пишет `1` — сбрасывает активные аварии |

### Переключатели (`switch`)
| Сущность | Регистр | Описание |
|---|---|---|
| Ночное охлаждение | `COIL_NIGHT_COOLING_FUNCTION` (Coil, адрес **4**) | ON=1/OFF=0, персистентный флаг функции |
| Питание (Standby) | `HR_USER_CONFIG_CURRENT_SYSTEM_MODE` (Holding, адрес **1**) | OFF пишет `0` (Standby), ON восстанавливает последний рабочий режим (по умолчанию Комфорт=3) |

### Выбор режима (`select.rekuperator_mode`)
| Опция | Действие |
|---|---|
| Защита здания | `HR_USER_CONFIG_CURRENT_SYSTEM_MODE = 1` |
| Эконом | `HR_USER_CONFIG_CURRENT_SYSTEM_MODE = 2` |
| Комфорт | `HR_USER_CONFIG_CURRENT_SYSTEM_MODE = 3` |
| Интенсивный обдув | Импульс `COIL_INTENSIVE_AIR_FLOW_BOOST` (Coil, адрес **5**), `write_coil(True)` |

`COIL_INTENSIVE_AIR_FLOW_BOOST` — не постоянный режим, а «одноразовый` триггер (`0: Nothing, 1: Activate`
по таблице), поэтому после активации boost сущность продолжит отображать фактический
режим, присланный контроллером (`IR_CURRENT_SYSTEM_MODE`).

### Числовые параметры (`number`)
Ночное охлаждение (Holding registers 25–32):

| Сущность | Регистр |
|---|---|
| Час старта | `HR_NIGHT_COOLING_START_HOURS` (25) |
| Минута старта | `HR_NIGHT_COOLING_START_MINS` (26) |
| Час окончания | `HR_NIGHT_COOLING_STOP_HOURS` (27) |
| Минута окончания | `HR_NIGHT_COOLING_STOP_MINS` (28) |
| t\u00b0 вытяжки, старт | `HR_NIGHT_COOLING_START_EXTRACT` (29), ×0.1\u00b0C |
| t\u00b0 вытяжки, стоп | `HR_NIGHT_COOLING_STOP_EXTRACT` (30), ×0.1\u00b0C |
| t\u00b0 наружного воздуха | `HR_NIGHT_COOLING_START_OUTDOOR` (31), ×0.1\u00b0C |
| Заданная t\u00b0 притока | `HR_NIGHT_COOLING_SETPOINT` (32), ×0.1\u00b0C |

Расход воздуха по ступеням (Holding registers 450–459, значения в **%**, шаг записи ×0.1%):

| Сущность | Регистр |
|---|---|
| Расход приток, ступень 1–4 | `HR_AIR_FLOW_1_SUPPLY` … `HR_AIR_FLOW_4_SUPPLY` (450–453) |
| Расход вытяжка, ступень 1–4 | `HR_AIR_FLOW_1_EXTRACT` … `HR_AIR_FLOW_4_EXTRACT` (456–459) |

**Целевая температура** (одна сущность `number.rekuperator_target_temperature`):
всегда читает/пишет значение в Holding-регистр **текущего активного режима**:

| Активный режим | Регистр температуры |
|---|---|
| Защита здания | `HR_USER_CONFIG_BUILDING_PROTECTION_MODE_TEMPERATURE_SET_POINT` (6) |
| Эконом | `HR_USER_CONFIG_ECONOMY_MODE_TEMPERATURE_SET_POINT` (4) |
| Комфорт | `HR_USER_CONFIG_COMFORT_MODE_TEMPERATURE_SET_POINT` (2) |

Если контроллер в `Standby`, запись недоступна — сначала выберите рабочий режим
через `select.rekuperator_mode`. Отображение — **21.0 \u00b0C** формат (одна десятая градуса).

### Сенсоры (`sensor`)
| Сущность | Регистр (Input, ф-я 0x04) | Ед. изм. |
|---|---|---|
| КПД теплообменника | `IR_TEMP_TRANSFER_EFFICIENCY` (125) | % |
| Осталось дней до замены фильтров | `IR_FILTERS_TIMER_DAYS_LEFT` (30) | дней |
| Скорость воздушного потока | `IR_CURRENT_AIR_FLOW` (16) | % |
| Режим системы | `IR_CURRENT_SYSTEM_MODE` (15) | текст |
| Текущие ошибки вентиляции | `IR_ACTIVE_ALARMS_COUNT` (28) | шт. |
| Температура выброса | `IR_EXHAUST_AIR_TEMPERATURE` (20, T3) | \u00b0C |
| Температура вытяжки | `IR_EXTRACT_AIR_TEMPERATURE` (19, T2) | \u00b0C |
| Температура наружного воздуха | `IR_OUTDOOR_AIR_TEMPERATURE` (21, T4) | \u00b0C |
| Температура притока | `IR_SUPPLY_AIR_TEMPERATURE` (18, T1) | \u00b0C |
| Расход вытяжка, факт. ступень 1–4 | `IR_1_EXTRACT_AIR_FLOW_M3H` … `IR_4_EXTRACT_AIR_FLOW_M3H` (83–86) | м\u00b3/ч |
| Расход приток, факт. ступень 1–4 | `IR_1_SUPPLY_AIR_FLOW_M3H` … `IR_4_SUPPLY_AIR_FLOW_M3H` (77–80) | м\u00b3/ч |

## Важное примечание по адресации

Все адреса в `const.py` указаны **как в таблице AlpicAir/NEST** (0-based).
Клиент (`modbus_client.py`) **не применяет дополнительного смещения** — это
исправленная версия, которая работает с устройствами AlpicAir/NEST, где
документированный адрес уже совпадает с адресом «на проводе" [web:26][web:27].

## Установка через HACS

1. HACS → **Integrations** → меню (⋮) → **Custom repositories**.
2. Добавьте URL этого репозитория, категория **Integration**.
3. Найдите «Rekuperator MCB Modbus" в списке HACS и установите.
4. Перезапустите Home Assistant.
5. **Настройки → Устройства и службы → Добавить интеграцию** → «Rekuperator MCB Modbus".
6. Укажите IP-адрес/хост, порт (по умолчанию 502), Modbus Slave ID и интервал опроса.

## Установка вручную

Скопируйте папку `custom_components/rekuperator_mcb` в `<config>/custom_components/`
вашей установки Home Assistant, перезапустите HA и добавьте интеграцию через UI.

## Зависимости

* [pymodbus](https://pypi.org/project/pymodbus/) >= 3.6.0 (устанавливается автоматически
  Home Assistant по `manifest.json`).

## Структура репозитория

```
custom_components/rekuperator_mcb/
├── __init__.py
├── button.py
├── config_flow.py
├── const.py
├── coordinator.py
├── manifest.json
├── modbus_client.py
├── number.py
├── select.py
├── sensor.py
├── strings.json
├── switch.py
└── translations/
    ├── en.json
    └── ru.json
hacs.json
LICENSE
.gitignore
.github/workflows/validate.yaml
```

## Как загрузить в GitHub как новый репозиторий

```bash
cd rekuperator_mcb_hacs_fixed
git init
git add .
git commit -m "Initial commit: Rekuperator MCB Modbus HACS integration (AlpicAir/NEST 0-based)"
git branch -M main
git remote add origin https://github.com/<ваш-логин>/rekuperator-mcb-modbus.git
git push -u origin main
```

После пуша замените `@your-github-username` в `manifest.json` и ссылки в `hacs.json`/README
на свой реальный GitHub-логин и название репозитория.
