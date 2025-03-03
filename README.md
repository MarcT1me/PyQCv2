> # TestApp

###### powered by QuantumCore

<img alt="icon" height="128" src="presets/Logo.png" width="128"/>

### Description
The engine project looks something like the written files outside the Engine.\
In addition, to create a standard project, the Engine folder contains the folder `Engine.data.default_project`. 
This folder contains the project for getting started.

In `main.py` In the demo version of the engine project, the main class `TestApp` is declared. 
It creates application data, initializes the engine, processes events, updates, renders, and their `pre-` counterparts.

To initialize the `TestApp` class, inheritances of the Toml config loader and the related `TestAppData` class are also required.

Later, in the main loop, events are processed in an `event` with decorators for multithreading, single event, and deferred calls.\
nothing happens in the `update` methods, it will be implemented later.\
In the `render` methods, surfaces are rendered before processing (not always permanent), and in the main method, they are already displayed on the screen (always permanent)

To catch errors, `on_failure` is inherited and `on_exit` is used for subsequent processing after the release of the mainloop.
It also calls a method that works only in `debug` mode.

The assets for the `TestApp` class are loaded in the same way before initialization, and they are stored in the `DataTable` in `App.data`.\
The config file is completely dependent on `TestApp`, this is confirmed by the need for inheritance of the loader and `TestAppData`


### Command on compilation
* pyinstaller:
  * windows
    ```shell
    # ========== Build Config ==========
    pyinstaller `
      --name "Test Bild" `
      --icon="presets/Logo.png" `
    
    # ========== Engine Data ==========
      --add-data "C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext" `
      --add-data "Engine/data/settings.engconf;Engine/data/settings.engconf" `
      --add-data "Engine/data/graphics.engconf;Engine/data/graphics.engconf" `
    
    # ========== App Data ==========
      --add-data "presets;presets" `
      --add-data "gamedata;gamedata" `
    
    # ========== Libraries ==========
      --add-data "C:/Program Files/Python311/Lib/site-packages/toml;toml" `
    
    # ========== Entry Point ==========
      main.py  # app file
    ```