from collections.abc import MutableMapping
from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass(kw_only=True)
class ConfigData(AssetData):
    type = Engine.DataType.Config
    content: dict = None

    def setdefault(self, defaults: dict, category_name: str = None):
        """
        Sets the default values in the specified category.
        Automatically creates nested dictionaries for categories.

        :param defaults: Dictionary of default values
        :param category_name: The path to the category is separated by '/' (for example, "Win/size")
        """
        category = self.content
        if category_name:
            for name in category_name.split('/'):
                # Creating a new level, if there is none
                if name not in category:
                    category[name] = {}
                # Checking the type of the existing level
                if not isinstance(category[name], MutableMapping):
                    raise TypeError(f"Категория '{name}' не является словарем")
                category = category[name]

        # Setting the default values
        for key, value in defaults.items():
            category.setdefault(key, value)