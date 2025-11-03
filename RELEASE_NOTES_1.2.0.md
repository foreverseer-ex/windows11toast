# Release v1.2.0

## 🎉 windows11toast v1.2.0 发布

基于 WinRT 的 Windows 10/11 通知库，完全重构版本。

---

## ✨ 主要特性

### 🚀 完全参数化的 API
- 告别字典参数，所有功能使用独立参数
- 完整的类型提示，提供 IDE 智能补全
- StrEnum 支持，类型更安全

### 📦 模块化架构
- 代码按功能模块化组织
- 符合 Python 包最佳实践
- 中英文双语文档

### 🎯 核心功能
- ✅ 基本通知、图片、图标
- ✅ 进度通知（实时更新）
- ✅ 音频通知、文本转语音
- ✅ OCR 光学字符识别
- ✅ 按钮、输入、选择等交互功能

---

## 📥 安装

```bash
pip install windows11toast
```

**要求：** Windows 10/11, Python 3.9-3.13

---

## 🚀 快速开始

```python
from windows11toast import toast, ImagePlacement

# 简单通知
toast('Hello Python🐍')

# 带图片的通知
toast(
    'Hello',
    'Hello from Python',
    image_src='https://example.com/image.jpg',
    image_placement=ImagePlacement.HERO
)

# 进度通知
from windows11toast import notify_progress, update_progress
notify_progress(title='下载', status='下载中...', value=0.0)
update_progress(value=0.5, status='50% 完成')
```

---

## 📚 文档

- 📖 [完整文档](https://github.com/foreverseer-ex/windows11toast/blob/main/README.md)
- 💡 [示例代码](https://github.com/foreverseer-ex/windows11toast/blob/main/examples.py)

---

## 🆕 主要改进

- ✅ **完全参数化 API**：`toast(image_src='url', image_placement=ImagePlacement.HERO)`
- ✅ **类型安全**：完整的类型提示和 StrEnum 支持
- ✅ **模块化架构**：从单文件 1300+ 行重构为模块化结构
- ✅ **双语文档**：中英文注释和文档

---

## 🙏 致谢

本项目基于 [win11toast](https://github.com/GitHub30/win11toast)，感谢原作者 [GitHub30](https://github.com/GitHub30) 的开源贡献。

---

## 🔗 相关链接

- 🏠 [GitHub 仓库](https://github.com/foreverseer-ex/windows11toast)
- 🐛 [问题反馈](https://github.com/foreverseer-ex/windows11toast/issues)
- 📦 [PyPI 页面](https://pypi.org/project/windows11toast/)
