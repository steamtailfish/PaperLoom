# 字体资源

完整使用包包含以下用户提供的原始文件，字节未修改：

| 字体 | 文件 | 用途 |
|---|---|---|
| Times New Roman Regular | `TIMES.TTF` | 英文和数字 |
| Times New Roman Bold | `TIMESBD.TTF` | 英文加粗 |
| Times New Roman Italic | `TIMESI.TTF` | 英文斜体 |
| Times New Roman Bold Italic | `TIMESBI.TTF` | 英文粗斜体 |
| 仿宋 GB2312 | `仿宋_GB2312.ttf` | 中文，内部 family 为 `FangSong_GB2312` |

`manifest.json` 记录 SHA-256、字体 family、嵌入标志、原始版权和许可字段。原文件来源于本次用户上传的 Paper Prism 压缩包；该来源不自动授予本项目公开再分发字体的权利。

**字体不属于项目 MIT 许可。** Times New Roman 文件包含 Microsoft/Monotype 的使用和嵌入限制；仿宋文件保留 GreatWall Computer 的版权声明。字体的 `fsType` 是文档嵌入约束，不能当作公开发布独立 TTF 的授权。[Microsoft 字体再分发与文档嵌入说明](https://learn.microsoft.com/en-us/typography/fonts/font-faq)

因此 GitHub 源码发行包仅包含本 README 和 manifest，不包含独立 TTF；完整使用包按用户要求带入原始字体，供已有合法使用权的环境使用。需要公开发布带字体的包时，应先取得对应再分发授权。

使用 GitHub 源码包时，从自己获授权的 Windows/Office 安装或字体供应方取得字体，按上述文件名放入本目录。不要从不明网站自动下载字体。不同合法版本的 hash 可能不同，应核对 family、style 和许可，再更新自己的 manifest。

缺少仿宋 GB2312 时不能静默替换成仿宋、宋体或其他字体。复制文件不会自动注册到操作系统；预览时按渲染器的字体注册方式加载，PowerPoint 编辑环境按自身许可使用字体。
