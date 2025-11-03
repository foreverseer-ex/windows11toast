import asyncio
from pathlib import Path
from typing import Optional, Dict, List, Callable, Union, Any
from enum import Enum
from winrt.windows.data.xml.dom import XmlDocument
from winrt.windows.foundation import IPropertyValue
from winrt.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    NotificationData,
    ToastActivatedEventArgs,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)

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


DEFAULT_APP_ID = 'Python'

xml = """
<toast activationType="protocol" launch="http:" scenario="{scenario}">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
"""


def set_attribute(document, xpath, name, value):
    attribute = document.create_attribute(name)
    attribute.value = value
    document.select_single_node(xpath).attributes.set_named_item(attribute)


def add_text(msg, document):
    if isinstance(msg, str):
        msg = {
            'text': msg
        }
    binding = document.select_single_node('//binding')
    text = document.create_element('text')
    for name, value in msg.items():
        if name == 'text':
            text.inner_text = msg['text']
        else:
            text.set_attribute(name, value)
    binding.append_child(text)


def add_icon(icon_src: str, placement: Optional[Union[str, IconPlacement]] = None,
             hint_crop: Optional[Union[str, IconCrop]] = None, document=None):
    """
    Add icon to toast notification.
    向通知添加图标。

    Args / 参数:
        icon_src: Icon source URL/path / 图标源URL/路径
        placement: Icon placement / 图标位置
        hint_crop: Icon crop hint / 图标裁剪提示
        document: XML document / XML文档
    """
    if document is None:
        raise ValueError("document parameter is required")

    # Convert StrEnum to string if needed / 如果需要，将 StrEnum 转换为字符串
    placement_str = str(placement) if placement else 'appLogoOverride'
    hint_crop_str = str(hint_crop) if hint_crop else 'circle'

    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    image.set_attribute('src', icon_src)
    image.set_attribute('placement', placement_str)
    image.set_attribute('hint-crop', hint_crop_str)
    binding.append_child(image)


def add_image(image_src: str, placement: Optional[Union[str, ImagePlacement]] = None, document=None):
    """
    Add image to toast notification.
    向通知添加图片。

    Args / 参数:
        image_src: Image source URL/path / 图片源URL/路径
        placement: Image placement / 图片位置
        document: XML document / XML文档
    """
    if document is None:
        raise ValueError("document parameter is required")

    # Convert StrEnum to string if needed / 如果需要，将 StrEnum 转换为字符串
    placement_str = str(placement) if placement else None

    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    image.set_attribute('src', image_src)
    if placement_str:
        image.set_attribute('placement', placement_str)
    binding.append_child(image)


def add_progress(prog, document):
    binding = document.select_single_node('//binding')
    progress = document.create_element('progress')
    for name in prog:
        progress.set_attribute(name, '{' + name + '}')
    binding.append_child(progress)


def add_audio(audio_src: Optional[Union[str, AudioEvent]] = None,
              loop: bool = False, document=None):
    """
    Add audio to toast notification.
    向通知添加音频。

    Args / 参数:
        audio_src: Audio source (URL, file path, or AudioEvent) / 音频源（URL、文件路径或AudioEvent）
        loop: Whether to loop the audio / 是否循环播放音频
        document: XML document / XML文档
    """
    if document is None:
        raise ValueError("document parameter is required")

    toast = document.select_single_node('/toast')
    audio = document.create_element('audio')

    if audio_src:
        # Convert StrEnum to string if needed / 如果需要，将 StrEnum 转换为字符串
        audio_src_str = str(audio_src)
        audio.set_attribute('src', audio_src_str)
        if loop:
            audio.set_attribute('loop', 'true')
    else:
        # Silent / 静音
        audio.set_attribute('silent', 'true')

    toast.append_child(audio)


def create_actions(document):
    toast = document.select_single_node('/toast')
    actions = document.create_element('actions')
    toast.append_child(actions)
    return actions


def add_button(button, document):
    if isinstance(button, str):
        button = {
            'activationType': 'protocol',
            'arguments': 'http:' + button,
            'content': button
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    action = document.create_element('action')
    for name, value in button.items():
        action.set_attribute(name, value)
    actions.append_child(action)


def add_input(id, document):
    if isinstance(id, str):
        id = {
            'id': id,
            'type': 'text',
            'placeHolderContent': id
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    for name, value in id.items():
        input.set_attribute(name, value)
    actions.append_child(input)


def add_selection(selection, document):
    if isinstance(selection, list):
        selection = {
            'input': {
                'id': 'selection',
                'type': 'selection'
            },
            'selection': selection
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    input = document.create_element('input')
    for name, value in selection['input'].items():
        input.set_attribute(name, value)
    actions.append_child(input)
    for sel in selection['selection']:
        if isinstance(sel, str):
            sel = {
                'id': sel,
                'content': sel
            }
        selection_element = document.create_element('selection')
        for name, value in sel.items():
            selection_element.set_attribute(name, value)
        input.append_child(selection_element)


result = list()


def result_wrapper(*args):
    global result
    result = args
    return result


def _default_on_click(result: Dict[str, Any]) -> None:
    """
    Default on_click handler that does nothing.
    默认的on_click处理器，不执行任何操作。

    Args / 参数:
        result: Notification result dictionary / 通知结果字典
    """
    pass


def activated_args(_, event) -> Dict[str, Any]:
    """
    Extract activation arguments from toast notification event.
    从通知事件中提取激活参数。

    Args / 参数:
        _: Unused parameter / 未使用的参数
        event: Toast activation event / 通知激活事件

    Returns / 返回:
        Dictionary with 'arguments' and 'user_input' keys / 包含'arguments'和'user_input'键的字典
    """
    global result
    e = ToastActivatedEventArgs._from(event)
    user_input = dict([(name, IPropertyValue._from(
        e.user_input[name]).get_string()) for name in e.user_input.keys()])
    result = {
        'arguments': e.arguments,
        'user_input': user_input
    }
    return result


async def play_sound(audio: str) -> None:
    """
    Play audio file using Windows Media Player.
    使用Windows媒体播放器播放音频文件。

    Args / 参数:
        audio: Audio file path or URL / 音频文件路径或URL
    """
    from winrt.windows.media.core import MediaSource
    from winrt.windows.media.playback import MediaPlayer

    if audio.startswith('http'):
        from winrt.windows.foundation import Uri
        source = MediaSource.create_from_uri(Uri(audio))
    else:
        from winrt.windows.storage import StorageFile
        file = await StorageFile.get_file_from_path_async(audio)
        source = MediaSource.create_from_storage_file(file)

    player = MediaPlayer()
    player.source = source
    player.play()
    await asyncio.sleep(7)


async def speak(text: str) -> None:
    """
    Speak text using Windows speech synthesis.
    使用Windows语音合成朗读文本。

    Args / 参数:
        text: Text to speak / 要朗读的文本
    """
    from winrt.windows.media.core import MediaSource
    from winrt.windows.media.playback import MediaPlayer
    from winrt.windows.media.speechsynthesis import SpeechSynthesizer

    # print(list(map(lambda info: info.description, SpeechSynthesizer.get_all_voices())))

    stream = await SpeechSynthesizer().synthesize_text_to_stream_async(text)
    player = MediaPlayer()
    player.source = MediaSource.create_from_stream(stream, stream.content_type)
    player.play()
    await asyncio.sleep(7)


async def recognize(ocr_src: str, lang: Optional[Union[str, OcrLanguage]] = None):
    """
    Recognize text from an image using OCR.
    使用OCR识别图片中的文本。

    Args / 参数:
        ocr_src: Image source URL or file path / 图片源URL或文件路径
        lang: OCR language (OcrLanguage enum or language tag like 'en-US'). None for auto / OCR语言（OcrLanguage枚举或语言标签如'en-US'）。None表示自动

    Returns / 返回:
        OCR result object / OCR结果对象
    """
    from winrt.windows.media.ocr import OcrEngine
    from winrt.windows.graphics.imaging import BitmapDecoder

    if ocr_src.startswith('http'):
        from winrt.windows.foundation import Uri
        from winrt.windows.storage.streams import RandomAccessStreamReference
        ref = RandomAccessStreamReference.create_from_uri(Uri(ocr_src))
        stream = await ref.open_read_async()
    else:
        from winrt.windows.storage import StorageFile, FileAccessMode
        file = await StorageFile.get_file_from_path_async(ocr_src)
        stream = await file.open_async(FileAccessMode.READ)
    decoder = await BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()

    if lang:
        from winrt.windows.globalization import Language
        lang_str = str(lang) if lang != OcrLanguage.AUTO else None
        if lang_str and OcrEngine.is_language_supported(Language(lang_str)):
            engine = OcrEngine.try_create_from_language(Language(lang_str))
        else:
            class UnsupportedOcrResult:
                def __init__(self):
                    self.text = 'Please install. Get-WindowsCapability -Online -Name "Language.OCR*"'

            return UnsupportedOcrResult()
    else:
        engine = OcrEngine.try_create_from_user_profile_languages()
    # Available properties (lines, angle, word, BoundingRect(x,y,width,height))
    # https://docs.microsoft.com/en-us/uwp/api/windows.media.ocr.ocrresult?view=winrt-22621#properties
    return await engine.recognize_async(bitmap)


def available_recognizer_languages():
    from winrt.windows.media.ocr import OcrEngine
    for language in OcrEngine.get_available_recognizer_languages():
        print(language.display_name, language.language_tag)
    print('Run as Administrator')
    print('Get-WindowsCapability -Online -Name "Language.OCR*"')
    print('Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"')


# Store original notification info for update_progress
_notification_cache = {}
_notification_sequence = {}


def notify(title: Optional[str] = None, body: Optional[str] = None,
           on_click: Optional[Union[Callable, str]] = None,
           # Image options / 图片选项
           image_src: Optional[str] = None,
           image_placement: Optional[Union[str, ImagePlacement]] = None,
           # Icon options / 图标选项
           icon_src: Optional[str] = None,
           icon_placement: Optional[Union[str, IconPlacement]] = None,
           icon_hint_crop: Optional[Union[str, IconCrop]] = None,
           # Progress options / 进度选项
           progress_title: Optional[str] = None,
           progress_status: Optional[str] = None,
           progress_value: Optional[float] = None,
           progress_value_string_override: Optional[str] = None,
           # Audio options / 音频选项
           audio: Optional[Union[str, AudioEvent]] = None,
           audio_loop: bool = False,
           # Text-to-speech / 文本转语音
           dialogue: Optional[str] = None,
           # Duration / 持续时间
           duration: Optional[Union[str, ToastDuration]] = None,
           # Input options / 输入选项
           input_id: Optional[str] = None,
           input_placeholder: Optional[str] = None,
           # Selection options / 选择选项
           selection_id: Optional[str] = None,
           selections: Optional[List[str]] = None,
           # Button options / 按钮选项
           button_content: Optional[str] = None,
           buttons: Optional[List[str]] = None,
           # Advanced options / 高级选项
           xml: Optional[str] = None,
           app_id: str = DEFAULT_APP_ID,
           tag: Optional[str] = None,
           group: Optional[str] = None) -> ToastNotification:
    """
    Create and show a Windows toast notification.
    创建并显示一个 Windows 通知。

    Args / 参数:
        title: Notification title text / 通知标题文本
        body: Notification body text / 通知正文文本
        on_click: Callback function or URL string / 回调函数或URL字符串

        # Image options / 图片选项
        image_src: Image source URL/path / 图片源URL/路径
        image_placement: Image placement (ImagePlacement enum or str) / 图片位置（ImagePlacement枚举或字符串）

        # Icon options / 图标选项
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement (IconPlacement enum or str) / 图标位置（IconPlacement枚举或字符串）
        icon_hint_crop: Icon crop hint (IconCrop enum or str) / 图标裁剪提示（IconCrop枚举或字符串）

        # Progress options / 进度选项
        progress_title: Progress bar title / 进度条标题
        progress_status: Progress status text / 进度状态文本
        progress_value: Progress value (0.0 to 1.0) / 进度值（0.0到1.0）
        progress_value_string_override: Custom progress string / 自定义进度字符串

        # Audio options / 音频选项
        audio: Audio source (AudioEvent enum, URL, or file path). None for silent / 音频源（AudioEvent枚举、URL或文件路径）。None表示静音
        audio_loop: Whether to loop the audio / 是否循环播放音频

        # Text-to-speech / 文本转语音
        dialogue: Text to speak / 要朗读的文本

        # Duration / 持续时间
        duration: Toast duration (ToastDuration enum or str) / 通知持续时间（ToastDuration枚举或字符串）

        # Input options / 输入选项
        input_id: Input field ID / 输入字段ID
        input_placeholder: Input placeholder text / 输入占位符文本

        # Selection options / 选择选项
        selection_id: Selection field ID / 选择字段ID
        selections: List of selection options / 选择选项列表

        # Button options / 按钮选项
        button_content: Single button content / 单个按钮内容
        buttons: List of button contents / 按钮内容列表

        # Advanced options / 高级选项
        xml: Custom XML template / 自定义XML模板
        app_id: Application ID / 应用程序ID
        tag: Notification tag / 通知标签
        group: Notification group / 通知组

    Returns / 返回:
        ToastNotification object / ToastNotification对象

    Examples / 示例:
        # Basic notification / 基本通知
        notify('Hello', 'World')

        # With image / 带图片
        notify('Hello', 'World', image_src='path/to/image.jpg', image_placement=ImagePlacement.HERO)

        # With audio / 带音频
        notify('Hello', 'World', audio=AudioEvent.LOOPING_ALARM, audio_loop=True)

        # Silent notification / 静音通知
        notify('Hello', 'World', audio=None)
    """
    # Determine scenario from duration if it's a no-timeout option / 如果duration是无超时选项，确定scenario
    scenario = None
    duration_str = None
    if duration:
        duration_str = str(duration)
        # Check if duration is a scenario (no timeout) / 检查duration是否为场景（无超时）
        if duration_str in ['alarm', 'reminder', 'incomingCall', 'urgent']:
            scenario = duration_str
        else:
            duration_str = duration_str if duration_str in ['short', 'long'] else None

    document = XmlDocument()
    # Use the xml parameter if provided, otherwise use the module-level xml variable / 如果提供了xml参数则使用，否则使用模块级xml变量
    xml_template = xml
    if xml_template is None:
        # Use module-level xml variable / 使用模块级xml变量
        xml_template = globals().get('xml')
    if xml_template is None:
        # Default XML template / 默认XML模板
        xml_template = """
<toast activationType="protocol" launch="http:" scenario="{scenario}">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>"""
    document.load_xml(xml_template.format(scenario=scenario if scenario else 'default'))

    if isinstance(on_click, str):
        set_attribute(document, '/toast', 'launch', on_click)

    if duration_str:
        set_attribute(document, '/toast', 'duration', duration_str)

    # Use progress_title/progress_status if provided, otherwise use title/body / 如果提供了progress_title/progress_status则使用，否则使用title/body
    display_title = progress_title if progress_title else title
    display_body = progress_status if progress_status else body

    if display_title:
        add_text(display_title, document)
    if display_body:
        add_text(display_body, document)

    # Store notification info for updates
    has_progress = progress_value is not None or progress_title is not None or progress_status is not None
    notification_tag = tag if tag else ('my_tag' if has_progress else None)
    if notification_tag:
        _notification_cache[notification_tag] = {
            'title': display_title,
            'body': display_body,
            'progress_title': progress_title,
            'app_id': app_id,
            'group': group,
            'icon_src': icon_src,
            'icon_placement': icon_placement,
            'icon_hint_crop': icon_hint_crop,
            'image_src': image_src,
            'image_placement': image_placement
        }
        # Initialize sequence number
        if notification_tag not in _notification_sequence:
            _notification_sequence[notification_tag] = 1

    # Add input field / 添加输入字段
    if input_id:
        add_input({'id': input_id, 'type': 'text', 'placeHolderContent': input_placeholder or input_id}, document)

    # Add selection field / 添加选择字段
    if selection_id and selections:
        add_selection({'input': {'id': selection_id, 'type': 'selection'}, 'selection': selections}, document)

    # Add buttons / 添加按钮
    if button_content:
        add_button(button_content, document)
    if buttons:
        for btn_content in buttons:
            add_button(btn_content, document)

    # Add icon / 添加图标
    if icon_src:
        add_icon(icon_src, icon_placement, icon_hint_crop, document)

    # Add image / 添加图片
    if image_src:
        add_image(image_src, image_placement, document)

    # Add progress bar / 添加进度条
    if has_progress:
        progress_dict = {}
        if progress_title:
            progress_dict['title'] = progress_title
        if progress_status:
            progress_dict['status'] = progress_status
        if progress_value is not None:
            progress_dict['value'] = str(progress_value)
        if progress_value_string_override:
            progress_dict['valueStringOverride'] = progress_value_string_override
        add_progress(progress_dict, document)

    # Handle audio / 处理音频
    audio_src = None
    audio_loop_flag = False
    if audio is not None:
        # Check if it's a file path / 检查是否为文件路径
        if isinstance(audio, str) and not audio.startswith('ms-winsoundevent:'):
            path = Path(audio)
            if path.is_file():
                audio_src = f"file:///{path.absolute().as_posix()}"
            else:
                # Assume it's a URL / 假设是URL
                audio_src = audio
        else:
            # Convert StrEnum to string if needed / 如果需要，将 StrEnum 转换为字符串
            audio_src = str(audio)
        audio_loop_flag = audio_loop

    # Add audio or make silent / 添加音频或设置为静音
    if dialogue:
        # Text-to-speech needs silent audio / 文本转语音需要静音音频
        add_audio(None, False, document)
    elif audio_src:
        add_audio(audio_src, audio_loop_flag, document)
    elif audio is None and (dialogue or has_progress):
        # Silent for progress notifications or when explicitly set to None / 进度通知静音或显式设置为None
        add_audio(None, False, document)

    notification = ToastNotification(document)

    # Set up progress data if needed / 如果需要，设置进度数据
    if has_progress:
        data = NotificationData()
        if notification_tag:
            if notification_tag not in _notification_sequence:
                _notification_sequence[notification_tag] = 1

        progress_dict = {}
        if progress_title:
            progress_dict['title'] = progress_title
        if progress_status:
            progress_dict['status'] = progress_status
        if progress_value is not None:
            progress_dict['value'] = str(progress_value)
        if progress_value_string_override:
            progress_dict['valueStringOverride'] = progress_value_string_override

        for name, value in progress_dict.items():
            data.values[name] = str(value)
        data.sequence_number = _notification_sequence.get(notification_tag, 1) if notification_tag else 1
        notification.data = data
        notification.tag = notification_tag or 'my_tag'

    if tag:
        notification.tag = tag
    if group:
        notification.group = group

    if app_id == DEFAULT_APP_ID:
        try:
            notifier = ToastNotificationManager.create_toast_notifier()
        except Exception as e:
            notifier = ToastNotificationManager.create_toast_notifier_with_id(app_id)
    else:
        notifier = ToastNotificationManager.create_toast_notifier_with_id(app_id)
    notifier.show(notification)
    return notification


async def toast_async(title: Optional[str] = None, body: Optional[str] = None,
                      on_click: Optional[Union[Callable, str]] = None,
                      icon: Optional[Union[str, Dict[str, str]]] = None,
                      image: Optional[Union[str, Dict[str, str]]] = None,
                      progress: Optional[Dict[str, Any]] = None,
                      audio: Optional[Union[str, Dict[str, str]]] = None,
                      dialogue: Optional[str] = None,
                      duration: Optional[str] = None,
                      input: Optional[Union[str, Dict[str, str]]] = None,
                      inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
                      selection: Optional[Union[List[str], Dict[str, Any]]] = None,
                      selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
                      button: Optional[Union[str, Dict[str, str]]] = None,
                      buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
                      xml: str = xml,
                      app_id: str = DEFAULT_APP_ID,
                      ocr: Optional[Union[str, Dict[str, str]]] = None,
                      on_dismissed: Callable = print,
                      on_failed: Callable = print,
                      scenario: Optional[str] = None,
                      tag: Optional[str] = None,
                      group: Optional[str] = None,
                      # Parameterized image options / 参数化的图片选项
                      image_src: Optional[str] = None,
                      image_placement: Optional[str] = None,
                      # Parameterized icon options / 参数化的图标选项
                      icon_src: Optional[str] = None,
                      icon_placement: Optional[str] = None,
                      icon_hint_crop: Optional[str] = None) -> Dict[str, Any]:
    """
    Create and show a Windows toast notification (async version).
    创建并显示一个 Windows 通知（异步版本）。

    Args / 参数:
        title: Notification title text / 通知标题文本
        body: Notification body text / 通知正文文本
        on_click: Callback function or URL string / 回调函数或URL字符串
        on_dismissed: Callback function for dismissal / 通知被关闭时的回调函数
        on_failed: Callback function for failure / 通知失败时的回调函数
        icon: Icon URL/path (string) or dict with icon options / 图标URL/路径（字符串）或图标选项字典
        image: Image URL/path (string) or dict with image options / 图片URL/路径（字符串）或图片选项字典
        progress: Dictionary with progress values / 进度值字典
        audio: Audio file path or Windows sound event / 音频文件路径或Windows声音事件
        dialogue: Text to speak / 要朗读的文本
        duration: Toast duration ('short' or 'long') / 通知持续时间（'short' 或 'long'）
        input: Single input field / 单个输入字段
        inputs: List of input fields / 输入字段列表
        selection: Single selection field / 单个选择字段
        selections: List of selection fields / 选择字段列表
        button: Single button / 单个按钮
        buttons: List of buttons / 按钮列表
        xml: Custom XML template / 自定义XML模板
        app_id: Application ID / 应用程序ID
        ocr: OCR image path or dict / OCR图片路径或字典
        scenario: Toast scenario / 通知场景
        tag: Notification tag / 通知标签
        group: Notification group / 通知组

        # Parameterized image options (alternative to image dict) / 参数化的图片选项（替代图片字典）
        image_src: Image source URL/path / 图片源URL/路径
        image_placement: Image placement ('hero', 'appLogoOverride', 'inline') / 图片位置（'hero', 'appLogoOverride', 'inline'）

        # Parameterized icon options (alternative to icon dict) / 参数化的图标选项（替代图标字典）
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement ('appLogoOverride', 'appLogoOverrideAndHero') / 图标位置（'appLogoOverride', 'appLogoOverrideAndHero'）
        icon_hint_crop: Icon crop hint ('circle', 'none') / 图标裁剪提示（'circle', 'none'）

    Returns / 返回:
        Result dictionary / 结果字典

    Examples / 示例:
        # Simple notification / 简单通知
        await toast_async('Hello', 'World')

        # With parameterized image / 使用参数化的图片
        await toast_async('Hello', 'World', image_src='path/to/image.jpg', image_placement='hero')
    """
    # Handle OCR first / 首先处理OCR
    if ocr:
        title = 'OCR Result'
        body = (await recognize(ocr)).text
        src = ocr if isinstance(ocr, str) else ocr['ocr']
        if not image_src:
            image_src = src
            image_placement = ImagePlacement.HERO if not image_placement else image_placement

    # Convert old dict-style parameters to new parameterized format / 将旧字典参数转换为新参数化格式
    # Only use dict parameters if parameterized ones are not provided / 只有在没有提供参数化参数时才使用字典参数
    if icon and not icon_src:
        if isinstance(icon, str):
            icon_src = icon
        elif isinstance(icon, dict):
            icon_src = icon.get('src')
            if not icon_placement:
                icon_placement = icon.get('placement')
            if not icon_hint_crop:
                icon_hint_crop = icon.get('hint-crop')

    if image and not image_src:
        if isinstance(image, str):
            image_src = image
        elif isinstance(image, dict):
            image_src = image.get('src')
            if not image_placement:
                image_placement = image.get('placement')

    # Convert progress dict to parameterized format / 将进度字典转换为参数化格式
    progress_title = None
    progress_status = None
    progress_value = None
    progress_value_string_override = None
    if progress:
        progress_title = progress.get('title')
        progress_status = progress.get('status')
        if 'value' in progress:
            progress_value = float(progress['value'])
        progress_value_string_override = progress.get('valueStringOverride')

    # Convert audio dict to parameterized format / 将音频字典转换为参数化格式
    audio_src = audio
    audio_loop_flag = False
    if isinstance(audio, dict):
        audio_src = audio.get('src')
        audio_loop_flag = audio.get('loop') == 'true' or audio.get('loop') is True

    # Convert duration to ToastDuration enum if needed / 如果需要，将duration转换为ToastDuration枚举
    duration_enum = duration
    if isinstance(duration, str):
        # Try to match to ToastDuration enum / 尝试匹配到ToastDuration枚举
        duration_upper = duration.upper()
        if hasattr(ToastDuration, duration_upper):
            duration_enum = getattr(ToastDuration, duration_upper)

    # Convert input to parameterized format / 将输入转换为参数化格式
    input_id_param = None
    input_placeholder_param = None
    if input:
        if isinstance(input, str):
            input_id_param = input
            input_placeholder_param = input
        elif isinstance(input, dict):
            input_id_param = input.get('id')
            input_placeholder_param = input.get('placeHolderContent') or input.get('placeholder')

    # Convert selection to parameterized format / 将选择转换为参数化格式
    selection_id_param = None
    selections_param = None
    if selection:
        if isinstance(selection, list):
            selection_id_param = 'selection'
            selections_param = selection
        elif isinstance(selection, dict):
            selection_id_param = selection.get('input', {}).get('id', 'selection')
            selections_param = selection.get('selection', [])

    # Convert button to parameterized format / 将按钮转换为参数化格式
    button_content_param = None
    buttons_param = buttons
    if button:
        if isinstance(button, str):
            button_content_param = button
        elif isinstance(button, dict):
            button_content_param = button.get('content')

    notification = notify(
        title=title,
        body=body,
        on_click=on_click,
        image_src=image_src,
        image_placement=image_placement,
        icon_src=icon_src,
        icon_placement=icon_placement,
        icon_hint_crop=icon_hint_crop,
        progress_title=progress_title,
        progress_status=progress_status,
        progress_value=progress_value,
        progress_value_string_override=progress_value_string_override,
        audio=audio_src,
        audio_loop=audio_loop_flag,
        dialogue=dialogue,
        duration=duration_enum,
        input_id=input_id_param,
        input_placeholder=input_placeholder_param,
        selection_id=selection_id_param,
        selections=selections_param if selections_param else selections,
        button_content=button_content_param,
        buttons=buttons_param,
        xml=xml,
        app_id=app_id,
        tag=tag,
        group=group
    )
    loop = asyncio.get_running_loop()
    futures = []

    if audio and isinstance(audio, str) and not audio.startswith('ms'):
        futures.append(loop.create_task(play_sound(audio)))
    if dialogue:
        futures.append(loop.create_task(speak(dialogue)))

    if isinstance(on_click, str):
        on_click = _default_on_click
    elif on_click is None:
        on_click = _default_on_click
    activated_future = loop.create_future()
    activated_token = notification.add_activated(
        lambda *args: loop.call_soon_threadsafe(
            activated_future.set_result, on_click(activated_args(*args))
        )
    )
    futures.append(activated_future)

    dismissed_future = loop.create_future()
    dismissed_token = notification.add_dismissed(
        lambda _, event_args: loop.call_soon_threadsafe(
            dismissed_future.set_result, on_dismissed(result_wrapper(ToastDismissedEventArgs._from(event_args).reason)))
    )
    futures.append(dismissed_future)

    failed_future = loop.create_future()
    failed_token = notification.add_failed(
        lambda _, event_args: loop.call_soon_threadsafe(
            failed_future.set_result, on_failed(result_wrapper(ToastFailedEventArgs._from(event_args).error_code)))
    )
    futures.append(failed_future)

    try:
        _, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    finally:
        if activated_token is not None:
            notification.remove_activated(activated_token)
        if dismissed_token is not None:
            notification.remove_dismissed(dismissed_token)
        if failed_token is not None:
            notification.remove_failed(failed_token)
        return result


def toast(title: Optional[str] = None, body: Optional[str] = None,
          on_click: Optional[Union[Callable, str]] = None,
          icon: Optional[Union[str, Dict[str, str]]] = None,
          image: Optional[Union[str, Dict[str, str]]] = None,
          progress: Optional[Dict[str, Any]] = None,
          audio: Optional[Union[str, Dict[str, str]]] = None,
          dialogue: Optional[str] = None,
          duration: Optional[str] = None,
          input: Optional[Union[str, Dict[str, str]]] = None,
          inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
          selection: Optional[Union[List[str], Dict[str, Any]]] = None,
          selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
          button: Optional[Union[str, Dict[str, str]]] = None,
          buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
          xml: str = xml,
          app_id: str = DEFAULT_APP_ID,
          ocr: Optional[Union[str, Dict[str, str]]] = None,
          on_dismissed: Callable = print,
          on_failed: Callable = print,
          scenario: Optional[str] = None,
          tag: Optional[str] = None,
          group: Optional[str] = None,
          # Parameterized image options / 参数化的图片选项
          image_src: Optional[str] = None,
          image_placement: Optional[str] = None,
          # Parameterized icon options / 参数化的图标选项
          icon_src: Optional[str] = None,
          icon_placement: Optional[str] = None,
          icon_hint_crop: Optional[str] = None) -> Union[Dict[str, Any], Any]:
    """
    Create and show a Windows toast notification (synchronous wrapper).
    创建并显示一个 Windows 通知（同步包装器）。

    Args / 参数:
        title: Notification title text / 通知标题文本
        body: Notification body text / 通知正文文本
        on_click: Callback function or URL string / 回调函数或URL字符串
        on_dismissed: Callback function for dismissal / 通知被关闭时的回调函数
        on_failed: Callback function for failure / 通知失败时的回调函数
        icon: Icon URL/path (string) or dict with icon options / 图标URL/路径（字符串）或图标选项字典
        image: Image URL/path (string) or dict with image options / 图片URL/路径（字符串）或图片选项字典
        progress: Dictionary with progress values / 进度值字典
        audio: Audio file path or Windows sound event / 音频文件路径或Windows声音事件
        dialogue: Text to speak / 要朗读的文本
        duration: Toast duration ('short' or 'long') / 通知持续时间（'short' 或 'long'）
        input: Single input field / 单个输入字段
        inputs: List of input fields / 输入字段列表
        selection: Single selection field / 单个选择字段
        selections: List of selection fields / 选择字段列表
        button: Single button / 单个按钮
        buttons: List of buttons / 按钮列表
        xml: Custom XML template / 自定义XML模板
        app_id: Application ID / 应用程序ID
        ocr: OCR image path or dict / OCR图片路径或字典
        scenario: Toast scenario / 通知场景
        tag: Notification tag / 通知标签
        group: Notification group / 通知组

        # Parameterized image options (alternative to image dict) / 参数化的图片选项（替代图片字典）
        image_src: Image source URL/path / 图片源URL/路径
        image_placement: Image placement ('hero', 'appLogoOverride', 'inline') / 图片位置（'hero', 'appLogoOverride', 'inline'）

        # Parameterized icon options (alternative to icon dict) / 参数化的图标选项（替代图标字典）
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement ('appLogoOverride', 'appLogoOverrideAndHero') / 图标位置（'appLogoOverride', 'appLogoOverrideAndHero'）
        icon_hint_crop: Icon crop hint ('circle', 'none') / 图标裁剪提示（'circle', 'none'）

    Returns / 返回:
        Result dictionary or Future object / 结果字典或Future对象

    Examples / 示例:
        # Simple notification / 简单通知
        toast('Hello', 'World')

        # With parameterized image / 使用参数化的图片
        toast('Hello', 'World', image_src='path/to/image.jpg', image_placement='hero')

        # With parameterized icon / 使用参数化的图标
        toast('Hello', 'World', icon_src='path/to/icon.png', icon_placement='appLogoOverride')
    """
    toast_coroutine = toast_async(title, body, on_click, icon, image, progress, audio,
                                  dialogue, duration, input, inputs, selection, selections, button, buttons,
                                  xml, app_id, ocr, on_dismissed, on_failed,
                                  scenario, tag, group,
                                  image_src, image_placement,
                                  icon_src, icon_placement, icon_hint_crop)

    # check if there is an existing loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(toast_coroutine)
    else:
        future = asyncio.Future()
        task = loop.create_task(toast_coroutine)

        def on_done(t):
            if t.exception() is not None:
                future.set_exception(t.exception())
            else:
                future.set_result(t.result())

        task.add_done_callback(on_done)
        return future


async def atoast(title: Optional[str] = None, body: Optional[str] = None,
                 on_click: Optional[Union[Callable, str]] = None,
                 icon: Optional[Union[str, Dict[str, str]]] = None,
                 image: Optional[Union[str, Dict[str, str]]] = None,
                 progress: Optional[Dict[str, Any]] = None,
                 audio: Optional[Union[str, Dict[str, str]]] = None,
                 dialogue: Optional[str] = None,
                 duration: Optional[str] = None,
                 input: Optional[Union[str, Dict[str, str]]] = None,
                 inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
                 selection: Optional[Union[List[str], Dict[str, Any]]] = None,
                 selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
                 button: Optional[Union[str, Dict[str, str]]] = None,
                 buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
                 xml: str = xml,
                 app_id: str = DEFAULT_APP_ID,
                 ocr: Optional[Union[str, Dict[str, str]]] = None,
                 on_dismissed: Callable = print,
                 on_failed: Callable = print,
                 scenario: Optional[str] = None,
                 tag: Optional[str] = None,
                 group: Optional[str] = None,
                 # Parameterized image options / 参数化的图片选项
                 image_src: Optional[str] = None,
                 image_placement: Optional[str] = None,
                 # Parameterized icon options / 参数化的图标选项
                 icon_src: Optional[str] = None,
                 icon_placement: Optional[str] = None,
                 icon_hint_crop: Optional[str] = None) -> Dict[str, Any]:
    """
    Async alias for toast_async.
    toast_async 的异步别名。
    """
    return await toast_async(title, body, on_click, icon, image, progress, audio,
                             dialogue, duration, input, inputs, selection, selections, button, buttons,
                             xml, app_id, ocr, on_dismissed, on_failed,
                             scenario, tag, group,
                             image_src, image_placement,
                             icon_src, icon_placement, icon_hint_crop)


def notify_progress(title: Optional[str] = None,
                    status: Optional[str] = None,
                    value: Optional[float] = None,
                    value_string_override: Optional[str] = None,
                    app_id: str = DEFAULT_APP_ID,
                    tag: str = 'my_tag',
                    group: Optional[str] = None,
                    # Icon options / 图标选项
                    icon_src: Optional[str] = None,
                    icon_placement: Optional[Union[str, IconPlacement]] = None,
                    icon_hint_crop: Optional[Union[str, IconCrop]] = None,
                    # Image options / 图片选项
                    image_src: Optional[str] = None,
                    image_placement: Optional[Union[str, ImagePlacement]] = None,
                    # Audio options / 音频选项
                    audio: Optional[Union[str, AudioEvent]] = None,
                    audio_loop: bool = False,
                    # Duration / 持续时间
                    duration: Optional[Union[str, ToastDuration]] = None,
                    # Callback / 回调
                    on_click: Optional[Union[Callable, str]] = None) -> ToastNotification:
    """
    Create a progress notification with a more Pythonic API.
    使用更Pythonic的API创建进度通知。

    Args / 参数:
        title: Progress bar title (e.g., 'YouTube', 'Downloading files') / 进度条标题（例如：'YouTube', '下载文件'）
        status: Status text displayed below progress bar (e.g., 'Downloading...', 'Processing...') / 进度条下方显示的状态文本（例如：'下载中...', '处理中...'）
        value: Progress value between 0.0 and 1.0 (e.g., 0.5 for 50%) / 进度值，范围0.0到1.0（例如：0.5表示50%）
        value_string_override: Custom string to display instead of percentage (e.g., '5/15 videos') / 自定义字符串，替代百分比显示（例如：'5/15 视频'）
        app_id: Application ID / 应用程序ID
        tag: Notification tag (used for updates). Default 'my_tag'. Use different tags for multiple concurrent notifications. / 通知标签（用于更新）。默认为'my_tag'。多个并发通知使用不同的标签。
        group: Notification group (optional) / 通知组（可选）

        # Icon options / 图标选项
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement (IconPlacement enum or str) / 图标位置（IconPlacement枚举或字符串）
        icon_hint_crop: Icon crop hint (IconCrop enum or str) / 图标裁剪提示（IconCrop枚举或字符串）

        # Image options / 图片选项
        image_src: Image source URL/path / 图片源URL/路径
        image_placement: Image placement (ImagePlacement enum or str) / 图片位置（ImagePlacement枚举或字符串）

        # Audio options / 音频选项
        audio: Audio source (AudioEvent enum, URL, or file path). None for silent / 音频源（AudioEvent枚举、URL或文件路径）。None表示静音
        audio_loop: Whether to loop the audio / 是否循环播放音频

        # Duration / 持续时间
        duration: Toast duration (ToastDuration enum or str) / 通知持续时间（ToastDuration枚举或字符串）

        # Callback / 回调
        on_click: Callback function or URL string / 回调函数或URL字符串

    Returns / 返回:
        ToastNotification object / ToastNotification对象

    Example / 示例:
        notify_progress(
            title='YouTube',
            status='Downloading...',
            value=0.0,
            value_string_override='0/15 videos'
        )
    """
    return notify(
        progress_title=title,
        progress_status=status,
        progress_value=value,
        progress_value_string_override=value_string_override,
        app_id=app_id,
        tag=tag,
        group=group,
        icon_src=icon_src,
        icon_placement=icon_placement,
        icon_hint_crop=icon_hint_crop,
        image_src=image_src,
        image_placement=image_placement,
        audio=audio,
        audio_loop=audio_loop,
        duration=duration,
        on_click=on_click
    )


def update_progress(value: Optional[float] = None,
                    status: Optional[str] = None,
                    value_string_override: Optional[str] = None,
                    app_id: str = DEFAULT_APP_ID,
                    tag: str = 'my_tag',
                    group: Optional[str] = None) -> ToastNotification:
    """
    Update a progress notification with a more Pythonic API.
    使用更Pythonic的API更新进度通知。

    Args / 参数:
        value: Progress value between 0.0 and 1.0 (e.g., 0.5 for 50%) / 进度值，范围0.0到1.0（例如：0.5表示50%）
        status: Status text to update (e.g., 'Downloading...', 'Completed!') / 要更新的状态文本（例如：'下载中...', '完成！'）
        value_string_override: Custom string to display instead of percentage (e.g., '5/15 videos') / 自定义字符串，替代百分比显示（例如：'5/15 视频'）
        app_id: Application ID (must match original notification) / 应用程序ID（必须与原始通知匹配）
        tag: Notification tag (must match original notification). Default 'my_tag' / 通知标签（必须与原始通知匹配）。默认为'my_tag'
        group: Notification group (optional, should match original if provided) / 通知组（可选，如果提供了应与原始通知匹配）

    Returns / 返回:
        ToastNotification object / ToastNotification对象

    Example / 示例:
        # Update progress value / 更新进度值
        update_progress(value=0.5, value_string_override='5/15 videos')

        # Update status only / 仅更新状态
        update_progress(status='Completed!')

        # Update everything / 更新所有内容
        update_progress(value=1.0, status='Done!', value_string_override='15/15 videos')
    """
    progress = {}
    if value is not None:
        progress['value'] = str(value)
    if status is not None:
        progress['status'] = status
    if value_string_override is not None:
        progress['valueStringOverride'] = value_string_override

    # If no progress dict provided, use empty dict (will preserve existing values)
    return _update_progress_internal(progress, app_id, tag, group)


def _update_progress_internal(progress: Dict[str, Any],
                              app_id: str = DEFAULT_APP_ID,
                              tag: str = 'my_tag',
                              group: Optional[str] = None) -> ToastNotification:
    """
    Internal function to update progress notification.
    更新进度通知的内部函数。
    This is the actual implementation that handles the update logic.
    这是处理更新逻辑的实际实现。

    Args / 参数:
        progress: Dictionary with progress values / 进度值字典
        app_id: Application ID / 应用程序ID
        tag: Notification tag / 通知标签
        group: Notification group / 通知组

    Returns / 返回:
        ToastNotification object / ToastNotification对象

    Raises / 异常:
        ValueError: If no cached notification found for the tag / 如果找不到指定标签的缓存通知
    """
    # Get cached notification info if available
    if tag not in _notification_cache:
        # If no cache exists, this is likely an error - can't update a notification that doesn't exist
        raise ValueError(
            f"No cached notification found for tag '{tag}'. Please create a notification first using notify_progress() or notify().")

    cached = _notification_cache[tag]

    # Merge progress data with cached values
    progress_dict = progress.copy()

    # Preserve existing progress values that aren't being updated
    # This ensures we don't lose values like 'title' that might be in the original progress
    if 'title' not in progress_dict and cached.get('progress_title'):
        progress_dict['title'] = cached.get('progress_title')
    if 'status' not in progress_dict:
        # Use cached status if not updating it
        if cached.get('body'):
            progress_dict['status'] = cached.get('body')
    else:
        # Update cached status if new status provided
        cached['body'] = progress_dict['status']

    # Update cached progress title if provided
    if 'title' in progress_dict:
        cached['progress_title'] = progress_dict['title']

    # Get cached app_id and group
    cached_app_id = cached.get('app_id', app_id)
    cached_group = cached.get('group') if group is None else group

    # Increment sequence number for this update
    if tag in _notification_sequence:
        _notification_sequence[tag] += 1
    else:
        _notification_sequence[tag] = 2

    # Re-create notification with updated progress data
    # Using the same tag will replace the existing notification
    return notify(
        progress_title=progress_dict.get('title') or cached.get('progress_title'),
        progress_status=progress_dict.get('status') or cached.get('body'),
        progress_value=float(progress_dict['value']) if 'value' in progress_dict else None,
        progress_value_string_override=progress_dict.get('valueStringOverride'),
        app_id=cached_app_id,
        tag=tag,
        group=cached_group,
        icon_src=cached.get('icon_src'),
        icon_placement=cached.get('icon_placement'),
        icon_hint_crop=cached.get('icon_hint_crop'),
        image_src=cached.get('image_src'),
        image_placement=cached.get('image_placement')
    )


def clear_toast(app_id: str = DEFAULT_APP_ID, tag: Optional[str] = None, group: Optional[str] = None) -> None:
    """
    Clear toast notifications from notification history.
    从通知历史中清除通知。

    Args / 参数:
        app_id: Application ID / 应用程序ID
        tag: Notification tag. If None, clears all notifications. / 通知标签。如果为None，清除所有通知。
        group: Notification group. Required if tag is provided. / 通知组。如果提供了tag，则必须提供。

    Raises / 异常:
        AttributeError: If tag is provided but group is not / 如果提供了tag但没有提供group
    """
    # Get the notification history / 获取通知历史
    history = ToastNotificationManager.history

    if tag is None and group is None:
        # Clear all notifications / 清除所有通知
        history.clear(app_id)
    elif tag is not None and not group:
        # Cannot remove notification only using tag. Group is required. / 不能仅使用tag删除通知。需要提供group。
        raise AttributeError('group value is required to clear a toast')
    elif tag is not None and group is not None:
        # Remove notification by tag and group / 通过tag和group删除通知
        history.remove(tag, group, app_id)
    elif tag is None and group is not None:
        # Remove all notifications in the group / 删除组中的所有通知
        history.remove_group(group, app_id)
