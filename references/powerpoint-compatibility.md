# PowerPoint 兼容性、字体与原生公式

交付物是 `.pptx`。WPS、LibreOffice 或渲染器可以打开，不能单独证明桌面 Microsoft PowerPoint 能打开；生成预览图也不能证明原生公式仍然可编辑。保留生成前的输入文件，所有修复输出到新文件。

## GB2312 字符集表示

`ppt/presentation.xml` 的 `p:font/@charset` 以及 DrawingML 字体字符集属性使用 `SByteValue`，范围为 `-128..127`。简体中文 GB2312 的字节值 134 在 XML 中应写为 **-122**；写成 `charset="134"` 不符合该字段类型。字符集合法性与桌面软件兼容性分别检查，不能从单项结构检查推断整个文件已通过 PowerPoint 验证。

注意两个位置的类型不同：

| 位置 | 类型 | GB2312 的写法 |
| --- | --- | --- |
| `p:font/@charset`、DrawingML 字体的 `charset` XML 属性 | 有符号字节 | `-122` |
| EOT 字体数据里的 `Charset` | 无符号 `BYTE` | `134` |

不要全局搜索替换二进制字体中的 `134`。`embed_fonts.py` 分别处理这两种表示。

规范依据：[Microsoft 字体字符集属性定义](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.textfonttype.characterset?view=openxml-3.0.1)、[EOT 文件结构](https://www.w3.org/submissions/EOT/)。

## 字体处理

中文设为 `FangSong_GB2312`（仿宋 GB2312），英文、数字设为 `Times New Roman`。在同一文本段中按中文与西文拆分字体运行；仅设文本框的默认字体无法保证混排全部正确。字体文件的真实 family name 应从字体元数据读取，不能把其他字体重命名冒充。

`embed_fonts.py` 默认读取根目录 `fonts/` 中以下五个原始文件：

- `仿宋_GB2312.ttf`
- `TIMES.TTF`
- `TIMESBD.TTF`
- `TIMESI.TTF`
- `TIMESBI.TTF`

```bash
python scripts/embed_fonts.py build/equations.pptx build/embedded.pptx
```

也可显式重复传入 `--font path/to/font.ttf`。脚本使用完整 TrueType 数据生成 EOT，不做子集化。它检查 `fsType`，拒绝限制嵌入、仅预览打印、仅位图等不适合本流程的输入。**嵌入权限不等于允许把字体文件公开上传到 GitHub。** 发布规则见 `fonts/README.md`。

同一字体家族在 XML 中必须按 `font → regular → bold → italic → boldItalic` 排序，不能按传入文件的顺序直接追加。脚本会排序；若目标字体的同一槽位已嵌入，则明确报错，不覆盖原文件。所有幻灯片 XML、幻灯片关系和媒体数据保持逐字节不变。

## 原生公式转换

只保留解释方法所必需的少量公式。长推导放演讲者备注或讲稿。公式必须是原生 Office Math 对象；LaTeX 原码、公式图片和形似公式的普通文本均不能替代。

1. 在需要公式的文本框中创建独立段落，整段只放占位符，例如 `[[EQ_1]]`。不要把占位符夹在一句话中。
2. 写明公式映射 JSON，不能依赖某个环境里的默认文件：

   ```json
   {
     "[[EQ_1]]": {
       "latex": "P=\\frac{x}{1+x}",
       "font_size": 20,
       "color": "183B66"
     }
   }
   ```

3. 确认本机 `pandoc` 在 PATH 中，或用 `--pandoc` 指定可执行文件。转换并保存到新文件：

   ```bash
   python scripts/inject_equations.py build/source.pptx build/equations.pptx --mapping equations.json --require-all --report build/equations-report.json
   ```

4. 做公式结构计数和占位符检查：

   ```bash
   python scripts/inject_equations.py build/equations.pptx --verify-only
   python scripts/validate_pptx.py build/equations.pptx --expected-math 1
   ```

转换路线为 `LaTeX → Pandoc TeXMath → OMML → DrawingML a14:m`。公式文字默认请求 Times New Roman；数学结构和特殊字形的实际渲染可能受 PowerPoint 的数学字体回退机制影响，必须看预览并在可用时用目标 PowerPoint 检查。不要为了截图效果把公式栅格化。

包装结构：`a:p / a14:m / m:oMathPara / m:oMath`；内联模式可省去 `m:oMathPara`。公式内使用 DrawingML 的 `a:rPr`，清理 Pandoc 生成的 `w:rPr`。声明正确的 `a14`、`m`、`mc` 命名空间，并在继承范围内声明 `mc:Ignorable="a14"`。同一个段落保留原位置、尺寸、边距和对齐；转换不自动保证文本框足够高。

依据：[Microsoft TextMath (`a14:m`)](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.office2010.drawing.textmath)、[Pandoc 用户手册](https://pandoc.org/MANUAL.html)。目标为支持该原生数学扩展的 PowerPoint 2010 及以上版本；其他客户端可能有不同的显示或另存行为。

## 交付检查

### PptxGenJS 示例的备注主题

本包在 PowerPoint 16.0 实测中发现：仅将 PptxGenJS 4.0.1 的 `notesMasterIdLst` 调到规范顺序，而备注母版与幻灯片母版仍共用 `theme1.xml` 时，两份示例无法打开。为备注母版复制相同内容的独立主题、更新其关系与 Content Type 后，文件可以打开，备注仍在。

两个示例生成器使用独立备注主题和规范顺序，并保留备注、公式及字体。验证器将共享主题报告为兼容风险提示，不将其一概判为 XSD 错误。其他生成器或文件须按实际关系和目标应用验证，不能盲目替换所有主题。规范顺序也可见 [Microsoft 的主题应用示例](https://learn.microsoft.com/en-us/office/open-xml/presentation/how-to-apply-a-theme-to-a-presentation)。

### 检查命令

PptxGenJS 混排文本应先按逻辑行切分，再按字体分 run，并显式设置每个 run 的 `breakLine`。若一个 run 内含换行后再接另一字体，4.0.1 可能把后续变量或数字另起段落。两个示例的 `runs()` 已处理该情况，回归测试直接检查文本框和原生表格中的实际段落及字体。

```bash
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report build/validation.json
python scripts/audit_slide_quality.py final.pptx --report work/slide-quality.json
python scripts/render_preview.py final.pptx --output work/preview
```

渲染命令的依赖与 PDF 回退见 [渲染指南](rendering.md)。`validate_pptx.py` 不依赖内部运行时。它检查：

- ZIP 可读性、CRC、重复部件名和 XML 可解析性。
- 关系 ID、引用目标存在性、相对与包内绝对 Target、Content Types 覆盖。
- 幻灯片计数和形状 ID 重复。
- `presentation.xml` 已知核心子元素顺序；`notesMasterIdLst` 必须在 `sldIdLst` 之前。
- DrawingML `a:p` 中的 `a:pPr` 最多一个，且必须位于文本运行之前，作为首个子元素。
- 字体 `charset` 的有符号范围、嵌入字体槽位顺序。
- `a14:m` 包装、OMML 表达式计数、扩展命名空间和未转换的公式占位符。

局部修改时可额外比较旧文件，检查非目标页的 XML 和关系部件没有变化：

```bash
python scripts/validate_pptx.py revised.pptx --compare previous.pptx --allow-changed-slides 2
```

`--allow-changed-slides` 接收包内 `slideN.xml` 的 N。普通生成文件中它与页序通常一致，手工重排的文件可能不同；先核对 `presentation.xml` 的页序与关系映射。报告会列出所有变动部件。此选项不声称共享主题、共享媒体或备注不会影响其他页；若改动这些部件，要单独核对视觉影响。

**这些检查不是全 XSD 验证，也不是桌面 Office 打开验证。** 检查通过后仍需逐页看预览，确认无裁切、重叠、字体替换、图像失真；有桌面 Microsoft PowerPoint 时，再测试打开、保存和公式编辑。无法运行时，要在交付说明中如实交代，不写“已在 PowerPoint 实测通过”。用户报告“WPS 可开、Office 不可开”时，优先检查 XML 合法性、关系和扩展，不让用户反复重装软件，也不把 WPS 另存作为唯一解决方案。

## 回归测试

```bash
python -m unittest discover -s tests -v
```

Office 辅助脚本测试包括：演示文稿备注母版列表顺序、段落属性重复或后置、非法 `charset=134` 必须失败、乱序字体输入必须生成合法顺序、EOT 字节仍为 134、包内绝对 Target、LaTeX 分式变为原生公式、非目标页改动检测，以及拒绝覆盖源文件。没有字体文件或 Pandoc 时，相应测试以明确原因跳过，不把跳过报告成通过。

Office 兼容性回归检查 `layout-demo` 的 3 页 / 1 个原生公式；`evidence-demo` 为 3 页 / 0 公式，无需为了凑数量添加公式。可用环境变量 `PAPER_DECK_REAL_PPTX` 指向 GeoNav 的 8 页 / 3 公式文件，以运行该特定回归。其他论文按实际页数与公式数调用验证器；渲染检查和桌面软件检查需另行执行。
