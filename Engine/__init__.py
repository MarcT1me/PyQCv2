""" Hello world!
"""
""" Encapsulations """
import Engine.pg
import Engine.mgl
import Engine.math

""" Engine """
from Engine.constants import *
# data
import Engine.data
import Engine.threading
import Engine.decorators  # need threading and used in data

# wrapper classes
import Engine.timing
import Engine.events.event  # user events class
import Engine.audio

# utils
import Engine.failures
import Engine.assets

# space context
import Engine.objects
# Engine network API
import Engine.network
# main `graphic` module and main graphic class
import Engine.graphic
# GENERAL APP CLASS
import Engine.app
from Engine.app import App
import Engine.api
