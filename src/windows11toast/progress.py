"""Progress notification functions / 进度通知函数"""

from typing import Optional, Dict, Any, Union, Callable
from winrt.windows.ui.notifications import ToastNotification

from .enums import ImagePlacement, IconPlacement, IconCrop, AudioEvent, ToastDuration
from .constants import DEFAULT_APP_ID
from .notification import notify, _notification_cache, _notification_sequence


def notify_progress(title: Optional[str] = None,
                    status: Optional[str] = None,
                    value: Optional[float] = None,
                    value_string_override: Optional[str] = None,
                    app_id: str = DEFAULT_APP_ID,
                    tag: str = 'my_tag',
                    group: Optional[str] = None,
                    # Icon options / 图标选项
                    icon_src: Optional[str] = None,
                    icon_placement: Optional[IconPlacement] = None,
                    icon_hint_crop: Optional[IconCrop] = None,
                    # Image options / 图片选项
                    image_src: Optional[str] = None,
                    image_placement: Optional[ImagePlacement] = None,
                    # Audio options / 音频选项
                    audio: Optional[Union[str, AudioEvent]] = None,
                    audio_loop: bool = False,
                    # Duration / 持续时间
                    duration: Optional[ToastDuration] = None,
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
        icon_placement: Icon placement (IconPlacement enum only) / 图标位置（仅IconPlacement枚举）
        icon_hint_crop: Icon crop hint (IconCrop enum only) / 图标裁剪提示（仅IconCrop枚举）

        # Image options / 图片选项
        image_src: Image source URL/path / 图片源URL/路径
        image_placement: Image placement (ImagePlacement enum only) / 图片位置（仅ImagePlacement枚举）

        # Audio options / 音频选项
        audio: Audio source (AudioEvent enum for built-in sounds, or URL/file path string). None for silent / 音频源（AudioEvent枚举用于内置声音，或URL/文件路径字符串）。None表示静音
        audio_loop: Whether to loop the audio / 是否循环播放音频

        # Duration / 持续时间
        duration: Toast duration (ToastDuration enum only) / 通知持续时间（仅ToastDuration枚举）

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

