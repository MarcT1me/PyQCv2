""" Hello world!
"""
""" Encapsulations """
import Engine.pg
import Engine.mgl
import Engine.math

""" Basic """
# data
from Engine.constants import *
import Engine.data
# utils
import Engine.failures
import Engine.threading
import Engine.decorators  # need threading and used in data

# wrapper classes
import Engine.timing
import Engine.events  # user events class
import Engine.audio

""" Systems """
# file loading
import Engine.assets
# space context
import Engine.objects
# network
import Engine.network
# main `graphic` module
import Engine.graphic

import Engine.scripts
# GENERAL APP CLASS
import Engine.app
from Engine.app import App
import Engine.api
