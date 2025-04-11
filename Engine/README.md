> QuantumCore Game Engine

<img alt="icon" height="128" src="data/presets/Logo.png" width="128"/>

## Description

This is the engine itself.\
The engine is implemented using SDL(PyGame) and the OpenGL graphics library (ModernGL). In the future, it is planned to
change the graphics library to DirectX or Vulkan in order to introduce modern technologies similar to RTX or DLSS.

### Briefly about the engine

Several modules are implemented in the engine:

- app - the App class and AppData needed to create your own entry point class
- assets - a module with tools and standard asset classes and their loaders from the file system
- audio - sub-system working with sound, in the future it is planned to transfer from SDL to other libraries to add better functionality
- decorators - various tools for changing the operation of some functions, for example: multithreaded functions or functions with support for post-calls
- events - a sub-system for event handling
- network - a sub-system for data transfer between the server and the client of the game
- objects - objects related to the scene, for example, a Sama scene, a light source, or a camera
- scripts - small additions, so far only for experiments
- timing - sub-system for working with time, triggering deferred events and FPS management
- graphics - a huge sub-system for working with graphics (shaders have not yet been implemented)
- failures - a module for catching errors and accurately processing them in an application or handler
- threading - a module for working with many threads and improved locking

All of them implement intuitive aspects of the game, which I described just in case.\

I did not mention the data module. It implements engine data, loading configs (not very good yet, via exec), and storing file system data in the engine. The standard project, shaders, and standard images such as icons and window backgrounds with error messages are also stored there.

And now I will describe the approximate work of some complex ones.:

##### assets
This module initializes its manager first. This is done by registering all types of files (and their uploaders), which can be easily downloaded, knowing only its type, without having the downloader itself with you.\
TomlConfigLoader in [TestApp](../main.pyw) L9-L32 was used as an example.

##### events
An incomplete event processing module, it should send messages to subscribers in the future and implement mouse events and many others.

##### timing
Just a class for working with time in an application, it can simulate delays, delay a cycle based on the number of tps, create timers, or issue events to the main cycle with a delay

##### failures
An old module with an old implementation. It implements its own Catch, which catches errors, wraps them in Failure and passes them to the handler. All this happens in connection with the trapping settings.

##### objects
The module implements interfaces for different types of cyclic events (the main ICL is event -> update -> render -> repeat). Everything starts working in the scene, which starts processing for other nodes and is itself a node (there may be a scene in the scene). Different types of nodes are implemented, each of which implements a new and new aspect, which allows you to use different nodes for different tasks. Standard objects are also implemented here, such as a camera and a light source. In the future, a model node will be implemented that will combine almost all the engine modules.

##### graphics
the most massive module. implemented aspects
- window for managing the main window and additional
- interface is a surface for rendering on top of the scene (in the future, a new one will be added that can render interface objects on the GPU)
- the model collects many different types of assets and can be used in the previously described object. The Model combines a 3D grid of Mesh points, Material, and the model object itself, wrapping everything in one class.
- GL is an internal engine module with its own sub-system for working with a video card. So far, it has not been implemented at all. But the structure is already emerging
  1. buffer - moving data from CPU to GPU
  2. gl-data - the object data of this sub-system
  3. shader - creating shaders and uploading them to the GPU
  4. vertex is an extremely crude structure. The lowest level of work with Mash is implemented here.
  5. texture - loading textures into a video card with the ability to control it on the CPU (for example, for decals)

Sub-systems have been described more than once in the description. These are special classes that combine the entire module to simplify work with a certain aspect.
Such sub-systems are initialized during App creation and remain static during its operation.

To simplify working with data from systems and other metaobjects, MetaData was implemented. These are objects that can be passed from object to object and, without access to the scene, change its data, etc. It also simplifies the initialization of the sub-system and objects, allowing you to store data in files and initialize them without any problems when uploading files (for example, configs or game saving).

In addition to MetaObject, the data module also implements several interesting data types:
- Transform, which stores object data in 3d (for 2d, z is simply ignored)
 - returnValue, which was made for rare cases. I plan to cut it out as unnecessary and difficult to use.
 - Identifier, stores the unique object id and its name
- arrays - a collection of different types of arrays, for example, a roster, which is a tree. In the future, it is planned to introduce into all engine modules, simplifying the search for MetaData by getting data along the "path" (for example, "shader/id" or "audio/device/id") 


So far, this is all that is implemented in the engine, as well as a lot is planned, for example:
  - d - variables connecting several objects, this will be useful, for example, for logical circuits in a game (transmitting a signal from one object to another along a chain of d variables)
- finally, adding physics
- surfaces for rendering (for example, for in-game dynamic surfaces like screens)
- adding normal functions and classes to scripts, for example widgets Interface