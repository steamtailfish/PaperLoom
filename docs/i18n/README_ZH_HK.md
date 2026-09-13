<div align="center">

# 🧵 PaperLoom · 论文织图

### 將科研論文，織成以圖表說故事的 PowerPoint

**預設 6–8 頁 · 緊湊證據 · 論文原圖 · 原生公式 · 可編輯 PPTX**

![Version](https://img.shields.io/badge/version-1.1.0-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 快速開始](#quick-start) · [🖼️ 預覽](#preview) · [🧭 投影片結構](#workflow) · [🛠️ 開發](#development) · [📚 指南](#guides)

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

PaperLoom 是一個將科研論文製作成精簡、以圖表為先、可編輯的 **PowerPoint `.pptx`** 的 skill。支援在本機客戶端安裝，亦可將專案 ZIP 與論文上載至具備程式碼執行功能的網頁版 GPT。

<a id="features"></a>

## ✨ 核心特點

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 以圖表說故事</strong><br>圖表直接解釋輸入、狀態、變換和回饋；相關證據同頁呈現，實驗保留原生對照表及不利結果。</td>
    <td width="50%" valign="top"><strong>🖼️ 直接擷取論文原圖</strong><br>直接擷取 PDF 的內嵌圖片，不擷取整頁畫面，也不以裁剪截圖冒充圖片擷取。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 可編輯的原生公式</strong><br>將必要公式由 LaTeX 轉換為 PowerPoint 原生 Office Math，可繼續編輯。</td>
    <td width="50%" valign="top"><strong>🔤 可核實的字型</strong><br>中文採用仿宋 GB2312，英文與數字採用 Times New Roman；字型檔案、屬性及雜湊值均可核實。</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 證據放在備忘稿</strong><br>詳細來源與長講解放備忘稿；指標、單位、比較條件與重要邊界留在圖表旁，頁尾保持簡約。</td>
    <td width="50%" valign="top"><strong>🛠️ 精準修改指定位置</strong><br>只修改指定位置，保護已確認的其他頁面、字型、公式及相容性設定。</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ 版面預覽

這三頁示例使用明確標示的**虛構數據**，並不代表真實論文的結論。

<table>
  <tr>
    <th width="33%">機制與狀態</th>
    <th width="33%">訓練與推理</th>
    <th width="33%">結果與邊界</th>
  </tr>
  <tr>
    <td><a href="../../examples/evidence-demo/preview-01.png"><img src="../../examples/evidence-demo/preview-01.png" alt="機制與狀態" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-02.png"><img src="../../examples/evidence-demo/preview-02.png" alt="訓練與推理" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-03.png"><img src="../../examples/evidence-demo/preview-03.png" alt="結果與邊界" width="100%"></a></td>
  </tr>
</table>

[可編輯 PPTX](../../examples/evidence-demo/evidence-demo.pptx) · [原始碼與重現步驟](../../examples/evidence-demo/README.md)

<a id="quick-start"></a>

## 🚀 快速開始

### 💻 本機客戶端

複製或下載本儲存庫（已附帶所需字型），閱讀[字型指南](../../fonts/README.md)，然後在儲存庫根目錄執行：

```bash
python scripts/install_skill.py
```

預設複製至目前用戶的 `~/.agents/skills/paper-loom/`，如目錄已存在便會停止，不會覆寫你的版本。亦可在支援匯入 skill 的客戶端中直接選取這個完整資料夾。[客戶端詳細指南](../../references/client-mode.md)

安裝後，在客戶端選取 PaperLoom，或輸入：

```text
使用 $paper-loom，將這篇論文製作成科研組會議 PowerPoint。
按照 skill 的結構、字型、圖片擷取及原生公式要求，直接交付 .pptx。
```

### 🌐 上載至網頁

優先使用發行版 **`paper-loom-v1.1.0-full.zip`**，與論文 PDF 一併上載。若由原始碼建立，請使用下方 `package_skill.py --variant full` 指令產生完整套件；它會排除建置產物與私有快取。然後傳送：

```text
請解壓縮我上載的 PaperLoom，閱讀 WEB_START.md，按照其中的完整流程製作這篇論文的
科研組會 PowerPoint。先讀 SKILL.md、references/design.md、references/reference-patterns.md
及 references/quality-gates.md，整理證據並保存 slide-plan.json，然後直接生成。
預設 6–8 頁，複雜內容可用 8–10 頁；不用為湊頁數另做綜述或公式頁。
讓同一頁的圖表解釋相關機制與證據，保留實驗條件、比較對象、單位和不利結果。
遵守套件的字型、原圖擷取及必要原生公式要求，詳細來源與長講解放備忘稿。
執行結構及品質檢查，逐頁渲染、查看和修正，最後交付可下載的 .pptx。
```

> [!NOTE]
> 網頁版 GPT 需要能夠解壓縮、執行程式碼及產生可下載的檔案；上載 ZIP 本身不會賦予這些工具，也不會永久安裝 skill。完整操作入口請參閱 [WEB_START.md](../../WEB_START.md)。

<a id="workflow"></a>

## 🧭 按證據安排投影片

預設 **6–8 頁**，複雜論文可用 **8–10 頁**；用戶指定的頁數與模板優先。任務與定位、核心機制、訓練與執行、實驗與邊界、總結都要覆蓋，但不要求各自獨佔一頁，也不強制獨立綜述或固定的技術頁數。

製作前必讀[頁面設計](../../references/design.md)、[參考版式與反例](../../references/reference-patterns.md)及[品質關卡](../../references/quality-gates.md)。先按[逐頁設計範本](../../examples/slide-plan.template.json)完成工作目錄的 `slide-plan.json`，然後繼續生成，不預設等待大綱批准。

同一機制的總覽、狀態與回饋條件可合頁；同口徑主結果、消融及不利結果可並列。比較條件留在圖表附近，長講解與詳細來源放備忘稿。以[緊湊證據示例](../../examples/evidence-demo/README.md)作視覺參考，逐頁檢查可讀性。

<details>
<summary><b>工作流程背後的經驗</b></summary>

以下是早期 GeoNav 個案的回顧，當時的固定頁數與六區塊綜述不是目前的預設要求。

這個 skill 源自一次 GeoNav 研究組會議匯報的多輪製作與修改：從精簡內容、調整敘事，到字型與原生公式、Office 格式修復，再到移除頁尾說明、將大型文獻綜述表格改成六個研究路線區塊。它將經過驗證的工作方式整理成可重用的說明與指令碼。

1. **確定研究組會議目標與視覺標準**：真正的 PPTX、精簡高密度、圖表優先、指定字型與原生公式。
2. **閱讀論文並建立證據索引**：將結論、圖表、實驗條件與評估標準、失敗案例及判斷界限逐一對應。
3. **先組織證據，再安排頁面**：以逐頁設計串連任務、機制、實驗和邊界；合併依賴同一圖表或機制的頁面，按可讀性決定是否拆頁。
4. **處理原始素材與可編輯物件**：直接擷取圖片，將表格與圖表轉為原生物件，LaTeX 轉為 Office Math，字型設定落實至每個 run。
5. **檢查內容、版面與相容性**：逐頁渲染、比對數據，將 GB2312 `charset=134` 的不合規寫法修正為 `-122`。
6. **按回饋作局部修改**：保留詳細來源備忘稿及必要的圖旁條件，保護其餘已確認頁面與格式修復。

完整過程請參閱 [GeoNav 製作回顧](../../examples/geonav/workflow.md)。

</details>

<a id="development"></a>

## 🛠️ 開發與驗證

使用 Python 3.10+、Node.js 20+。在 skill 根目錄執行：

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

原生公式轉換另需 `pandoc` 指令，請按照 [Pandoc 官方文件](https://pandoc.org/installing.html)安裝。所需字型已包含在 `fonts/` 中，使用說明請參閱[字型指南](../../fonts/README.md)；目前環境如已有專用 PowerPoint 工具，毋須強制轉用其他工具。

<details>
<summary><b>🖼️ 擷取論文圖片</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

輸出包括原始資源與 manifest。支援 `--pages 1,3-5`。一個內嵌物件可能只是圖的一部分，必須對照 Figure，確認圖意完整；純向量圖或疊有文字的圖，不可自動降級為截圖處理。[圖片擷取指南](../../references/figure-extraction.md)

</details>

<details>
<summary><b>🧮 公式、字型與驗證</b></summary>

在原生 PPTX 中，為每條必要公式預留一個獨立段落，例如 `[[EQ_FUSION]]`，並在對應表檔案中記錄相應的 LaTeX：

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

`8` 頁與 `3` 條公式是本次 GeoNav 的示例要求，新的論文應按實際需要調整。沒有必要公式的論文，毋須為了湊數而加入公式。字型內嵌必須符合字型本身的授權條款；預設內嵌 `fonts/` 的五個檔案。

驗證工具會檢查套件結構、關聯、字型字元集、原生公式及預留位置等，但**不等於完整的 OOXML Schema 驗證，更不等於在桌面版 Microsoft PowerPoint 中實測**。渲染後仍需逐頁檢查內容與版面。[相容性指南](../../references/powerpoint-compatibility.md)

</details>

執行指令碼行為測試與回歸測試：

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 建置發行封存檔</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.1.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.0-full.zip
```

完整封存檔包含儲存庫附帶的字型，封裝工具會檢查檔案是否齊全；`--variant github` 會產生不含獨立字型檔案的原始碼封存檔。

</details>

<a id="guides"></a>

## 📚 指南與儲存庫

- [客戶端詳細指南](../../references/client-mode.md)
- [網頁版執行入口](../../WEB_START.md)
- [圖片擷取指南](../../references/figure-extraction.md)
- [PowerPoint 相容性指南](../../references/powerpoint-compatibility.md)

<details>
<summary><b>儲存庫目錄</b></summary>

| 路徑 | 內容 |
|---|---|
| `SKILL.md` | 供 AI 閱讀的核心工作流程與品質要求 |
| `WEB_START.md` | 網頁版可複製的提示詞與執行入口 |
| `README.md` | 專案的英文版 README |
| `docs/i18n/` | 其他語言的 README |
| `fonts/` | 隨儲存庫提供的字型檔案、使用說明與核對清單 |
| `scripts/` | 圖片擷取、原生公式、字型內嵌、PPTX 檢查、安裝及封裝工具 |
| `references/` | 頁面設計、圖片擷取、相容性及客戶端使用指南 |
| `examples/evidence-demo/` | 可執行的三頁原生版面示範及建置原始碼 |
| `examples/geonav/workflow.md` | 本次製作流程、最終 8 頁結構及關鍵修正 |
| `examples/evidence.template.json` | 來源、實驗條件與評估標準、驗證紀錄範本 |
| `examples/slide-plan.template.json` | 逐頁問題、證據、視覺與合頁判斷範本 |
| `tests/` | 指令碼行為測試與回歸測試 |

</details>

<a id="license"></a>

## 📄 授權

專案的原創程式碼與文件按 [MIT](../../LICENSE) 發佈；第三方字型、論文與相依套件請參閱 [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md)。
