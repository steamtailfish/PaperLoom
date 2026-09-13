<div align="center">

# 🧵 PaperLoom · 论文织图

### 研究論文から、図表で伝わる PowerPoint へ

**8〜10 枚のスライド · 論文の原図 · ネイティブ数式 · 編集可能な PPTX**

![Version](https://img.shields.io/badge/version-1.0.0-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 クイックスタート](#quick-start) · [🖼️ プレビュー](#preview) · [🧭 スライド構成](#workflow) · [🛠️ 開発](#development) · [📚 ガイド](#guides)

</div>

<p align="center">
  <a href="../../README.md"><img src="https://img.shields.io/badge/English-0A66C2?style=for-the-badge" alt="English"></a>
  <a href="README_ZH.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-E53935?style=for-the-badge" alt="简体中文"></a>
  <a href="README_ZH_HK.md"><img src="https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87%EF%BC%88%E9%A6%99%E6%B8%AF%EF%BC%89-EF6C00?style=for-the-badge" alt="繁體中文（香港）"></a>
  <a href="README_JA.md"><img src="https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-8E24AA?style=for-the-badge" alt="日本語"></a>
  <a href="README_FR.md"><img src="https://img.shields.io/badge/Fran%C3%A7ais-1565C0?style=for-the-badge" alt="Français"></a>
  <a href="README_RU.md"><img src="https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-3949AB?style=for-the-badge" alt="Русский"></a>
  <a href="README_DE.md"><img src="https://img.shields.io/badge/Deutsch-2E7D32?style=for-the-badge" alt="Deutsch"></a>
</p>

---

PaperLoom は、研究論文をコンパクトで図表を中心とした、編集可能な **PowerPoint `.pptx`** に仕上げるスキルです。ローカルのクライアントにインストールする方法と、プロジェクトの ZIP と論文をコード実行機能のある Web 版 GPT にアップロードする方法に対応しています。

<a id="features"></a>

## ✨ 主な特徴

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 図で伝える構成</strong><br>関連研究はブロック分け、手法はフロー図や仕組みの図で説明。実験には、値を正確に読み取れるネイティブの表とグラフを使用します。</td>
    <td width="50%" valign="top"><strong>🖼️ 論文の原図を直接抽出</strong><br>PDF に埋め込まれた画像を直接抽出。ページのスクリーンショットや、その切り抜きを抽出画像として扱いません。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 編集できるネイティブ数式</strong><br>必要な数式を LaTeX から PowerPoint ネイティブの Office Math に変換し、引き続き編集できます。</td>
    <td width="50%" valign="top"><strong>🔤 検証可能なフォント</strong><br>中国語は仿宋 GB2312、英語と数字は Times New Roman。フォントファイル、属性、ハッシュ値を検証できます。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 根拠は発表者ノートに</strong><br>出典と詳細な根拠をノートに記載。ページ下部には控えめな装飾とページ番号だけを残します。</td>
    <td width="50%" valign="top"><strong>🛠️ 指定箇所を丁寧に修正</strong><br>修正箇所を限定し、確認済みの他のページ、フォント、数式、互換性設定を保護します。</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ プレビュー

この 3 枚のサンプルには、明示的に**架空のデータ**を使用しています。実際の論文の結論を表すものではありません。

<table>
  <tr>
    <th width="33%">関連研究</th>
    <th width="33%">手法と数式</th>
    <th width="33%">実験</th>
  </tr>
  <tr>
    <td><a href="../../examples/layout-demo/preview-01.png"><img src="../../examples/layout-demo/preview-01.png" alt="関連研究" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-02.png"><img src="../../examples/layout-demo/preview-02.png" alt="手法と数式" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-03.png"><img src="../../examples/layout-demo/preview-03.png" alt="実験" width="100%"></a></td>
  </tr>
</table>

[編集可能な PPTX](../../examples/layout-demo/layout-demo.pptx) · [ソースコードと再現手順](../../examples/layout-demo/README.md)

<a id="quick-start"></a>

## 🚀 クイックスタート

### 💻 ローカルクライアント

必要なフォントが同梱されたこのリポジトリをクローンまたはダウンロードし、[フォントガイド](../../fonts/README.md)を確認してから、リポジトリのルートで実行します。

```bash
python scripts/install_skill.py
```

既定では現在のユーザーの `~/.agents/skills/paper-loom/` にコピーします。同名のディレクトリがある場合は停止し、既存のバージョンを上書きしません。スキルのインポートに対応したクライアントでは、このフォルダー全体を直接選択することもできます。[クライアントの詳細ガイド](../../references/client-mode.md)

インストール後、クライアントで PaperLoom を選択するか、次のように入力します。

```text
$paper-loom を使って、この論文を研究室ミーティング用の PowerPoint にしてください。
スキルの構成、フォント、画像抽出、ネイティブ数式の要件に従い、.pptx を直接納品してくださ
い。
```

### 🌐 Web にアップロード

**必要なフォントを含むプロジェクトディレクトリ全体を ZIP に圧縮**し、論文 PDF と一緒にアップロードして、次のメッセージを送信します。

```text
アップロードした PaperLoom を展開し、まず SKILL.md を読んでから、その要件に従ってこの論
文の研究室ミーティング用 PowerPoint を作成してください。標準構成は課題 1 枚、関連研究 1
枚、手法 3〜5 枚、実験 2 枚、まとめ 1 枚です。関連研究はブロック分けし、図表を優先して、
パッケージ内の仿宋 GB2312 と Times New Roman を使用してください。論文の図は直接抽出し、
重要な数式は PowerPoint のネイティブ数式に変換してください。根拠はノートに記載し、出典を
フッターの小さな文字で載せないでください。.pptx を実際に生成し、検査してください。
```

> [!NOTE]
> Web 版 GPT には、ZIP の展開、コードの実行、ダウンロード可能なファイルの生成機能が必要です。アップロードだけでこれらのツールが追加されたり、スキルが永続的にインストールされたりするわけではありません。詳しい手順は [WEB_START.md](../../WEB_START.md) を参照してください。

<a id="workflow"></a>

## 🧭 標準のスライド構成

標準構成は **8〜10 枚**です。

| パート | 枚数 |
|---|---|
| 既存の課題 | 1 |
| 関連研究 | 1 |
| 手法 | 3〜5 |
| 実験 | 2 |
| まとめ | 1 |

<details>
<summary><b>ワークフローの背景</b></summary>

このスキルは、GeoNav の研究室ミーティング用発表資料を何度も作成・修正した経験から生まれました。内容の圧縮とストーリーの調整、フォントとネイティブ数式への対応、Office 形式の修復、出典フッターの削除、大きな関連研究一覧表を 6 つの研究アプローチに分ける変更など、実際に検証した作業方法を再利用可能な手順とスクリプトにまとめています。

1. **研究室ミーティングの目的とビジュアル基準を決める**：実際の PPTX、コンパクトで情報密度の高い構成、図表の優先、指定フォント、ネイティブ数式。
2. **論文を読み、根拠の索引を作る**：結論、図表、実験条件・評価基準、失敗例、判断の限界を対応付ける。
3. **先にストーリーを組み、次にページを配置する**：既存の課題から関連研究、手法、実験、まとめへ進み、手法のページ数は実際の内容量に応じて配分する。
4. **元の素材と編集可能なオブジェクトを処理する**：画像を直接抽出し、表とグラフをネイティブ化し、LaTeX を Office Math に変換し、フォントを run 単位で設定する。
5. **内容、レイアウト、互換性を確認する**：各ページをレンダリングしてデータを照合し、GB2312 の不適合な `charset=134` を `-122` に修正する。
6. **フィードバックに応じて部分的に修正する**：出典フッターを削除してノートを残し、関連研究の表をブロック分けに変更する。他のページや形式の修正が元に戻らないようにする。

全工程は [GeoNav の振り返り](../../examples/geonav/workflow.md)をご覧ください。

</details>

<a id="development"></a>

## 🛠️ 開発と検証

Python 3.10+ と Node.js 20+ を使用します。スキルのルートディレクトリで実行してください。

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

ネイティブ数式への変換には、別途 `pandoc` コマンドが必要です。[Pandoc 公式ドキュメント](https://pandoc.org/installing.html)に従ってインストールしてください。必要なフォントは `fonts/` に同梱されています。使用方法は[フォントガイド](../../fonts/README.md)を参照してください。現在の環境に専用の PowerPoint ツールがある場合は、無理にツールを変更する必要はありません。

<details>
<summary><b>🖼️ 論文の画像を抽出</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

出力には元の画像リソースと manifest が含まれます。`--pages 1,3-5` に対応しています。埋め込みオブジェクト 1 個が図の一部分でしかない場合もあるため、Figure として意味の通った完全な図になっているか照合する必要があります。ベクターのみの図や文字が重ねられた図を、自動的にスクリーンショットで代用してはいけません。[画像抽出ガイド](../../references/figure-extraction.md)

</details>

<details>
<summary><b>🧮 数式、フォント、検証</b></summary>

ネイティブ PPTX 内で、必要な数式ごとに `[[EQ_FUSION]]` などの独立した段落を用意し、マッピングファイルに対応する LaTeX を記録します。

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

スライド `8` 枚、数式 `3` 個は今回の GeoNav のサンプル要件です。別の論文では実際の必要に応じて調整してください。必要な数式がない論文に、数合わせのために数式を追加する必要はありません。フォントの埋め込みは、そのフォント自体のライセンスに従う必要があります。既定では `fonts/` の 5 個のファイルを埋め込みます。

検証ツールはパッケージ構造、リレーションシップ、フォントの文字セット、ネイティブ数式、プレースホルダーなどを検査しますが、**完全な OOXML Schema 検証でも、デスクトップ版 Microsoft PowerPoint での実動作確認でもありません**。レンダリング後も、内容とレイアウトを 1 枚ずつ確認する必要があります。[互換性ガイド](../../references/powerpoint-compatibility.md)

</details>

スクリプトの動作テストと回帰テストを実行します。

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 配布用アーカイブの作成</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.0.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.0.0-full.zip
```

完全版アーカイブにはリポジトリに同梱されたフォントが含まれ、パッケージ作成ツールがファイルの不足を確認します。`--variant github` は、独立したフォントファイルを含まないソースコードアーカイブを作成します。

</details>

<a id="guides"></a>

## 📚 ガイドとリポジトリ

- [クライアントの詳細ガイド](../../references/client-mode.md)
- [Web 版の実行手順](../../WEB_START.md)
- [画像抽出ガイド](../../references/figure-extraction.md)
- [PowerPoint 互換性ガイド](../../references/powerpoint-compatibility.md)

<details>
<summary><b>リポジトリの構成</b></summary>

| パス | 内容 |
|---|---|
| `SKILL.md` | AI が読む、中心となるワークフローと品質要件 |
| `WEB_START.md` | Web 版向けのコピー用プロンプトと実行手順 |
| `README.md` | プロジェクトの英語版 README |
| `docs/i18n/` | その他の言語の README |
| `fonts/` | 同梱フォントファイル、使用方法、検証用一覧 |
| `scripts/` | 画像抽出、ネイティブ数式、フォント埋め込み、PPTX 検査、インストール、パッケージ作成用ツール |
| `references/` | ページデザイン、画像抽出、互換性、クライアント利用のガイド |
| `examples/layout-demo/` | 実行可能な 3 枚のネイティブレイアウトデモとビルド用ソース |
| `examples/geonav/workflow.md` | 今回の制作フロー、最終的な 8 枚の構成、主な修正点 |
| `examples/evidence.template.json` | 出典、実験条件・評価基準、検証記録のテンプレート |
| `tests/` | スクリプトの動作テストと回帰テスト |

</details>

<a id="license"></a>

## 📄 ライセンス

プロジェクト独自のコードとドキュメントは [MIT](../../LICENSE) ライセンスで公開しています。第三者のフォント、論文、依存関係については [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md) を参照してください。
