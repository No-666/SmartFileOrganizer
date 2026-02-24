# 🚀 SmartFileOrganizer (sfo)

**智能文件自动整理大师**  
再也不用手动整理「下载」「桌面」「照片」「文档」文件夹！  
支持**规则引擎 + 智能去重 + 实时监控 + 多线程加速**，一键把乱七八糟的文件整理得井井有条。

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/version-0.1.0-orange?style=flat-square)
[![GitHub stars](https://img.shields.io/github/stars/你的用户名/smartfileorganizer?style=social)](https://github.com/你的用户名/smartfileorganizer)

---

## ✨ 核心特性

- **灵活规则引擎**：按扩展名、文件名关键字、创建/修改日期（支持 `{year}/{month}` 占位符）、文件大小等多维度规则
- **智能重复文件检测**：MD5/SHA256 哈希精准识别，支持「保留最新」「保留最大」「移动到回收站」三种策略
- **Dry-run 安全模式**：任何操作前可预览，绝不误删误移
- **多线程 + 进度条**：处理上万文件丝滑流畅（Rich + tqdm）
- **实时监控模式**：使用 watchdog 监听文件夹，新文件自动整理
- **YAML 配置持久化**：支持自定义任意规则，一次配置永久生效
- **美观终端界面**：Rich 渲染，日志自动保存
- **现代打包**：pyproject.toml + editable 安装，一行命令全局可用 `sfo`

---

## 📥 安装

### 1. 克隆项目
```bash
git clone https://github.com/你的用户名/smartfileorganizer.git
cd smartfileorganizer