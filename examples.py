# win11toast 使用示例 / Examples
# 本文档包含所有功能的完整使用示例。
# This document contains complete examples for all features.

from time import sleep

from windows11toast import (
    toast,
    notify,
    notify_progress,
    update_progress,
    ImagePlacement,
    IconPlacement,
    IconCrop,
    AudioEvent,
    ToastDuration,
    OcrLanguage,
    recognize,
    toast_async
)


# ============================================================================
# 1. 基本通知 / Basic Notifications
# ============================================================================

def example_simple_notification():
    """简单通知 / Simple Notification"""
    toast('Hello Python🐍')


def example_notification_with_title_and_body():
    """带标题和正文 / With Title and Body"""
    toast('Hello Python', 'Click to open url', on_click='https://www.python.org')


def example_wrap_text():
    """文本换行 / Wrap Text"""
    toast('Hello', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...')


# ============================================================================
# 2. 图片通知 / Image Notifications
# ============================================================================

def example_image_with_strenum():
    """使用 StrEnum / Using StrEnum"""
    # Hero 图片（大图）
    toast(
        'Hello',
        'Hello from Python',
        image_src='https://example.com/image.jpg',
        image_placement=ImagePlacement.HERO
    )


def example_image_local_file():
    """本地文件 / Local File"""
    toast(
        'Hello',
        'Hello from Python',
        image_src=r'C:\Users\YourName\Pictures\image.jpg',
        image_placement=ImagePlacement.HERO
    )


def example_image_app_logo():
    """应用Logo覆盖 / App Logo Override"""
    toast(
        'Hello',
        'Hello from Python',
        image_src='https://example.com/logo.png',
        image_placement=ImagePlacement.APP_LOGO_OVERRIDE
    )


def example_image_inline():
    """内联图片 / Inline Image"""
    toast(
        'Hello',
        'Hello from Python',
        image_src='https://example.com/image.jpg',
        image_placement=ImagePlacement.INLINE
    )


def example_image_with_string():
    """使用字符串 / Using String"""
    toast(
        'Hello',
        'Hello from Python',
        image_src='https://example.com/image.jpg',
        image_placement='hero'  # 也支持字符串
    )


# ============================================================================
# 3. 图标通知 / Icon Notifications
# ============================================================================

def example_icon_circular():
    """圆形图标 / Circular Icon"""
    toast(
        'Hello',
        'Hello from Python',
        icon_src='https://example.com/icon.png',
        icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
        icon_hint_crop=IconCrop.CIRCLE
    )


def example_icon_square():
    """方形图标 / Square Icon"""
    toast(
        'Hello',
        'Hello from Python',
        icon_src='https://example.com/icon.png',
        icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
        icon_hint_crop=IconCrop.NONE
    )


# ============================================================================
# 4. 进度通知 / Progress Notifications
# ============================================================================

def example_progress_notification():
    """创建进度通知 / Create Progress Notification"""
    # 创建进度通知
    notify_progress(
        title='YouTube',
        status='下载中...',
        value=0.0,
        value_string_override='0/15 视频'
    )

    # 更新进度
    for i in range(1, 16):
        sleep(1)
        update_progress(
            value=i/15,
            value_string_override=f'{i}/15 视频'
        )

    # 更新状态
    update_progress(status='完成！')


def example_multiple_progress_notifications():
    """多个并发进度通知 / Multiple Concurrent Progress Notifications"""
    # 创建多个不同标签的通知
    notify_progress(
        title='视频 1',
        status='下载中...',
        value=0.0,
        tag='video1'
    )

    notify_progress(
        title='视频 2',
        status='下载中...',
        value=0.0,
        tag='video2'
    )

    # 独立更新每个
    update_progress(value=0.5, tag='video1')
    update_progress(value=0.7, tag='video2')


def example_progress_with_icon():
    """带图标的进度通知 / Progress Notification with Icon"""
    notify_progress(
        title='下载',
        status='正在下载文件...',
        value=0.0,
        icon_src='https://example.com/icon.png',
        icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
        icon_hint_crop=IconCrop.CIRCLE,
        image_src='https://example.com/image.jpg',
        image_placement=ImagePlacement.HERO
    )


# ============================================================================
# 5. 音频通知 / Audio Notifications
# ============================================================================

def example_audio_default():
    """默认通知声音 / Default Notification Sound"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.DEFAULT)


def example_audio_im():
    """IM 声音 / IM Sound"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.IM)


def example_audio_mail():
    """邮件声音 / Mail Sound"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.MAIL)


def example_audio_reminder():
    """提醒声音 / Reminder Sound"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.REMINDER)


def example_audio_sms():
    """SMS 声音 / SMS Sound"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.SMS)


def example_audio_looping_alarm():
    """循环闹钟 / Looping Alarm"""
    notify('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM)


def example_audio_from_url():
    """从 URL 播放音频 / Audio from URL"""
    toast('Hello', 'Hello from Python', audio='https://example.com/sound.mp3')


def example_audio_from_file():
    """从文件播放音频 / Audio from File"""
    toast('Hello', 'Hello from Python', audio=r'C:\Users\YourName\Music\sound.mp3')


def example_audio_silent():
    """静音通知 / Silent Notification"""
    notify('Hello Python🐍', audio=None)  # audio=None 表示静音


def example_audio_loop():
    """循环播放 / Loop Audio"""
    notify(
        'Hello',
        'Hello from Python',
        audio=AudioEvent.LOOPING_ALARM,
        audio_loop=True  # 循环播放
    )


# ============================================================================
# 6. 文本转语音 / Text-to-Speech
# ============================================================================

def example_text_to_speech():
    """文本转语音 / Text-to-Speech"""
    toast('Hello Python🐍', dialogue='Hello world')


# ============================================================================
# 7. OCR（光学字符识别）/ OCR
# ============================================================================

async def example_ocr_from_url():
    """从 URL OCR / OCR from URL"""
    result = await recognize('https://example.com/image.png')
    print(result.text)


async def example_ocr_from_file():
    """从文件 OCR / OCR from File"""
    result = await recognize(r'C:\Users\YourName\Pictures\image.png')
    print(result.text)


async def example_ocr_chinese():
    """指定语言 - 中文 / Specify Language - Chinese"""
    result = await recognize(
        r'C:\Users\YourName\Pictures\hello.png',
        lang=OcrLanguage.ZH_CN  # 中文
    )
    print(result.text)


async def example_ocr_japanese():
    """指定语言 - 日语 / Specify Language - Japanese"""
    result = await recognize(
        r'C:\Users\YourName\Pictures\hello.png',
        lang=OcrLanguage.JA  # 日语
    )
    print(result.text)


async def example_ocr_with_string():
    """使用字符串指定语言 / Using String for Language"""
    result = await recognize(
        r'C:\Users\YourName\Pictures\hello.png',
        lang='en-US'  # 英语
    )
    print(result.text)


async def example_ocr_auto():
    """自动检测语言 / Auto-detect Language"""
    result = await recognize(
        r'C:\Users\YourName\Pictures\hello.png',
        lang=None  # 或 lang=OcrLanguage.AUTO
    )
    print(result.text)


# ============================================================================
# 8. 持续时间 / Duration
# ============================================================================

def example_duration_short():
    """短时间（默认）/ Short Duration (default)"""
    notify('Hello Python🐍', duration=ToastDuration.SHORT)


def example_duration_long():
    """长时间（25秒）/ Long Duration (25 seconds)"""
    notify('Hello Python🐍', duration=ToastDuration.LONG)


def example_duration_alarm():
    """无超时 - 闹钟场景 / No Timeout - Alarm Scenario"""
    notify('Hello Python🐍', duration=ToastDuration.ALARM)


def example_duration_reminder():
    """无超时 - 提醒场景 / No Timeout - Reminder Scenario"""
    notify('Hello Python🐍', duration=ToastDuration.REMINDER)


def example_duration_incoming_call():
    """无超时 - 来电场景 / No Timeout - Incoming Call Scenario"""
    notify('Hello Python🐍', duration=ToastDuration.INCOMING_CALL)


def example_duration_urgent():
    """无超时 - 紧急场景 / No Timeout - Urgent Scenario"""
    notify('Hello Python🐍', duration=ToastDuration.URGENT)


def example_duration_string():
    """使用字符串 / Using String"""
    toast('Hello Python🐍', duration='long')  # 也支持字符串


# ============================================================================
# 9. 按钮 / Buttons
# ============================================================================

def example_button_single():
    """单个按钮 / Single Button"""
    notify('Hello', 'Hello from Python', button_content='Dismiss')


def example_button_multiple():
    """多个按钮 / Multiple Buttons"""
    notify('Hello', 'Click a button', buttons=['Approve', 'Dismiss', 'Other'])


# ============================================================================
# 10. 输入字段 / Input Fields
# ============================================================================

def example_input_field():
    """输入字段 / Input Field"""
    result = notify(
        'Hello',
        'Type anything',
        input_id='reply',
        input_placeholder='输入回复...',
        button_content='Send'
    )
    # result['user_input'] 将包含 {'reply': '用户输入的文本'}
    print(f"User input: {result.get('user_input', {})}")


# ============================================================================
# 11. 选择 / Selection
# ============================================================================

def example_selection():
    """选择 / Selection"""
    result = notify(
        'Hello',
        'Which do you like?',
        selection_id='fruit',
        selections=['Apple', 'Banana', 'Grape'],
        button_content='Submit'
    )
    # result['user_input'] 将包含 {'fruit': '选中的选项'}
    print(f"User input: {result.get('user_input', {})}")


# ============================================================================
# 12. 回调函数 / Callback
# ============================================================================

def example_callback():
    """回调函数 / Callback"""
    def handle_click(result):
        print('Clicked!', result)
        print('Arguments:', result['arguments'])
        print('User Input:', result['user_input'])

    toast('Hello Python', 'Click to open url', on_click=handle_click)


# ============================================================================
# 13. 异步 / Async
# ============================================================================

async def example_async():
    """异步函数 / Async Function"""
    await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')


def example_non_blocking():
    """非阻塞 / Non-blocking"""
    notify('Hello Python', 'Click to open url', on_click='https://www.python.org')


# ============================================================================
# 14. 完整示例 / Complete Example
# ============================================================================

def example_complete():
    """完整示例 / Complete Example"""
    # 1. 基本通知
    toast('欢迎', '欢迎使用 win11toast！')
    sleep(1)

    # 2. 带图片的通知
    toast(
        '图片通知',
        '这是一条带图片的通知',
        image_src=r'C:\Users\YourName\Pictures\image.jpg',
        image_placement=ImagePlacement.HERO
    )
    sleep(1)

    # 3. 带图标和音频的通知
    notify(
        '通知',
        '带图标和音频的通知',
        icon_src='https://example.com/icon.png',
        icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
        icon_hint_crop=IconCrop.CIRCLE,
        audio=AudioEvent.DEFAULT,
        duration=ToastDuration.LONG
    )
    sleep(1)

    # 4. 进度通知
    notify_progress(
        title='下载任务',
        status='正在下载...',
        value=0.0,
        value_string_override='0/100 MB',
        icon_src='https://example.com/download.png',
        icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
        audio=None  # 静音
    )

    # 更新进度
    for i in range(1, 101):
        sleep(0.1)
        update_progress(
            value=i/100,
            value_string_override=f'{i}/100 MB'
        )

    # 完成
    update_progress(
        value=1.0,
        status='下载完成！',
        value_string_override='100/100 MB'
    )
    sleep(1)

    # 5. 静音通知
    notify('静音通知', '这是一条静音通知', audio=None)
    sleep(1)

    # 6. 循环播放音频
    notify(
        '循环播放',
        '这条通知的音频会循环播放',
        audio=AudioEvent.LOOPING_ALARM,
        audio_loop=True
    )
    sleep(1)

    # 7. 无超时通知（来电场景）
    notify(
        '来电',
        '这是一个无超时的通知',
        duration=ToastDuration.INCOMING_CALL
    )


# ============================================================================
# 主函数 - 依次调用所有示例 / Main Function - Call All Examples
# ============================================================================

def main():
    """运行所有示例 / Run all examples"""
    print("=" * 60)
    print("win11toast 示例程序 / Examples")
    print("=" * 60)
    
    # 基本通知
    print("\n1. 基本通知 / Basic Notifications")
    example_simple_notification()
    sleep(1)
    example_notification_with_title_and_body()
    sleep(1)
    example_wrap_text()
    sleep(2)
    
    # 图片通知
    print("\n2. 图片通知 / Image Notifications")
    example_image_with_strenum()
    sleep(1)
    example_image_with_string()
    sleep(2)
    
    # 图标通知
    print("\n3. 图标通知 / Icon Notifications")
    example_icon_circular()
    sleep(1)
    example_icon_square()
    sleep(2)
    
    # 进度通知
    print("\n4. 进度通知 / Progress Notifications")
    example_progress_notification()
    sleep(2)
    
    # 音频通知
    print("\n5. 音频通知 / Audio Notifications")
    example_audio_default()
    sleep(1)
    example_audio_silent()
    sleep(1)
    example_audio_loop()
    sleep(2)
    
    # 文本转语音
    print("\n6. 文本转语音 / Text-to-Speech")
    example_text_to_speech()
    sleep(2)
    
    # 持续时间
    print("\n7. 持续时间 / Duration")
    example_duration_short()
    sleep(1)
    example_duration_long()
    sleep(2)
    
    # 按钮
    print("\n8. 按钮 / Buttons")
    example_button_single()
    sleep(1)
    example_button_multiple()
    sleep(2)
    
    # 非阻塞
    print("\n9. 非阻塞 / Non-blocking")
    example_non_blocking()
    sleep(2)
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！/ All examples completed!")
    print("=" * 60)
    print("\n注意：某些示例需要用户交互（如输入字段、选择、回调）")
    print("Note: Some examples require user interaction (input fields, selection, callbacks)")
    print("\n要运行完整示例，请调用：example_complete()")
    print("To run complete example, call: example_complete()")


async def main_async():
    """运行异步示例 / Run async examples"""
    import asyncio
    print("\n运行异步示例 / Running async examples...")
    
    # OCR 示例（需要实际的图片文件）
    # print("\n10. OCR 示例 / OCR Examples")
    # await example_ocr_auto()
    
    # 异步通知示例
    print("\n10. 异步通知 / Async Notification")
    await example_async()
    sleep(2)
    
    print("\n异步示例完成！/ Async examples completed!")


if __name__ == '__main__':
    # 运行同步示例
    main()
    
    # 运行异步示例（取消注释以运行）
    # import asyncio
    # asyncio.run(main_async())

