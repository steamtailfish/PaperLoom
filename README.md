<div align="center">

# 🧵 PaperLoom · 论文织图

### Turn research papers into clear, editable PowerPoint presentations.

**8–10 slides · Original figures · Native equations · Editable PPTX**

![Version](https://img.shields.io/badge/version-1.0.0-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 Quick Start](#quick-start) · [🖼️ Preview](#preview) · [🧭 Workflow](#workflow) · [🛠️ Development](#development) · [📚 Guides](#guides)

</div>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-0A66C2?style=for-the-badge" alt="English"></a>
  <a href="docs/i18n/README_ZH.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-E53935?style=for-the-badge" alt="简体中文"></a>
  <a href="docs/i18n/README_ZH_HK.md"><img src="https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87%EF%BC%88%E9%A6%99%E6%B8%AF%EF%BC%89-EF6C00?style=for-the-badge" alt="繁體中文（香港）"></a>
  <a href="docs/i18n/README_JA.md"><img src="https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-8E24AA?style=for-the-badge" alt="日本語"></a>
  <a href="docs/i18n/README_FR.md"><img src="https://img.shields.io/badge/Fran%C3%A7ais-1565C0?style=for-the-badge" alt="Français"></a>
  <a href="docs/i18n/README_RU.md"><img src="https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-3949AB?style=for-the-badge" alt="Русский"></a>
  <a href="docs/i18n/README_DE.md"><img src="https://img.shields.io/badge/Deutsch-2E7D32?style=for-the-badge" alt="Deutsch"></a>
</p>

---

PaperLoom turns research papers into compact, visual-first presentations for research group meetings. Use it as a skill in a local client, or upload the complete project ZIP and a paper to a web GPT with code execution capabilities.

<a id="features"></a>

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top"><b>🎨 Visual storytelling</b><br>Organize literature reviews into thematic blocks, explain methods with flowcharts and mechanism diagrams, and present results in native tables and charts.</td>
<td width="50%" valign="top"><b>🖼️ Original paper figures</b><br>Extract images embedded in the paper PDF directly. Keep original figure assets instead of using page screenshots or cropped screenshots.</td>
</tr>
<tr>
<td width="50%" valign="top"><b>🧮 Editable equations</b><br>Convert necessary LaTeX equations into native PowerPoint Office Math, ready for further editing.</td>
<td width="50%" valign="top"><b>🔤 Consistent typography</b><br>Use FangSong GB2312 for Chinese and Times New Roman for English and numbers. Verify font files, properties, and hashes.</td>
</tr>
<tr>
<td width="50%" valign="top"><b>🔎 Evidence in speaker notes</b><br>Keep sources and detailed evidence in speaker notes, with only light decoration and slide numbers in the footer.</td>
<td width="50%" valign="top"><b>🛠️ Focused revisions</b><br>Make targeted edits while protecting other approved slides, fonts, equations, and compatibility settings.</td>
</tr>
</table>

<a id="preview"></a>

## 🖼️ Preview

These three slides demonstrate native, editable layouts using explicitly labeled **fictional data**. They illustrate the design, not findings from a real paper.

<table>
<tr>
<th width="33%">Literature review</th>
<th width="33%">Method & equation</th>
<th width="33%">Experiments</th>
</tr>
<tr>
<td><a href="examples/layout-demo/preview-01.png"><img src="examples/layout-demo/preview-01.png" alt="Literature review" width="100%"></a></td>
<td><a href="examples/layout-demo/preview-02.png"><img src="examples/layout-demo/preview-02.png" alt="Method & equation" width="100%"></a></td>
<td><a href="examples/layout-demo/preview-03.png"><img src="examples/layout-demo/preview-03.png" alt="Experiments" width="100%"></a></td>
</tr>
</table>

[Open the editable PowerPoint](examples/layout-demo/layout-demo.pptx) · [View demo source & build instructions](examples/layout-demo/README.md)

<a id="quick-start"></a>

## 🚀 Quick Start

### 💻 Install in a Local Client

Clone or download this repository with its bundled fonts, review the [font guide](fonts/README.md), then run from the repository root:

```bash
python scripts/install_skill.py
```

By default, this copies the skill to `~/.agents/skills/paper-loom/` for the current user. It stops if the directory already exists, preserving your version. In clients that support importing skills, you can also select the complete folder directly. See the [detailed client guide](references/client-mode.md).

After installation, select PaperLoom in the client or enter:

```text
Use $paper-loom to turn this paper into a PowerPoint presentation for a research group
meeting.
Follow the skill's structure, font, figure extraction, and native equation requirements,
and deliver the .pptx file.
```

### 🌐 Upload on the Web

ZIP the **complete project directory, including the required fonts**, and upload it together with the **paper PDF**. Then send:

```text
Please extract the PaperLoom archive I uploaded, read SKILL.md first, and follow its
requirements to create a PowerPoint presentation of this paper for a research group
meeting. Use the default structure: problem (1 slide), literature review (1), methods
(3–5), experiments (2), and conclusion (1). Organize the literature review into thematic
blocks, prioritize figures and charts, and use the bundled FangSong GB2312 and Times New
Roman fonts. Extract figures directly from the paper and convert key equations into
native PowerPoint equations. Put evidence in speaker notes, without small source text in
slide footers. Actually generate and inspect the .pptx file.
```

> [!NOTE]
> The web GPT must be able to extract archives, run code, and generate downloadable files. Uploading a ZIP does not grant these tools or permanently install the skill. See [WEB_START.md](WEB_START.md) for the full guide.

<a id="workflow"></a>

## 🧭 Default Slide Structure

A compact **8–10-slide** narrative, with room to adjust the methods section to the paper:

| Section | Slides | Focus |
|---|:---:|---|
| 🎯 Research problem | 1 | Motivation, existing gaps, and the question to answer |
| 📚 Literature review | 1 | Research themes and the paper’s position |
| ⚙️ Methods | 3–5 | Mechanisms, information flow, and key equations |
| 📊 Experiments | 2 | Results, comparisons, and experimental conditions |
| 💡 Conclusion | 1 | Contributions and limitations |

<details>
<summary><b>Behind the workflow</b></summary>

This skill grew out of several rounds of creating and refining a GeoNav research group presentation: condensing content, adjusting the narrative, handling fonts and native equations, fixing Office formatting, removing footer notes, and replacing a large literature review table with six research themes. It turns that verified workflow into reusable instructions and scripts.

1. **Define the meeting's goals and visual standards**: a real PPTX, compact and information-rich slides, priority for figures and charts, specified fonts, and native equations.
2. **Read the paper and build an evidence index**: connect conclusions, figures, experimental conditions, failure cases, and the limits of each claim.
3. **Plan the narrative before the slides**: move from the problem to the literature review, methods, experiments, and conclusion; allocate method slides according to the actual content.
4. **Prepare original assets and editable objects**: extract figures directly, use native tables and charts, convert LaTeX to Office Math, and apply fonts at the text-run level.
5. **Check content, layout, and compatibility**: render every slide, cross-check data, and correct the invalid GB2312 `charset=134` value to `-122`.
6. **Iterate locally on feedback**: remove source footers while keeping speaker notes, replace the literature review table with thematic blocks, and preserve other slides and formatting fixes.

See the [GeoNav retrospective](examples/geonav/workflow.md) for the complete process.

</details>

<a id="development"></a>

## 🛠️ Development & Validation

Use Python 3.10+ and Node.js 20+. Run these commands from the skill's root directory:

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

Native equation conversion also requires the `pandoc` command; follow the [official Pandoc installation guide](https://pandoc.org/installing.html). The required fonts are included in `fonts/`; see [fonts/README.md](fonts/README.md) for usage details. If your environment already provides dedicated PowerPoint tools, there is no need to switch tools.

<details>
<summary><b>🖼️ Extract figures from a paper</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

The output includes original assets and a manifest. `--pages 1,3-5` is supported. An embedded object may be only part of a figure, so check the semantic completeness of each figure against the paper. Pure vector figures or figures with text overlays must not automatically fall back to screenshots. See the [figure extraction guide](references/figure-extraction.md).

</details>

<details>
<summary><b>🧮 Equations, fonts & PPTX validation</b></summary>

In the native PPTX, reserve a separate paragraph for each necessary equation, such as `[[EQ_FUSION]]`, and record the corresponding LaTeX in a mapping file:

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

The `8` slides and `3` equations are example requirements from the GeoNav presentation; adjust them for each new paper. Do not add equations just to reach a count when the paper does not need them. Font embedding must comply with the fonts' own licenses; by default, the five files in `fonts/` are embedded.

The validator checks package structure, relationships, font character sets, native equations, and placeholders. It **does not provide full OOXML Schema validation or replace testing in desktop Microsoft PowerPoint**. After rendering, inspect the content and layout of every slide. See the [compatibility guide](references/powerpoint-compatibility.md).

</details>

Run the script tests:

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Build release archives</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.0.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.0.0-full.zip
```

The full archive includes the bundled fonts, and the packager checks that all required files are present. `--variant github` creates a source archive without standalone font files.

</details>

<a id="guides"></a>

## 📚 Guides & Repository

[💻 Client guide](references/client-mode.md) · [🌐 Web guide](WEB_START.md) · [🖼️ Figure extraction](references/figure-extraction.md) · [✅ PowerPoint compatibility](references/powerpoint-compatibility.md)

<details>
<summary><b>Repository map</b></summary>

| Path | Contents |
|---|---|
| `SKILL.md` | Core workflow and quality requirements for the AI |
| `WEB_START.md` | Copyable prompts and execution entry point for web use |
| `README.md` | English project overview and language navigation |
| `docs/i18n/` | READMEs in Simplified Chinese, Traditional Chinese (Hong Kong), Japanese, French, Russian, and German |
| `fonts/` | Bundled font files, usage notes, and verification manifest |
| `scripts/` | Tools for figure extraction, native equations, font embedding, PPTX inspection, installation, and packaging |
| `references/` | Guides to slide design, figure extraction, compatibility, and client use |
| `examples/layout-demo/` | Runnable three-slide demo with native editable layouts and build source |
| `examples/geonav/workflow.md` | The production workflow, final eight-slide structure, and key corrections |
| `examples/evidence.template.json` | Template for sources, experimental conditions, and validation records |
| `tests/` | Script behavior and regression tests |

</details>

<a id="license"></a>

## 📄 License

Original project code and documentation are released under [MIT](LICENSE). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for third-party fonts, papers, and dependencies.
