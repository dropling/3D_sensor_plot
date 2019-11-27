import json

try:
    from objects.class_point import Point
except ImportError:
    from .objects.class_point import Point


try:
    from objects.class_sensor import Sensor
except ImportError:
    from .objects.class_sensor import Sensor

