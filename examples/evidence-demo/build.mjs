#!/usr/bin/env node
/**
 * Three native, editable evidence compositions. All methods and data are fictional.
 * Public dependencies only: pptxgenjs 4.0.1 and jszip. No private runtime required.
 * node examples/evidence-demo/build.mjs [--out FILE.pptx]
 */
import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
let PptxGenJS, JSZip;
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
let output = path.resolve(here, '../../build/evidence-demo.draft.pptx');
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out' && args[i + 1]) output = path.resolve(args[++i]);
  else if (args[i] === '--help' || args[i] === '-h') {
    console.log('Usage: node examples/evidence-demo/build.mjs [--out FILE.pptx]');
    process.exit(0);
  } else throw new Error(`Unknown or incomplete argument: ${args[i]}`);
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'PaperLoom';
pptx.company = 'PaperLoom';
pptx.title = 'PaperLoom — 紧凑证据组织示例';
pptx.subject = 'Three editable research evidence compositions. DemoNav and all data are fictional.';
pptx.lang = 'zh-CN';
const ZH = 'FangSong_GB2312', EN = 'Times New Roman';
pptx.theme = {headFontFace: ZH, bodyFontFace: ZH, lang: 'zh-CN'};
const C = {
  navy: '153556', blue: '245F9F', orange: 'B66624', text: '263D50',
  muted: '5E7181', rule: 'CCD6DE', white: 'FFFFFF',
  pale: 'F1F5F8', bluePale: 'EAF2F8', orangePale: 'FAF1E7',
};
const W = 13.333333;

// Script-aware runs apply equally to shape text and native table cells.
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
  s.addText(runs(value), {x, y, w, h, fontFace: ZH, fontSize: 18,
    color: C.text, margin: 0, breakLine: false, valign: 'middle',
    paraSpaceAfterPt: 0, lineSpacingMultiple: 1.0, ...options});
}
function rect(s, x, y, w, h, fill = C.white, border = C.rule, width = 0.8) {
  s.addShape(pptx.ShapeType.rect, {x, y, w, h,
    fill: {color: fill}, line: {color: border, width}});
}
function line(s, x1, y1, x2, y2, color = C.rule, width = 1, arrow = false, dash = false) {
  s.addShape(pptx.ShapeType.line, {
    x: Math.min(x1, x2), y: Math.min(y1, y2),
    w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {color, width, ...(arrow ? {endArrowType: 'triangle'} : {}),
      ...(dash ? {dashType: 'dash'} : {})},
  });
}
function node(s, title, body, x, y, w, h, fill = C.white) {
  rect(s, x, y, w, h, fill);
  text(s, title, x + 0.10, y + 0.09, w - 0.20, 0.29,
    {fontSize: 18.3, bold: true, color: C.navy, align: 'center'});
  text(s, body, x + 0.10, y + 0.43, w - 0.20, h - 0.49,
    {fontSize: 17, align: 'center'});
}
function section(s, title, x, y, w) {
  text(s, title, x, y, w, 0.34, {fontSize: 21.5, color: C.navy, bold: true});
  line(s, x, y + 0.45, x + w, y + 0.45, C.rule, 0.8);
}
function page(title, n) {
  const s = pptx.addSlide();
  s.background = {color: C.white};
  text(s, title, 0.43, 0.27, 12.47, 0.52, {fontSize: 29, color: C.navy, bold: true});
  line(s, 0.43, 0.87, 12.90, 0.87, C.navy, 1.5);
  text(s, '虚构教学案例：DemoNav 的机制、协议与数值均为示例',
    0.44, 0.96, 12.45, 0.28, {fontSize: 15, color: C.muted});
  line(s, 0.43, 7.12, 12.90, 7.12, C.rule, 0.7);
  text(s, `${n} / 3`, 12.14, 7.23, 0.75, 0.17,
    {fontSize: 10.5, color: C.muted, align: 'right'});
  return s;
}
function note(s, value) {
  s.addNotes('【虚构案例声明】DemoNav、比较方法、机制参数、训练协议、数据集与所有实验数值均由 PaperLoom 为版式演示虚构，不能作为论文证据。\n' + value);
}
function table(s, rows, x, y, widths, rowH, highlight = []) {
  s.addTable(rows.map((row, ri) => row.map((value, ci) => ({
    text: runs(value, {bold: ri === 0 || highlight.includes(ri)}),
    options: {
      fill: {color: ri === 0 ? C.navy : highlight.includes(ri) ? C.bluePale : C.white},
      color: ri === 0 ? C.white : C.text,
      align: ci === 0 ? 'left' : 'center',
      margin: [0.045, 0.075, 0.045, 0.09],
    },
  }))), {x, y, w: widths.reduce((a, b) => a + b, 0), h: rows.length * rowH,
    colW: widths, rowH, fontFace: EN, fontSize: 17.5,
    border: {color: C.rule, pt: 0.6}, valign: 'middle',
    autoPage: false, paraSpaceAfterPt: 0});
}

// 1. A narrow overview connects two expanded mechanisms with concrete states.
{
  const s = page('双尺度记忆：区域选择与对象核验', 1);
  const xs = [0.44, 2.89, 5.35, 7.81, 10.40];
  const widths = [1.98, 1.98, 1.98, 2.12, 2.49];
  [
    ['输入', '图像 + 目标'],
    ['区域记忆', '候选区域 r_t'],
    ['对象记忆', '对象与关系 G_t'],
    ['置信门控', '融合分 s ≥ 0.80'],
    ['动作输出', '探索 / 观察 / 停止'],
  ].forEach(([title, body], i) => {
    node(s, title, body, xs[i], 1.47, widths[i], 0.96,
      i === 1 || i === 2 ? C.bluePale : C.white);
    if (i < 4) line(s, xs[i] + widths[i] + 0.035, 1.95, xs[i + 1] - 0.035, 1.95, C.blue, 1.6, true);
  });
  section(s, 'A  区域记忆：观测后更新候选顺序', 0.44, 2.73, 6.02);
  section(s, 'B  对象记忆：属性与关系共同核验', 6.87, 2.73, 6.02);
  text(s, '更新前', 0.45, 3.43, 0.89, 0.3, {fontSize: 17, color: C.muted});
  const regionXs = [1.48, 3.16, 4.84];
  [['R1', '0.78  未访问'], ['R2', '0.52  未覆盖'], ['R3', '0.34  未覆盖']].forEach(([title, body], i) =>
    node(s, title, body, regionXs[i], 3.32, 1.60, 0.88, i === 0 ? C.bluePale : C.white));
  text(s, '新观测：R1 已查，无匹配对象', 1.48, 4.36, 4.96, 0.32,
    {fontSize: 18, color: C.orange});
  line(s, 2.28, 4.20, 2.28, 4.34, C.orange, 1.4, true);
  line(s, 2.28, 4.70, 2.28, 4.88, C.orange, 1.4, true);
  text(s, '更新后', 0.45, 5.03, 0.89, 0.3, {fontSize: 17, color: C.muted});
  [['R1', '0.18  已检查'], ['R2', '0.52  首选'], ['R3', '0.34  保留']].forEach(([title, body], i) =>
    node(s, title, body, regionXs[i], 4.90, 1.60, 0.88, i === 1 ? C.bluePale : C.white));
  text(s, '访问后降权，未覆盖候选保留；下一步选择 R2',
    0.45, 6.00, 6.0, 0.42, {fontSize: 18, color: C.navy});

  text(s, '目标 g：红椅，位于桌旁', 6.88, 3.31, 5.60, 0.3, {fontSize: 18});
  node(s, '椅子 o7', '红色置信 0.88', 7.02, 3.86, 1.84, 0.84, C.bluePale);
  node(s, '桌子 o2', '稳定检测 0.94', 10.49, 3.86, 1.86, 0.84);
  text(s, '旁边 0.91', 8.94, 3.86, 1.44, 0.27, {fontSize: 16.5, align: 'center', color: C.blue});
  line(s, 8.88, 4.29, 10.46, 4.29, C.blue, 1.5, true);
  table(s, [
    ['候选', '属性分', '关系分', '融合分'],
    ['o7', '0.88', '0.91', '0.90'],
    ['o9', '0.93', '0.30', '0.55'],
  ], 6.89, 4.99, [1.18, 1.52, 1.51, 1.24], 0.40, [1]);
  text(s, 's < 0.80 时补充观察，再更新对象关系',
    6.89, 6.31, 5.99, 0.33, {fontSize: 17.5, color: C.orange});
  line(s, 12.59, 6.13, 12.75, 6.13, C.orange, 1.25);
  line(s, 12.75, 6.13, 12.75, 3.59, C.orange, 1.25);
  line(s, 12.75, 3.59, 11.45, 3.59, C.orange, 1.25, true);
  text(s, '区域分数决定先去哪里，对象分数决定是否停止',
    0.45, 6.71, 12.42, 0.29, {fontSize: 18.5, color: C.navy, bold: true});
  note(s, '【机制】左侧展示访问前后区域排序变化，R1 的相关分由 0.78 降至 0.18，R2 成为首选。右侧展示 o7 与 o2 的关系边，以及两个候选对象的属性分、关系分和融合分。融合分采用 0.4×属性分+0.6×关系分并保留两位小数：o7 为 0.898≈0.90，o9 为 0.552≈0.55。停止门槛 0.80 仅为虚构参数。橙色回路代表分数不足后的再次观测。\n【版式用途】总览保持五个接口，下方分别展开状态更新与对象关系。真实论文使用时应替换为可追溯的中间状态、更新规则和阈值来源，不能沿用这些虚构数值。');
}

// 2. Aligned offline and online lanes expose supervision and deployment differences.
{
  const s = page('训练与部署：共享编码器与独立监督路径', 2);
  const cols = [2.09, 4.62, 7.16, 10.07];
  ['输入与状态', '共享表征', '预测与记忆', '监督或动作'].forEach((label, i) =>
    text(s, label, cols[i], 1.43, i === 3 ? 2.81 : 2.04, 0.31,
      {fontSize: 19.5, bold: true, color: C.navy, align: 'center'}));
  line(s, 0.44, 1.90, 12.89, 1.90, C.rule, 0.8);
  text(s, '离线\n训练', 0.47, 2.28, 1.29, 0.91,
    {fontSize: 23, color: C.blue, bold: true, align: 'center'});
  text(s, '有标注轨迹', 0.47, 3.31, 1.29, 0.26, {fontSize: 15, color: C.muted, align: 'center'});
  node(s, '轨迹样本', '图像 I_t\n目标 g', cols[0], 2.22, 2.04, 1.15);
  node(s, '编码器 E', '图像 + 目标\n联合特征 z', cols[1], 2.22, 2.04, 1.15, C.bluePale);
  node(s, '两个预测头', '区域预测 r\n对象预测 o', cols[2], 2.22, 2.17, 1.15, C.bluePale);
  node(s, '轨迹标注', '区域标签 r*\n对象标签 o*', cols[3], 2.22, 2.81, 1.15, C.orangePale);
  line(s, 4.16, 2.80, 4.56, 2.80, C.blue, 1.6, true);
  line(s, 6.70, 2.80, 7.10, 2.80, C.blue, 1.6, true);
  line(s, 10.02, 2.80, 9.39, 2.80, C.orange, 1.6, true);
  text(s, '监督', 9.43, 2.31, 0.56, 0.27, {fontSize: 15, color: C.orange, align: 'center'});
  line(s, 8.25, 3.41, 8.25, 3.80, C.orange, 1.4);
  line(s, 8.25, 3.80, 5.63, 3.80, C.orange, 1.4);
  line(s, 5.63, 3.80, 5.63, 3.42, C.orange, 1.4, true);
  text(s, '监督误差更新参数 θ', 6.12, 3.48, 2.08, 0.26,
    {fontSize: 16.5, color: C.orange, align: 'center'});
  line(s, 0.44, 4.12, 12.89, 4.12, C.rule, 0.8);
  text(s, '在线\n推理', 0.47, 4.69, 1.29, 0.91,
    {fontSize: 23, color: C.blue, bold: true, align: 'center'});
  text(s, '无标签输入', 0.47, 5.73, 1.29, 0.26, {fontSize: 15, color: C.muted, align: 'center'});
  node(s, '当前观测', '当前图像\n目标 + 旧记忆', cols[0], 4.66, 2.04, 1.19);
  node(s, '编码器 E', '固定训练参数\n每帧一次编码', cols[1], 4.66, 2.04, 1.19, C.bluePale);
  node(s, '记忆更新', '重排区域 r_t\n核验对象 G_t', cols[2], 4.66, 2.17, 1.19, C.bluePale);
  node(s, '门控动作', 's ≥ 0.80：停止\ns < 0.80：观察', cols[3], 4.66, 2.81, 1.19);
  line(s, 4.16, 5.25, 4.56, 5.25, C.blue, 1.6, true);
  line(s, 6.70, 5.25, 7.10, 5.25, C.blue, 1.6, true);
  line(s, 9.38, 5.25, 10.01, 5.25, C.blue, 1.6, true);
  line(s, 4.89, 3.42, 4.89, 4.60, C.muted, 1.0, true, true);
  text(s, '固化参数', 5.04, 4.24, 1.56, 0.24, {fontSize: 15.5, color: C.muted});
  line(s, 11.48, 5.89, 11.48, 6.37, C.blue, 1.4);
  line(s, 11.48, 6.37, 3.11, 6.37, C.blue, 1.4);
  line(s, 3.11, 6.37, 3.11, 5.90, C.blue, 1.4, true);
  text(s, '观察动作改变视角，新观测更新记忆', 4.43, 6.04, 6.47, 0.29,
    {fontSize: 18, color: C.blue, align: 'center'});
  text(s, '部署保留编码、记忆与门控；移除标注输入和参数更新',
    0.45, 6.72, 12.41, 0.29, {fontSize: 18.5, color: C.navy, bold: true});
  note(s, '【训练协议】示例从有区域/对象标签的轨迹学习共享编码器与两个预测头。蓝色边为数据流，橙色边为标注监督和参数更新，虚线为训练参数传递到部署。预测头同时接收联合特征，真实论文应补充具体监督目标及梯度是否回传编码器。\n【部署协议】部署冻结参数，移除标签与监督更新，仅使用当前观测、目标和旧记忆。图中示例着重呈现对象置信门控；没有找到候选对象时，完整示例沿用第 1 页的区域探索分支。0.80 阈值、编码次数与训练设计均为虚构，不对应真实论文。');
}

// 3. Matched-protocol results, ablations and adverse outcomes share one canvas.
{
  const s = page('同协议实验：收益、模块贡献与代价', 3);
  text(s, '比较条件：同划分、同输入、同单卡；每种子 100 回合，报告 3 个种子的均值',
    0.45, 1.41, 12.42, 0.30, {fontSize: 17.5, color: C.text});
  section(s, '主结果：完整模型同时增加效果与开销', 0.44, 1.94, 7.44);
  section(s, '消融：成功率与误停共同解释', 8.26, 1.94, 4.63);
  table(s, [
    ['方法', 'SR (%)', 'SPL (%)', '延迟(ms)', '内存(MB)'],
    ['Direct policy', '62.0', '48.6', '18.0', '210'],
    ['Region only', '67.5', '52.1', '21.4', '252'],
    ['Object only', '69.0', '54.7', '24.8', '290'],
    ['DemoNav', '75.0', '59.6', '29.3', '348'],
  ], 0.44, 2.56, [2.16, 1.22, 1.34, 1.38, 1.34], 0.46, [4]);
  table(s, [
    ['配置', 'SR (%)', '误停(%)'],
    ['完整模型', '75.0', '2.5'],
    ['去关系边', '71.2', '4.1'],
    ['去回访', '72.4', '3.9'],
    ['去置信门控', '76.1', '8.4'],
  ], 8.26, 2.56, [2.10, 1.24, 1.29], 0.46, [1]);
  text(s, 'SR：到达率↑；SPL：路径加权到达率↑',
    0.45, 4.99, 7.41, 0.28, {fontSize: 15.5, color: C.muted});
  text(s, '+6.0 pp SR', 0.45, 5.39, 2.63, 0.35,
    {fontSize: 23, color: C.blue, bold: true});
  text(s, '+4.5 ms 延迟', 3.99, 5.39, 3.85, 0.35,
    {fontSize: 23, color: C.orange, bold: true});
  text(s, '两项均相对 Object only；pp 表示百分点',
    0.45, 5.89, 7.4, 0.26, {fontSize: 16, color: C.muted});
  text(s, '误停率↓：停错回合 / 全部回合',
    8.27, 4.99, 4.59, 0.28, {fontSize: 15.5, color: C.muted});
  text(s, '去门控：到达率 +1.1 pp\n误停率 +5.9 pp',
    8.27, 5.39, 4.59, 0.70, {fontSize: 18.2, color: C.orange});
  line(s, 0.44, 6.27, 12.89, 6.27, C.rule, 0.8);
  text(s, '条件边界', 0.45, 6.42, 1.45, 0.32, {fontSize: 19.5, bold: true, color: C.navy});
  text(s, '静态室内；动态遮挡待验证\n端到端延迟，批量 1',
    1.98, 6.40, 5.59, 0.61, {fontSize: 17.3});
  text(s, '不利结果', 8.27, 6.42, 1.47, 0.32, {fontSize: 19.5, bold: true, color: C.orange});
  text(s, '低光：51% < 54%\n基线：Object only',
    9.82, 6.40, 3.07, 0.61, {fontSize: 17.3});
  note(s, '【虚构主表】列为方法、SR (%)、SPL (%)、端到端延迟 (ms)、峰值内存 (MB)。Direct policy: 62.0,48.6,18.0,210。Region only: 67.5,52.1,21.4,252。Object only: 69.0,54.7,24.8,290。DemoNav: 75.0,59.6,29.3,348。三随机种子均值，每种子一百回合，同划分、同输入、同单卡，批量1。这里只提供布局所需均值，没有方差，不能据此宣称统计显著。\n【虚构消融】完整模型 SR 75.0/误停2.5，去关系边71.2/4.1，去回访72.4/3.9，去置信门控76.1/8.4。误停率指停止时对象不符合目标的回合比例，以全部评估回合为分母。SR 定义为预算内进入目标邻域的回合比例，不要求停止判断正确，因此 SR 与误停率并非互补。所有配置使用相同训练和评估协议，只改变所列组件。\n【算术】75.0−69.0=6.0 pp；29.3−24.8=4.5 ms；76.1−75.0=1.1 pp；8.4−2.5=5.9 pp。低光子集数据 51.0% vs 54.0% 为独立虚构子集结果。\n【真实替换】必须记录原论文表号、页码、评估划分、硬件、指标定义、计时范围与不利结果，保留不确定性。');
}

await mkdir(path.dirname(output), {recursive: true});
await pptx.writeFile({fileName: output});

// Reuse the old demo's narrowly scoped repairs for PptxGenJS 4.0.1.
// This deck has no animations or shape-ID links. This is not a general PPTX fixer.
const zip = await JSZip.loadAsync(await readFile(output));
const names = new Set(Object.keys(zip.files));
const types = await zip.file('[Content_Types].xml').async('string');
let repairedTypes = types.replace(/<Override\b[^>]*\/>/g, (entry) => {
  const part = /\bPartName="([^"]+)"/.exec(entry)?.[1];
  if (part?.startsWith('/ppt/slideMasters/') && !names.has(part.slice(1))) return '';
  return entry;
});
// A dedicated notes theme is required for desktop PowerPoint compatibility in
// this PptxGenJS 4.0.1 demo. Moving notesMasterIdLst to its schema position while
// sharing theme1.xml with the slide master caused COM Open to fail (0x80070570).
// Copy the theme bytes; preserve every notes placeholder and speaker note.
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
console.log('Next: validate the PPTX, render all three slides, and inspect text fit and connectors.');
