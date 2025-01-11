import struct
from dataclasses import dataclass, field
from Engine.math import vec3

@dataclass
class LightData:
    position: vec3 = field(default=vec3(0, 0, 0))  # 3 x float32
    color: vec3 = field(default=vec3(1, 1, 1))  # 3 x byte (0-255)
    intensity: int = field(default=100)  # int16

    def __bytes__(self) -> bytes:
        """
        Сериализация LightData в бинарный формат.
        """
        # Упаковываем цвет в 3 байта (RGB)
        r, g, b = [int(c * 255) for c in self.color]
        color_data = (r << 24) | (g << 16) | (b << 8)

        # Упаковываем данные в бинарный формат
        return struct.pack(
            "3f I H",  # Формат: 3 float, 3 byte, 1 ushort
            self.position.x, self.position.y, self.position.z,  # position (12 байт)
            color_data,  # color (3 байта)
            self.intensity  # intensity (2 байта)
        )

@dataclass
class PointLightData(LightData):
    radius: int = field(default=10)  # int16

    def __bytes__(self) -> bytes:
        """
        Сериализация PointLight в бинарный формат.
        """
        parent_bytes = super().__bytes__()
        return parent_bytes + struct.pack("H", self.radius)  # radius (2 байта)

@dataclass
class DirectionalLightData(LightData):
    direction: vec3 = field(default=vec3(0, 0, 0))  # 9 бит (3 x 3 бита)

    def __bytes__(self) -> bytes:
        """
        Сериализация DirectionalLightData в бинарный формат.
        """
        parent_bytes = super().__bytes__()

        # Упаковываем direction в 9 бит (3 x 3 бита)
        packed_direction = (
            (int(self.direction.x * 7) & 0x7) << 6 |
            (int(self.direction.y * 7) & 0x7) << 3 |
            (int(self.direction.z * 7) & 0x7)
        )
        return parent_bytes + struct.pack("B", packed_direction)  # direction (1 байт)

@dataclass
class SpotLightData(PointLightData, DirectionalLightData):
    cone_angle: int = field(default=45)  # 9 бит

    def __bytes__(self) -> bytes:
        """
        Сериализация SpotLight в бинарный формат.
        """
        parent_bytes = super(PointLightData).__bytes__()
        parent_bytes += super(DirectionalLightData).__bytes__()

        # Упаковываем cone_angle в 9 бит
        packed_cone_angle = self.cone_angle & 0x1FF  # 9 бит
        return parent_bytes + struct.pack("B", packed_cone_angle)  # cone_angle (1 байт)