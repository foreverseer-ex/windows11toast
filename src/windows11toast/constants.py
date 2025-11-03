"""Constants for Windows toast notifications / Windows 通知的常量"""

DEFAULT_APP_ID = 'Python'

DEFAULT_XML_TEMPLATE = """
<toast activationType="protocol" launch="http:" scenario="{scenario}">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
"""

