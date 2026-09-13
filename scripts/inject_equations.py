#!/usr/bin/env python3
"""Convert LaTeX placeholders into editable native PowerPoint equations.

Usage:
  python scripts/inject_equations.py source.pptx result.pptx --mapping equations.json
  python scripts/inject_equations.py result.pptx --verify-only

Use one placeholder (for example [[EQ_1]]) as the complete text of a paragraph.
The paragraph may be split across DrawingML runs. The containing text box and
its position, dimensions, margins, fill, and paragraph alignment are retained.
The first existing run's size and color are inherited; --font-size overrides
the size in points. Equations use Times New Roman unless --font is supplied. PowerPoint may use
its math-font fallback for glyphs that Times New Roman does not contain.

Conversion route: Pandoc's TeXMath parser -> OMML -> a14:m in DrawingML.
This is the native Office Math structure used by PowerPoint's equation editor,
not a formula picture or an OLE object. Requires local pandoc and Python lxml.
Format target: PowerPoint 2010+ OOXML; desktop opening is a separate check. Other presentation clients may render
or round-trip OMML differently. Do not re-export the delivered PPTX through a
client that replaces Office Math with pictures.

Mapping formats:
  {"[[EQ_1]]": "P=\\Pi(\\mathcal{T},\\mathcal{K})"}
  {"[[EQ_1]]": {"latex": "...", "font_size": 20, "color": "123456"}}
  {"equations": [{"token": "[[EQ_1]]", "latex": "...", ...}, ...]}

Source: Microsoft TextMath a14:m specification, Office 2010 and above:
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.office2010.drawing.textmath
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from lxml import etree


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
for prefix, uri in NS.items():
    etree.register_namespace(prefix, uri)


def q(prefix, local):
    return "{" + NS[prefix] + "}" + local


def read_mapping(path: Path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = raw.get("equations") if isinstance(raw, dict) and isinstance(raw.get("equations"), list) else raw
    if isinstance(entries, list):
        mapping = {}
        for entry in entries:
            if not isinstance(entry, dict) or "token" not in entry:
                raise ValueError("Each equation-list entry needs a token and latex")
            token = entry["token"]
            if not isinstance(token, str) or token in mapping:
                raise ValueError(f"Invalid or duplicate equation token: {token!r}")
            mapping[token] = entry
    elif isinstance(raw, dict):
        mapping = raw
    else:
        raise ValueError("Equation mapping must be a JSON object or list")
    if not mapping:
        raise ValueError("Equation mapping cannot be empty")
    for token, entry in list(mapping.items()):
        if not isinstance(token, str) or not re.fullmatch(r"\[\[EQ_[A-Za-z0-9_]+\]\]", token):
            raise ValueError(f"Use a token such as [[EQ_1]], got {token!r}")
        if isinstance(entry, str):
            entry = {"latex": entry}
        if not isinstance(entry, dict) or not isinstance(entry.get("latex"), str):
            raise ValueError(f"Invalid mapping for {token!r}")
        mapping[token] = entry
    return mapping


def latex_to_omml(latex: str, pandoc: str):
    """Return exactly one native m:oMath parsed from a TeX math expression."""
    latex = latex.strip()
    if latex.startswith("$$") and latex.endswith("$$"):
        latex = latex[2:-2].strip()
    elif latex.startswith("$") and latex.endswith("$"):
        latex = latex[1:-1].strip()
    proc = subprocess.run(
        # DOCX is binary; current Pandoc requires explicit stdout output even
        # when subprocess captures stdout through a pipe.
        [pandoc, "--from=markdown+tex_math_dollars", "--to=docx", "--output=-", "--fail-if-warnings"],
        input=("$$\n" + latex + "\n$$\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise RuntimeError("LaTeX -> OMML conversion failed: " + proc.stderr.decode("utf-8", "replace"))
    with zipfile.ZipFile(io.BytesIO(proc.stdout)) as zf:
        root = etree.fromstring(zf.read("word/document.xml"))
    maths = root.findall(".//m:oMath", NS)
    if len(maths) != 1 or not maths[0].findall(".//m:t", NS):
        raise RuntimeError(f"Expected one nonempty Office Math expression, found {len(maths)}")
    result = deepcopy(maths[0])
    # Avoid unused Word namespace declarations in the PowerPoint package.
    etree.cleanup_namespaces(result)
    return result


def base_run_properties(paragraph, options, defaults):
    candidates = paragraph.xpath("./a:r/a:rPr", namespaces=NS)
    if not candidates:
        candidates = paragraph.xpath("./a:pPr/a:defRPr | ./a:endParaRPr", namespaces=NS)
    prop = deepcopy(candidates[0]) if candidates else etree.Element(q("a", "rPr"))
    prop.tag = q("a", "rPr")
    font_size = options.get("font_size", defaults.get("font_size"))
    if font_size is not None:
        prop.set("sz", str(round(float(font_size) * 100)))
    elif not prop.get("sz"):
        prop.set("sz", "2000")
    # Equation math-style attributes (m:sty, m:scr) control mathematical italics;
    # do not force all formula characters to the original token's text style.
    for attr in ["b", "i", "u", "baseline", "spc", "kern", "cap"]:
        prop.attrib.pop(attr, None)
    prop.set("lang", "en-US")
    prop.set("dirty", "0")
    font = options.get("font", defaults.get("font", "Times New Roman"))
    for child in list(prop):
        if child.tag in {q("a", x) for x in ("latin", "ea", "cs", "sym", "hlinkClick", "hlinkMouseOver")}:
            prop.remove(child)
    color = options.get("color", defaults.get("color"))
    if color:
        for child in list(prop):
            if child.tag in {q("a", x) for x in ("solidFill", "gradFill", "noFill", "blipFill", "pattFill", "grpFill")}:
                prop.remove(child)
        fill = etree.SubElement(prop, q("a", "solidFill"))
        etree.SubElement(fill, q("a", "srgbClr"), val=str(color).lstrip("#"))
    etree.SubElement(prop, q("a", "latin"), typeface=font)
    etree.SubElement(prop, q("a", "ea"), typeface=font)
    etree.SubElement(prop, q("a", "cs"), typeface=font)
    # CT_TextCharacterProperties is a sequence, not an unordered bag.
    order = {name: index for index, group in enumerate([
        ("ln",), ("noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"),
        ("effectLst", "effectDag"), ("highlight",), ("uLnTx", "uLn"),
        ("uFillTx", "uFill"), ("latin",), ("ea",), ("cs",), ("sym",),
        ("hlinkClick",), ("hlinkMouseOver",), ("rtl",), ("extLst",)
    ]) for name in group}
    prop[:] = sorted(prop, key=lambda e: order.get(etree.QName(e).localname, 99))
    return prop


def add_drawing_styles(omath, prop):
    """Use DrawingML run properties inside OMML as required in a14 text math."""
    for wrpr in list(omath.findall(".//w:rPr", NS)):
        wrpr.getparent().remove(wrpr)
    for run in omath.findall(".//m:r", NS):
        for arpr in list(run.findall("a:rPr", NS)):
            run.remove(arpr)
        # m:rPr precedes a:rPr; mathematical content follows both.
        idx = 1 if len(run) and run[0].tag == q("m", "rPr") else 0
        run.insert(idx, deepcopy(prop))
    # Control properties style structural characters (fraction bars, fences,
    # radicals) as well as literal runs; only add where OOXML allows ctrlPr.
    property_names = {
        "accPr", "barPr", "boxPr", "borderBoxPr", "dPr", "eqArrPr", "fPr",
        "funcPr", "groupChrPr", "limLowPr", "limUppPr", "mPr", "naryPr",
        "phantPr", "radPr", "sPrePr", "sSubPr", "sSubSupPr", "sSupPr",
    }
    for element in omath.iter():
        if etree.QName(element).namespace == NS["m"] and etree.QName(element).localname in property_names:
            ctrl = element.find("m:ctrlPr", NS)
            if ctrl is None:
                ctrl = etree.SubElement(element, q("m", "ctrlPr"))
            for child in list(ctrl):
                ctrl.remove(child)
            ctrl.append(deepcopy(prop))


def replace_paragraph(paragraph, omath, prop, options):
    ppr = paragraph.find("a:pPr", NS)
    if ppr is None:
        ppr = etree.Element(q("a", "pPr"))
        paragraph.insert(0, ppr)
    existing_def = ppr.find("a:defRPr", NS)
    if existing_def is not None:
        ppr.remove(existing_def)
    defpr = deepcopy(prop)
    defpr.tag = q("a", "defRPr")
    ppr.append(defpr)
    for child in list(paragraph):
        if child is not ppr:
            paragraph.remove(child)
    wrapper = etree.SubElement(paragraph, q("a14", "m"), nsmap={"a14": NS["a14"], "m": NS["m"]})
    if options.get("inline", False):
        wrapper.append(omath)
    else:
        math_para = etree.SubElement(wrapper, q("m", "oMathPara"))
        math_ppr = etree.SubElement(math_para, q("m", "oMathParaPr"))
        align = {"l": "left", "ctr": "center", "r": "right"}.get(ppr.get("algn"), "left")
        etree.SubElement(math_ppr, q("m", "jc"), {q("m", "val"): align})
        math_para.append(omath)
    endpr = deepcopy(prop)
    endpr.tag = q("a", "endParaRPr")
    paragraph.append(endpr)


def ensure_math_namespaces(root):
    nsmap = dict(root.nsmap)
    nsmap.update({k: NS[k] for k in ("a14", "m", "mc")})
    replacement = etree.Element(root.tag, attrib=root.attrib, nsmap=nsmap)
    replacement.text, replacement.tail = root.text, root.tail
    for child in list(root):
        replacement.append(child)
    ignorable = set(replacement.get(q("mc", "Ignorable"), "").split())
    ignorable.add("a14")
    replacement.set(q("mc", "Ignorable"), " ".join(sorted(ignorable)))
    return replacement


def verify_pptx(path: Path):
    report = {"file": str(path), "math_objects": 0, "math_expressions": 0, "slides_with_math": [], "unresolved_tokens": []}
    with zipfile.ZipFile(path) as zf:
        if zf.testzip() is not None:
            raise RuntimeError("PPTX ZIP integrity check failed")
        for name in sorted(zf.namelist()):
            if not re.fullmatch(r"ppt/slides/slide\d+\.xml", name):
                continue
            root = etree.fromstring(zf.read(name))
            wrappers = root.findall(".//a14:m", NS)
            maths = root.findall(".//a14:m//m:oMath", NS)
            for wrapper in wrappers:
                if not wrapper.findall(".//m:oMath", NS):
                    raise RuntimeError(f"Empty math object in {name}")
            if wrappers:
                report["slides_with_math"].append({"slide": name, "objects": len(wrappers), "expressions": len(maths)})
            report["math_objects"] += len(wrappers)
            report["math_expressions"] += len(maths)
            text = "".join(root.xpath("//a:t/text()", namespaces=NS))
            report["unresolved_tokens"].extend({"slide": name, "token": t} for t in re.findall(r"\[\[EQ_[^\]]+\]\]", text))
    if report["unresolved_tokens"]:
        raise RuntimeError("Unresolved equation tokens: " + json.dumps(report["unresolved_tokens"], ensure_ascii=False))
    return report


def inject_equations(source: Path, destination: Path, mapping, pandoc="pandoc", defaults=None, require_all=False):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output must be different; the source is never overwritten")
    if destination.exists():
        raise FileExistsError(f"Output already exists; choose a new filename: {destination}")
    defaults = defaults or {"font": "Times New Roman"}
    if not Path(pandoc).is_file():
        pandoc = shutil.which(pandoc) or shutil.which("pandoc")
    if not pandoc:
        raise FileNotFoundError("Pandoc is required for native OMML conversion")
    cache = {}
    used = set()
    changes = []
    output = io.BytesIO()
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(output, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", info.filename):
                root = etree.fromstring(data)
                changed = False
                for paragraph in root.findall(".//a:p", NS):
                    content = "".join(paragraph.xpath(".//a:t/text()", namespaces=NS)).strip()
                    if content not in mapping:
                        partial = [token for token in mapping if token in content]
                        if partial:
                            raise ValueError(f"Equation token must occupy a whole paragraph: {partial[0]} in {info.filename}")
                        continue
                    entry = mapping[content]
                    latex = entry["latex"]
                    if latex not in cache:
                        cache[latex] = latex_to_omml(latex, pandoc)
                    omath = deepcopy(cache[latex])
                    prop = base_run_properties(paragraph, entry, defaults)
                    add_drawing_styles(omath, prop)
                    replace_paragraph(paragraph, omath, prop, entry)
                    changes.append({"slide": info.filename, "token": content, "font_size": int(prop.get("sz")) / 100, "latex": latex})
                    used.add(content)
                    changed = True
                if changed:
                    root = ensure_math_namespaces(root)
                    data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zout.writestr(info, data)
    if not changes:
        raise ValueError("No equation placeholders were found; nothing was written")
    unused = sorted(set(mapping) - used)
    if require_all and unused:
        raise ValueError("Mapping contains unused tokens: " + ", ".join(unused))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".pptx", delete=False) as tmp:
            tmp.write(output.getvalue())
            temp_path = Path(tmp.name)
        report = verify_pptx(temp_path)
        temp_path.replace(destination)
        report["file"] = str(destination)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    report.update({"pandoc": pandoc, "replacements": changes, "unused_mapping_tokens": unused})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--mapping", type=Path, help="Required JSON token-to-LaTeX mapping when converting")
    parser.add_argument("--pandoc", default="pandoc", help="Executable name on PATH or full executable path")
    parser.add_argument("--font", default="Times New Roman")
    parser.add_argument("--font-size", type=float, default=None, help="Override inherited font size, in points")
    parser.add_argument("--color", default=None, help="Override inherited color, six-digit hex")
    parser.add_argument("--require-all", action="store_true", help="Require every mapping token to occur in input")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report and args.report.resolve() in {args.input.resolve(), args.output.resolve() if args.output else args.input.resolve()}:
        parser.error("--report must not overwrite the input or output PPTX")
    if args.verify_only:
        report = verify_pptx(args.input)
    else:
        if args.output is None:
            parser.error("output.pptx is required unless --verify-only is used")
        if args.mapping is None:
            parser.error("--mapping equations.json is required when converting")
        defaults = {"font": args.font, "font_size": args.font_size, "color": args.color}
        report = inject_equations(args.input, args.output, read_mapping(args.mapping), args.pandoc, defaults, args.require_all)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, etree.XMLSyntaxError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
