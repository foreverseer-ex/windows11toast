"""Core notification functions / 核心通知函数"""

import asyncio
from pathlib import Path
from typing import Optional, Dict, List, Callable, Union, Any
from winrt.windows.data.xml.dom import XmlDocument
from winrt.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    NotificationData,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)

from .enums import ImagePlacement, IconPlacement, IconCrop, AudioEvent, ToastDuration
from .constants import DEFAULT_APP_ID, DEFAULT_XML_TEMPLATE
from .xml_builder import (
    set_attribute, add_text, add_icon, add_image, add_progress,
    add_audio, add_button, add_input, add_selection
)
from .utils import result_wrapper, activated_args, _default_on_click, result
from .media import play_sound, speak, recognize

# Store original notification info for update_progress
_notification_cache = {}
_notification_sequence = {}


def notify(title: Optional[str] = None, body: Optional[str] = None,
           on_click: Optional[Union[Callable, str]] = None,
           # Image options / 图片选项
           image_src: Optional[str] = None,
           image_placement: Optional[ImagePlacement] = None,
           # Icon options / 图标选项
           icon_src: Optional[str] = None,
           icon_placement: Optional[IconPlacement] = None,
           icon_hint_crop: Optional[IconCrop] = None,
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
           duration: Optional[ToastDuration] = None,
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
        image_placement: Image placement (ImagePlacement enum only) / 图片位置（仅ImagePlacement枚举）

        # Icon options / 图标选项
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement (IconPlacement enum only) / 图标位置（仅IconPlacement枚举）
        icon_hint_crop: Icon crop hint (IconCrop enum only) / 图标裁剪提示（仅IconCrop枚举）

        # Progress options / 进度选项
        progress_title: Progress bar title / 进度条标题
        progress_status: Progress status text / 进度状态文本
        progress_value: Progress value (0.0 to 1.0) / 进度值（0.0到1.0）
        progress_value_string_override: Custom progress string / 自定义进度字符串

        # Audio options / 音频选项
        audio: Audio source (AudioEvent enum for built-in sounds, or URL/file path string). None for silent / 音频源（AudioEvent枚举用于内置声音，或URL/文件路径字符串）。None表示静音
        audio_loop: Whether to loop the audio / 是否循环播放音频

        # Text-to-speech / 文本转语音
        dialogue: Text to speak / 要朗读的文本

        # Duration / 持续时间
        duration: Toast duration (ToastDuration enum only) / 通知持续时间（仅ToastDuration枚举）

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
        duration_value = str(duration)
        # Check if duration is a scenario (no timeout) / 检查duration是否为场景（无超时）
        if duration in [ToastDuration.ALARM, ToastDuration.REMINDER, ToastDuration.INCOMING_CALL, ToastDuration.URGENT]:
            scenario = duration_value
        elif duration in [ToastDuration.SHORT, ToastDuration.LONG]:
            duration_str = duration_value

    document = XmlDocument()
    # Use the xml parameter if provided, otherwise use default template / 如果提供了xml参数则使用，否则使用默认模板
    xml_template = xml if xml else DEFAULT_XML_TEMPLATE
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
        except Exception:
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
                      duration: Optional[ToastDuration] = None,
                      input: Optional[Union[str, Dict[str, str]]] = None,
                      inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
                      selection: Optional[Union[List[str], Dict[str, Any]]] = None,
                      selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
                      button: Optional[Union[str, Dict[str, str]]] = None,
                      buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
                      xml: Optional[str] = None,
                      app_id: str = DEFAULT_APP_ID,
                      ocr: Optional[Union[str, Dict[str, str]]] = None,
                      on_dismissed: Callable = print,
                      on_failed: Callable = print,
                      scenario: Optional[str] = None,
                      tag: Optional[str] = None,
                      group: Optional[str] = None,
                      # Parameterized image options / 参数化的图片选项
                      image_src: Optional[str] = None,
                      image_placement: Optional[ImagePlacement] = None,
                      # Parameterized icon options / 参数化的图标选项
                      icon_src: Optional[str] = None,
                      icon_placement: Optional[IconPlacement] = None,
                      icon_hint_crop: Optional[IconCrop] = None,
                      # Parameterized progress options / 参数化的进度选项
                      progress_title: Optional[str] = None,
                      progress_status: Optional[str] = None,
                      progress_value: Optional[float] = None,
                      progress_value_string_override: Optional[str] = None,
                      # Parameterized input options / 参数化的输入选项
                      input_id: Optional[str] = None,
                      input_placeholder: Optional[str] = None,
                      selection_id: Optional[str] = None,
                      # Parameterized button options / 参数化的按钮选项
                      button_content: Optional[str] = None,
                      # Parameterized audio options / 参数化的音频选项
                      audio_loop: bool = False) -> Dict[str, Any]:
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
        duration: Toast duration (ToastDuration enum only) / 通知持续时间（仅ToastDuration枚举）
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
        image_placement: Image placement (ImagePlacement enum only) / 图片位置（仅ImagePlacement枚举）

        # Parameterized icon options (alternative to icon dict) / 参数化的图标选项（替代图标字典）
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement (IconPlacement enum only) / 图标位置（仅IconPlacement枚举）
        icon_hint_crop: Icon crop hint (IconCrop enum only) / 图标裁剪提示（仅IconCrop枚举）

        # Parameterized progress options (alternative to progress dict) / 参数化的进度选项（替代进度字典）
        progress_title: Progress bar title / 进度条标题
        progress_status: Progress status text / 进度状态文本
        progress_value: Progress value (0.0 to 1.0) / 进度值（0.0到1.0）
        progress_value_string_override: Custom progress string / 自定义进度字符串

        # Parameterized input options (alternative to input dict) / 参数化的输入选项（替代输入字典）
        input_id: Input field ID / 输入字段ID
        input_placeholder: Input placeholder text / 输入占位符文本
        selection_id: Selection field ID / 选择字段ID

        # Parameterized button options (alternative to button dict) / 参数化的按钮选项（替代按钮字典）
        button_content: Single button content / 单个按钮内容

        # Parameterized audio options (alternative to audio dict) / 参数化的音频选项（替代音频字典）
        audio_loop: Whether to loop the audio / 是否循环播放音频

    Examples / 示例:
        # Simple notification / 简单通知
        await toast_async('Hello', 'World')

        # With parameterized image / 使用参数化的图片
        await toast_async('Hello', 'World', image_src='path/to/image.jpg', image_placement=ImagePlacement.HERO)
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
                placement_str = icon.get('placement')
                if placement_str:
                    # Convert string to enum / 将字符串转换为枚举
                    placement_upper = placement_str.replace('-', '_').upper()
                    if hasattr(IconPlacement, placement_upper):
                        icon_placement = getattr(IconPlacement, placement_upper)
            if not icon_hint_crop:
                hint_crop_str = icon.get('hint-crop')
                if hint_crop_str:
                    # Convert string to enum / 将字符串转换为枚举
                    hint_crop_upper = hint_crop_str.upper()
                    if hasattr(IconCrop, hint_crop_upper):
                        icon_hint_crop = getattr(IconCrop, hint_crop_upper)

    if image and not image_src:
        if isinstance(image, str):
            image_src = image
        elif isinstance(image, dict):
            image_src = image.get('src')
            if not image_placement:
                placement_str = image.get('placement')
                if placement_str:
                    # Convert string to enum / 将字符串转换为枚举
                    placement_upper = placement_str.replace('-', '_').upper()
                    if hasattr(ImagePlacement, placement_upper):
                        image_placement = getattr(ImagePlacement, placement_upper)

    # Convert progress dict to parameterized format / 将进度字典转换为参数化格式
    # Use parameterized form if provided, otherwise use dict / 如果提供了参数化形式则使用，否则使用字典
    if progress_title is None and progress_status is None and progress_value is None and progress_value_string_override is None:
        if progress:
            progress_title = progress.get('title')
            progress_status = progress.get('status')
            if 'value' in progress:
                progress_value = float(progress['value'])
            progress_value_string_override = progress.get('valueStringOverride')
    else:
        # Parameterized form takes precedence / 参数化形式优先
        pass

    # Convert audio dict to parameterized format / 将音频字典转换为参数化格式
    audio_src = audio
    audio_loop_flag = audio_loop  # Use parameterized audio_loop if provided / 如果提供了参数化的audio_loop则使用
    if isinstance(audio, dict):
        audio_src = audio.get('src')
        if not audio_loop_flag:  # Only override if not explicitly set / 只有在未明确设置时才覆盖
            audio_loop_flag = audio.get('loop') == 'true' or audio.get('loop') is True
    elif isinstance(audio, str):
        audio_src = audio

    # Duration should already be a ToastDuration enum / duration应该已经是ToastDuration枚举
    duration_enum = duration

    # Convert input to parameterized format / 将输入转换为参数化格式
    # Use parameterized form if provided, otherwise use dict / 如果提供了参数化形式则使用，否则使用字典
    input_id_param = input_id
    input_placeholder_param = input_placeholder
    if input_id_param is None and input_placeholder_param is None:
        if input:
            if isinstance(input, str):
                input_id_param = input
                input_placeholder_param = input
            elif isinstance(input, dict):
                input_id_param = input.get('id')
                input_placeholder_param = input.get('placeHolderContent') or input.get('placeholder')
        # Also check inputs list / 同时检查inputs列表
        if inputs and input_id_param is None:
            # Use first input if available / 如果可用则使用第一个输入
            first_input = inputs[0] if inputs else None
            if isinstance(first_input, dict):
                input_id_param = first_input.get('id')
                input_placeholder_param = first_input.get('placeHolderContent') or first_input.get('placeholder')

    # Convert selection to parameterized format / 将选择转换为参数化格式
    # Use parameterized form if provided, otherwise use dict / 如果提供了参数化形式则使用，否则使用字典
    selection_id_param = selection_id
    selections_param = selections
    if selection_id_param is None:
        if selection:
            if isinstance(selection, list):
                selection_id_param = 'selection'
                selections_param = selection
            elif isinstance(selection, dict):
                selection_id_param = selection.get('input', {}).get('id', 'selection')
                selections_param = selection.get('selection', [])

    # Convert button to parameterized format / 将按钮转换为参数化格式
    # Use parameterized form if provided, otherwise use dict / 如果提供了参数化形式则使用，否则使用字典
    button_content_param = button_content
    buttons_param = buttons
    if button_content_param is None:
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
            dismissed_future.set_result, on_dismissed(result_wrapper(ToastDismissedEventArgs._from(event_args).reason))
        )
    )
    futures.append(dismissed_future)

    failed_future = loop.create_future()
    failed_token = notification.add_failed(
        lambda _, event_args: loop.call_soon_threadsafe(
            failed_future.set_result, on_failed(result_wrapper(ToastFailedEventArgs._from(event_args).error_code))
        )
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
          duration: Optional[ToastDuration] = None,
          input: Optional[Union[str, Dict[str, str]]] = None,
          inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
          selection: Optional[Union[List[str], Dict[str, Any]]] = None,
          selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
          button: Optional[Union[str, Dict[str, str]]] = None,
          buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
          xml: Optional[str] = None,
          app_id: str = DEFAULT_APP_ID,
          ocr: Optional[Union[str, Dict[str, str]]] = None,
          on_dismissed: Callable = print,
          on_failed: Callable = print,
          scenario: Optional[str] = None,
          tag: Optional[str] = None,
          group: Optional[str] = None,
          # Parameterized image options / 参数化的图片选项
          image_src: Optional[str] = None,
          image_placement: Optional[ImagePlacement] = None,
          # Parameterized icon options / 参数化的图标选项
          icon_src: Optional[str] = None,
          icon_placement: Optional[IconPlacement] = None,
          icon_hint_crop: Optional[IconCrop] = None,
          # Parameterized progress options / 参数化的进度选项
          progress_title: Optional[str] = None,
          progress_status: Optional[str] = None,
          progress_value: Optional[float] = None,
          progress_value_string_override: Optional[str] = None,
          # Parameterized input options / 参数化的输入选项
          input_id: Optional[str] = None,
          input_placeholder: Optional[str] = None,
          selection_id: Optional[str] = None,
          # Parameterized button options / 参数化的按钮选项
          button_content: Optional[str] = None,
          # Parameterized audio options / 参数化的音频选项
          audio_loop: bool = False) -> Union[Dict[str, Any], Any]:
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
        duration: Toast duration (ToastDuration enum only) / 通知持续时间（仅ToastDuration枚举）
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
        image_placement: Image placement (ImagePlacement enum only) / 图片位置（仅ImagePlacement枚举）

        # Parameterized icon options (alternative to icon dict) / 参数化的图标选项（替代图标字典）
        icon_src: Icon source URL/path / 图标源URL/路径
        icon_placement: Icon placement (IconPlacement enum only) / 图标位置（仅IconPlacement枚举）
        icon_hint_crop: Icon crop hint (IconCrop enum only) / 图标裁剪提示（仅IconCrop枚举）

        # Parameterized progress options (alternative to progress dict) / 参数化的进度选项（替代进度字典）
        progress_title: Progress bar title / 进度条标题
        progress_status: Progress status text / 进度状态文本
        progress_value: Progress value (0.0 to 1.0) / 进度值（0.0到1.0）
        progress_value_string_override: Custom progress string / 自定义进度字符串

        # Parameterized input options (alternative to input dict) / 参数化的输入选项（替代输入字典）
        input_id: Input field ID / 输入字段ID
        input_placeholder: Input placeholder text / 输入占位符文本
        selection_id: Selection field ID / 选择字段ID

        # Parameterized button options (alternative to button dict) / 参数化的按钮选项（替代按钮字典）
        button_content: Single button content / 单个按钮内容

        # Parameterized audio options (alternative to audio dict) / 参数化的音频选项（替代音频字典）
        audio_loop: Whether to loop the audio / 是否循环播放音频

    Returns / 返回:
        Result dictionary or Future object / 结果字典或Future对象

    Examples / 示例:
        # Simple notification / 简单通知
        toast('Hello', 'World')

        # With parameterized image / 使用参数化的图片
        toast('Hello', 'World', image_src='path/to/image.jpg', image_placement=ImagePlacement.HERO)

        # With parameterized icon / 使用参数化的图标
        toast('Hello', 'World', icon_src='path/to/icon.png', icon_placement=IconPlacement.APP_LOGO_OVERRIDE)
    """
    toast_coroutine = toast_async(title, body, on_click, icon, image, progress, audio,
                                  dialogue, duration, input, inputs, selection, selections, button, buttons,
                                  xml, app_id, ocr, on_dismissed, on_failed,
                                  scenario, tag, group,
                                  image_src, image_placement,
                                  icon_src, icon_placement, icon_hint_crop,
                                  progress_title, progress_status, progress_value, progress_value_string_override,
                                  input_id, input_placeholder, selection_id,
                                  button_content, audio_loop)

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
                 duration: Optional[ToastDuration] = None,
                 input: Optional[Union[str, Dict[str, str]]] = None,
                 inputs: Optional[List[Union[str, Dict[str, str]]]] = None,
                 selection: Optional[Union[List[str], Dict[str, Any]]] = None,
                 selections: Optional[List[Union[List[str], Dict[str, Any]]]] = None,
                 button: Optional[Union[str, Dict[str, str]]] = None,
                 buttons: Optional[List[Union[str, Dict[str, str]]]] = None,
                 xml: Optional[str] = None,
                 app_id: str = DEFAULT_APP_ID,
                 ocr: Optional[Union[str, Dict[str, str]]] = None,
                 on_dismissed: Callable = print,
                 on_failed: Callable = print,
                 scenario: Optional[str] = None,
                 tag: Optional[str] = None,
                 group: Optional[str] = None,
                 # Parameterized image options / 参数化的图片选项
                 image_src: Optional[str] = None,
                 image_placement: Optional[ImagePlacement] = None,
                 # Parameterized icon options / 参数化的图标选项
                 icon_src: Optional[str] = None,
                 icon_placement: Optional[IconPlacement] = None,
                 icon_hint_crop: Optional[IconCrop] = None,
                 # Parameterized progress options / 参数化的进度选项
                 progress_title: Optional[str] = None,
                 progress_status: Optional[str] = None,
                 progress_value: Optional[float] = None,
                 progress_value_string_override: Optional[str] = None,
                 # Parameterized input options / 参数化的输入选项
                 input_id: Optional[str] = None,
                 input_placeholder: Optional[str] = None,
                 selection_id: Optional[str] = None,
                 # Parameterized button options / 参数化的按钮选项
                 button_content: Optional[str] = None,
                 # Parameterized audio options / 参数化的音频选项
                 audio_loop: bool = False) -> Dict[str, Any]:
    """
    Async alias for toast_async.
    toast_async 的异步别名。
    """
    return await toast_async(title, body, on_click, icon, image, progress, audio,
                             dialogue, duration, input, inputs, selection, selections, button, buttons,
                             xml, app_id, ocr, on_dismissed, on_failed,
                             scenario, tag, group,
                             image_src, image_placement,
                             icon_src, icon_placement, icon_hint_crop,
                             progress_title, progress_status, progress_value, progress_value_string_override,
                             input_id, input_placeholder, selection_id,
                             button_content, audio_loop)


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

