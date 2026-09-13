#!/usr/bin/env node
/**
 * Portable editable layout demonstration.
 * Run from the repository root: npm install && npm run demo:legacy
 * Optional: node examples/layout-demo/build.mjs --out /path/to/draft.pptx
 * Then run scripts/inject_equations.py to replace [[EQ_FUSION]] with OMML.
 * Public dependencies only: pptxgenjs and jszip. No private runtime is required.
 */
import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
let PptxGenJS;
let JSZip;
try {
  const mod = require('pptxgenjs');
  PptxGenJS = mod.default ?? mod;
  JSZip = require('jszip');
} catch (error) {
  console.error('Missing dependency. From the repository root run: npm install');
  throw error;
}

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
let output = path.resolve(here, '../../build/layout-demo.draft.pptx');
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out' && args[i + 1]) output = path.resolve(args[++i]);
  else if (args[i] === '--help' || args[i] === '-h') {
    console.log('Usage: node examples/layout-demo/build.mjs [--out FILE.pptx]');
    process.exit(0);
  } else throw new Error(`Unknown or incomplete argument: ${args[i]}`);
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'PaperLoom';
pptx.subject = 'Three editable layout components. All DemoNav methods and numbers are fictional.';
pptx.title = 'PaperLoom — 版式组件示例';
pptx.company = 'PaperLoom';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'FangSong_GB2312',
  bodyFontFace: 'FangSong_GB2312',
  lang: 'zh-CN',
};

const C = {
  navy: '142B4A', blue: '245CC0', orange: 'D57D31',
  text: '243850', muted: '627995', pale: 'F1F4F8',
  bluePale: 'EAF0FA', rule: 'D4DFED', white: 'FFFFFF',
};
const W = 13.333333, H = 7.5;
const ZH = 'FangSong_GB2312', EN = 'Times New Roman';

// Split by script, including in native table cells. ASCII uses Times New Roman.
// Split logical lines first: PptxGenJS 4.0.1 leaks breakLine=true from an
// embedded newline into the last script fragment, stranding following numbers.
function runs(value, options = {}) {
  const result = [];
  const lines = String(value).replace(/\r\n?/g, '\n').split('\n');
  lines.forEach((line, index) => {
    let buffer = '', previous = null;
    const first = result.length;
    const flush = () => {
      if (buffer) result.push({text: buffer, options: {...options, fontFace: previous, breakLine: false}});
      buffer = '';
    };
    for (const char of line) {
      const font = /[\p{Script=Han}\u3000-\u303f\uff00-\uffef]/u.test(char) ? ZH :
        (/\s/u.test(char) && previous ? previous : EN);
      if (previous && font !== previous) flush();
      buffer += char;
      previous = font;
    }
    flush();
    // An empty run preserves intentional leading, trailing and consecutive
    // blank lines without inserting visible placeholder characters.
    if (result.length === first) result.push({text: '', options: {...options, fontFace: EN, breakLine: false}});
    result[result.length - 1].options.breakLine = index < lines.length - 1 || options.breakLine === true;
  });
  return result;
}
function text(s, value, x, y, w, h, options = {}) {
  s.addText(runs(value), {
    x, y, w, h, fontFace: ZH, fontSize: 18, color: C.text,
    margin: 0, breakLine: false, valign: 'middle', paraSpaceAfterPt: 0,
    lineSpacingMultiple: 1.0, ...options,
  });
}
function rect(s, x, y, w, h, fill, border = fill, width = 0) {
  s.addShape(pptx.ShapeType.rect, {x, y, w, h,
    fill: {color: fill}, line: {color: border, width}});
}
function line(s, x1, y1, x2, y2, color = C.rule, width = 1, arrow = false) {
  const opts = {x: Math.min(x1, x2), y: Math.min(y1, y2),
    w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {color, width, ...(arrow ? {endArrowType: 'triangle'} : {})}};
  s.addShape(pptx.ShapeType.line, opts);
}
function page(title, n) {
  const s = pptx.addSlide();
  s.background = {color: C.white};
  rect(s, 0, 0, W, 0.78, C.navy);
  rect(s, 0.40, 0.19, 0.045, 0.41, C.orange);
  text(s, title, 0.58, 0.16, 10.8, 0.48,
    {fontSize: 27, color: C.white});
  text(s, 'DemoNav', 11.55, 0.24, 1.35, 0.30,
    {fontSize: 16, color: 'CDD8E8', align: 'right'});
  // Footer contains only decorative lines and a page number. Sources stay in notes.
  line(s, 0.42, 7.17, 12.91, 7.17, C.rule, 0.6);
  line(s, 0.42, 7.17, 0.98, 7.17, C.navy, 1.6);
  line(s, 0.98, 7.17, 1.20, 7.17, C.orange, 1.6);
  text(s, `${String(n).padStart(2, '0')} / 03`, 11.95, 7.25, 0.96, 0.18,
    {fontSize: 10, color: C.muted, align: 'right'});
  return s;
}
function caption(s, value, x, y, w) {
  rect(s, x, y + 0.045, 0.035, 0.23, C.orange);
  text(s, value, x + 0.13, y, w - 0.13, 0.34,
    {fontSize: 19.5, color: C.navy, bold: true});
}
function note(s, value) {
  s.addNotes(`【示例声明】这是 PaperLoom 的版式演示，不是完整论文汇报。DemoNav、Method A–F 与所有实验数值均为虚构，不能作为科研证据。\n${value}`);
}

// 1. Literature review: six readable blocks and a distinct research position.
{
  const s = page('文献综述  研究路线与方法定位', 1);
  text(s, '虚构案例：每块只保留方法、机制、局限，供真实论文内容替换',
    0.42, 0.88, 12.49, 0.30, {fontSize: 15.5, color: C.muted});
  const cards = [
    ['A', '直接策略学习', 'Method A', '图像与目标描述输入\n端到端预测动作', '依赖轨迹监督\n跨场景表现需要验证'],
    ['B', '全局语义地图', 'Method B', '累计区域与地标信息\n支持粗粒度路径规划', '区域选择较清楚\n相似对象仍难区分'],
    ['C', '局部对象推理', 'Method C', '对象属性与空间关系\n支持近距离目标匹配', '对象关系较细致\n长程方向感不足'],
    ['D', '语言推理控制', 'Method D', '将观测转成文字证据\n按目标分阶段决策', '描述错误会传播\n中间状态须可核验'],
    ['E', '跨视角视觉融合', 'Method E', '组合多视角观测\n补充被遮挡的线索', '观测信息较充分\n时序一致性需要维护'],
    ['F', '图结构记忆', 'Method F', '保存对象及其连接\n持续更新关系与状态', '结构支持追溯\n错误合并影响后续判断'],
  ];
  for (let i = 0; i < cards.length; i++) {
    const x = 0.42 + (i % 3) * 4.245, y = 1.28 + Math.floor(i / 3) * 2.04;
    const [id, title, method, mechanism, limit] = cards[i];
    rect(s, x, y, 4.0, 1.85, C.pale);
    line(s, x, y, x + 4.0, y, C.rule, 1.5);
    rect(s, x + 0.14, y + 0.13, 0.28, 0.29, C.blue);
    text(s, id, x + 0.14, y + 0.13, 0.28, 0.29,
      {fontSize: 19, bold: true, color: C.white, align: 'center'});
    text(s, title, x + 0.54, y + 0.11, 3.27, 0.32,
      {fontSize: 20.2, color: C.navy});
    text(s, method, x + 0.14, y + 0.49, 3.73, 0.25,
      {fontSize: 18.5, color: C.blue, bold: true});
    text(s, mechanism, x + 0.14, y + 0.81, 3.73, 0.49,
      {fontSize: 17});
    rect(s, x + 0.14, y + 1.36, 3.72, 0.38, C.white);
    rect(s, x + 0.14, y + 1.36, 0.025, 0.38, C.orange);
    text(s, limit.replace('\n', '，'), x + 0.24, y + 1.37, 3.53, 0.35,
      {fontSize: 14.3, color: C.muted});
  }
  text(s, 'DemoNav 的示例定位', 0.42, 5.48, 3.5, 0.38,
    {fontSize: 21, color: C.navy, bold: true});
  text(s, '全局选区域，局部辨对象，阶段策略连接两个尺度',
    3.6, 5.52, 9.3, 0.30, {fontSize: 18, color: C.muted});
  rect(s, 0.42, 5.97, 12.49, 0.86, C.bluePale);
  const positions = [0.58, 4.91, 9.18];
  [['全局地图', '区域、方位与覆盖状态'], ['局部对象图', '对象属性、关系与置信度'], ['阶段策略', '探索、匹配与停止条件']].forEach((pair, i) => {
    text(s, pair[0], positions[i], 6.06, 3.3, 0.28,
      {fontSize: 20, color: C.navy, bold: true});
    text(s, pair[1], positions[i], 6.44, 3.3, 0.27,
      {fontSize: 17.1});
  });
  for (const x of [4.48, 8.75]) text(s, '+', x, 6.20, 0.32, 0.30,
    {fontSize: 24, color: C.orange, align: 'center'});
  note(s, '【设计用途】综述以六个分块代替大型对照表。真实使用时，每块填入来源明确的代表方法、机制和比较边界；来源与页码写入备注。该页所有 Method A–F 均为虚构。');
}

// 2. Technical mechanism: native editable shapes, connectors and one math slot.
{
  const s = page('技术机制  双尺度记忆与决策', 2);
  text(s, '虚构机制示例：用输入、状态更新和输出解释一个核心模块',
    0.42, 0.88, 12.49, 0.30, {fontSize: 15.5, color: C.muted});
  caption(s, '输入', 0.42, 1.28, 2.12);
  caption(s, '状态更新', 3.00, 1.28, 3.45);
  caption(s, '匹配与决策', 6.95, 1.28, 2.65);
  caption(s, '输出', 10.18, 1.28, 2.73);

  const node = (x, y, w, h, title, body, fill = C.pale) => {
    rect(s, x, y, w, h, fill);
    text(s, title, x + 0.15, y + 0.13, w - 0.30, 0.33,
      {fontSize: 20.5, color: C.navy, bold: true});
    line(s, x + 0.15, y + 0.60, x + w - 0.15, y + 0.60, C.rule, 0.75);
    text(s, body, x + 0.15, y + 0.76, w - 0.30, h - 0.90,
      {fontSize: 17.5, valign: 'top'});
  };
  node(0.42, 1.88, 2.10, 1.47, '语言目标', '对象类别\n属性与关系');
  node(0.42, 3.64, 2.10, 1.47, '视觉观测', '当前图像\n位置与朝向');
  node(3.00, 1.88, 3.43, 1.47, '全局地图', '定位候选区域\n更新覆盖与访问状态', C.bluePale);
  node(3.00, 3.64, 3.43, 1.47, '局部对象图', '关联对象与属性\n更新空间关系与置信度', C.bluePale);
  node(6.95, 1.88, 2.70, 3.23, '目标匹配', '全局分数\n区域是否相关\n\n局部分数\n对象是否吻合\n\n融合后选择目标');
  node(10.18, 1.88, 2.73, 3.23, '动作与终止', '相关区域未覆盖\n继续探索\n\n候选对象不确定\n补充观察\n\n证据满足条件\n输出停止动作');
  // Native arrow connectors encode the mechanism and remain individually editable.
  line(s, 2.52, 2.615, 3.00, 2.615, C.blue, 1.5, true);
  line(s, 2.52, 4.375, 3.00, 4.375, C.blue, 1.5, true);
  line(s, 6.43, 2.615, 6.95, 2.615, C.blue, 1.5, true);
  line(s, 6.43, 4.375, 6.95, 4.375, C.blue, 1.5, true);
  line(s, 9.65, 3.495, 10.18, 3.495, C.blue, 1.5, true);
  line(s, 4.715, 3.35, 4.715, 3.64, C.orange, 1.4, true);
  rect(s, 0.42, 5.50, 12.49, 1.35, C.bluePale);
  text(s, '融合评分', 0.60, 5.66, 2.10, 0.36,
    {fontSize: 21, color: C.navy, bold: true});
  // This entire paragraph is the sole equation placeholder; do not split its box.
  text(s, '[[EQ_FUSION]]', 3.04, 5.62, 9.55, 0.52,
    {fontSize: 25, color: C.navy, align: 'center'});
  text(s, '权重控制两个尺度的贡献。真实汇报只展示解释核心机制所必需的公式。',
    0.61, 6.35, 12.08, 0.31, {fontSize: 18, color: C.text});
  note(s, '【设计用途】技术页使用原生 PowerPoint 形状及连接线，保留输入、更新、匹配和输出。融合公式仅用于展示原生 OMML 转换，并非 GeoNav 或任何真实论文的技术主张。');
}

// 3. Experiment: native table + native chart with embedded editable data workbook.
{
  const s = page('实验结果  主结果与消融证据', 3);
  text(s, '以下方法、指标和数值全部为虚构数据，仅用于演示可编辑表格与图表',
    0.42, 0.88, 12.49, 0.30, {fontSize: 15.5, color: C.muted});
  caption(s, '主结果：同时保留效果与成本', 0.42, 1.28, 6.04);
  caption(s, '消融结果：解释模块贡献', 6.82, 1.28, 6.08);
  const rows = [
    ['方法', 'SR (%)', 'SPL (%)', 'Time (s)'],
    ['Baseline A', '32.0', '25.8', '8.4'],
    ['Baseline B', '38.5', '30.7', '10.1'],
    ['Global only', '41.2', '32.4', '9.3'],
    ['Local only', '43.6', '34.1', '10.7'],
    ['DemoNav', '50.8', '40.9', '11.2'],
  ];
  const tableRows = rows.map((row, ri) => row.map((value, ci) => ({
    text: runs(value, {bold: ri === 0 || ri === rows.length - 1}),
    options: {fill: {color: ri === 0 ? C.navy : ri === rows.length - 1 ? C.bluePale : ri % 2 ? C.white : C.pale},
      color: ri === 0 ? C.white : ri === rows.length - 1 ? C.blue : C.text,
      align: ci === 0 ? 'left' : 'center',
      margin: [0.09, 0.10, 0.09, 0.12],
    },
  })));
  s.addTable(tableRows, {
    x: 0.42, y: 1.88, w: 6.04, h: 3.12,
    colW: [2.38, 1.20, 1.24, 1.22], rowH: 0.52,
    fontFace: EN, fontSize: 18.5,
    border: {color: C.rule, pt: 0.5},
    color: C.text, valign: 'middle', autoPage: false,
    paraSpaceAfterPt: 0,
  });
  text(s, 'SR：成功率   SPL：按路径长度加权的成功率',
    0.43, 5.14, 6.02, 0.33, {fontSize: 16, color: C.muted});
  s.addChart(pptx.ChartType.bar, [{name: 'SR (%)',
    labels: ['Base', '+ Global', '+ Local', 'Full'], values: [32.0, 41.2, 43.6, 50.8]}], {
    x: 6.82, y: 1.83, w: 6.08, h: 3.62,
    catAxisLabelFontFace: EN, catAxisLabelFontSize: 15,
    catAxisLabelColor: C.text, catAxisLineColor: C.rule,
    valAxisLabelFontFace: EN, valAxisLabelFontSize: 13,
    valAxisLabelColor: C.muted, valAxisLineColor: C.rule,
    valAxisMinVal: 0, valAxisMaxVal: 60, valAxisMajorUnit: 20,
    valAxisLabelFormatCode: '0',
    valGridLine: {color: C.rule, width: 0.6},
    catAxisTitle: '', valAxisTitle: '',
    showLegend: false, showTitle: false, showValue: true,
    dataLabelPosition: 'outEnd', dataLabelFontFace: EN,
    dataLabelFontSize: 17, dataLabelColor: C.navy,
    dataLabelFormatCode: '0.0',
    chartColors: [C.blue],
    showBorder: false,
    chartArea: {fill: {color: C.white}, border: {color: C.white, pt: 0}},
    plotArea: {fill: {color: C.white}, border: {color: C.white, pt: 0}},
    showCatName: false, showCatNameLegend: false,
    showSerName: false,
    barDir: 'col', catAxisLabelsPos: 'low',
    gapSize: 90,
  });
  rect(s, 0.42, 5.74, 6.04, 1.10, C.bluePale);
  rect(s, 6.82, 5.74, 6.08, 1.10, C.pale);
  text(s, '+12.3 个百分点', 0.61, 5.86, 3.1, 0.37,
    {fontSize: 24, color: C.blue, bold: true});
  text(s, 'DemoNav 相对 Baseline B 的 SR 差值',
    0.61, 6.38, 5.67, 0.28, {fontSize: 17});
  text(s, '+7.2 个百分点', 7.01, 5.86, 3.1, 0.37,
    {fontSize: 24, color: C.orange, bold: true});
  text(s, '完整配置相对 Local only 的 SR 差值',
    7.01, 6.38, 5.69, 0.28, {fontSize: 17});
  note(s, '【虚构数据】主表：Baseline A (32.0,25.8,8.4)，Baseline B (38.5,30.7,10.1)，Global only (41.2,32.4,9.3)，Local only (43.6,34.1,10.7)，DemoNav (50.8,40.9,11.2)。列为 SR (%), SPL (%), Time (s)。差值以百分点计算，50.8−38.5=12.3，50.8−43.6=7.2。此页不能被引用为真实实验结果。\n【真实论文替换】记录数据页码、表号、指标定义、评测划分和可比条件。');
}

await mkdir(path.dirname(output), {recursive: true});
await pptx.writeFile({fileName: output});

// Correct narrowly scoped PptxGenJS 4.0.1 output issues in this demo:
// 1. extra ContentTypes entries for nonexistent default slide masters;
// 2. table shape IDs that can repeat an earlier text shape's ID.
// 3. notesMasterIdLst appearing after sldIdLst instead of before it;
// 4. identical paragraph properties repeated between mixed-script runs.
// 5. a shared notes/slide-master theme that fails desktop PowerPoint loading
//    after correcting presentation child order; use a dedicated notes theme.
// This deck has no animation/shape-ID links, so a fresh duplicate ID is safe.
// This is not a general purpose repair tool for arbitrary user presentations.
const zip = await JSZip.loadAsync(await readFile(output));
const names = new Set(Object.keys(zip.files));
const types = await zip.file('[Content_Types].xml').async('string');
let repairedTypes = types.replace(/<Override\b[^>]*\/>/g, (entry) => {
  const part = /\bPartName="([^"]+)"/.exec(entry)?.[1];
  if (part?.startsWith('/ppt/slideMasters/') && !names.has(part.slice(1))) return '';
  return entry;
});
// Verified with desktop PowerPoint 16.0: retaining the correct notesMasterIdLst
// order and giving notesMaster its own theme fixes 0x80070570, without removing
// notes placeholders or altering the slides, fonts or native equation content.
const notesRelPath = 'ppt/notesMasters/_rels/notesMaster1.xml.rels';
const notesRels = await zip.file(notesRelPath).async('string');
if ((notesRels.match(/Target="\.\.\/theme\/theme1\.xml"/g) ?? []).length !== 1 ||
    names.has('ppt/theme/notesTheme.xml')) {
  throw new Error('Unexpected notes-theme structure; stop instead of rewriting arbitrary themes.');
}
zip.file('ppt/theme/notesTheme.xml', await zip.file('ppt/theme/theme1.xml').async('nodebuffer'));
zip.file(notesRelPath, notesRels.replace('Target="../theme/theme1.xml"', 'Target="../theme/notesTheme.xml"'));
repairedTypes = repairedTypes.replace('</Types>',
  '<Override PartName="/ppt/theme/notesTheme.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/></Types>');
zip.file('[Content_Types].xml', repairedTypes);
let presentationXml = await zip.file('ppt/presentation.xml').async('string');
const noteLists = Array.from(presentationXml.matchAll(/<p:notesMasterIdLst\b[^>]*>[\s\S]*?<\/p:notesMasterIdLst>/g));
if (noteLists.length !== 1 || !presentationXml.includes('</p:sldMasterIdLst>')) {
  throw new Error('Unexpected master structure: stop instead of guessing presentation child order.');
}
presentationXml = presentationXml.replace(noteLists[0][0], '')
  .replace('</p:sldMasterIdLst>', `</p:sldMasterIdLst>${noteLists[0][0]}`);
zip.file('ppt/presentation.xml', presentationXml);
for (const name of names) {
  if (!/^ppt\/slides\/slide\d+\.xml$/.test(name)) continue;
  let xml = await zip.file(name).async('string');
  let next = Math.max(...Array.from(xml.matchAll(/<p:cNvPr\b[^>]*\bid="(\d+)"/g),
    (match) => Number(match[1])), 0) + 1;
  const seen = new Set();
  xml = xml.replace(/<p:cNvPr\b[^>]*\bid="(\d+)"[^>]*>/g, (entry, id) => {
    if (!seen.has(id)) { seen.add(id); return entry; }
    return entry.replace(/\bid="\d+"/, `id="${next++}"`);
  });
  // runs() changes only fontFace; paragraph formatting belongs to text(), so
  // all duplicated pPr should be byte-identical. Refuse differing properties.
  // Preserve the first property element and put it before all paragraph runs.
  xml = xml.replace(/(<a:p(?:\s[^>]*)?>)([\s\S]*?)(<\/a:p>)/g,
    (paragraph, open, content, close) => {
      const pattern = /<a:pPr\b[^>]*(?:\/>|>[\s\S]*?<\/a:pPr>)/g;
      const properties = Array.from(content.matchAll(pattern), (match) => match[0]);
      if (!properties.length) return paragraph;
      if (properties.some((value) => value !== properties[0])) {
        throw new Error(`Conflicting paragraph properties in ${name}; fix the builder configuration.`);
      }
      return open + properties[0] + content.replace(pattern, '') + close;
    });
  zip.file(name, xml);
}
await writeFile(output, await zip.generateAsync({type: 'nodebuffer', compression: 'DEFLATE'}));
console.log(`Created draft: ${output}`);
console.log('Next: convert [[EQ_FUSION]] with scripts/inject_equations.py; the draft is not the final deliverable.');
