from typing import Optional, final
from loguru import logger

import Engine


@final
class System:
    def __init__(self):
        self._devices: dict[str, Engine.audio.Device] = {}
        self._active_device: Optional[Engine.audio.Device] = None

        logger.success("Engine audio System - init")

    def add_device(self, which: int, is_capture: bool):
        device_name = self.get_device_name(which, is_capture)

        if device_name not in self._devices:
            new_device = Engine.audio.Device(device_name)
            self._devices[device_name] = new_device

            logger.success(f"Add a device with the name {device_name} in the audio System")
        else:
            logger.warning(f"Device with the name {device_name} already added in the audio System")

    def remove_device(self, which: int, is_capture: bool):
        device_name = self.get_device_name(which, is_capture)

        if device_name in self._devices:
            device = self._devices[device_name]
            if device.is_active:
                device.deactivate()
            del self._devices[device_name]

            logger.success(f"Remove a device with name {device_name} in the audio System")
        else:
            logger.warning(f"Device already deleted from the audio System {device_name}")

    @property
    def active_device(self) -> 'Optional[Engine.audio.Device]':
        return self._active_device

    def set_active_device(self, name: str):
        if self._active_device.name == name: return
        if self._active_device is not None: self._active_device.deactivate()

        self._active_device = self._devices[name]
        self._active_device.activate()

    def get_devices(self) -> 'dict[Engine.audio.Device]':
        """Возвращает список всех доступных устройств"""
        return self._devices

    @staticmethod
    def get_device_name(which: int, is_capture: bool):
        return Engine.pg.sdl2.get_audio_device_names(is_capture)[which]

    def get_device_by_name(self, name: str) -> 'Optional[Engine.audio.Device]':
        """Возвращает устройство по имени"""
        return self._devices.get(name)
