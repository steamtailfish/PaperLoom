<div align="center">

# 🧵 PaperLoom · 论文织图

### Vom wissenschaftlichen Artikel zur klaren, visuellen Präsentation.

**Standardmäßig 6–8 Folien · Zusammenhängende Belege · Originalabbildungen · Native Formeln · Bearbeitbares PPTX**

![Version](https://img.shields.io/badge/version-1.1.2-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 Schnellstart](#quick-start) · [🖼️ Vorschau](#preview) · [🧭 Folienstruktur](#workflow) · [🛠️ Entwicklung](#development) · [📚 Anleitungen](#guides)

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

PaperLoom erstellt aus wissenschaftlichen Artikeln kompakte, bearbeitbare **PowerPoint-Präsentationen im Format `.pptx`**, bei denen Abbildungen und Diagramme im Vordergrund stehen. Installiere den Skill in einem kompatiblen Client oder lade das vollständige Projekt als ZIP zusammen mit dem Artikel in einen Web-GPT hoch, der Code ausführen kann.

<a id="quick-start"></a>

## 🚀 Schnellstart

### 🌐 Upload im Web

Lade **paper-loom-v1.1.2-full.zip** und die **Artikel-PDF** hoch und schreibe:

> Erstelle die PPT zu diesem Artikel gemäß dem Skill im ZIP.

Das ist alles. SKILL.md enthält Standardwerte, Erstellung, visuelle Prüfung und Dateiausgabe. Eine lange Eingabe, eine Konfigurationsdatei oder eine zusätzliche Referenzpräsentation ist nicht erforderlich.

### 💻 Lokaler Client

Klone dieses Repository mit den enthaltenen Schriftarten oder lade es herunter. Lies die [Schriftartenanleitung](../../fonts/README.md) und führe anschließend im Stammverzeichnis des Repositorys Folgendes aus:

```bash
python scripts/install_skill.py
```

Standardmäßig wird der Skill für den aktuellen Benutzer nach `~/.agents/skills/paper-loom/` kopiert. Ist das Verzeichnis bereits vorhanden, wird die Installation angehalten, ohne deine Version zu überschreiben. In einem Client, der den Import von Skills unterstützt, kannst du auch direkt diesen vollständigen Ordner auswählen. [Ausführliche Anleitung für Clients](../../references/client-mode.md)

Wähle nach der Installation PaperLoom im Client aus oder gib Folgendes ein:

> Erstelle mit $paper-loom eine Präsentation zu diesem Artikel.

<a id="features"></a>

## ✨ Funktionen

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 Visuell erklären</strong><br>Abbildungen erklären Eingaben, Zustände, Veränderungen und Rückkopplungen. Zusammengehörige Belege stehen auf derselben Folie; Experimente enthalten native Tabellen und ungünstige Ergebnisse.</td>
    <td width="50%" valign="top"><strong>🖼️ Originalabbildungen</strong><br>Direkte Extraktion der im PDF eingebetteten Bilder: keine Seitenaufnahmen oder zugeschnittenen Screenshots, die als extrahierte Bilder ausgegeben werden.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 Bearbeitbare Formeln</strong><br>Erforderliche Formeln werden aus LaTeX in das native Office-Math-Format von PowerPoint umgewandelt und bleiben bearbeitbar.</td>
    <td width="50%" valign="top"><strong>🔤 Überprüfbare Schriftarten</strong><br>FangSong GB2312 (仿宋 GB2312) für chinesischen Text, Times New Roman für englischen Text und Zahlen. Dateien, Eigenschaften und Hashwerte lassen sich überprüfen.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 Belege in den Notizen</strong><br>Ausführliche Quellen und Erklärungen stehen in den Notizen. Kennzahlen, Einheiten, Vergleichsbedingungen und wichtige Grenzen bleiben bei den Abbildungen und Tabellen; die Fußzeile bleibt schlicht.</td>
    <td width="50%" valign="top"><strong>🛠️ Gezielte Überarbeitungen</strong><br>Änderungen schützen bereits bestätigte andere Folien, Schriftarten, Formeln und Kompatibilitätseinstellungen.</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ Vorschau

Dieses Beispiel verwendet ausdrücklich gekennzeichnete **fiktive Daten**, die keine Ergebnisse eines realen Artikels darstellen.

<table>
  <tr>
    <th width="33%">Mechanismen und Zustände</th>
    <th width="33%">Training und Inferenz</th>
    <th width="33%">Ergebnisse und Grenzen</th>
  </tr>
  <tr>
    <td><a href="../../examples/evidence-demo/preview-01.png"><img src="../../examples/evidence-demo/preview-01.png" alt="Mechanismen und Zustände" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-02.png"><img src="../../examples/evidence-demo/preview-02.png" alt="Training und Inferenz" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-03.png"><img src="../../examples/evidence-demo/preview-03.png" alt="Ergebnisse und Grenzen" width="100%"></a></td>
  </tr>
</table>

[📥 Bearbeitbare PPTX-Präsentation](../../examples/evidence-demo/evidence-demo.pptx) · [📖 Quellcode und Befehle zur Reproduktion](../../examples/evidence-demo/README.md)

[Enthaltene AeroDuo-Referenz als sechsseitiges PDF](../../examples/aeroduo-reference/AeroDuo_组会汇报_合并精简6页版.pdf)

<a id="workflow"></a>

## 🧭 Folien nach Belegen gliedern

Standardmäßig sind **6–8 Folien** vorgesehen, bei komplexen Artikeln **8–10**. Die vom Nutzer gewünschte Anzahl und Vorlage haben Vorrang. Behandle Aufgabe und Forschungsposition, Mechanismen, Training und Ausführung, Experimente und Grenzen sowie die Zusammenfassung. Diese Inhalte benötigen nicht jeweils eine eigene Folie. Ein separater Forschungsüberblick und eine feste Anzahl an Methodenfolien sind nicht vorgeschrieben.

Lies vor der Erstellung die Regeln zu [Gestaltung](../../references/design.md), [Kompositionen und Gegenbeispielen](../../references/reference-patterns.md) und [Qualitätsprüfung](../../references/quality-gates.md). Erstelle `slide-plan.json` im Arbeitsverzeichnis anhand der [Planvorlage](../../examples/slide-plan.template.json) und fahre anschließend fort, ohne standardmäßig auf eine Freigabe des Plans zu warten.

Verbinde die Übersicht, Zwischenzustände und Rückkopplungsbedingungen eines Mechanismus. Stelle Hauptergebnisse unter demselben Protokoll, Ablationen und ungünstige Ergebnisse nebeneinander. Vergleichsbedingungen bleiben an den Abbildungen und Tabellen, ausführliche Erklärungen und Quellen in den Notizen. Nutze das [Beispiel zur kompakten Darstellung von Belegen](../../examples/evidence-demo/README.md) und prüfe die Lesbarkeit jeder Folie.

<a id="development"></a>

## 🛠️ Entwicklung und Validierung

Verwende Python 3.10+ und Node.js 20+. Führe im Stammverzeichnis des Repositorys Folgendes aus:

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

Für die Konvertierung in native Formeln wird zusätzlich `pandoc` benötigt; folge der [offiziellen Pandoc-Dokumentation](https://pandoc.org/installing.html). Die erforderlichen Schriftarten sind in `fonts/` enthalten; Hinweise zur Verwendung findest du in der [Schriftartenanleitung](../../fonts/README.md). Wenn in der Umgebung bereits ein spezielles PowerPoint-Werkzeug verfügbar ist, muss dieses nicht ersetzt werden.

<details>
<summary><b>🖼️ Bilder extrahieren</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

Die Ausgabe enthält die Originalressourcen und ein Manifest. Die Option `--pages 1,3-5` wird unterstützt. Ein eingebettetes Objekt kann nur einen Teil einer Abbildung enthalten; deshalb muss geprüft werden, ob die Abbildung inhaltlich vollständig ist. Rein vektorbasierte Abbildungen oder Abbildungen mit überlagertem Text dürfen nicht automatisch durch Screenshots ersetzt werden. [Anleitung zur Bildextraktion](../../references/figure-extraction.md)

</details>

<details>
<summary><b>🧮 Formeln, Schriftarten und Validierung</b></summary>

Lege im nativen PPTX für jede erforderliche Formel einen eigenen Absatz an, etwa `[[EQ_FUSION]]`. Die Zuordnungsdatei enthält den entsprechenden LaTeX-Ausdruck:

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

Die Folien- und Formelanzahlen in den Befehlen sind Beispiele und müssen zum Artikel passen. Das Einbetten von Schriftarten muss deren Lizenzen entsprechen; standardmäßig werden die fünf Dateien in `fonts/` eingebettet.

Der Validator prüft unter anderem Paketstruktur, Beziehungen, Schriftzeichensätze, native Formeln und Platzhalter. **Er ersetzt weder eine vollständige Prüfung gegen das OOXML-Schema noch einen tatsächlichen Test in der Desktopversion von Microsoft PowerPoint.** Nach dem Rendern müssen Inhalt und Layout weiterhin Folie für Folie geprüft werden. [Kompatibilitätsleitfaden](../../references/powerpoint-compatibility.md)

</details>

Führe die Tests aus:

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Distributionsarchive erstellen</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.1.2-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.2-full.zip
```

Das vollständige Archiv enthält die im Repository mitgelieferten Schriftarten; das Paketierungswerkzeug prüft deren Vollständigkeit. Mit `--variant github` wird ein Quellcodearchiv ohne separate Schriftdateien erstellt.

</details>

<a id="guides"></a>

## 📚 Anleitungen und Repository

- [💻 Ausführliche Anleitung für Clients](../../references/client-mode.md)
- [🌐 Einstieg in die Web-Nutzung](../../WEB_START.md)
- [🖼️ Anleitung zur Bildextraktion](../../references/figure-extraction.md)
- [🧩 Leitfaden zur PowerPoint-Kompatibilität](../../references/powerpoint-compatibility.md)

<details>
<summary><b>Repository-Übersicht</b></summary>

| Pfad | Inhalt |
|---|---|
| `SKILL.md` | Zentraler Arbeitsablauf und Qualitätsanforderungen zum Einlesen durch die KI |
| `WEB_START.md` | Optionale Hinweise zu Upload und Umgebung; Einstiegspunkt: SKILL.md |
| `README.md` | Projektbeschreibung auf Englisch |
| `docs/i18n/` | Übersetzungen der README |
| `fonts/` | Enthaltene Schriftdateien, Nutzungshinweise und Prüfmanifest |
| `scripts/` | Werkzeuge für Bildextraktion, native Formeln, Schrifteinbettung, PPTX-Prüfung, Installation und Paketierung |
| `references/` | Anleitungen zu Foliengestaltung, Bildextraktion, Kompatibilität und Nutzung im Client |
| `examples/aeroduo-reference/` | Sechsseitige visuelle Referenz und Leseanleitung |
| `examples/evidence-demo/` | Ausführbares Beispiel mit drei nativen Folienlayouts und Quellcode zur Erstellung |
| `examples/geonav/workflow.md` | Beispiel für Belegauswahl und Folienplanung |
| `examples/evidence.template.json` | Vorlage für Quellen, Versuchsbedingungen und Messdefinitionen sowie Prüfprotokolle |
| `examples/slide-plan.template.json` | Vorlage für Fragen, Belege, Abbildungen und Entscheidungen zum Zusammenführen von Folien |
| `tests/` | Tests des Skriptverhaltens und Regressionstests |

</details>

<a id="license"></a>

## 📄 Lizenz

Der vom Projekt selbst verfasste Code und die Dokumentation stehen unter der [MIT-Lizenz](../../LICENSE). Informationen zu Schriftarten Dritter, Artikeln und Abhängigkeiten stehen in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
