"""Utility functions for toast notifications / 通知工具函数"""

from typing import Dict, Any
from winrt.windows.foundation import IPropertyValue
from winrt.windows.ui.notifications import ToastActivatedEventArgs

# Global result storage / 全局结果存储
result = list()


def result_wrapper(*args):
    """Wrapper for result storage / 结果存储包装器"""
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

