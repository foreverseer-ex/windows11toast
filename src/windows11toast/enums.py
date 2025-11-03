"""Enumerations for Windows toast notifications / Windows 通知的枚举类"""

from enum import Enum

# StrEnum compatibility for Python < 3.11
# Python 3.11+ 兼容性：为 Python < 3.11 提供 StrEnum 支持
try:
    from enum import StrEnum
except ImportError:
    class StrEnum(str, Enum):
        """Compatible StrEnum for Python < 3.11 / Python < 3.11 的兼容 StrEnum"""

        def __str__(self):
            return self.value


class ImagePlacement(StrEnum):
    """Image placement options / 图片位置选项"""
    HERO = "hero"
    APP_LOGO_OVERRIDE = "appLogoOverride"
    INLINE = "inline"


class IconPlacement(StrEnum):
    """Icon placement options / 图标位置选项"""
    APP_LOGO_OVERRIDE = "appLogoOverride"
    APP_LOGO_OVERRIDE_AND_HERO = "appLogoOverrideAndHero"


class IconCrop(StrEnum):
    """Icon crop hint options / 图标裁剪提示选项"""
    CIRCLE = "circle"
    NONE = "none"


class AudioEvent(StrEnum):
    """Built-in Windows audio events / 内置 Windows 音频事件"""
    DEFAULT = "ms-winsoundevent:Notification.Default"
    IM = "ms-winsoundevent:Notification.IM"
    MAIL = "ms-winsoundevent:Notification.Mail"
    REMINDER = "ms-winsoundevent:Notification.Reminder"
    SMS = "ms-winsoundevent:Notification.SMS"
    LOOPING_ALARM = "ms-winsoundevent:Notification.Looping.Alarm"
    LOOPING_ALARM2 = "ms-winsoundevent:Notification.Looping.Alarm2"
    LOOPING_ALARM3 = "ms-winsoundevent:Notification.Looping.Alarm3"
    LOOPING_ALARM4 = "ms-winsoundevent:Notification.Looping.Alarm4"
    LOOPING_ALARM5 = "ms-winsoundevent:Notification.Looping.Alarm5"
    LOOPING_ALARM6 = "ms-winsoundevent:Notification.Looping.Alarm6"
    LOOPING_ALARM7 = "ms-winsoundevent:Notification.Looping.Alarm7"
    LOOPING_ALARM8 = "ms-winsoundevent:Notification.Looping.Alarm8"
    LOOPING_ALARM9 = "ms-winsoundevent:Notification.Looping.Alarm9"
    LOOPING_ALARM10 = "ms-winsoundevent:Notification.Looping.Alarm10"
    LOOPING_CALL = "ms-winsoundevent:Notification.Looping.Call"
    LOOPING_CALL2 = "ms-winsoundevent:Notification.Looping.Call2"
    LOOPING_CALL3 = "ms-winsoundevent:Notification.Looping.Call3"
    LOOPING_CALL4 = "ms-winsoundevent:Notification.Looping.Call4"
    LOOPING_CALL5 = "ms-winsoundevent:Notification.Looping.Call5"
    LOOPING_CALL6 = "ms-winsoundevent:Notification.Looping.Call6"
    LOOPING_CALL7 = "ms-winsoundevent:Notification.Looping.Call7"
    LOOPING_CALL8 = "ms-winsoundevent:Notification.Looping.Call8"
    LOOPING_CALL9 = "ms-winsoundevent:Notification.Looping.Call9"
    LOOPING_CALL10 = "ms-winsoundevent:Notification.Looping.Call10"


class ToastDuration(StrEnum):
    """Toast duration options / 通知持续时间选项"""
    SHORT = "short"
    LONG = "long"
    ALARM = "alarm"  # No timeout / 无超时
    REMINDER = "reminder"  # No timeout / 无超时
    INCOMING_CALL = "incomingCall"  # No timeout / 无超时
    URGENT = "urgent"  # No timeout / 无超时


class OcrLanguage(StrEnum):
    """OCR language options / OCR 语言选项"""
    AUTO = "auto"  # Use user profile language / 使用用户配置文件语言
    EN_US = "en-US"
    ZH_CN = "zh-CN"
    JA = "ja"
    KO = "ko"
    FR = "fr"
    DE = "de"
    ES = "es"
    IT = "it"
    PT = "pt"
    RU = "ru"
    AR = "ar"
    HI = "hi"

