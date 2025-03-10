from typing import Any

import Engine
from Engine.data.arrays import DataTable


class EngineDataTable:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            return super().__new__(cls)
        else:
            return cls._instance

    def __init__(self):
        interface_shader = Engine.App.assets.load(
            Engine.assets.AssetFileData(
                id=Engine.data.Identifier("interface_shader"),  # interface shader
                type=Engine.DataType.Shader,
                dependencies=[
                    Engine.assets.AssetFileData(
                        type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Vertex),
                        path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                             f"{Engine.data.FileSystem.PRESETS_dir}\\shaders\\"
                             f"interface.vert"
                    ),
                    Engine.assets.AssetFileData(
                        type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Fragment),
                        path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                             f"{Engine.data.FileSystem.PRESETS_dir}\\shaders\\"
                             f"interface.frag"
                    ),
                ]
            )
        ).asset_data
        service_logo = Engine.App.assets.load(
            Engine.assets.AssetFileData(
                id=Engine.data.Identifier("Service.png"),
                type=Engine.assets.AssetType(major=Engine.DataType.PyGame | Engine.DataType.Texture),
                path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                     f"{Engine.data.FileSystem.PRESETS_dir}\\"
                     f"Service.png"
            )
        ).asset_data
        default_logo = Engine.App.assets.load(
            Engine.assets.AssetFileData(
                id=Engine.data.Identifier("Logo.png"),
                type=Engine.assets.AssetType(major=Engine.DataType.PyGame | Engine.DataType.Texture),
                path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                     f"{Engine.data.FileSystem.PRESETS_dir}\\"
                     f"Logo.png"
            )
        ).asset_data

        self.data_table = DataTable(
            interface_shader=interface_shader,
            service_logo=service_logo,
            default_logo=default_logo
        )

    def get(self, item: str) -> Any:
        return self.data_table.get(item)
