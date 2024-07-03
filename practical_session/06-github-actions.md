# Automatisation

:::{note} Les objectifs de cette partie
- Avoir un aperçu de ce qu'on peut faire avec de l'intégration continue.
- Premier cas d'usage avec github-actions.
- Automatiser pytest lors d'une pull request.
- Automatiser la publication de nouveaux paquets sur PyPi et conda lors d'une release.
:::

Lors de la première version de cet atelier, github-actions n'existait pas. L'automatisation se faisait alors depuis les outils d'intégration continue disponibles sur github: travis, appveyor, circle-ci, ... Si ces outils sont toujours disponibles, github-actions change grandement la façon de faire son intégration continue. Il est plus flexible grâce aux différentes actions que l'on peut trouver dans son marketplace. Il permet d'exécuter facilement des actions pour tous les processus gérés par github: ouverture d'issue, pull request, release, ... Sortie fin 2019, il est rapidement arrivé numéro un dans les usages détrônant ainsi travis.

## pre-commit

L'outil [pre-commit](https://pre-commit.com/) va nous permettre d'automatiser l'utilisation du linter et du formatage à chaque commit pour vérifier que ce que l'on met dans le code suit certaines règles. Il permet de créer des *hooks* git de manière très simple et il est aisément extensible. Vous pouvez aller voir la liste des [hooks](https://pre-commit.com/hooks.html) et trouver votre bonheur.

:::{note} Remarque
Nous nous intéressons ici à un projet écrit en Python mais il vous est bien évidemment possible d'utiliser pre-commit pour d'autres langages
:::

Commençons par son installation. Nous allons rester dans l'univers de pixi et donc faire

```bash
pixi add pre-commit
```

Vous pouvez à présent initier pre-commit à l'aide de la ligne de commande suivante

```bash
pre-commit install
```

:::{attention}
Si un contributeur ne fait pas le `pre-commit install` localement les hooks ne seront pas installés et donc, aucun test ne sera effectué. Il est important de bien documenter cette étape pour qu'elle rentre dans les habitudes et intervienne juste après le clonage du dépôt.
:::

Il nous faut à présent définir ce que nous voulons tester à chaque commit en écrivant un fichier de configuration appelé `.pre-commit-config.yaml`. C'est bien évidemment à vous de mesurer l'impact de l'utilisation de cet outil. Si vous êtes trop contraignant et que le pre-commit prend une minute, vous n'aurez probablement pas l'adhésion des contributeurs. Il vous faudra donc trouver une solution acceptable qui profite à tous.

Dans le cadre de cet atelier, nous souhaitons vérifier la liste suivante à chaque commit

- ne pas mettre des fichiers trop gros (`check-added-large-files`)
- ne pas donner des noms de fichiers ou de répertoires qui ne sont pas compatibles avec tous les OS (`check-case-conflict`)
- vérifier que les fichiers `json` et `yaml` sont bien construits (`check-json`, `check-yaml`)
- faire en sorte que tous les fichiers finissent par une ligne vide (`end-of-file-fixer`)
- enlever les espaces qui ne servent à rien (`trailing-whitespace`)
- vérifier qu'il n'y a pas de fichiers qui sont en conflit de fusion (`check-merge-conflict`)
- vérifie que l'on n'essaie pas de pousser dans la branche principale (`no-commit-to-branch`)
- vérifier les caractères de fin de lignes et les rendre homogènes (`mixed-line-ending`)
- remplacer les tabulations par des espaces (https://GitHub.com/Lucas-C/pre-commit-hooks)
- vérifier que les changements sont bien compatibles avec ruff (https://GitHub.com/pre-commit/mirrors-clang-format)

(pre_commit_target)=
Voici à quoi ressemble le fichier `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://GitHub.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
      - id: check-case-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict
      - id: check-yaml
        exclude: conda/recipe/meta.yaml
      - id: check-json
      - id: no-commit-to-branch
      - id: mixed-line-ending
        args: ["--fix=lf"]
        description: Forces to replace line ending by the UNIX 'lf' character.
  - repo: https://GitHub.com/Lucas-C/pre-commit-hooks
    rev: v1.5.1
    hooks:
      - id: forbid-tabs
      - id: remove-tabs
        args: [--whitespaces-count, "4"]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.5.0
    hooks:
      # Run the linter.
      - id: ruff
        types_or: [python, pyi, jupyter]
        args: [--fix]
      # Run the formatter.
      - id: ruff-format
        types_or: [python, pyi, jupyter]
```

:::{note}
Par défaut, pre-commit ne s'exécute que sur les fichiers qui concernent le commit en cours. Si vous voulez exécuter la vérification sur l'ensemble des fichiers, vous pouvez le faire à l'aide de la commande

```bash
pre-commit run --all-files
```
:::

À partir de maintenant, à chaque fois que vous ferez un commit, l'ensemble de ces règles seront vérifiées.

## Github

Si vous n'avez pas encore de compte sur github, créez en un. Vous devez ensuite créer un nouveau projet que vous pouvez par exemple nommer `splinart`.

L'idée étant de mettre dans ce dépôt le `final_step` de la partie sur `pytest`, copiez ce répertoire dans un répertoire à part. Lorsque vous créez un dépôt sur github, celui-ci vous donne plusieurs recettes pour l'initialiser. Nous choisirons la première.

Mais avant cela, nous allons ajouter un fichier `readme.md` et un `.gitignore`.

:::{note} `readme.md`

splinart is a package used for a tutorial that explains how to do Python packaging using ruff, pytest, sphinx, ... And automates the process to distribute this package using github.

The original idea of splinart was found on the great invonvergent website.

If you want to install splinart

```bash
pip install splinart
```

or

```
conda install -c gouarin splinart
```

:::

:::{note} `.gitignore`

```txt
build
_build
.cache
dist
.ipynb_checkpoints
__pycache__
```
:::

Vous pouvez à présent initialiser votre projet en utilisant la commande suivante

```bash
git init
```

Nous allons dans un premier temps ajouter les deux fichiers que nous avons créés précédemment.

```bash
git add readme.md .gitignore
git commit -m "initial commit"
```

Puis tous les autres fichiers en faisant

```bash
git add splinart doc demos ...
```

Vérifiez avant de faire le commit que tous les fichiers sont les bons et qu'il n'en manque pas.

```bash
git commit -m "add splinart"
```

Initialisez le `remote` en suivant ce qui est écrit sur votre github. J'avais pour cette exemple

```bash
git remote add origin https://github.com/gouarin/splinart.git
```

Vous pouvez maintenant faire un push de vos trois commits en faisant

```bash
git push --set-upstream origin main
```

Vous pouvez à présent vérifier que tous vos fichiers sont présents sur votre github.

Maintenant que votre dépôt a bien été créé, nous allons nous intéresser (dans l'ordre) aux étapes suivantes

- Mise en place d'un premièr workflow github-actions pour l'intégration continue.
- Validation des push en utilisant pytest.
- Déploiement de `splinart` sur PyPi et conda.


## github-actions

Les actions sont déclenchées à partir de ce qu'il y a dans le répertoire `.github/workflows`. Nous allons créer une branche qui va initier la CI.

```bash
git checkout -b init-ci
```

Il faut maintenant créer le premier worflow en ajoutant le fichier `.github/worflows/ci.yml`dont le contenut est

```yaml
name: ci

on:
  pull_request:
    branches: [main]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"

```

:::{tip} Petite explication de texte

Cette action est exécutée lorsque l'on fait une pull request sur la branche `main`. Elle est réalisée sur une distribution `ubuntu` donc une machine `linux`. Nous verrons par la suite que l'on peut également utiliser `mac os` et `windows`. Cette action est constituée de 2 étapes

1. On clone le dépôt.
2. On installe Python 10
:::

Il vous faut ajouter le fichier

```bash
git add .github/worflows/ci.yml
```

puis de pousser la branche sur github

```bash
git push --set-upstream origin init-ci
```

Vous n'avez plus qu'à retourner sur github et demander à ouvrir une pull request. Vous verrez alors la CI se mettre en place.

Nous allons à présent ajouter l'installation de pytest, l'installation de notre application et enfin vérifier que tous les tests passent bien avec pytest.

```yaml
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Test with pytest
      run: |
        pytest
```

Vous pouvez rester dans le même branche et commiter les changements au fur et à mesure. La pull request sera mise à jour automatiquement.

Nous allons à présent ajouter différentes versions de Python dans la CI ainsi que plusieurs OS.

Il suffit de changer la première partie de `build`

```yaml
    runs-on: ubuntu-latest
```

par

```yaml
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", 3.11,  3.12]
        os:
          - ubuntu-latest
          - macos-latest
          - windows-latest
```

Nous avons créé ici une matrice qui a deux paramètres. La CI va réaliser toutes les combinaisons possibles.

```{attention} Python 3.10
Si nous mettons `3.10` directement dans les versions de Python, le `0` sera retiré ce qui fera que la version `3.1`sera recherchée entrainant une erreur de la CI. C'est pouquoi il faut mettre des `"` autour de cette version.
```

## ReadTheDocs

Nous allons à présent nous intéresser à générer la documentation automatiquement sur ReadTheDocs. Pour cela, nous allons ajouter un fichier `environment.yml` dans le répertoire `doc` indiquant tout ce dont nous avons besoin pour sphinx et ses dépendances. Et un fichier `.readthedocs.yml` à la racine du projet indiquant comment installer notre projet.

Voici à quoi ressemblent ces deux fichiers

```yaml
name: splinart
channels:
  - conda-forge
dependencies:
  - notebook
  - sphinx
  - nbsphinx
  - pydata-sphinx-theme
  - numpydoc
  - nbsphinx-link
  - myst-parser
```

```yaml
version: 2

build:
   os: "ubuntu-20.04"
   tools:
      python: "mambaforge-22.9"

python:
   install:
      - method: pip
        path: .

conda:
   environment: doc/environment.yml
```

Vous devez à présent vous créer un compte sur https://readthedocs.org/ et connecter votre projet github à celui-ci. De cette manière, à chaque fois que vous ferez une mise à jour du dépôt, la documentation sera regénérée.

Vous pouvez également faire en sorte que la génération de la documentation sur readthedocs fasse partie intégrante de la CI. Pour cela, il vous suffit d'aller dans votre projet sur readthedocs et aller dans `Admin/advanced parameters` et de cocher la case sur les `pull request`.

## Mise en place d'une nouvelle release

Nous allons changer un peu la recette conda pour faire le package de l'application. Nous avions vu dans la [partie 3](#conda-recipe) comment faire une recette conda à partir d'un dossier local. Nous allons à présent le faire directement à partir d'une release du dépôt github. Il suffit de changer le fichier comme suit avec les bonnes dépendances

```yaml
{% set version = "0.2.0" %}

package:
  name: splinart
  version: {{ version }}

source:
  git_url: https://github.com/gouarin/splinart.git
  git_rev: v{{ version }}

build:
  number: 0
  script: "{{PYTHON}} -m pip install . --no-deps -vv"
  noarch: python

requirements:
  build:
    - python>=3.8
    - setuptools
  run:
    - python>=3.8
    - numpy
    - matplotlib

test:
  imports:
    - splinart

about:
  home: http://github.com/gouarin/splinart
  license: BSD
  license_family: BSD
  summary: 'spline art generator'
  description: 'spline art generator'

extra:
  recipe-maintainers: 'loic.gouarin@gmail.com'
```

:::{attention} Version
- La version est entrée en dur et doit correspondre à la version se trouvant dans `splinart/version.py`. Il est possible de faire autrement mais nous ne le verrons pas ici.
- Le nom de la release sur github est ici `v0.2.0` car `git_rev: v{{ version }}`.
- Pour que l'application fonctionne, elle a besoin de `numpy` et de `matplotlib` au moment de l'installation.
:::

:::{note} Création d'une nouvelle release
- Changer la version dans `splinart/version.py`.
- Changer la version dans `recipes/meta.yaml`.
- Pousser les changements sur le dépôt.
- Créer une [nouvelle release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) sur le dépôt
:::

## Publication

Nous avons maintenant une CI qui teste notre application. Nous allons en créer une autre qui va être déclanchée au moment d'une release et qui va déployer une nouvelle version de l'application sur PyPi et sur conda.

Voici l'action correspondante

```yaml
name: publish

on:
    release:
      types: [published]

jobs:
    make_sdist:
        name: Make SDist and weel
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4

            - name: Install build
              run: pip install build

            - name: Build SDist
              run: python -m build --sdist

            - name: Build wheel
              run: python -m build --wheel

            - uses: actions/upload-artifact@v3
              with:
                path: dist/*

    upload_on_pypi:
        needs: [make_sdist]
        environment: pypi
        permissions:
            id-token: write
        runs-on: ubuntu-latest
        steps:
            - uses: actions/download-artifact@v3
              with:
                name: artifact
                path: dist

            - uses: pypa/gh-action-pypi-publish@release/v1
              with:
                repository-url: https://test.pypi.org/legacy/

    upload_on_conda:
        needs: [make_sdist]
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v1

            - uses: mamba-org/setup-micromamba@v1
              with:
                environment-name: build-env
                create-args: >-
                  python=3.10
                  conda-build
                  anaconda-client

            - name: Build the recipe
              shell: bash -l {0}
              run: conda build recipes

            - name: upload on conda
              shell: bash -l {0}
              run: anaconda -t ${{ secrets.ANACONDA_TOKEN }} upload --force /home/runner/micromamba/envs/build-env/conda-bld/*/splinart-*.tar.bz2
```

:::{note} Quelques remarques
- On peut voir que cette action n'est déclanchée qu'au moment d'une release
  ```yaml
  on:
      release:
          types: [published]
  ```
- On commence par créer l'archive et les wheels: `makes_sdist`.
- Si tout se passe bien alors on déploie sur PyPi et sur conda c'est pourquoi ces deux travaux ont `needs: [make_sdist]`.
- le déploiement sur PyPi se fait sans token car nous avons ajouté le site github de notre application comme site de confiance.
- le déploiement sur conda se fait à l'aide d'un token qu'il faut ajouter aux secrets de votre dépôt.
:::

Nous allons commencer par créer un token sur anaconda. Il faut aller sur votre compte anaconda dans la partie `settings->access` et créer un token. Celui-ci devra avoir les droits suivants

- `api:read` (Allow read access to the API site)
- `api:write` (Allow write access to the API site)

Vous pouvez à présent l'ajouter dans les secrets de guthub en allant, au niveau de votre dépôt, dans `settings/secrets and variables/actions` et ajouter votre token dans la partie `repository secrets`.

:::{attention} Le nom
Le nom du token doit correspondre à celui qui a été mis dans l'action. Ici: `ANACONDA_TOKEN`.
:::

Pour la partie PyPi, vous pouvez faire de même (ajouter un token) en allant sur [Api token](https://pypi.org/help/#apitoken) ou dire que votre dépôt github est un dépôt de confiance ([trusted publisher](https://docs.pypi.org/trusted-publishers/)). Vous devrez pour cela activer la double authentification.

Une fois que vous avec mis tout ça en place et que l'action est mise dans la branche `main` du dépôt, vous pouvez tester celle-ci en créant une nouvelle release.****
