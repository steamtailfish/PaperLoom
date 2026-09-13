# 紧凑证据组织示例

这三页展示如何在同一页内组织可核验的机制、状态和实验比较。**DemoNav、方法、协议、参数及全部数值均为虚构**，每页与演讲者备注均有声明，不能直接用于真实论文汇报。

| 页码 | 页面组织 | 原生可编辑内容 |
| --- | --- | --- |
| 1 | 五阶段总览，下方并列展开区域状态更新与对象关系核验 | 输入输出、区域前后状态、对象关系边、候选评分表、补充观察回路 |
| 2 | 对齐训练与推理泳道，区分数据流、监督边、参数传递和动作反馈 | 全部文字、节点、箭头和监督回路 |
| 3 | 同协议主表与消融表并列，同时保留代价、协议边界和不利结果 | 两张原生表格、比较差值、条件说明与低光子集反例 |

这是三个证据组织组件，不是完整汇报的默认页数。白底、深蓝标题、细分隔线只提供层次；页面主体用中间状态、带单位数值和明确关系回答问题。不要把这些内容替换成大小相同的概念卡片，也不要沿用虚构方法或数值。

[打开可编辑示例](evidence-demo.pptx)

![总览与机制](preview-01.png)

![训练与推理](preview-02.png)

![结果、消融与边界](preview-03.png)

## 本地复现

需要 Node.js 18+，使用仓库 `package.json` 指定的公开依赖：

```sh
npm install
npm run demo
python scripts/validate_pptx.py build/evidence-demo.draft.pptx --expected-slides 3 --expected-math 0
python scripts/audit_slide_quality.py build/evidence-demo.draft.pptx --report work/demo-quality.json
python scripts/embed_fonts.py build/evidence-demo.draft.pptx build/evidence-demo.pptx
python scripts/render_preview.py build/evidence-demo.pptx --output work/demo-preview
```

默认输出为仓库 `build/evidence-demo.draft.pptx`。指定新路径：

```sh
node examples/evidence-demo/build.mjs --out build/evidence-demo-review.pptx
```

脚本仅使用公开的 PptxGenJS 与 JSZip。导出后修复重复对象 ID、重复段落属性、备注母版顺序及悬空内容类型，并给备注母版保留独立主题。这些定向修复不代表完整 OOXML 校验。渲染命令需要 LibreOffice；已有 PDF 时直接用 PDF 输入，详见 [公开渲染指南](../../references/rendering.md)。

中文按 run 指定 `FangSong_GB2312`，英文、数字及符号按 run 指定 `Times New Roman`，包括表格单元格。查看与渲染环境应安装仓库指定字体。该示例没有公式占位符，不需要公式注入步骤。原生对象保持可编辑，没有使用整页图片或外部论文图。

发布成品前应渲染三页，检查文字、表格、回路箭头及字体。如果替换为真实论文，先建立来源映射，再同步改写页内内容和备注中的机制、条件、定义、算术与来源；尤其不要丢掉推理时移除的模块、失败条件与不利结果。

本包发布的三页示例已嵌入指定字体，使用 Microsoft PowerPoint 16.0 打开并导出预览，逐页检查后修正了混排换行与底部文字溢出。替换内容后仍需重新渲染；示例通过不代表其他论文自动达到同样质量。

内容规划参见 [多分区与完整性指南](../../references/panel-planning.md)。演示页数只用于展示组件；真实汇报按完整内容增加页面，每个分区可以展开多个有依据的要点。
