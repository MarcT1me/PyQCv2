from typing import Optional, final
from loguru import logger
from dataclasses import dataclass
import sounddevice as sd

import Engine
from Engine.events.event import Event
from Engine.audio.device import Device


class UpdateDefaultDevices(Event):
    def __init__(self, is_input: int):
        super().__init__()
        self.is_input = is_input


@dataclass
class ActiveDevice:
    input: Device
    output: Device


@final
class System:
    update_default: UpdateDefaultDevices = UpdateDefaultDevices(3).update()

    def __init__(self):
        self._devices: dict[str, Device] = {}
        self.active_devices: ActiveDevice = ActiveDevice(None, None)

        logger.success("Engine audio System - init\n")

    def add_device(self, which: int, is_input: bool):
        device_name = self.get_device_name(which, is_input)

        if device_name not in self._devices:
            new_device = Device(
                self, which, is_input,
                device_name
            )
            self._devices[device_name] = new_device

            logger.success(f"Add a device with the name {device_name} in the audio System\n")
        else:
            logger.warning(f"Device with the name {device_name} already added in the audio System\n")

    def remove_device(self, which: int, is_input: bool):
        device_name = self.get_device_name(which, is_input)

        if device_name in self._devices:
            device = self._devices[device_name]
            if device.is_active:
                device.deactivate()
            del self._devices[device_name]

            logger.success(f"Remove a device with name {device_name} in the audio System")
        else:
            logger.warning(f"Device already deleted from the audio System {device_name}")

    def set_default_device(self, is_input):
        device_sd_index = sd.default.device[0] if is_input else sd.default.device[1]
        device_name = sd.query_devices(device_sd_index)["name"]

        logger.info(
            f"Engine audio System - set_default_device\n"
            f"input: {is_input}\n"
            f"name: {device_name}"
        )
        self.activate_device(device_name)

    def activate_device(self, name: str):
        device = self._devices[name]
        active_device = self.active_devices.input if device.is_input else self.active_devices.output

        if active_device is not None:
            if active_device.name == name:
                return
            else:
                active_device.deactivate()

        if device.is_input:
            self.active_devices.input = device
        else:
            self.active_devices.output = device
        device.activate()

    def deactivate_device(self, name: str):
        device = self._devices[name]
        active_device = self.active_devices.input if device.is_input else self.active_devices.output

        if active_device is not None:
            if active_device.name != name:
                return

        if device.is_input:
            self.active_devices.input = None
        else:
            self.active_devices.output = None
        device.deactivate()

    def get_devices(self) -> dict[str, Device]:
        """Возвращает список всех доступных устройств"""
        return self._devices

    @staticmethod
    def get_device_name(which: int, is_input: bool):
        return Engine.pg.sdl2.get_audio_device_names(is_input)[which]

    def get_device_by_name(self, name: str) -> Optional[Device]:
        """Возвращает устройство по имени"""
        return self._devices.get(name)
