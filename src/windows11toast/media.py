"""Media functions for audio, speech, and OCR / 音频、语音和OCR相关函数"""

import asyncio
from typing import Optional, Union
from winrt.windows.media.core import MediaSource
from winrt.windows.media.playback import MediaPlayer
from winrt.windows.media.speechsynthesis import SpeechSynthesizer
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.storage import StorageFile, FileAccessMode
from winrt.windows.foundation import Uri
from winrt.windows.storage.streams import RandomAccessStreamReference
from winrt.windows.globalization import Language
from .enums import OcrLanguage


async def play_sound(audio: str) -> None:
    """
    Play audio file using Windows Media Player.
    使用Windows媒体播放器播放音频文件。

    Args / 参数:
        audio: Audio file path or URL / 音频文件路径或URL
    """
    if audio.startswith('http'):
        source = MediaSource.create_from_uri(Uri(audio))
    else:
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
    if ocr_src.startswith('http'):
        ref = RandomAccessStreamReference.create_from_uri(Uri(ocr_src))
        stream = await ref.open_read_async()
    else:
        file = await StorageFile.get_file_from_path_async(ocr_src)
        stream = await file.open_async(FileAccessMode.READ)
    decoder = await BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()

    if lang:
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
    """
    Print available OCR languages and installation instructions.
    打印可用的OCR语言和安装说明。
    """
    for language in OcrEngine.get_available_recognizer_languages():
        print(language.display_name, language.language_tag)
    print('Run as Administrator')
    print('Get-WindowsCapability -Online -Name "Language.OCR*"')
    print('Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"')

