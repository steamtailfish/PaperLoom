# 逐页渲染：公开工具回退

有现成演示文稿工具时，用它导出逐页预览或 PDF，然后实际查看图片。不要因为两个 XML 检查器通过，就跳过视觉审阅。

## 只有公开代码环境时

PPTX 需要 LibreOffice 的 `soffice`；PDF 渲染使用本包已有的 PyMuPDF 与 Pillow。先运行 `scripts/doctor.py`，按当前环境安装缺少的依赖，不假设私有工具存在。

```bash
# 保留最终 PPTX，另建质检预览目录
python scripts/render_preview.py final.pptx --output work/preview

# 若 soffice 不在 PATH 中，显式传入可执行文件
python scripts/render_preview.py final.pptx --output work/preview --soffice /path/to/soffice

# 如果现有工具已导出 PDF，可直接检查这个 PDF
python scripts/render_preview.py final.pdf --output work/preview
```

脚本拒绝覆盖已有输出目录。再次检查时使用新目录，例如 `work/preview-v2`。PPTX 路线使用隔离的临时 LibreOffice 配置转换，源 PPTX 不会被重新保存。PDF 只是放映效果的预览，不替代原生 PPTX，也不能用于提取论文图片。

输出中的 `contact-sheet.png` 用于全套节奏检查，`slide-01.png` 等单页图用于文字、图表、公式和连接线检查；`manifest.json` 记录来源与渲染结果。打开图片并观察后才能填写视觉检查记录。

## 字体与渲染差异

渲染器必须能找到 `fonts/` 中指定字体。字体存在于 ZIP 或声明在 XML 中，不等于操作系统已经发现它。使用环境支持的字体注册/安装方式；Linux 下可用 `fc-match FangSong_GB2312` 和 `fc-match "Times New Roman"` 查看实际命中字体。发现替代字体先修复字体可用性，再判断换行与溢出。

LibreOffice、专用渲染器和桌面 PowerPoint 可能有差异。尤其关注公式、中文换行和表格高度；只在实际执行了对应检查时声称该环境已验证。

没有 LibreOffice，但现有工具能导 PDF 时使用 PDF 路线；两条路线都不可用时，交付时注明“未完成逐页渲染检查”，不能把无告警包装成视觉验收。无需因此改用整页图片生成 PPTX。
