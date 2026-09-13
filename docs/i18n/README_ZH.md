<div align="center">

# 🧵 PaperLoom · 论文织图

### 把科研论文，织成清晰、可编辑的 PowerPoint。

**证据紧凑 · 论文原图 · 原生公式 · 可编辑 PPTX**

![Version](https://img.shields.io/badge/version-1.1.0-4455AA?style=flat-square)
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

<a id="features"></a>

## ✨ 核心特点

<table>
<tr>
<td width="50%" valign="top"><b>🎨 图表优先的叙事</b><br>文献综述按研究路线分块，技术用流程和机制图展开，实验保留便于精确读取的原生表格与图表。</td>
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

以下三页展示“总览与机制同页”“训练与推理泳道”“主结果与消融及边界同页”，内容均明确标注为**虚构**。包内已固化 AeroDuo 参考稿的信息组织规则，无需每次再次上传参考 PDF；不分发第三方论文和原图。

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

<a id="quick-start"></a>

## 🚀 快速开始

### 💻 客户端安装

克隆或下载本仓库（已附带所需字体），阅读[字体指南](../../fonts/README.md)，然后在仓库根目录执行：

```bash
python scripts/install_skill.py
```

默认复制到当前用户的 `~/.agents/skills/paper-loom/`，遇到已有目录会停止，不覆盖你的版本。也可在支持导入 skill 的客户端中直接选择这个完整文件夹。[客户端详细指南](../../references/client-mode.md)

安装后，在客户端选择 PaperLoom，或输入：

```text
使用 $paper-loom，把这篇论文做成科研组会 PowerPoint。
按 skill 的结构、字体、提图和原生公式要求，直接交付 .pptx。
```

### 🌐 网页上传

优先上传发布的 **paper-loom-v1.1.0-full.zip** 与**论文 PDF**。如需从仓库重建，执行 `python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.0-full.zip`，自动排除工作文件和缓存，然后发送：

```text
请解压 PaperLoom，先读取 SKILL.md、references/design.md、
references/reference-patterns.md 和 references/quality-gates.md。
读取论文并整理证据，完成逐页 slide-plan.json 后直接生成中文科研组会 PPT。
默认6–8页，复杂内容可增加；相关机制与证据同页，避免文字卡片堆砌、图小空白多。
保留关键对照、数据、条件与局限，长讲解放备注。使用包内字体、原始提图和原生公式。
运行结构检查与 audit_slide_quality.py，渲染并实际查看每页、修正问题，再交付 .pptx。
```

> [!NOTE]
> 网页 GPT 需要能解压、运行代码并生成可下载文件。上传 ZIP 本身不赋予这些工具，也不会永久安装 skill。完整说明见 [WEB_START.md](../../WEB_START.md)。

<a id="workflow"></a>

## 🧭 默认汇报结构

默认 **6–8 页**，复杂论文可用 8–10 页；用户指定页数优先。以下是覆盖要求，不要求每项独占一页：

| 内容 | 组织方式 |
|---|---|
| 任务与研究定位 | 场景实例、输入输出、相关路线和成功判定 |
| 核心方法 | 总览条加关键机制、接口和中间状态 |
| 训练与执行 | 监督来源、部署输入、更新和终止条件 |
| 实验 | 主结果结合消融、案例、代价和例外 |
| 总结讨论 | 贡献对应证据，局限说明影响 |

不再强制六宫格综述或按公式数量拆页。制作前读[参考版式](../../references/reference-patterns.md)，填写[逐页计划](../../examples/slide-plan.template.json)，按[质量关卡](../../references/quality-gates.md)审阅。总字数和图片面积均不等于有效信息密度。

<details>
<summary><b>展开查看制作流程与实践经验</b></summary>

早期 GeoNav 迭代建立了字体、原生公式与兼容性要求。1.1 版增加 YOPO 与 AeroDuo 的对照经验：先整理证据，再合并相关解释，最后检查真实放映效果。GeoNav 的八页分配只作为历史案例。

1. **确定组会目标和视觉标准**：真实 PPTX、紧凑高密度、图表优先、指定字体和原生公式。
2. **阅读论文并建立证据索引**：把结论、图表、实验口径、失败案例和判断边界对应起来。
3. **先排叙事再排页面**：从现有问题到综述，再到技术、实验和总结；按实际工作量分配技术页数。
4. **处理原始素材与可编辑对象**：直接提图，表格图表原生化，LaTeX 转 Office Math，字体落实到 run。
5. **检查内容、布局与兼容性**：逐页渲染、比对数据，修正 GB2312 `charset=134` 的不合规写法为 `-122`。
6. **按反馈局部迭代**：删除来源页脚，保留备注；将综述表格改成分块；确保其他页面和格式修复不回退。

完整过程见 [GeoNav 复盘](../../examples/geonav/workflow.md)。

</details>

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
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
python scripts/audit_slide_quality.py final.pptx --report work/slide-quality.json
```

`8` 页和 `3` 条公式是本次 GeoNav 的示例要求，新论文按实际调整。没有必要公式的论文不必为了凑数量添加。字体嵌入必须符合字体自身许可；默认嵌入 `fonts/` 五个文件。

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
python scripts/package_skill.py --variant github --output ../paper-loom-v1.1.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.0-full.zip
```

完整归档包含字体、新版设计规则和示例；打包器排除工作产物，只生成一份与文件内容一致的校验清单；`--variant github` 生成不含独立字体文件的源码归档。

</details>

<a id="guides"></a>

## 📚 使用指南与项目目录

[💻 客户端指南](../../references/client-mode.md) · [🌐 网页使用指南](../../WEB_START.md) · [🖼️ 提图指南](../../references/figure-extraction.md) · [✅ PowerPoint 兼容性](../../references/powerpoint-compatibility.md)

<details>
<summary><b>展开查看项目目录</b></summary>

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 给 AI 读取的核心工作流和质量要求 |
| `WEB_START.md` | 网页端复制提示词与执行入口 |
| `README.md` | 英文项目说明与语言切换入口 |
| `docs/i18n/` | 简体中文、繁體中文（香港）、日语、法语、俄语和德语 README |
| `fonts/` | 随仓库提供的字体文件、使用说明与校验清单 |
| `scripts/` | 提图、原生公式、字体嵌入、PPTX 检查、安装和打包工具 |
| `references/` | 页面设计、提图、兼容性、客户端使用指南 |
| `examples/evidence-demo/` | 紧凑证据布局、可编辑示例与公开构建源码 |
| `examples/slide-plan.template.json` | 逐页证据、视觉关系、布局和审阅计划 |
| `references/rendering.md` | 公开 PPTX/PDF 渲染回退与视觉检查 |
| `examples/geonav/workflow.md` | 本次制作流程、最终 8 页结构与关键修正 |
| `examples/evidence.template.json` | 来源、实验口径和验证记录模板 |
| `tests/` | 脚本行为与回归测试 |

</details>

<a id="license"></a>

## 📄 开源许可

项目原创代码与文档按 [MIT](../../LICENSE) 发布；第三方字体、论文与依赖见 [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md)。
