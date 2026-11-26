# Bug Severity Classifier

Classifieur qui devine la gravité d'un bug (critical, major, minor) à partir de son titre, et surtout **analyse honnêtement ses résultats** : métriques par catégorie, erreurs concrètes, limites des données.

Le but n'est pas d'obtenir le meilleur score, mais de montrer comment évaluer un modèle sans se laisser tromper par un chiffre global.

## Données

- **88 682 bugs réels** issus de Mozilla (Core, Firefox, Thunderbird, Bugzilla : 73 %) et d'Eclipse (Platform, JDT, CDT : 27 %).
- Source : [AliArshad/Bugzilla_Eclipse_Bug_Reports_Dataset](https://huggingface.co/datasets/AliArshad/Bugzilla_Eclipse_Bug_Reports_Dataset) sur Hugging Face. La licence n'est pas précisée : le fichier n'est donc **pas inclus** dans ce dépôt. Pour relancer le notebook, télécharger le CSV depuis cette page et le placer dans `data/bugs_eclipse.csv`.
- Les 6 sévérités d'origine sont regroupées en 3 : blocker + critical → **critical** ; major + normal → **major** ; minor + trivial → **minor**.
- Répartition après regroupement : major 86,5 %, critical 7,6 %, minor 5,9 %. Le jeu est très déséquilibré.
- Jeu d'exemple de 12 bugs : `data/bugs_sample.csv`.

Citation demandée par la fiche du jeu de données : Lamkanfi, Pérez, Demeyer, *The Eclipse and Mozilla Defect Tracking Dataset: a Genuine Dataset for Mining Bug Information*, MSR 2013.

## Les robots comparés

| Robot | Score global | Critical : rappel | Critical : précision |
|---|---|---|---|
| Baseline : répondre « major » à tout | 86,5 % | 0 % | – |
| v1 : règles écrites à la main (mots-clés) | 17,9 % | 47 % | – |
| v2 : TF-IDF + régression logistique | 89,4 % | 56 % | 75 % |
| v2 équilibré (`class_weight="balanced"`) | 72,7 % | 75 % | 45 % |

Notes : le v1 est évalué sur l'ensemble des bugs (il n'apprend rien). Les v2 sont évalués sur un jeu de test de 17 737 bugs (20 %) jamais vus pendant l'entraînement, tirés avec un découpage stratifié (`random_state=42`). Le 0 % de la baseline vient du raisonnement (elle ne répond jamais « critical »).

## Ce que montre l'analyse

- **Le score global trompe.** Répondre « major » à tout donne 86,5 % ; le v2 à 89,4 % ne fait que 2,9 points de mieux, et ignore presque les bugs « minor » (rappel de 4 %).
- **Le choix dépend du coût des erreurs.** Le v2 équilibré trouve 3 bugs critiques sur 4, mais plus de la moitié de ses alertes critiques sont fausses. Le v2 est plus précis mais en rate près de la moitié.
- **Erreurs sur les bugs critiques.** Sur 332 bugs critiques ratés par le v2 équilibré, seuls 15 % contiennent un mot fort dans le titre (crash, freeze, hang…). Pour la majorité, le titre ne porte aucun signal de gravité.
- **Le score varie selon le projet** : de 51 % (Bugzilla, 473 bugs) à 78 % (Core, 9 389 bugs). Core pèse 53 % du jeu de test et tire le score global vers le haut.

## Limites

- Le modèle ne lit que le **titre** du bug.
- Les classes sont très déséquilibrées.
- La sévérité est choisie par la personne qui signale le bug : le corrigé contient du **bruit** (certains classements sont discutables).
- Le modèle ne comprend pas le sens (la négation, par exemple) et traite chaque forme d'un mot séparément (crash / crashed).

## Pistes d'amélioration

- Donner plus d'informations au modèle (description, composant, étapes de reproduction).
- Tester une convention d'écriture des titres, mesurée par une expérience avant/après.
- Regrouper les formes d'un même mot.
- Tester d'autres réglages d'équilibrage et d'autres modèles.

## Lancer le projet

Prérequis : [uv](https://docs.astral.sh/uv/).

```bash
uv sync                # installe les dépendances
uv run pytest          # lance les tests du robot à règles
```

Ouvrir `notebooks/exploration.ipynb` dans VS Code (extension Jupyter, noyau du dossier `.venv`) et lancer toutes les cellules.

## Structure

```
src/bug_severity_classifier/rules.py   robot v1 à base de règles
tests/test_rules.py                    tests pytest du robot v1
data/bugs_sample.csv                   12 bugs d'exemple
notebooks/exploration.ipynb            données, modèles, métriques, erreurs
```
