# win11toast

Toast notifications for Windows 10 and 11 based on WinRT

A library for Windows 10 and 11 toast notifications based on WinRT

## Installation

```bash
pip install win11toast
```

## Features

- ✅ **Pythonic API** - Fully parameterized functions, no need to pass dictionaries
- ✅ **Type Hints** - Complete type hint support
- ✅ **StrEnum Support** - Use enums for better IDE autocomplete and type safety
- ✅ **Bilingual Documentation** - English and Chinese comments and documentation
- ✅ **Progress Notifications** - Support for real-time progress bar updates
- ✅ **Rich Notifications** - Support for images, icons, buttons, inputs, etc.
- ✅ **Built-in Resources** - Built-in Windows audio events and language options

## Basic Usage

### Simple Notification

```python
from win11toast import toast

toast('Hello Python🐍')
```

### With Title and Body

```python
from win11toast import toast

toast('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

### Wrap Text

```python
from win11toast import toast

toast('Hello', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...')
```

## Parameterized Image

### Using StrEnum (Recommended)

```python
from win11toast import toast, ImagePlacement

# Hero image (large image)
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement=ImagePlacement.HERO
)

# Local file
toast(
    'Hello',
    'Hello from Python',
    image_src=r'C:\Users\YourName\Pictures\image.jpg',
    image_placement=ImagePlacement.HERO
)

# App logo override
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/logo.png',
    image_placement=ImagePlacement.APP_LOGO_OVERRIDE
)

# Inline image
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement=ImagePlacement.INLINE
)
```

### Using String

```python
from win11toast import toast

toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement='hero'  # String is also supported
)
```

## Parameterized Icon

### Using StrEnum (Recommended)

```python
from win11toast import toast, IconPlacement, IconCrop

# Circular icon
toast(
    'Hello',
    'Hello from Python',
    icon_src='https://example.com/icon.png',
    icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
    icon_hint_crop=IconCrop.CIRCLE
)

# Square icon
toast(
    'Hello',
    'Hello from Python',
    icon_src='https://example.com/icon.png',
    icon_placement=IconPlacement.APP_LOGO_OVERRIDE,
    icon_hint_crop=IconCrop.NONE
)
```

## Progress Notifications

### Create Progress Notification

```python
from time import sleep
from win11toast import notify_progress, update_progress

# Parameterized API - more Pythonic
notify_progress(
    title='YouTube',
    status='Downloading...',
    value=0.0,
    value_string_override='0/15 videos'
)

# Update progress
for i in range(1, 16):
    sleep(1)
    update_progress(
        value=i/15,
        value_string_override=f'{i}/15 videos'
    )

# Update status
update_progress(status='Completed!')
```

### Multiple Concurrent Progress Notifications

```python
from win11toast import notify_progress, update_progress

# Create multiple notifications with different tags
notify_progress(
    title='Video 1',
    status='Downloading...',
    value=0.0,
    tag='video1'
)

notify_progress(
    title='Video 2',
    status='Downloading...',
    value=0.0,
    tag='video2'
)

# Update each independently
update_progress(value=0.5, tag='video1')
update_progress(value=0.7, tag='video2')
```

## Audio

### Windows Built-in Audio Events (Using StrEnum)

```python
from win11toast import toast, AudioEvent

# Using StrEnum - IDE autocomplete
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM)

# Default notification sound
toast('Hello', 'Hello from Python', audio=AudioEvent.DEFAULT)

# IM sound
toast('Hello', 'Hello from Python', audio=AudioEvent.IM)

# Mail sound
toast('Hello', 'Hello from Python', audio=AudioEvent.MAIL)

# Reminder sound
toast('Hello', 'Hello from Python', audio=AudioEvent.REMINDER)

# SMS sound
toast('Hello', 'Hello from Python', audio=AudioEvent.SMS)

# Looping alarms (1-10)
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM)
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_ALARM2)
# ... up to LOOPING_ALARM10

# Looping calls (1-10)
toast('Hello', 'Hello from Python', audio=AudioEvent.LOOPING_CALL)
# ... up to LOOPING_CALL10
```

### From URL

```python
from win11toast import toast

toast('Hello', 'Hello from Python', audio='https://example.com/sound.mp3')
```

### From File

```python
from win11toast import toast

toast('Hello', 'Hello from Python', audio=r'C:\Users\YourName\Music\sound.mp3')
```

### Silent

```python
from win11toast import toast

toast('Hello Python🐍', audio=None)  # audio=None means silent
```

### Loop

```python
from win11toast import toast, AudioEvent

toast(
    'Hello',
    'Hello from Python',
    audio=AudioEvent.LOOPING_ALARM,
    audio_loop=True  # Loop the audio
)
```

## Text-to-Speech

```python
from win11toast import toast

toast('Hello Python🐍', dialogue='Hello world')
```

## OCR

### From URL

```python
from win11toast import recognize

result = await recognize('https://example.com/image.png')
print(result.text)
```

### From File

```python
from win11toast import recognize

result = await recognize(r'C:\Users\YourName\Pictures\image.png')
print(result.text)
```

### With Language (Using StrEnum)

```python
from win11toast import recognize, OcrLanguage

# Using StrEnum
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=OcrLanguage.ZH_CN  # Chinese
)

result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=OcrLanguage.JA  # Japanese
)

# Using string
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang='en-US'  # English
)

# Auto-detect (use user profile language)
result = await recognize(
    r'C:\Users\YourName\Pictures\hello.png',
    lang=None  # or lang=OcrLanguage.AUTO
)
```

## Duration

### Using StrEnum (Recommended)

```python
from win11toast import toast, ToastDuration

# Short duration (default)
toast('Hello Python🐍', duration=ToastDuration.SHORT)

# Long duration (25 seconds)
toast('Hello Python🐍', duration=ToastDuration.LONG)

# No timeout - Alarm scenario
toast('Hello Python🐍', duration=ToastDuration.ALARM)

# No timeout - Reminder scenario
toast('Hello Python🐍', duration=ToastDuration.REMINDER)

# No timeout - Incoming call scenario
toast('Hello Python🐍', duration=ToastDuration.INCOMING_CALL)

# No timeout - Urgent scenario
toast('Hello Python🐍', duration=ToastDuration.URGENT)
```

### Using String

```python
from win11toast import toast

toast('Hello Python🐍', duration='long')  # String is also supported
```

## Buttons

### Single Button

```python
from win11toast import toast

toast('Hello', 'Hello from Python', button_content='Dismiss')
```

### Multiple Buttons

```python
from win11toast import toast

toast('Hello', 'Click a button', buttons=['Approve', 'Dismiss', 'Other'])
```

## Input Fields

```python
from win11toast import toast

result = toast(
    'Hello',
    'Type anything',
    input_id='reply',
    input_placeholder='Enter reply...',
    button_content='Send'
)
# result['user_input'] will contain {'reply': 'user typed text'}
```

## Selection

```python
from win11toast import toast

result = toast(
    'Hello',
    'Which do you like?',
    selection_id='fruit',
    selections=['Apple', 'Banana', 'Grape'],
    button_content='Submit'
)
# result['user_input'] will contain {'fruit': 'selected option'}
```

## Callback

```python
from win11toast import toast

def handle_click(result):
    print('Clicked!', result)
    print('Arguments:', result['arguments'])
    print('User Input:', result['user_input'])

toast('Hello Python', 'Click to open url', on_click=handle_click)
```

## Async

### Async Function

```python
from win11toast import toast_async

async def main():
    await toast_async('Hello Python', 'Click to open url', on_click='https://www.python.org')

# Run in async context
import asyncio
asyncio.run(main())
```

### Non-blocking

```python
from win11toast import notify

notify('Hello Python', 'Click to open url', on_click='https://www.python.org')
```

## Custom XML

```python
from win11toast import toast

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

## StrEnum Options Reference

### ImagePlacement

- `ImagePlacement.HERO` - Large image
- `ImagePlacement.APP_LOGO_OVERRIDE` - App logo override
- `ImagePlacement.INLINE` - Inline

### IconPlacement

- `IconPlacement.APP_LOGO_OVERRIDE` - App logo override
- `IconPlacement.APP_LOGO_OVERRIDE_AND_HERO` - App logo override and hero

### IconCrop

- `IconCrop.CIRCLE` - Circular
- `IconCrop.NONE` - Square

### AudioEvent

- `AudioEvent.DEFAULT` - Default notification sound
- `AudioEvent.IM` - IM sound
- `AudioEvent.MAIL` - Mail sound
- `AudioEvent.REMINDER` - Reminder sound
- `AudioEvent.SMS` - SMS sound
- `AudioEvent.LOOPING_ALARM` to `LOOPING_ALARM10` - Looping alarms (1-10)
- `AudioEvent.LOOPING_CALL` to `LOOPING_CALL10` - Looping calls (1-10)

### ToastDuration

- `ToastDuration.SHORT` - Short duration
- `ToastDuration.LONG` - Long duration (25 seconds)
- `ToastDuration.ALARM` - No timeout - Alarm
- `ToastDuration.REMINDER` - No timeout - Reminder
- `ToastDuration.INCOMING_CALL` - No timeout - Incoming call
- `ToastDuration.URGENT` - No timeout - Urgent

### OcrLanguage

- `OcrLanguage.AUTO` - Auto (use user profile language)
- `OcrLanguage.EN_US` - English (US)
- `OcrLanguage.ZH_CN` - Chinese (Simplified)
- `OcrLanguage.JA` - Japanese
- `OcrLanguage.KO` - Korean
- `OcrLanguage.FR` - French
- `OcrLanguage.DE` - German
- `OcrLanguage.ES` - Spanish
- `OcrLanguage.IT` - Italian
- `OcrLanguage.PT` - Portuguese
- `OcrLanguage.RU` - Russian
- `OcrLanguage.AR` - Arabic
- `OcrLanguage.HI` - Hindi

## API Reference

### Main Functions

#### `toast(title, body, ...)`

Create and show a synchronous toast notification.

**Key Parameters:**
- `title`: Notification title
- `body`: Notification body
- `image_src`: Image source URL/path
- `image_placement`: Image placement (`ImagePlacement` enum or string)
- `icon_src`: Icon source URL/path
- `icon_placement`: Icon placement (`IconPlacement` enum or string)
- `icon_hint_crop`: Icon crop hint (`IconCrop` enum or string)
- `audio`: Audio source (`AudioEvent` enum, URL, or file path), `None` for silent
- `audio_loop`: Whether to loop the audio
- `duration`: Toast duration (`ToastDuration` enum or string)
- `on_click`: Callback function or URL string

#### `notify_progress(title, status, value, value_string_override, ...)`

Create a progress notification with parameterized API.

**Key Parameters:**
- `title`: Progress bar title
- `status`: Status text
- `value`: Progress value (0.0 to 1.0)
- `value_string_override`: Custom progress string
- `tag`: Notification tag for updates (default: `'my_tag'`)

#### `update_progress(value, status, value_string_override, tag, ...)`

Update a progress notification.

**Key Parameters:**
- `value`: Progress value (0.0 to 1.0)
- `status`: Status text to update
- `value_string_override`: Custom progress string
- `tag`: Notification tag (must match original)

#### `toast_async(...)`

Async version of `toast`.

#### `notify(...)`

Low-level notification function (non-blocking).

#### `clear_toast(app_id, tag, group)`

Clear notifications from history.

## Improvements

### What's New

1. **Fully Parameterized API**
   - Removed all dictionary support
   - Use StrEnum for better IDE support
   - Complete type hints for all functions

2. **Built-in Resources**
   - `AudioEvent` - Windows built-in audio event enums
   - `ToastDuration` - Toast duration enums (including no-timeout scenarios)
   - `OcrLanguage` - OCR language option enums
   - `ImagePlacement`, `IconPlacement`, `IconCrop` - Image and icon option enums

3. **Progress Notifications**
   - `notify_progress()` - Create progress notifications
   - `update_progress()` - Update progress
   - Support for multiple concurrent notifications

4. **Audio Improvements**
   - `audio=None` means silent (instead of `audio={'silent': 'true'}`)
   - `audio_loop` parameter for looping
   - Support for `AudioEvent` enum and strings

5. **OCR Improvements**
   - Parameterized `lang` parameter
   - Support for `OcrLanguage` enum

6. **Bug Fixes**
   - Fixed `user_input()` TypeError
   - Fixed notification update issues
   - Fixed default `on_click` printing unwanted output

7. **Documentation**
   - Bilingual comments (English/Chinese)
   - Complete type hints
   - Comprehensive examples

## Requirements

- Windows 10 or 11
- Python 3.7+
- `winrt` package

## License

MIT License

## Acknowledgements

- [winsdk_toast](https://github.com/...)
- [Windows-Toasts](https://github.com/...)
- [MarcAlx/notification.py](https://github.com/...)

## Related Links

- [Toast XML Schema](https://learn.microsoft.com/en-us/uwp/schemas/tiles/toastschema/element-toast)
- [Toast Progress Bar](https://learn.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/toast-progress-bar)
- [Notifications Visualizer](https://apps.microsoft.com/store/detail/notifications-visualizer/9NBLGGH5XSL1)

## Complete Examples

See `examples.py` file for complete examples of all features.
