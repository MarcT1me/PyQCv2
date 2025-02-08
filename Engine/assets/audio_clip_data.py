from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass
class AudioClipData(AssetData):
    asset_type = Engine.DataType.AudioClip
    data: 'Engine.audio.Clip' = None
