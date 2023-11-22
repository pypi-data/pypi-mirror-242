from enum import Enum
import os
class Voices(Enum):
    SILVAN = os.path.join(os.path.dirname(__file__), "voices", "silvan.voicex")
    GABBY = os.path.join(os.path.dirname(__file__), "voices", "gabby.voicex")
    GRANNY = os.path.join(os.path.dirname(__file__), "voices", "granny.voicex")
    KIMBERLY = os.path.join(os.path.dirname(__file__), "voices", "kimberly.voicex")