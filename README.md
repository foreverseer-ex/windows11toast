# windows11toast

基于 WinRT 的 Windows 10 和 11 通知库

Toast notifications for Windows 10 and 11 based on WinRT

## 安装

```bash
pip install windows11toast
```

## 特性

- ✅ **Pythonic API** - 完全参数化函数，无需传递字典
- ✅ **类型提示** - 完整的类型提示支持
- ✅ **StrEnum 支持** - 使用枚举提供更好的 IDE 自动补全和类型安全
- ✅ **双语文档** - 中英文注释和文档
- ✅ **进度通知** - 支持实时更新进度条
- ✅ **丰富通知** - 支持图片、图标、按钮、输入等
- ✅ **内置资源** - 提供 Windows 内置音频事件和语言选项

## 基本用法

### 简单通知

```python
from windows11toast import toast

toast('Hello Python🐍')
```

### 带标题和正文

```python
from windows11toast import toast

toast('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

### 文本换行

```python
from windows11toast import toast

toast('Hello', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...')
```

## 参数化图片

### 使用 StrEnum（推荐）

```python
from windows11toast import toast, ImagePlacement

# Hero 图片（大图）
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement=ImagePlacement.HERO
)

# 本地文件
toast(
    'Hello',
    'Hello from Python',
    image_src=r'C:\Users\YourName\Pictures\image.jpg',
    image_placement=ImagePlacement.HERO
)

# 应用Logo覆盖
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/logo.png',
    image_placement=ImagePlacement.APP_LOGO_OVERRIDE
)

# 内联图片
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement=ImagePlacement.INLINE
)
```

### 使用字符串

```python
from windows11toast import toast

toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement='hero'  # 也支持字符串
)
```

## 参数化图标

### 使用 StrEnum（推荐）

```python
from windows11toast import toast, IconPlacement, IconCrop

# 圆形图标
toast(
    'Hello',
    'Hello from Python',
    icon_src='https://example.com/icon.png',
    icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
    icon_hint_crop=IconCrop.CIRCLE
)

# 方形图标
toast(
    'Hello',
    'Hello from Python',
    icon_src='https://example.com/icon.png',
    icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
    icon_hint_crop=IconCrop.NONE
)
```

## 进度通知

### 创建进度通知

```python
from time import sleep
from windows11toast import notify_progress, update_progress

# 参数化API - 更Pythonic
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
```

### 多个并发进度通知

```python
from windows11toast import notify_progress, update_progress

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
```

## 音频

### Windows 内置音频事件（使用 StrEnum）

```python
from windows11toast import toast, AudioEvent

# 使用 StrEnum - IDE 自动补全
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM)

# 默认通知声音
toast('Hello', 'Hello from Python', audio=AudioEvent.DEFAULT)

# IM 声音
toast('Hello', 'Hello from Python', audio=AudioEvent.IM)

# 邮件声音
toast('Hello', 'Hello from Python', audio=AudioEvent.MAIL)

# 提醒声音
toast('Hello', 'Hello from Python', audio=AudioEvent.REMINDER)

# SMS 声音
toast('Hello', 'Hello from Python', audio=AudioEvent.SMS)

# 循环闹钟（1-10）
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM)
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM2)
# ... 直到 LOOPING_ALARM10

# 循环电话（1-10）
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_CALL)
# ... 直到 LOOPING_CALL10
```

### 从 URL

```python
from windows11toast import toast

toast('Hello', 'Hello from Python', audio='https://example.com/sound.mp3')
```

### 从文件

```python
from windows11toast import toast

toast('Hello', 'Hello from Python', audio=r'C:\Users\YourName\Music\sound.mp3')
```

### 静音

```python
from windows11toast import toast

toast('Hello Python🐍', audio=None)  # audio=None 表示静音
```

### 循环播放

```python
from windows11toast import toast, AudioEvent

toast(
    'Hello',
    'Hello from Python',
    audio=AudioEvent.LOOPING_ALARM,
    audio_loop=True  # 循环播放
)
```

## 文本转语音

```python
from windows11toast import toast

toast('Hello Python🐍', dialogue='Hello world')
```

## OCR（光学字符识别）

### 从 URL

```python
from windows11toast import recognize

result = await recognize('https://example.com/image.png')
print(result.text)
```

### 从文件

```python
from windows11toast import recognize

result = await recognize(r'C:\Users\YourName\Pictures\image.png')
print(result.text)
```

### 指定语言（使用 StrEnum）

```python
from windows11toast import recognize, OcrLanguage

# 使用 StrEnum
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=OcrLanguage.ZH_CN  # 中文
)

result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=OcrLanguage.JA  # 日语
)

# 使用字符串
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang='en-US'  # 英语
)

# 自动检测（使用用户配置文件语言）
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=None  # 或 lang=OcrLanguage.AUTO
)
```

## 持续时间

### 使用 StrEnum（推荐）

```python
from windows11toast import toast, ToastDuration

# 短时间（默认）
toast('Hello Python🐍', duration=ToastDuration.SHORT)

# 长时间（25秒）
toast('Hello Python🐍', duration=ToastDuration.LONG)

# 无超时 - 闹钟场景
toast('Hello Python🐍', duration=ToastDuration.ALARM)

# 无超时 - 提醒场景
toast('Hello Python🐍', duration=ToastDuration.REMINDER)

# 无超时 - 来电场景
toast('Hello Python🐍', duration=ToastDuration.INCOMING_CALL)

# 无超时 - 紧急场景
toast('Hello Python🐍', duration=ToastDuration.URGENT)
```

### 使用字符串

```python
from windows11toast import toast

toast('Hello Python🐍', duration='long')  # 也支持字符串
```

## 按钮

### 单个按钮

```python
from windows11toast import toast

toast('Hello', 'Hello from Python', button_content='Dismiss')
```

### 多个按钮

```python
from windows11toast import toast

toast('Hello', 'Click a button', buttons=['Approve', 'Dismiss', 'Other'])
```

## 输入字段

```python
from windows11toast import toast

result = toast(
    'Hello',
    'Type anything',
    input_id='reply',
    input_placeholder='输入回复...',
    button_content='Send'
)
# result['user_input'] 将包含 {'reply': '用户输入的文本'}
```

## 选择

```python
from windows11toast import toast

result = toast(
    'Hello',
    'Which do you like?',
    selection_id='fruit',
    selections=['Apple', 'Banana', 'Grape'],
    button_content='Submit'
)
# result['user_input'] 将包含 {'fruit': '选中的选项'}
```

## 回调函数

```python
from windows11toast import toast

def handle_click(result):
    print('Clicked!', result)
    print('Arguments:', result['arguments'])
    print('User Input:', result['user_input'])

toast('Hello Python', 'Click to open url', on_click=handle_click)
```

## 异步

### 异步函数

```python
from windows11toast import toast_async

async def main():
    await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')

# 在异步上下文中运行
import asyncio
asyncio.run(main())
```

### 非阻塞

```python
from windows11toast import notify

notify('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

## 自定义XML

```python
from windows11toast import toast

xml = """
<toast launch="action=openThread&amp;threadId=92187">
    <visual>
        <binding template="ToastGeneric">
            <text hint-maxLines="1">Jill Bender</text>
            <text>Check out where we camped last weekend!</text>
            <image placement="appLogoOverride" hint-crop="circle" src="https://example.com/icon.png"/>
            <image placement="hero" src="https://example.com/image.jpg"/>
        </binding>
    </visual>
    <actions>
        <input id="textBox" type="text" placeHolderContent="reply"/>
        <action
          content="Send"
          hint-inputId="textBox"
          activationType="background"
          arguments="action=reply&amp;threadId=92187"/>
    </actions>
</toast>"""

toast(xml=xml)
```

## StrEnum 选项参考

### ImagePlacement

- `ImagePlacement.HERO` - 大图
- `ImagePlacement.APP_LOGO_OVERRIDE` - 应用Logo覆盖
- `ImagePlacement.INLINE` - 内联

### IconPlacement

- `IconPlacement.APP_LOGO_OVERRIDE` - 应用Logo覆盖
- `IconPlacement.APP_LOGO_OVERRIDE_AND_HERO` - 应用Logo覆盖和Hero

### IconCrop

- `IconCrop.CIRCLE` - 圆形
- `IconCrop.NONE` - 方形

### AudioEvent

- `AudioEvent.DEFAULT` - 默认通知声音
- `AudioEvent.IM` - IM 声音
- `AudioEvent.MAIL` - 邮件声音
- `AudioEvent.REMINDER` - 提醒声音
- `AudioEvent.SMS` - SMS 声音
- `AudioEvent.LOOPING_ALARM` 到 `LOOPING_ALARM10` - 循环闹钟（1-10）
- `AudioEvent.LOOPING_CALL` 到 `LOOPING_CALL10` - 循环电话（1-10）

### ToastDuration

- `ToastDuration.SHORT` - 短时间
- `ToastDuration.LONG` - 长时间（25秒）
- `ToastDuration.ALARM` - 无超时 - 闹钟
- `ToastDuration.REMINDER` - 无超时 - 提醒
- `ToastDuration.INCOMING_CALL` - 无超时 - 来电
- `ToastDuration.URGENT` - 无超时 - 紧急

### OcrLanguage

- `OcrLanguage.AUTO` - 自动（使用用户配置文件语言）
- `OcrLanguage.EN_US` - 英语（美国）
- `OcrLanguage.ZH_CN` - 中文（简体）
- `OcrLanguage.JA` - 日语
- `OcrLanguage.KO` - 韩语
- `OcrLanguage.FR` - 法语
- `OcrLanguage.DE` - 德语
- `OcrLanguage.ES` - 西班牙语
- `OcrLanguage.IT` - 意大利语
- `OcrLanguage.PT` - 葡萄牙语
- `OcrLanguage.RU` - 俄语
- `OcrLanguage.AR` - 阿拉伯语
- `OcrLanguage.HI` - 印地语

## API参考

### 主要函数

#### `toast(title, body, ...)`

创建并显示同步通知。

**主要参数:**
- `title`: 通知标题
- `body`: 通知正文
- `image_src`: 图片源URL/路径
- `image_placement`: 图片位置（`ImagePlacement` enum 或字符串）
- `icon_src`: 图标源URL/路径
- `icon_placement`: 图标位置（`IconPlacement` enum 或字符串）
- `icon_hint_crop`: 图标裁剪（`IconCrop` enum 或字符串）
- `audio`: 音频源（`AudioEvent` enum、URL 或文件路径），`None` 表示静音
- `audio_loop`: 是否循环播放音频
- `duration`: 通知持续时间（`ToastDuration` enum 或字符串）
- `on_click`: 回调函数或URL字符串

#### `notify_progress(title, status, value, value_string_override, ...)`

使用参数化API创建进度通知。

**主要参数:**
- `title`: 进度条标题
- `status`: 状态文本
- `value`: 进度值（0.0到1.0）
- `value_string_override`: 自定义进度字符串
- `tag`: 通知标签（默认：`'my_tag'`）

#### `update_progress(value, status, value_string_override, tag, ...)`

更新进度通知。

**主要参数:**
- `value`: 进度值（0.0到1.0）
- `status`: 要更新的状态文本
- `value_string_override`: 自定义进度字符串
- `tag`: 通知标签（必须与原始匹配）

#### `toast_async(...)`

`toast` 的异步版本。

#### `notify(...)`

底层通知函数（非阻塞）。

#### `clear_toast(app_id, tag, group)`

从历史记录中清除通知。

## 改进

### 新功能

1. **完全参数化API**
   - 移除了所有字典支持
   - 使用 StrEnum 提供更好的 IDE 支持
   - 所有函数都有完整的类型提示

2. **内置资源**
   - `AudioEvent` - Windows 内置音频事件枚举
   - `ToastDuration` - 通知持续时间枚举（包含无超时场景）
   - `OcrLanguage` - OCR 语言选项枚举
   - `ImagePlacement`, `IconPlacement`, `IconCrop` - 图片和图标选项枚举

3. **进度通知**
   - `notify_progress()` - 创建进度通知
   - `update_progress()` - 更新进度
   - 支持多个并发通知

4. **音频改进**
   - `audio=None` 表示静音（替代 `audio={'silent': 'true'}`）
   - `audio_loop` 参数用于循环播放
   - 支持 `AudioEvent` enum 和字符串

5. **OCR 改进**
   - 参数化的 `lang` 参数
   - 支持 `OcrLanguage` enum

6. **错误修复**
   - 修复了 `user_input()` 类型错误
   - 修复了通知更新问题
   - 修复了默认 `on_click` 打印多余输出的问题

7. **文档**
   - 双语注释（英文/中文）
   - 完整的类型提示
   - 全面的示例

## 要求

- Windows 10 或 11
- Python 3.7+
- `winrt` 包

## 许可证

MIT License

## 致谢

本项目基于 [win11toast](https://github.com/GitHub30/win11toast) 项目，感谢原作者 [GitHub30](https://github.com/GitHub30) 的开源贡献。

本项目在原始项目的基础上进行了重构和改进：
- 完全参数化的API设计
- 使用StrEnum提供更好的类型安全
- 完整的类型提示支持
- 双语文档（中英文）
- 改进的代码结构

其他参考项目：
- [winsdk_toast](https://github.com/...)
- [Windows-Toasts](https://github.com/...)
- [MarcAlx/notification.py](https://github.com/...)

## 相关链接

- [Toast XML Schema](https://learn.microsoft.com/en-us/uwp/schemas/tiles/toastschema/element-toast)
- [Toast Progress Bar](https://learn.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/toast-progress-bar)
- [Notifications Visualizer](https://apps.microsoft.com/store/detail/notifications-visualizer/9NBLGGH5XSL1)

## 完整示例

查看 `examples.py` 文件获取所有功能的完整示例。
