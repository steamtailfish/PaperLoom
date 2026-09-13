<div align="center">

# 🧵 PaperLoom · 论文织图

### De l’article scientifique à une présentation claire et visuelle.

**8–10 diapositives · Figures d’origine · Équations natives · PPTX modifiable**

![Version](https://img.shields.io/badge/version-1.0.0-4455AA?style=flat-square)
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

<a id="features"></a>

## ✨ Fonctionnalités

<table>
  <tr>
    <td width="50%" valign="top"><strong>🎨 Un récit visuel</strong><br>Synthèse bibliographique en blocs, schémas de processus et de mécanismes pour la méthode, tableaux et graphiques natifs pour lire précisément les résultats expérimentaux.</td>
    <td width="50%" valign="top"><strong>🖼️ Les figures d’origine</strong><br>Extraction directe des images intégrées au PDF : aucune capture de page ni capture recadrée présentée comme une image extraite.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🧮 Des équations modifiables</strong><br>Conversion des équations nécessaires de LaTeX vers le format Office Math natif de PowerPoint, pour qu’elles restent modifiables.</td>
    <td width="50%" valign="top"><strong>🔤 Des polices vérifiables</strong><br>FangSong GB2312 (仿宋 GB2312) pour le chinois, Times New Roman pour l’anglais et les chiffres. Les fichiers, leurs propriétés et leurs empreintes de hachage sont vérifiables.</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>🔎 Des preuves dans les notes</strong><br>Sources et preuves détaillées dans les notes du présentateur ; seul un décor discret et le numéro de diapositive restent en bas de page.</td>
    <td width="50%" valign="top"><strong>🛠️ Des révisions ciblées</strong><br>Les modifications préservent les autres diapositives, polices, équations et paramètres de compatibilité déjà validés.</td>
  </tr>
</table>

<a id="preview"></a>

## 🖼️ Aperçu

Cette démonstration utilise des **données fictives** clairement signalées ; elle ne représente pas les conclusions d’un véritable article.

<table>
  <tr>
    <th width="33%">Synthèse bibliographique</th>
    <th width="33%">Méthode et équation</th>
    <th width="33%">Expériences</th>
  </tr>
  <tr>
    <td><a href="../../examples/layout-demo/preview-01.png"><img src="../../examples/layout-demo/preview-01.png" alt="Synthèse bibliographique en blocs" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-02.png"><img src="../../examples/layout-demo/preview-02.png" alt="Mécanisme technique et équation native" width="100%"></a></td>
    <td><a href="../../examples/layout-demo/preview-03.png"><img src="../../examples/layout-demo/preview-03.png" alt="Tableaux et graphiques expérimentaux" width="100%"></a></td>
  </tr>
</table>

[📥 Présentation PPTX modifiable](../../examples/layout-demo/layout-demo.pptx) · [📖 Code source et commandes de reproduction](../../examples/layout-demo/README.md)

<a id="quick-start"></a>

## 🚀 Démarrage rapide

### 💻 Client local

Clonez ou téléchargez ce dépôt avec les polices incluses, consultez le [guide des polices](../../fonts/README.md), puis exécutez la commande suivante à la racine du dépôt :

```bash
python scripts/install_skill.py
```

Par défaut, le skill est copié dans `~/.agents/skills/paper-loom/` pour l’utilisateur courant. Si ce répertoire existe déjà, l’installation s’arrête sans écraser votre version. Vous pouvez aussi sélectionner directement ce dossier complet dans un client prenant en charge l’importation de skills. [Guide détaillé pour les clients](../../references/client-mode.md)

Après l’installation, sélectionnez PaperLoom dans le client ou saisissez :

```text
Utilise $paper-loom pour transformer cet article en une présentation PowerPoint pour une
réunion de laboratoire.
Respecte les exigences du skill concernant la structure, les polices, l’extraction des
images et les équations natives, puis livre directement le fichier .pptx.
```

### 🌐 Téléversement sur le web

Compressez le **répertoire complet du projet, avec les polices requises, au format ZIP**, puis téléversez-le avec le **PDF de l’article** et envoyez :

```text
Décompresse le paquet PaperLoom que j’ai téléversé, lis d’abord SKILL.md, puis suis ses
exigences pour créer une présentation PowerPoint de cet article pour une réunion de
laboratoire. Prévois par défaut 1 diapositive pour les problèmes, 1 pour la synthèse
bibliographique, 3–5 pour la méthode, 2 pour les expériences et 1 pour la conclusion.
Organise la synthèse bibliographique en blocs, privilégie les figures et les graphiques,
et utilise les polices FangSong GB2312 et Times New Roman du paquet. Extrais directement
les figures de l’article et convertis les équations essentielles en équations natives de
PowerPoint. Place les preuves dans les notes, sans petits textes de sources en pied de
page. Génère réellement le fichier .pptx et vérifie-le.
```

> [!NOTE]
> Le GPT web doit pouvoir décompresser des archives, exécuter du code et produire des fichiers téléchargeables. Téléverser le ZIP ne lui fournit pas ces outils et n’installe pas le skill de façon permanente. Les instructions complètes se trouvent dans [WEB_START.md](../../WEB_START.md).

<a id="workflow"></a>

## 🧭 Structure par défaut des diapositives

Par défaut, la présentation compte **8–10 diapositives** :

| Partie | Diapositives |
|---|---|
| Problèmes existants | 1 |
| Synthèse bibliographique | 1 |
| Méthode | 3–5 |
| Expériences | 2 |
| Conclusion | 1 |

<details>
<summary><b>Les étapes de la méthode de travail</b></summary>

Ce skill est né de plusieurs cycles de création et de révision d’une présentation de GeoNav pour une réunion de laboratoire : condensation du contenu, ajustement du fil narratif, gestion des polices et des équations natives, correction du format Office, suppression des annotations en pied de page et remplacement d’un grand tableau de synthèse bibliographique par six blocs d’axes de recherche. Il transforme ces méthodes éprouvées en instructions et scripts réutilisables.

1. **Définir les objectifs de la réunion et les critères visuels** : véritable PPTX, contenu compact et dense, priorité aux figures et graphiques, polices imposées et équations natives.
2. **Lire l’article et constituer un index des preuves** : relier les conclusions, les figures et tableaux, les protocoles et définitions des expériences, les cas d’échec et les limites d’interprétation.
3. **Structurer le récit avant les diapositives** : partir des problèmes existants, puis présenter la synthèse bibliographique, la méthode, les expériences et la conclusion ; répartir les diapositives de méthode selon le travail réellement présenté.
4. **Traiter les ressources d’origine et les objets modifiables** : extraire directement les images, créer des tableaux et graphiques natifs, convertir le LaTeX en Office Math et appliquer les polices à chaque segment de texte (`run`).
5. **Vérifier le contenu, la mise en page et la compatibilité** : rendre chaque diapositive, comparer les données et remplacer la valeur non conforme `charset=134` de GB2312 par `-122`.
6. **Procéder à des révisions ciblées selon les retours** : supprimer les sources en pied de page en conservant les notes ; remplacer le tableau de synthèse bibliographique par des blocs ; préserver les autres diapositives et les corrections de format.

Le déroulement complet est présenté dans le [retour d’expérience GeoNav](../../examples/geonav/workflow.md).

</details>

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

Les `8` diapositives et les `3` équations correspondent aux exigences de cet exemple GeoNav ; adaptez-les à chaque nouvel article. Si un article n’a pas besoin d’équations, il n’est pas nécessaire d’en ajouter pour atteindre un nombre donné. L’incorporation des polices doit respecter leurs licences ; par défaut, les cinq fichiers de `fonts/` sont incorporés.

Le validateur vérifie notamment la structure du paquet, les relations, les jeux de caractères des polices, les équations natives et les espaces réservés, mais **il ne constitue ni une validation complète du schéma OOXML, ni un test dans la version de bureau de Microsoft PowerPoint**. Après le rendu, le contenu et la mise en page doivent encore être contrôlés diapositive par diapositive. [Guide de compatibilité](../../references/powerpoint-compatibility.md)

</details>

Exécutez les tests :

```bash
python -m unittest discover -s tests -v
```

<details>
<summary><b>📦 Créer les archives de distribution</b></summary>

```bash
python scripts/package_skill.py --variant github --output ../paper-loom-v1.0.0-github.zip
python scripts/package_skill.py --variant full --output ../paper-loom-v1.0.0-full.zip
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
| `WEB_START.md` | Prompts à copier et instructions d’exécution pour le web |
| `README.md` | Présentation du projet en anglais |
| `docs/i18n/` | Traductions du README |
| `fonts/` | Fichiers de polices inclus, instructions d’utilisation et manifeste de vérification |
| `scripts/` | Outils d’extraction d’images, d’équations natives, d’incorporation de polices, de vérification PPTX, d’installation et de création de paquets |
| `references/` | Guides de conception des diapositives, d’extraction d’images, de compatibilité et d’utilisation dans un client |
| `examples/layout-demo/` | Démonstration exécutable de trois diapositives avec des mises en page natives et code source de génération |
| `examples/geonav/workflow.md` | Déroulement de cette réalisation, structure finale en 8 diapositives et principales corrections |
| `examples/evidence.template.json` | Modèle pour les sources, les protocoles et définitions des expériences, et les enregistrements de validation |
| `tests/` | Tests du comportement des scripts et de non-régression |

</details>

<a id="license"></a>

## 📄 Licence

Le code et la documentation originaux du projet sont publiés sous licence [MIT](../../LICENSE). Pour les polices tierces, les articles et les dépendances, consultez [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
