# 第三方资源说明

- **用户提供的字体**：Times New Roman 系列与仿宋 GB2312 的原始声明记录在 `fonts/manifest.json`。字体不按本项目 MIT 许可再授权。完整使用包保留原文件；公开源码包排除独立字体文件。
- **Paper Prism**：本流程的 PDF 原生资源提取理念参考了用户提供的 `paper-prism-master`。本项目提图脚本另行实现，不打包其代码或完整资源。原项目声明为 MIT，Copyright (c) 2026 Steamtailfish；这不覆盖其包内所有第三方资产。
- **GeoNav 论文**：复盘用于说明制作过程，不附论文全文与论文原图。论文及其图像版权属于原权利人。
- **示例**：`examples/layout-demo/` 使用项目自制的虚构数据、文字和原生图形，不表示真实论文实验。示例中声明使用的字体仍受各自许可约束。
- **运行依赖**：PyMuPDF、Pillow、lxml、fontTools、PyYAML、PptxGenJS 和 Pandoc 按各自许可使用。本包不打包这些程序的运行时或声称它们属于本项目 MIT 代码。
