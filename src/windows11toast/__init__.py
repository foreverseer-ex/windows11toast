"""Windows 11 Toast Notification Library / Windows 11 通知库

A Pythonic library for creating Windows 10/11 toast notifications.
一个用于创建 Windows 10/11 通知的 Pythonic 库。
"""

# Import enums / 导入枚举
from .enums import (
    ImagePlacement,
    IconPlacement,
    IconCrop,
    AudioEvent,
    ToastDuration,
    OcrLanguage
)

# Import constants / 导入常量
from .constants import DEFAULT_APP_ID

# Import core notification functions / 导入核心通知函数
from .notification import (
    notify,
    toast,
    toast_async,
    atoast,
    clear_toast
)

# Import progress notification functions / 导入进度通知函数
from .progress import (
    notify_progress,
    update_progress
)

# Import media functions / 导入媒体函数
from .media import (
    play_sound,
    speak,
    recognize,
    available_recognizer_languages
)

# Define __all__ for public API / 定义公共API
__all__ = [
    # Enums / 枚举
    'ImagePlacement',
    'IconPlacement',
    'IconCrop',
    'AudioEvent',
    'ToastDuration',
    'OcrLanguage',
    # Constants / 常量
    'DEFAULT_APP_ID',
    # Core functions / 核心函数
    'notify',
    'toast',
    'toast_async',
    'atoast',
    'clear_toast',
    # Progress functions / 进度函数
    'notify_progress',
    'update_progress',
    # Media functions / 媒体函数
    'play_sound',
    'speak',
    'recognize',
    'available_recognizer_languages',
]

__version__ = '1.0.0'
