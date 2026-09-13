<div align="center">

# 🧵 PaperLoom · 论文织图

### De l’article scientifique à une présentation claire et visuelle.

**6–8 diapositives par défaut · Preuves regroupées · Figures d’origine · Équations natives · PPTX modifiable**

![Version](https://img.shields.io/badge/version-1.1.2-4455AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-%2Epptx-D24726?style=flat-square)

[🚀 Démarrage rapide](#quick-start) · [🖼️ Aperçu](#preview) · [🧭 Structure des diapositives](#workflow) · [🛠️ Développement](#development) · [📚 Guides](#guides)

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

PaperLoom transforme des articles scientifiques en présentations **PowerPoint `.pptx`** compactes, modifiables et centrées sur les figures et les graphiques. Installez le skill dans un client compatible, ou téléversez le projet complet au format ZIP avec l’article dans un GPT web capable d’exécuter du code.

<a id="quick-start"></a>

## 🚀 Démarrage rapide

### 🌐 Téléversement sur le web

Téléversez **paper-loom-v1.1.2-full.zip** et le **PDF de l’article**, puis demandez :

> Crée le PPT de cet article en suivant le skill contenu dans le ZIP.

Cela suffit. SKILL.md définit les paramètres par défaut, la création, la vérification visuelle et la livraison du fichier. Aucun long prompt, fichier de configuration ou diaporama de référence supplémentaire n’est nécessaire.

### 💻 Client local

Clonez ou téléchargez ce dépôt avec les polices incluses, consultez le [guide des polices](../../fonts/README.md), puis exécutez la commande suivante à la racine du dépôt :

```bash
python scripts/install_skill.py
```

Par défaut, le skill est copié dans `~/.agents/skills/paper-loom/` pour l’utilisateur courant. Si ce répertoire existe déjà, l’installation s’arrête sans écraser votre version. Vous pouvez aussi sélectionner directement ce dossier complet dans un client prenant en charge l’importation de skills. [Guide détaillé pour les clients](../../references/client-mode.md)

Après l’installation, sélectionnez PaperLoom dans le client ou saisissez :

> Utilise $paper-loom pour créer une présentation de cet article.

<a id="features"></a>

## ✨ Fonctionnalités

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 Un récit visuel</strong><br>Les figures expliquent les entrées, les états, les transformations et les retours. Les preuves liées partagent une page ; les expériences conservent des tableaux natifs et les résultats défavorables.</td>
    <td width="50%" valign="top"><strong>🖼️ Les figures d’origine</strong><br>Extraction directe des images intégrées au PDF : aucune capture de page ni capture recadrée présentée comme une image extraite.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 Des équations modifiables</strong><br>Conversion des équations nécessaires de LaTeX vers le format Office Math natif de PowerPoint, pour qu’elles restent modifiables.</td>
    <td width="50%" valign="top"><strong>🔤 Des polices vérifiables</strong><br>FangSong GB2312 (仿宋 GB2312) pour le chinois, Times New Roman pour l’anglais et les chiffres. Les fichiers, leurs propriétés et leurs empreintes de hachage sont vérifiables.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 Des preuves dans les notes</strong><br>Sources détaillées et explications longues dans les notes. Indicateurs, unités, conditions de comparaison et limites importantes restent près des figures et tableaux ; le pied de page reste discret.</td>
    <td width="50%" valign="top"><strong>🛠️ Des révisions ciblées</strong><br>Les modifications préservent les autres diapositives, polices, équations et paramètres de compatibilité déjà validés.</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ Aperçu

Cette démonstration utilise des **données fictives** clairement signalées ; elle ne représente pas les conclusions d’un véritable article.

<table>
  <tr>
    <th width="33%">Mécanismes et états</th>
    <th width="33%">Entraînement et inférence</th>
    <th width="33%">Résultats et limites</th>
  </tr>
  <tr>
    <td><a href="../../examples/evidence-demo/preview-01.png"><img src="../../examples/evidence-demo/preview-01.png" alt="Mécanismes et états" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-02.png"><img src="../../examples/evidence-demo/preview-02.png" alt="Entraînement et inférence" width="100%"></a></td>
    <td><a href="../../examples/evidence-demo/preview-03.png"><img src="../../examples/evidence-demo/preview-03.png" alt="Résultats et limites" width="100%"></a></td>
  </tr>
</table>

[📥 Présentation PPTX modifiable](../../examples/evidence-demo/evidence-demo.pptx) · [📖 Code source et commandes de reproduction](../../examples/evidence-demo/README.md)

[PDF de référence AeroDuo de six pages inclus](../../examples/aeroduo-reference/AeroDuo_组会汇报_合并精简6页版.pdf)

<a id="workflow"></a>

## 🧭 Une structure guidée par les preuves

Comptez **6–8 diapositives** par défaut, ou **8–10** pour un article complexe. Le nombre et le modèle demandés par l’utilisateur priment. Couvrez la tâche et son positionnement, les mécanismes, l’entraînement et l’exécution, les expériences et leurs limites, puis la synthèse. Ces éléments ne nécessitent pas chacun une page séparée. Une revue bibliographique autonome et un nombre fixe de pages de méthode ne sont pas obligatoires.

Avant de créer les diapositives, lisez les guides de [conception](../../references/design.md), de [compositions et contre-exemples](../../references/reference-patterns.md) et de [contrôle qualité](../../references/quality-gates.md). Préparez `slide-plan.json` dans le dossier de travail à partir du [modèle de plan](../../examples/slide-plan.template.json), puis continuez sans attendre par défaut une approbation du plan.

Regroupez la vue d’ensemble, les états intermédiaires et les conditions de retour d’un même mécanisme. Rapprochez les résultats principaux à protocole identique, les ablations et les résultats défavorables. Gardez les conditions près des figures et tableaux, les explications longues et sources détaillées dans les notes. Utilisez la [démonstration centrée sur les preuves](../../examples/evidence-demo/README.md) comme référence visuelle et vérifiez la lisibilité de chaque page.

<a id="development"></a>

## 🛠️ Développement et validation

Utilisez Python 3.10+ et Node.js 20+. Exécutez les commandes suivantes à la racine du dépôt :

```bash
python -m pip install -r requirements.txt
npm install
python scripts/doctor.py
```

La conversion en équations natives nécessite également `pandoc` : suivez la [documentation officielle de Pandoc](https://pandoc.org/installing.html). Les polices requises sont incluses dans `fonts/` ; consultez le [guide des polices](../../fonts/README.md) pour les modalités d’utilisation. Si l’environnement dispose déjà d’un outil dédié à PowerPoint, il n’est pas nécessaire d’en changer.

<details>
<summary><b>🖼️ Extraire les images</b></summary>

```bash
python scripts/extract_pdf_assets.py paper.pdf --output work/paper-assets
```

La sortie contient les ressources d’origine et un manifeste. L’option `--pages 1,3-5` est prise en charge. Un objet intégré peut ne représenter qu’une partie d’une figure : il faut vérifier que la figure reste complète sur le plan sémantique. Les figures purement vectorielles ou comportant du texte superposé ne doivent pas être automatiquement remplacées par des captures d’écran. [Guide d’extraction des images](../../references/figure-extraction.md)

</details>

<details>
<summary><b>🧮 Équations, polices et validation</b></summary>

Dans le PPTX natif, réservez un paragraphe distinct pour chaque équation nécessaire, par exemple `[[EQ_FUSION]]`, et indiquez le LaTeX correspondant dans le fichier de correspondance :

```bash
python scripts/inject_equations.py draft.pptx math.pptx --mapping equations.json --require-all
python scripts/embed_fonts.py math.pptx final.pptx
python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3 --report validation.json
```

Les nombres de diapositives et de formules dans ces commandes sont des exemples à adapter à l’article. L’incorporation des polices doit respecter leurs licences ; les cinq fichiers de `fonts/` sont utilisés par défaut.

Le validateur vérifie notamment la structure du paquet, les relations, les jeux de caractères des polices, les équations natives et les espaces réservés, mais **il ne constitue ni une validation complète du schéma OOXML, ni un test dans la version de bureau de Microsoft PowerPoint**. Après le rendu, le contenu et la mise en page doivent encore être contrôlés diapositive par diapositive. [Guide de compatibilité](../../references/powerpoint-compatibility.md)

</details>

Exécutez les tests :

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Créer les archives de distribution</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.1.2-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.1.2-full.zip
```

L’archive complète inclut les polices fournies avec le dépôt ; l’outil de création de paquets vérifie qu’elles sont toutes présentes. L’option `--variant github` crée une archive du code source sans les fichiers de polices séparés.

</details>

<a id="guides"></a>

## 📚 Guides et dépôt

- [💻 Guide détaillé pour les clients](../../references/client-mode.md)
- [🌐 Instructions pour le web](../../WEB_START.md)
- [🖼️ Guide d’extraction des images](../../references/figure-extraction.md)
- [🧩 Guide de compatibilité PowerPoint](../../references/powerpoint-compatibility.md)

<details>
<summary><b>Arborescence du dépôt</b></summary>

| Chemin | Contenu |
|---|---|
| `SKILL.md` | Flux de travail principal et exigences de qualité à lire par l’IA |
| `WEB_START.md` | Notes facultatives sur le téléversement et l’environnement ; entrée : SKILL.md |
| `README.md` | Présentation du projet en anglais |
| `docs/i18n/` | Traductions du README |
| `fonts/` | Fichiers de polices inclus, instructions d’utilisation et manifeste de vérification |
| `scripts/` | Outils d’extraction d’images, d’équations natives, d’incorporation de polices, de vérification PPTX, d’installation et de création de paquets |
| `references/` | Guides de conception des diapositives, d’extraction d’images, de compatibilité et d’utilisation dans un client |
| `examples/aeroduo-reference/` | Référence visuelle de six pages et guide de lecture |
| `examples/evidence-demo/` | Démonstration exécutable de trois diapositives avec des mises en page natives et code source de génération |
| `examples/geonav/workflow.md` | Exemple de planification à partir des preuves de l’article |
| `examples/evidence.template.json` | Modèle pour les sources, les protocoles et définitions des expériences, et les enregistrements de validation |
| `examples/slide-plan.template.json` | Modèle des questions, preuves, visuels et décisions de regroupement par page |
| `tests/` | Tests du comportement des scripts et de non-régression |

</details>

<a id="license"></a>

## 📄 Licence

Le code et la documentation originaux du projet sont publiés sous licence [MIT](../../LICENSE). Pour les polices tierces, les articles et les dépendances, consultez [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
