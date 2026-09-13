<div align="center">

# 🧵 PaperLoom · 论文织图

### Turn research papers into clear, editable PowerPoint presentations.

**Evidence-rich slides · Original figures · Native equations · Editable PPTX**

![Version](https://img.shields.io/badge/version-1.1.0-4455AA?style=flat-square)
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

These three slides show a compact overview with mechanism details, training/inference lanes, and results with ablations and limitations. All content is explicitly **fictional**. The package includes design patterns distilled from the user's AeroDuo reference, without redistributing third-party PDFs or paper figures.

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

Upload the released **paper-loom-v1.1.0-full.zip** together with the **paper PDF**. To rebuild from this repository, use `python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.0-full.zip`; this excludes working files and caches. Then send:

```text
Unzip PaperLoom and read SKILL.md, references/design.md,
references/reference-patterns.md and references/quality-gates.md before authoring.
Read the paper, map its evidence and prepare slide-plan.json, then continue directly
to an editable research presentation. Aim for 6–8 slides unless the evidence needs more.
Combine related mechanisms and evidence; avoid repetitive text cards, small figures
surrounded by whitespace, and splitting one mechanism across several pages.
Keep comparisons, data and conditions; put long explanations in speaker notes.
Use the bundled fonts, original extracted figures and native equations. Run the package
and slide-quality audits, render and inspect every slide, fix issues, then deliver .pptx.
```

> [!NOTE]
> The web GPT must be able to extract archives, run code, and generate downloadable files. Uploading a ZIP does not grant these tools or permanently install the skill. See [WEB_START.md](WEB_START.md) for the full guide.

<a id="workflow"></a>

## 🧭 Default Slide Structure

Default to **6–8 slides**; complex papers may need 8–10. A user-specified count takes priority. These are coverage requirements, not mandatory separate pages:

| Content | Organization |
|---|---|
| Task and research position | A concrete scene, input/output contract and relevant comparisons |
| Methods | A compact overview with expanded mechanisms and intermediate states |
| Training and execution | Supervision, deployed inputs, update and stopping conditions |
| Results | Main comparisons with ablations, cases, costs and limits |
| Discussion | Contributions paired with evidence and remaining questions |

Do not force a six-card literature page or one slide per equation. Read the [reference patterns](references/reference-patterns.md), use the [slide-plan template](examples/slide-plan.template.json), and apply the [quality gates](references/quality-gates.md). Total word count and picture area are not quality scores.

<details>
<summary><b>Behind the workflow</b></summary>

The original GeoNav iteration established fonts, native equations and Office compatibility. Version 1.1 adds lessons from comparing YOPO with AeroDuo: plan evidence before pages, combine related explanations, and inspect the actual visual result. The old GeoNav allocation is a historical example.

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
python scripts/audit_slide_quality.py final.pptx --report work/slide-quality.json
```

The `8` slides and `3` equations are example requirements from the GeoNav presentation; adjust them for each new paper. Do not add equations just to reach a count when the paper does not need them. Font embedding must comply with the fonts' own licenses; by default, the five files in `fonts/` are embedded.

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
python scripts/package_skill.py --variant github --output ../paper-loom-v1.1.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.0-full.zip
```

The full archive includes the bundled fonts, new design references and examples. The packager excludes work products and writes one fresh manifest with verified file hashes. `--variant github` creates a source archive without standalone font files.

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
| `examples/evidence-demo/` | Evidence compositions, editable demo and portable build source |
| `examples/slide-plan.template.json` | Per-slide evidence, layout and review plan |
| `references/rendering.md` | Public PPTX/PDF rendering fallback for visual review |
| `examples/geonav/workflow.md` | The production workflow, final eight-slide structure, and key corrections |
| `examples/evidence.template.json` | Template for sources, experimental conditions, and validation records |
| `tests/` | Script behavior and regression tests |

</details>

<a id="license"></a>

## 📄 License

Original project code and documentation are released under [MIT](LICENSE). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for third-party fonts, papers, and dependencies.
