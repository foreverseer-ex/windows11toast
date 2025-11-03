"""XML builder functions for toast notifications / 通知XML构建函数"""

from typing import Optional, Union
from winrt.windows.data.xml.dom import XmlDocument
from .enums import ImagePlacement, IconPlacement, IconCrop


def set_attribute(document: XmlDocument, xpath: str, name: str, value: str) -> None:
    """Set an attribute on an XML element / 在XML元素上设置属性"""
    attribute = document.create_attribute(name)
    attribute.value = value
    document.select_single_node(xpath).attributes.set_named_item(attribute)


def add_text(msg: Union[str, dict], document: XmlDocument) -> None:
    """Add text element to toast notification / 向通知添加文本元素"""
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
             hint_crop: Optional[Union[str, IconCrop]] = None, document: Optional[XmlDocument] = None) -> None:
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


def add_image(image_src: str, placement: Optional[Union[str, ImagePlacement]] = None, 
              document: Optional[XmlDocument] = None) -> None:
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


def add_progress(prog: dict, document: XmlDocument) -> None:
    """Add progress bar to toast notification / 向通知添加进度条"""
    binding = document.select_single_node('//binding')
    progress = document.create_element('progress')
    for name in prog:
        progress.set_attribute(name, '{' + name + '}')
    binding.append_child(progress)


def add_audio(audio_src: Optional[Union[str, 'AudioEvent']] = None,  # type: ignore
              loop: bool = False, document: Optional[XmlDocument] = None) -> None:
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


def create_actions(document: XmlDocument):
    """Create actions element in toast notification / 在通知中创建actions元素"""
    toast = document.select_single_node('/toast')
    actions = document.create_element('actions')
    toast.append_child(actions)
    return actions


def add_button(button: Union[str, dict], document: XmlDocument) -> None:
    """Add button to toast notification / 向通知添加按钮"""
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


def add_input(id: Union[str, dict], document: XmlDocument) -> None:
    """Add input field to toast notification / 向通知添加输入字段"""
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


def add_selection(selection: Union[list, dict], document: XmlDocument) -> None:
    """Add selection field to toast notification / 向通知添加选择字段"""
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

