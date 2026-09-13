<div align="center">

# 🧵 PaperLoom · 论文织图

### Vom wissenschaftlichen Artikel zur klaren, visuellen Präsentation.

**8–10 Folien · Originalabbildungen · Native Formeln · Bearbeitbares PPTX**

![Version](https://img.shields.io/badge/version-1.0.0-4455AA?style=flat-square)
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

<a id="features"></a>

## ✨ Funktionen

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 Visuell erklären</strong><br>Forschungsüberblick in Blöcken, Ablauf- und Mechanismusdiagramme für die Methode sowie native Tabellen und Diagramme zum präzisen Ablesen von Versuchsergebnissen.</td>
    <td width="50%" valign="top"><strong>🖼️ Originalabbildungen</strong><br>Direkte Extraktion der im PDF eingebetteten Bilder: keine Seitenaufnahmen oder zugeschnittenen Screenshots, die als extrahierte Bilder ausgegeben werden.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 Bearbeitbare Formeln</strong><br>Erforderliche Formeln werden aus LaTeX in das native Office-Math-Format von PowerPoint umgewandelt und bleiben bearbeitbar.</td>
    <td width="50%" valign="top"><strong>🔤 Überprüfbare Schriftarten</strong><br>FangSong GB2312 (仿宋 GB2312) für chinesischen Text, Times New Roman für englischen Text und Zahlen. Dateien, Eigenschaften und Hashwerte lassen sich überprüfen.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 Belege in den Notizen</strong><br>Quellen und ausführliche Belege stehen in den Referentennotizen; am unteren Folienrand bleiben nur dezente Gestaltungselemente und die Foliennummer.</td>
    <td width="50%" valign="top"><strong>🛠️ Gezielte Überarbeitungen</strong><br>Änderungen schützen bereits bestätigte andere Folien, Schriftarten, Formeln und Kompatibilitätseinstellungen.</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ Vorschau

Dieses Beispiel verwendet ausdrücklich gekennzeichnete **fiktive Daten**, die keine Ergebnisse eines realen Artikels darstellen.

<table>
  <tr>
    <th width="33%">Forschungsüberblick</th>
    <th width="33%">Methode und Formel</th>
    <th width="33%">Experimente</th>
  </tr>
  <tr>
    <td><a href="../../examples/layout-demo/preview-01.png"><img src="../../examples/layout-demo/preview-01.png" alt="Forschungsüberblick in Blöcken" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-02.png"><img src="../../examples/layout-demo/preview-02.png" alt="Technischer Mechanismus und native Formel" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-03.png"><img src="../../examples/layout-demo/preview-03.png" alt="Experimenttabellen und Diagramme" width="100%"></a></td>
  </tr>
</table>

[📥 Bearbeitbare PPTX-Präsentation](../../examples/layout-demo/layout-demo.pptx) · [📖 Quellcode und Befehle zur Reproduktion](../../examples/layout-demo/README.md)

<a id="quick-start"></a>

## 🚀 Schnellstart

### 💻 Lokaler Client

Klone dieses Repository mit den enthaltenen Schriftarten oder lade es herunter. Lies die [Schriftartenanleitung](../../fonts/README.md) und führe anschließend im Stammverzeichnis des Repositorys Folgendes aus:

```bash
python scripts/install_skill.py
```

Standardmäßig wird der Skill für den aktuellen Benutzer nach `~/.agents/skills/paper-loom/` kopiert. Ist das Verzeichnis bereits vorhanden, wird die Installation angehalten, ohne deine Version zu überschreiben. In einem Client, der den Import von Skills unterstützt, kannst du auch direkt diesen vollständigen Ordner auswählen. [Ausführliche Anleitung für Clients](../../references/client-mode.md)

Wähle nach der Installation PaperLoom im Client aus oder gib Folgendes ein:

```text
Verwende $paper-loom, um aus diesem Artikel eine PowerPoint-Präsentation für eine
Forschungsgruppenbesprechung zu erstellen.
Befolge die Vorgaben des Skills zu Struktur, Schriftarten, Bildextraktion und nativen
Formeln und liefere direkt die .pptx-Datei.
```

### 🌐 Upload im Web

Packe das **vollständige Projektverzeichnis einschließlich der erforderlichen Schriftarten in eine ZIP-Datei**, lade sie zusammen mit der **Artikel-PDF** hoch und sende anschließend:

```text
Entpacke das von mir hochgeladene PaperLoom-Paket und lies zuerst SKILL.md. Erstelle
anschließend nach den dortigen Vorgaben eine PowerPoint-Präsentation dieses Artikels für
eine Forschungsgruppenbesprechung. Verwende standardmäßig 1 Folie zu den Problemen, 1
zum Forschungsüberblick, 3–5 zur Methode, 2 zu Experimenten und 1 zur Zusammenfassung.
Gliedere den Forschungsüberblick in Blöcke, stelle Abbildungen und Diagramme in den
Vordergrund und verwende die im Paket enthaltenen Schriftarten FangSong GB2312 und Times
New Roman. Extrahiere die Abbildungen direkt aus dem Artikel und konvertiere zentrale
Formeln in native PowerPoint-Formeln. Platziere Belege in den Notizen und keine
kleingedruckten Quellenangaben am unteren Folienrand. Erzeuge die .pptx-Datei
tatsächlich und überprüfe sie.
```

> [!NOTE]
> Der Web-GPT muss Archive entpacken, Code ausführen und herunterladbare Dateien erzeugen können. Der ZIP-Upload stellt diese Werkzeuge nicht bereit und installiert den Skill nicht dauerhaft. Die vollständige Einstiegsanleitung steht in [WEB_START.md](../../WEB_START.md).

<a id="workflow"></a>

## 🧭 Standardmäßige Folienstruktur

Die Präsentation umfasst standardmäßig **8–10 Folien**:

| Abschnitt | Folien |
|---|---|
| Bestehende Probleme | 1 |
| Forschungsüberblick | 1 |
| Methode | 3–5 |
| Experimente | 2 |
| Zusammenfassung | 1 |

<details>
<summary><b>Hintergründe zum Arbeitsablauf</b></summary>

Dieser Skill entstand bei der mehrmaligen Erstellung und Überarbeitung einer GeoNav-Präsentation für eine Forschungsgruppenbesprechung: Inhalte wurden verdichtet, der Aufbau angepasst, Schriftarten und native Formeln eingerichtet sowie Office-Formatprobleme behoben. Anschließend wurden Hinweise am unteren Folienrand entfernt und die große Tabelle zum Forschungsüberblick durch sechs Blöcke zu Forschungsrichtungen ersetzt. Der Skill fasst diese bewährten Arbeitsweisen in wiederverwendbaren Anleitungen und Skripten zusammen.

1. **Ziele der Forschungsgruppenbesprechung und visuelle Standards festlegen**: echtes PPTX, kompakte Darstellung mit hoher Informationsdichte, Vorrang für Abbildungen und Diagramme, vorgegebene Schriftarten und native Formeln.
2. **Artikel lesen und einen Belegindex aufbauen**: Schlussfolgerungen, Abbildungen und Tabellen, Versuchsbedingungen und Messdefinitionen, Fehlerfälle und Grenzen der Aussagen einander zuordnen.
3. **Zuerst den roten Faden, dann die Folien planen**: von bestehenden Problemen über den Forschungsüberblick zu Methode, Experimenten und Zusammenfassung; die Anzahl der Methodenfolien am tatsächlichen Umfang der Arbeit ausrichten.
4. **Originalmaterial und bearbeitbare Objekte aufbereiten**: Bilder direkt extrahieren, Tabellen und Diagramme nativ erstellen, LaTeX in Office Math konvertieren und Schriftarten auf jeden Textabschnitt (`run`) anwenden.
5. **Inhalt, Layout und Kompatibilität prüfen**: jede Folie rendern, Daten abgleichen und den nicht konformen GB2312-Wert `charset=134` in `-122` korrigieren.
6. **Rückmeldungen durch gezielte Änderungen umsetzen**: Quellenangaben am unteren Folienrand entfernen, die Notizen beibehalten, die Tabelle zum Forschungsüberblick in Blöcke umwandeln und sicherstellen, dass andere Folien sowie Formatkorrekturen erhalten bleiben.

Den vollständigen Ablauf dokumentiert der [GeoNav-Rückblick](../../examples/geonav/workflow.md).

</details>

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

Die `8` Folien und `3` Formeln sind die Vorgaben für dieses GeoNav-Beispiel und müssen bei neuen Artikeln nach Bedarf angepasst werden. Wenn ein Artikel keine Formeln benötigt, sollten keine ergänzt werden, nur um eine bestimmte Anzahl zu erreichen. Die Einbettung von Schriftarten muss deren jeweilige Lizenz einhalten; standardmäßig werden die fünf Dateien aus `fonts/` eingebettet.

Der Validator prüft unter anderem Paketstruktur, Beziehungen, Schriftzeichensätze, native Formeln und Platzhalter. **Er ersetzt weder eine vollständige Prüfung gegen das OOXML-Schema noch einen tatsächlichen Test in der Desktopversion von Microsoft PowerPoint.** Nach dem Rendern müssen Inhalt und Layout weiterhin Folie für Folie geprüft werden. [Kompatibilitätsleitfaden](../../references/powerpoint-compatibility.md)

</details>

Führe die Tests aus:

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Distributionsarchive erstellen</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.0.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.0.0-full.zip
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
| `WEB_START.md` | Kopierbare Prompts und Ausführungsanleitung für die Web-Nutzung |
| `README.md` | Projektbeschreibung auf Englisch |
| `docs/i18n/` | Übersetzungen der README |
| `fonts/` | Enthaltene Schriftdateien, Nutzungshinweise und Prüfmanifest |
| `scripts/` | Werkzeuge für Bildextraktion, native Formeln, Schrifteinbettung, PPTX-Prüfung, Installation und Paketierung |
| `references/` | Anleitungen zu Foliengestaltung, Bildextraktion, Kompatibilität und Nutzung im Client |
| `examples/layout-demo/` | Ausführbares Beispiel mit drei nativen Folienlayouts und Quellcode zur Erstellung |
| `examples/geonav/workflow.md` | Ablauf dieser Erstellung, endgültige Struktur mit 8 Folien und wesentliche Korrekturen |
| `examples/evidence.template.json` | Vorlage für Quellen, Versuchsbedingungen und Messdefinitionen sowie Prüfprotokolle |
| `tests/` | Tests des Skriptverhaltens und Regressionstests |

</details>

<a id="license"></a>

## 📄 Lizenz

Der vom Projekt selbst verfasste Code und die Dokumentation stehen unter der [MIT-Lizenz](../../LICENSE). Informationen zu Schriftarten Dritter, Artikeln und Abhängigkeiten stehen in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
