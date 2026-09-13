# 客户端安装与调用

## 安装对象

安装整个 `paper-loom/` 目录，而不是单独的 `SKILL.md`。字体、脚本、指南和示例是同一个 skill 的资源。

客户端如果支持导入本地 skill 文件夹，直接选择解压后的目录。Codex 本地使用也可以放到用户级 `~/.agents/skills/paper-loom/`，或项目级 `.agents/skills/paper-loom/`。此路径依据 [OpenAI 的 skill 文档](https://developers.openai.com/codex/skills/)；其他客户端应遵循其自身技能目录约定。

本项目提供跨平台复制脚本，默认复制到当前用户的 `.agents/skills`，不会覆写已有目录：

```bash
python scripts/install_skill.py
```

指定其他客户端或测试目录：

```bash
python scripts/install_skill.py --dest /path/to/client/skills/paper-loom
```

Windows PowerShell 可使用 `py` 代替 `python`；默认目标为当前用户目录下 `.agents\skills\paper-loom`。安装后在客户端技能列表确认；未刷新时重新打开技能列表或新建会话，不要重复覆盖安装。

## 调用

```text
使用 $paper-loom，把这篇论文做成科研组会 PowerPoint。
请遵循 skill 的结构、字体、提图、原生公式和兼容性要求，直接交付 .pptx。
```

安装到通过 `@` 选择技能的客户端时，在技能选择器中选择 PaperLoom。也可以明确要求客户端读取安装目录中的 `SKILL.md`。

## 依赖与执行环境

从 skill 根目录运行：

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

原生公式转换使用 Pandoc 命令行程序。按 [Pandoc 官方安装说明](https://pandoc.org/installing.html) 安装；`doctor.py` 会报告是否可用。Node.js 和 PptxGenJS 用于公开示例；有其他可用原生 PowerPoint 构建工具时可使用它。

操作字体时不修改原始文件。字体复制到 `fonts/` 不等于已被系统渲染器发现：在有本地 PowerPoint 的系统中按许可安装字体，或使用支持局部字体注册的渲染器；可编辑嵌入由本包 `embed_fonts.py` 处理。不要把 PDF 预览正确当成 PPTX 一定正确。

## GitHub 源码包与完整包

GitHub 源码包保留 skill、代码、文档、示例及 `fonts/` 清单，第三方 TTF 不在其中。使用者从自己有权使用的来源补齐字体。完整包另含本次用户提供的五个原始字体文件，便于当前用户在获授权环境中直接使用。
