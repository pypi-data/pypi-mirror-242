from enum import Enum


class SinkFormat(Enum):
    Y800 = 0
    RGB24 = 1
    RGB32 = 2
    UYVY = 3
    Y16 = 4


class FRAMEFILTER_PARAM_TYPE(Enum):
    eParamLong = 0
    eParamBoolean = 1
    eParamFloat = 2
    eParamString = 3
    eParamData = 4


class ImageFileType(Enum):
    BMP = 0
    JPEG = 1


class CameraProperty(Enum):
    PAN = 0
    TILT = 1
    ROLL = 2
    ZOOM = 3
    EXPOSURE = 4
    IRIS = 5
    FOCUS = 6


class VideoProperty(Enum):
    BRIGHTNESS = 0
    CONTRAST = 1
    HUE = 2
    SATURATION = 3
    SHARPNESS = 4
    GAMMA = 5
    COLORENABLE = 6
    WHITEBALANCE = 7
    BLACKLIGHTCOMPENSATION = 8
    GAIN = 9
