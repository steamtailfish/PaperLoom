<div align="center">

# 🧵 PaperLoom · 论文织图

### Turn research papers into clear, editable PowerPoint presentations.

**Complete coverage · Multiple panels per slide · Editable PPTX**

![Version](https://img.shields.io/badge/version-1.2.0-4455AA?style=flat-square)
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

<a id="quick-start"></a>

## 🚀 Quick Start

### 🌐 Upload on the Web

Upload **paper-loom-v1.2.0-full.zip** and the **paper PDF**, then say:

> Please make a PPT of the paper following the skill in the ZIP.

That is the entire user workflow. SKILL.md contains the defaults and the complete process, including visual review and file delivery. No long prompt, configuration, or separate reference deck is required.

### 💻 Install in a Local Client

Clone or download this repository with its bundled fonts, review the [font guide](fonts/README.md), then run from the repository root:

```bash
python scripts/install_skill.py
```

By default, this copies the skill to `~/.agents/skills/paper-loom/` for the current user. It stops if the directory already exists, preserving your version. In clients that support importing skills, you can also select the complete folder directly. See the [detailed client guide](references/client-mode.md).

After installation, select PaperLoom in the client or enter:

> Use $paper-loom to make a research presentation from this paper.

<a id="features"></a>

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top"><b>🎨 Visual storytelling</b><br>Explain inputs, transformations and feedback with diagrams; combine related evidence and present comparisons in native tables and charts.</td>
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

These three slides show a compact overview with mechanism details, training/inference lanes, and results with ablations and limitations. All content is explicitly **fictional**. The bundled six-page AeroDuo PDF provides a complete visual reference for web and client use. See the reference below and THIRD_PARTY_NOTICES.md.

<table>
<tr>
<th width="33%">Overview & mechanisms</th>
<th width="33%">Training & inference</th>
<th width="33%">Experiments</th>
</tr>
<tr>
<td><a href="examples/evidence-demo/preview-01.png"><img src="examples/evidence-demo/preview-01.png" alt="Overview and mechanisms" width="100%"></a></td>
<td><a href="examples/evidence-demo/preview-02.png"><img src="examples/evidence-demo/preview-02.png" alt="Training & inference" width="100%"></a></td>
<td><a href="examples/evidence-demo/preview-03.png"><img src="examples/evidence-demo/preview-03.png" alt="Experiments" width="100%"></a></td>
</tr>
</table>

[Open the editable PowerPoint](examples/evidence-demo/evidence-demo.pptx) · [View demo source & build instructions](examples/evidence-demo/README.md)

[Bundled AeroDuo six-page reference PDF](examples/aeroduo-reference/AeroDuo_组会汇报_合并精简6页版.pdf)

<a id="workflow"></a>

## 🧭 Default Slide Structure

Build a complete research presentation with **no default slide-count cap**. Use A/B/C sections to explain several related points on each slide, typically starting with 3–5 substantive panels. Add body slides whenever mechanisms, experiments or readable evidence need more space. Keep essential content visible; notes carry supporting explanations. An explicit user slide count takes priority. The following describes coverage, not one slide per item:

| Content | Organization |
|---|---|
| Task and research position | A concrete scene, input/output contract and relevant comparisons |
| Methods | A compact overview with expanded mechanisms and intermediate states |
| Training and execution | Supervision, deployed inputs, update and stopping conditions |
| Results | Main comparisons with ablations, cases, costs and limits |
| Discussion | Contributions paired with evidence and remaining questions |

Do not force a six-card literature page or one slide per equation. Read the [reference patterns](references/reference-patterns.md), use the [slide-plan template](examples/slide-plan.template.json), and apply the [quality gates](references/quality-gates.md). Total word count and picture area are not quality scores.

[Panel planning and content coverage](references/panel-planning.md)

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
python scripts/audit_slide_plan.py work/slide-plan.json --report work/plan-audit.json
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
python scripts/audit_slide_quality.py final.pptx --report work/slide-quality.json
```

The slide and equation counts in these commands are illustrative; choose them for the paper. Font embedding must comply with each font’s license; by default the five files in `fonts/` are embedded.

The validator checks package structure, relationships, font character sets, native equations, and placeholders. It **does not provide full OOXML Schema validation or replace testing in desktop Microsoft PowerPoint**. After rendering, inspect the content and layout of every slide. See the [compatibility guide](references/powerpoint-compatibility.md).

</details>

The quality audit flags observable risks, distinguishes table data from prose, and does not impose a total-word ceiling. Zero warnings do not prove reference-quality design.

Run the script tests:

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Build release archives</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.2.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.2.0-full.zip
```

The full archive includes the bundled fonts, design references and examples. The packager excludes work products and writes one fresh manifest with verified file hashes. `--variant github` creates a source archive without standalone font files.

</details>

<a id="guides"></a>

## 📚 Guides & Repository

[💻 Client guide](references/client-mode.md) · [🌐 Web guide](WEB_START.md) · [🖼️ Figure extraction](references/figure-extraction.md) · [✅ PowerPoint compatibility](references/powerpoint-compatibility.md)

<details>
<summary><b>Repository map</b></summary>

| Path | Contents |
|---|---|
| `SKILL.md` | Core workflow and quality requirements for the AI |
| `WEB_START.md` | Optional upload and environment notes; SKILL.md is the execution entry point |
| `README.md` | English project overview and language navigation |
| `docs/i18n/` | READMEs in Simplified Chinese, Traditional Chinese (Hong Kong), Japanese, French, Russian, and German |
| `fonts/` | Bundled font files, usage notes, and verification manifest |
| `scripts/` | Tools for figure extraction, native equations, font embedding, PPTX inspection, installation, and packaging |
| `references/` | Guides to slide design, figure extraction, compatibility, and client use |
| `examples/aeroduo-reference/` | Six-page visual reference and reading guide |
| `examples/evidence-demo/` | Evidence compositions, editable demo and portable build source |
| `references/panel-planning.md` | Panel planning and content coverage |
| `examples/slide-plan.template.json` | Per-slide evidence, layout and review plan |
| `references/rendering.md` | Public PPTX/PDF rendering fallback for visual review |
| `examples/geonav/workflow.md` | A paper-to-presentation planning example |
| `examples/evidence.template.json` | Template for sources, experimental conditions, and validation records |
| `tests/` | Script behavior and regression tests |

</details>

<a id="license"></a>

## 📄 License

Original project code and documentation are released under [MIT](LICENSE). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for third-party fonts, papers, and dependencies.
