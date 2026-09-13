<div align="center">

# 🧵 PaperLoom · 论文织图

### 研究論文から、図表で伝わる PowerPoint へ

**内容を網羅 · 複数の区画で説明 · PPTX**

![Version](https://img.shields.io/badge/version-1.2.0-4455AA?style=flat-square)
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

<a id="quick-start"></a>

## 🚀 クイックスタート

### 🌐 Web にアップロード

**paper-loom-v1.2.0-full.zip** と**論文 PDF**をアップロードし、次のように伝えます。

> ZIP 内の skill の要件に従って、この論文の PPT を作成してください。

操作はこれだけです。既定の設定、作成手順、各スライドの確認、ファイルの納品は SKILL.md に定義されています。README の閲覧、長いプロンプト、設定ファイル、別の参考資料は不要です。

### 💻 ローカルクライアント

必要なフォントが同梱されたこのリポジトリをクローンまたはダウンロードし、[フォントガイド](../../fonts/README.md)を確認してから、リポジトリのルートで実行します。

```bash
python scripts/install_skill.py
```

既定では現在のユーザーの `~/.agents/skills/paper-loom/` にコピーします。同名のディレクトリがある場合は停止し、既存のバージョンを上書きしません。スキルのインポートに対応したクライアントでは、このフォルダー全体を直接選択することもできます。[クライアントの詳細ガイド](../../references/client-mode.md)

インストール後、クライアントで PaperLoom を選択するか、次のように入力します。

> $paper-loom を使って、この論文の研究室発表用 PPT を作成してください。

<a id="features"></a>

## ✨ 主な特徴

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 図で伝える構成</strong><br>図表で入力、状態、変換、フィードバックを説明し、関連する根拠を同じページに配置。実験では編集可能な比較表と不利な結果も残します。</td>
    <td width="50%" valign="top"><strong>🖼️ 論文の原図を直接抽出</strong><br>PDF に埋め込まれた画像を直接抽出。ページのスクリーンショットや、その切り抜きを抽出画像として扱いません。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 編集できるネイティブ数式</strong><br>必要な数式を LaTeX から PowerPoint ネイティブの Office Math に変換し、引き続き編集できます。</td>
    <td width="50%" valign="top"><strong>🔤 検証可能なフォント</strong><br>中国語は仿宋 GB2312、英語と数字は Times New Roman。フォントファイル、属性、ハッシュ値を検証できます。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 根拠は発表者ノートに</strong><br>詳しい出典と説明はノートに記載。指標、単位、比較条件、重要な限界は図表の近くに残し、フッターは簡潔にします。</td>
    <td width="50%" valign="top"><strong>🛠️ 指定箇所を丁寧に修正</strong><br>修正箇所を限定し、確認済みの他のページ、フォント、数式、互換性設定を保護します。</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ プレビュー

この 3 枚のサンプルには、明示的に**架空のデータ**を使用しています。実際の論文の結論を表すものではありません。

<table>
  <tr>
    <th width="33%">仕組みと状態</th>
    <th width="33%">学習と推論</th>
    <th width="33%">結果と適用限界</th>
  </tr>
  <tr>
    <td><a href="../../examples/evidence-demo/preview-01.png"><img src="../../examples/evidence-demo/preview-01.png" alt="仕組みと状態" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-02.png"><img src="../../examples/evidence-demo/preview-02.png" alt="学習と推論" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-03.png"><img src="../../examples/evidence-demo/preview-03.png" alt="結果と適用限界" width="100%"></a></td>
  </tr>
</table>

[編集可能な PPTX](../../examples/evidence-demo/evidence-demo.pptx) · [ソースコードと再現手順](../../examples/evidence-demo/README.md)

[同梱の AeroDuo 6 ページ参考 PDF](../../examples/aeroduo-reference/AeroDuo_组会汇报_合并精简6页版.pdf)

<a id="workflow"></a>

## 🧭 根拠に応じたスライド構成

**既定のスライド数上限を設けず、論文を十分に説明**します。各ページに A/B/C などの区画を設け、関連する複数の論点を扱います。実質的な 3〜5 区画を出発点とし、仕組みや実験を読みやすく収められなければ本文スライドを追加します。重要な内容を省略したりノートだけに移したりしません。ユーザーが明示した枚数を優先します。

制作前に[ページ設計](../../references/design.md)、[参考レイアウトと反例](../../references/reference-patterns.md)、[品質チェック](../../references/quality-gates.md)を読みます。[ページ設計テンプレート](../../examples/slide-plan.template.json)に沿って作業ディレクトリに `slide-plan.json` を保存し、構成案の承認待ちを標準動作にせず制作を続けます。

同じ仕組みの全体像、状態変化、フィードバック条件をまとめ、同条件の主結果とアブレーション、不利な結果を並べます。比較条件は図表の近くに、詳しい説明と出典はノートに残します。[根拠を集約したデモ](../../examples/evidence-demo/README.md)を参考に、全ページの読みやすさを確認してください。

[区画の計画と内容の網羅性](../../references/panel-planning.md)

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
python scripts/audit_slide_plan.py work/slide-plan.json --report work/plan-audit.json
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

コマンドのスライド数と数式数は例です。対象の論文に合わせて指定してください。 フォントの埋め込みは各フォントのライセンスに従います。既定では `fonts/` の 5 ファイルを埋め込みます。

検証ツールはパッケージ構造、リレーションシップ、フォントの文字セット、ネイティブ数式、プレースホルダーなどを検査しますが、**完全な OOXML Schema 検証でも、デスクトップ版 Microsoft PowerPoint での実動作確認でもありません**。レンダリング後も、内容とレイアウトを 1 枚ずつ確認する必要があります。[互換性ガイド](../../references/powerpoint-compatibility.md)

</details>

スクリプトの動作テストと回帰テストを実行します。

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 配布用アーカイブの作成</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.2.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.2.0-full.zip
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
| `WEB_START.md` | 任意のアップロード・実行環境の説明。実行入口は SKILL.md |
| `README.md` | プロジェクトの英語版 README |
| `docs/i18n/` | その他の言語の README |
| `fonts/` | 同梱フォントファイル、使用方法、検証用一覧 |
| `scripts/` | 画像抽出、ネイティブ数式、フォント埋め込み、PPTX 検査、インストール、パッケージ作成用ツール |
| `references/` | ページデザイン、画像抽出、互換性、クライアント利用のガイド |
| `examples/aeroduo-reference/` | 6 ページの視覚参考と閲覧ガイド |
| `examples/evidence-demo/` | 実行可能な 3 枚のネイティブレイアウトデモとビルド用ソース |
| `examples/geonav/workflow.md` | 論文の根拠整理とスライド計画の例 |
| `examples/evidence.template.json` | 出典、実験条件・評価基準、検証記録のテンプレート |
| `references/panel-planning.md` | 区画の計画と内容の網羅性 |
| `examples/slide-plan.template.json` | 各ページの問い、根拠、図表、統合判断のテンプレート |
| `tests/` | スクリプトの動作テストと回帰テスト |

</details>

<a id="license"></a>

## 📄 ライセンス

プロジェクト独自のコードとドキュメントは [MIT](../../LICENSE) ライセンスで公開しています。第三者のフォント、論文、依存関係については [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md) を参照してください。
