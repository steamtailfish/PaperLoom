<div align="center">

# 🧵 PaperLoom · 论文织图

### 把科研论文，织成清晰、可编辑的 PowerPoint。

**完整讲解 · 多分区页面 · PPTX**

![Version](https://img.shields.io/badge/version-1.3.0-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 快速开始](#quick-start) · [🖼️ 效果预览](#preview) · [🧭 汇报结构](#workflow) · [🛠️ 开发验证](#development) · [📚 使用指南](#guides)

</div>

<p align="center">
  <a href="../../README.md"><img src="https://img.shields.io/badge/English-0A66C2?style=for-the-badge" alt="English"></a>
  <a href="README_ZH.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-E53935?style=for-the-badge" alt="简体中文"></a>
  <a href="README_ZH_HK.md"><img src="https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87%EF%BC%88%E9%A6%99%E6%B8%AF%EF%BC%89-EF6C00?style=for-the-badge" alt="繁體中文（香港）"></a>
  <a href="README_JA.md"><img src="https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-8E24AA?style=for-the-badge" alt="日本語"></a>
  <a href="README_FR.md"><img src="https://img.shields.io/badge/Fran%C3%A7ais-1565C0?style=for-the-badge" alt="Français"></a>
  <a href="README_RU.md"><img src="https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-3949AB?style=for-the-badge" alt="Русский"></a>
  <a href="README_DE.md"><img src="https://img.shields.io/badge/Deutsch-2E7D32?style=for-the-badge" alt="Deutsch"></a>
</p>

---

PaperLoom 面向科研组会，把论文整理成紧凑、图表优先的可编辑演示文稿。既可在客户端安装为 skill，也可将完整项目 ZIP 与论文一起上传给具备代码执行能力的网页 GPT。

<a id="quick-start"></a>

## 🚀 快速开始

### 🌐 网页上传

上传 **paper-loom-v1.3.0-full.zip** 和**论文 PDF**，然后说：

> 请你按照压缩包内skill的要求制作论文的ppt

这就是全部操作。默认设置、制作流程、逐页检查和成品交付都已写入 SKILL.md，无需阅读 README、复制长提示词、填写配置或另传参考稿。

### 💻 客户端安装

克隆或下载本仓库（已附带所需字体），阅读[字体指南](../../fonts/README.md)，然后在仓库根目录执行：

```bash
python scripts/install_skill.py
```

默认复制到当前用户的 `~/.agents/skills/paper-loom/`，遇到已有目录会停止，不覆盖你的版本。也可在支持导入 skill 的客户端中直接选择这个完整文件夹。[客户端详细指南](../../references/client-mode.md)

安装后，在客户端选择 PaperLoom，或输入：

> 使用 $paper-loom，把这篇论文做成科研组会 PPT。

<a id="features"></a>

## ✨ 核心特点

<table>
<tr>
<td width="50%" valign="top"><b>🎨 图表优先的叙事</b><br>图表解释输入、状态、变换与反馈；相关证据同页，实验保留便于精确读取的原生表格与图表。</td>
<td width="50%" valign="top"><b>🖼️ 直接提取论文原图</b><br>直接提取 PDF 的内嵌图片，保留原始图像资源，不截页面、不裁截图冒充提图。</td>
</tr>
<tr>
<td width="50%" valign="top"><b>🧮 真正可编辑的公式</b><br>将必要的 LaTeX 公式转换为 PowerPoint 原生 Office Math，交付后仍可继续编辑。</td>
<td width="50%" valign="top"><b>🔤 统一且可核验的字体</b><br>中文仿宋 GB2312，英文与数字 Times New Roman；字体文件、属性与 hash 均可核验。</td>
</tr>
<tr>
<td width="50%" valign="top"><b>🔎 证据留在演讲者备注</b><br>来源与详细证据放入备注，页面底部只保留轻量装饰和页码，让画面聚焦内容。</td>
<td width="50%" valign="top"><b>🛠️ 按反馈定点修改</b><br>只调整需要修改的内容，保护已经确认的其他页、字体、公式与兼容性设置。</td>
</tr>
</table>

<a id="preview"></a>

## 🖼️ 效果预览

以下三页展示“总览与机制同页”“训练与推理泳道”“主结果与消融及边界同页”，内容均明确标注为**虚构**。包内包含 AeroDuo 六页参考 PDF，供网页端与客户端直接查看，无需另行上传；权利说明见 THIRD_PARTY_NOTICES.md。

<table>
<tr>
<th width="33%">总览与机制</th>
<th width="33%">训练与推理</th>
<th width="33%">实验表格与图表</th>
</tr>
<tr>
<td><a href="../../examples/evidence-demo/preview-01.png"><img src="../../examples/evidence-demo/preview-01.png" alt="总览与机制" width="100%"></a></td>
<td><a href="../../examples/evidence-demo/preview-02.png"><img src="../../examples/evidence-demo/preview-02.png" alt="训练与推理" width="100%"></a></td>
<td><a href="../../examples/evidence-demo/preview-03.png"><img src="../../examples/evidence-demo/preview-03.png" alt="实验表格与图表" width="100%"></a></td>
</tr>
</table>

[打开可编辑 PowerPoint](../../examples/evidence-demo/evidence-demo.pptx) · [查看示例源码与复现步骤](../../examples/evidence-demo/README.md)

[包内 AeroDuo 六页参考 PDF](../../examples/aeroduo-reference/AeroDuo_组会汇报_合并精简6页版.pdf)

<a id="workflow"></a>

## 🧭 默认汇报结构

默认制作**完整科研汇报，不设固定页数区间或上限**。每页用 A/B/C 等区域讲多个相关点，分区数量与面积由图表和子问题决定；机制、实验或图表放不下时增加正文页。核心内容必须可见，不能为压页数省略或仅放备注。用户明确限定页数时以用户要求为准。以下是覆盖范围，各项可安排为分区或展开为多页：

| 内容 | 组织方式 |
|---|---|
| 任务与研究定位 | 场景实例、输入输出、相关路线和成功判定 |
| 核心方法 | 总览条加关键机制、接口和中间状态 |
| 训练与执行 | 监督来源、部署输入、更新和终止条件 |
| 实验 | 主结果结合消融、案例、代价和例外 |
| 总结讨论 | 贡献对应证据，局限说明影响 |

按证据关联与可读性分配页面。制作前读[参考版式](../../references/reference-patterns.md)，填写[逐页计划](../../examples/slide-plan.template.json)，按[质量关卡](../../references/quality-gates.md)审阅。总字数和图片面积均不等于有效信息密度。

[分区规划与内容完整性](../../references/panel-planning.md)

优先使用完整原图解释任务、机制和结果。逐图记录用途与去向，通用公式用操作标签和训练关系表达；只对独特且必要的数学关系另排原生公式。参见 [图文取舍](../../references/visual-selection.md)。

复合图可用 `python scripts/export_pdf_form.py paper.pdf --xref 200 --page 3 --output work/figure-2` 导出独立 PDF、SVG 与 PNG；xref 和页码必须来自当前论文候选清单。

<a id="development"></a>

## 🛠️ 开发与验证

使用 Python 3.10+、Node.js 20+。在 skill 根目录运行：

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

原生公式转换另需 `pandoc` 命令，按 [Pandoc 官方文档](https://pandoc.org/installing.html) 安装。所需字体已包含在 `fonts/` 中，使用说明见 [fonts/README.md](../../fonts/README.md)；当前环境已有专用 PowerPoint 工具时不必强制换工具。

<details>
<summary><b>🖼️ 提取论文图片</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

输出包含原始资源和 manifest。支持 `--pages 1,3-5`。一个内嵌对象可能只是图的一部分，必须对照 Figure 语义完整性；纯矢量或文字叠加的图不能自动截图降级。[提图指南](../../references/figure-extraction.md)

</details>

<details>
<summary><b>🧮 转换公式、嵌入字体与 PPTX 检查</b></summary>

在原生 PPTX 中为每条必要公式留一个独立段落，如 `[[EQ_FUSION]]`，映射文件记录对应 LaTeX：

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/audit_slide_plan.py work/slide-plan.json --report work/plan-audit.json
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
python scripts/audit_slide_quality.py final.pptx --report work/slide-quality.json
```

命令中的页数和公式数仅为示例，请按当前论文调整。 字体嵌入必须符合字体自身许可；默认嵌入 `fonts/` 五个文件。

验证器检查包结构、关系、字体字符集、原生公式与占位符等，但**不等于全量 OOXML Schema 验证，更不等于桌面版 Microsoft PowerPoint 实测**。渲染后仍需逐页检查内容和版式。[兼容性指南](../../references/powerpoint-compatibility.md)

</details>

质量审计将表格与正文分开统计，提示长段落、小图、小字和重复布局风险。它不以总字数判质量，零告警也不能代替逐页视觉审阅。

运行脚本测试：

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 构建发行归档</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.3.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.3.0-full.zip
```

完整归档包含字体、设计规则和示例；打包器排除工作产物，只生成一份与文件内容一致的校验清单；`--variant github` 生成不含独立字体文件的源码归档。

</details>

<a id="guides"></a>

## 📚 使用指南与项目目录

[💻 客户端指南](../../references/client-mode.md) · [🌐 网页使用指南](../../WEB_START.md) · [🖼️ 提图指南](../../references/figure-extraction.md) · [✅ PowerPoint 兼容性](../../references/powerpoint-compatibility.md)

<details>
<summary><b>展开查看项目目录</b></summary>

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 给 AI 读取的核心工作流和质量要求 |
| `WEB_START.md` | 可选的上传与环境说明；SKILL.md 是执行入口 |
| `README.md` | 英文项目说明与语言切换入口 |
| `docs/i18n/` | 简体中文、繁體中文（香港）、日语、法语、俄语和德语 README |
| `fonts/` | 随仓库提供的字体文件、使用说明与校验清单 |
| `scripts/` | 提图、原生公式、字体嵌入、PPTX 检查、安装和打包工具 |
| `references/` | 页面设计、提图、兼容性、客户端使用指南 |
| `examples/aeroduo-reference/` | 六页视觉参考与阅读指南 |
| `examples/evidence-demo/` | 紧凑证据布局、可编辑示例与公开构建源码 |
| `references/panel-planning.md` | 分区规划与内容完整性 |
| `examples/slide-plan.template.json` | 逐页证据、视觉关系、布局和审阅计划 |
| `references/rendering.md` | 公开 PPTX/PDF 渲染回退与视觉检查 |
| `examples/geonav/workflow.md` | 论文证据与页面规划示例 |
| `examples/evidence.template.json` | 来源、实验口径和验证记录模板 |
| `tests/` | 脚本行为与回归测试 |

</details>

<a id="license"></a>

## 📄 开源许可

项目原创代码与文档按 [MIT](../../LICENSE) 发布；第三方字体、论文与依赖见 [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md)。
