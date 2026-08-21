"""Thin async Modbus TCP client wrapper for the Rekuperator MCB controller."""
from __future__ import annotations

import logging
from typing import Any

from pymodbus.client import AsyncModbusTcpClient

_LOGGER = logging.getLogger(__name__)


class RekuperatorModbusClient:
    """Wraps pymodbus async TCP client with helpers for signed 16-bit registers."""

    def __init__(self, host: str, port: int, slave_id: int) -> None:
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._client = AsyncModbusTcpClient(host=host, port=port)

    async def _ensure_connected(self) -> None:
        if not self._client.connected:
            await self._client.connect()

    async def close(self) -> None:
        self._client.close()

    # ---------------------------------------------------------------
    # Holding registers (function code 0x03 read / 0x06-0x10 write)
    # ---------------------------------------------------------------
    async def read_holding_register(self, address: int) -> int | None:
        """Read a single holding register, address is 1-based per Modbus table."""
        await self._ensure_connected()
        try:
            result = await self._client.read_holding_registers(
                address - 1, count=1, slave=self._slave_id
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Error reading HR%s: %s", address, err)
            return None
        if result.isError():
            _LOGGER.debug("Modbus error reading HR%s: %s", address, result)
            return None
        value = result.registers[0]
        if value >= 0x8000:
            value -= 0x10000
        return value

    async def write_holding_register(self, address: int, value: int) -> bool:
        """Write a single holding register, address is 1-based per Modbus table."""
        await self._ensure_connected()
        if value < 0:
            value += 0x10000
        try:
            result = await self._client.write_register(
                address - 1, value, slave=self._slave_id
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Error writing HR%s: %s", address, err)
            return False
        if result.isError():
            _LOGGER.debug("Modbus error writing HR%s: %s", address, result)
            return False
        return True

    # ---------------------------------------------------------------
    # Coils (function code 0x01 read / 0x05 write)
    # ---------------------------------------------------------------
    async def read_coil(self, address: int) -> bool | None:
        """Read a single coil, address is 1-based per Modbus table."""
        await self._ensure_connected()
        try:
            result = await self._client.read_coils(
                address - 1, count=1, slave=self._slave_id
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Error reading coil %s: %s", address, err)
            return None
        if result.isError():
            _LOGGER.debug("Modbus error reading coil %s: %s", address, result)
            return None
        return bool(result.bits[0])

    async def write_coil(self, address: int, value: bool) -> bool:
        """Write a single coil, address is 1-based per Modbus table."""
        await self._ensure_connected()
        try:
            result = await self._client.write_coil(
                address - 1, value, slave=self._slave_id
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Error writing coil %s: %s", address, err)
            return False
        if result.isError():
            _LOGGER.debug("Modbus error writing coil %s: %s", address, result)
            return False
        return True

    # ---------------------------------------------------------------
    # Input registers (function code 0x04, read only)
    # ---------------------------------------------------------------
    async def read_input_register(self, address: int) -> int | None:
        """Read a single input register, address is 1-based per Modbus table."""
        await self._ensure_connected()
        try:
            result = await self._client.read_input_registers(
                address - 1, count=1, slave=self._slave_id
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Error reading IR%s: %s", address, err)
            return None
        if result.isError():
            _LOGGER.debug("Modbus error reading IR%s: %s", address, result)
            return None
        value = result.registers[0]
        if value >= 0x8000:
            value -= 0x10000
        return value

    async def read_holding_registers_bulk(
        self, addresses: list[int]
    ) -> dict[int, int | None]:
        """Read multiple holding registers individually (controller has gaps)."""
        return {addr: await self.read_holding_register(addr) for addr in addresses}

    async def read_input_registers_bulk(
        self, addresses: list[int]
    ) -> dict[int, int | None]:
        """Read multiple input registers individually (controller has gaps)."""
        return {addr: await self.read_input_register(addr) for addr in addresses}

    async def read_coils_bulk(self, addresses: list[int]) -> dict[int, bool | None]:
        """Read multiple coils individually."""
        return {addr: await self.read_coil(addr) for addr in addresses}
