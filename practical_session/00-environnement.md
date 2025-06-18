## Définition

On appelle ici environnement de développement un espace restreint, facile à reproduire et à effacer qui prend en compte l'ensemble des dépendances de notre projet Python. Il permet de travailler de manière isolée. Il permet également à d'autres contributeurs de travailler dans une même configuration.

## Les outils

Il en existe un certain nombre et c'est en les utilisant que l'on peut se faire sa propre opinion. J'utilise pour ma part `mamba` et `pixi` car je ne développe pas qu'en Python et `conda-forge` est bien pratique lorsqu'on a des dépendances à des librairies écrites dans d'autres langages. Mais, pour des développements que Python, d'autres choix peuvent être plus pertinents.

Voici une liste d'outils que vous pouvez utiliser pour créer vos environnements de développement

- [venv](https://docs.python.org/3/library/venv.html)

    Cet outil est disponible depuis la version `3.3` de Python et est installé sur votre système en même temps que Python.

- [pipenv](https://pipenv.pypa.io/en/latest/)

    Cet outil offre plus de flexibilité que `venv`.

- [mamba](https://mamba.readthedocs.io/en/latest/index.html)

  Cet outil permet de gérer plusieurs environnements en s'appuyant sur les packages se trouvant sur PyPi et sur les différentes ***channels*** de conda.

- [poetry](https://python-poetry.org/)

  Cet outil ressemble à ce que l'on peut trouver lorsqu'on utilise `nodejs` à savoir que la configuration de votre environnement va évoluer en fonction de ce que vous installez et ce que vous désinstallez. Tous ces changements sont décrits dans un fichier permettant de reproduire un environnement à l'identique.

- [uv](https://docs.astral.sh/uv/)

   uv est un gestionnaire de paquets Python nouvelle génération et multiplateforme, développé par Astral (l’équipe derrière Ruff), et écrit en Rust pour des performances exceptionnelles. Il se veut un remplaçant rapide et moderne de pip, pip-tools, poetry, virtualenv, pyenv, pipx, et même twine, en offrant une interface unique et cohérente pour gérer l’installation de paquets, la résolution des dépendances, la gestion des environnements virtuels, et même l’installation de différentes versions de Python

- [pixi](https://pixi.sh/)

    Pixi est un gestionnaire de paquets moderne et multiplateforme, conçu pour gérer les environnements et dépendances Python (et d’autres langages) de manière rapide, fiable et reproductible. Développé en Rust et basé sur l’écosystème conda, il permet d’installer des paquets depuis conda et PyPI, tout en résolvant automatiquement les dépendances et en générant un fichier de verrouillage (lock file) pour garantir la reproductibilité des environnements. Il est également possible de définir des tâches personnalisées pour automatiser les workflows de développement.

## Définir ses dépendances via `requirements.txt` ou `environment.yml`

Si nous avons vu précédemment que certains outils pouvaient écrire leur propre fichier indiquant les dépendances d'un environnement, nous allons voir ici deux formats un peu plus universels

- `requirements.txt` est un fichier permettant de décrire les dépendances et peut être utilisé avec l'ensemble des outils cités.
- `environment.yml` est utilisé par les outils s'appuyant sur des packages `conda`.

### Exemple de fichier `requirements.txt`

:::{card}
:header: Sans versions définies

```txt
numpy
matplotlib
jupyterlab
```

:::

:::{card}
:header: Avec des versions bien précises

```txt
numpy>1.20
matplotlib==3.7.1
jupyterlab>4.0,<4.1
```

:::

### Exemple de fichier `environment.yml`

:::{card}
:header: Sans versions définies

```yaml
name: my-env
channels:
    - conda-forge
dependencies:
    - numpy
    - matplotlib
    - jupyterlab
```

:::

:::{card}
:header: Avec des versions bien précises

```yaml
name: my-env
channels:
    - conda-forge
dependencies:
    - numpy>1.20
    - matplotlib=3.7.1
    - jupyterlab>4.0,<4.1
```

:::

### Installer son environnement

#### Avec le fichier `requirements.txt`

- En utilisant `pipenv`

```bash
pipenv install -r requirements.txt
```

- En utilisant `mamba`

  Il faut d'abord créer un environnement avec la version Python que vous souhaitez

  ```bash
  mamba create -n my-env python
  ```

  puis l'activer

  ```bash
  mamba activate my-env
  ```

  Puis installer les dépendances

  ```bash
  mamba install --file requirements.txt
  ```

#### Avec le fichier `environment.yml`

Cet étape se fait uniquement avec `mamba`.

```bash
mamba env create --file environment.yml
```

Il ne reste plus qu'à activer l'environment

```bash
mamba activate my-env
```

:::{exercise}
Installer les dépendances pour cet atelier en utilisant soit `pipenv`, soit `mamba`.

Les fichiers `requirements.txt` et `environment.yml` se trouvent dans le répertoire `practical_session/configuration`.
:::

## Utilisation de uv

Il est également possible de construire son environnement via `uv` de manière incrémentale en ajoutant au fur et à mesure les dépendances de son projet et en créant un ensemble de tâches nous facilitant le travail.

La première chose à faire est d'installer `uv` en suivant ce lien: https://docs.astral.sh/uv/getting-started/installation/

Placez-vous dans le répertoire `practical_session`, puis initialiser l'environnement de développement en utilisant la commande suivante

```bash
uv init
```

Vous avez à présent un fichier `pyproject.toml` qui initialise votre environnement de développement. Il contient normalement au moins les éléments suivants

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []
```

Vous pouvez facilement ajouter vos dépendances à l'aide de la commande `uv add`.

```bash
uv add numpy
```

Vous pouvez mettre à jour votre environnement avec la commande

```bash
uv sync
```

## Utilisation de pixi

Il est également possible de construire son environnement via `pixi` de manière incrémentale en ajoutant au fur et à mesure les dépendances de son projet et en créant un ensemble de tâches nous facilitant le travail.

La première chose à faire est d'installer `pixi` en suivant ce lien: https://pixi.sh/latest/installation/

Placez-vous dans le répertoire `practical_session`, puis initialiser l'environnement de développement en utilisant la commande suivante

```bash
pixi init
```

Vous avez à présent un fichier `pixi.toml` qui initialise votre environnement de développement. Il contient normalement au moins les éléments suivants

```toml
[project]
name = "project name"
channels = ["conda-forge"]
platforms = ["osx-arm64"]

[tasks]

[dependencies]
```

La section `projet` vous permet de spécifier où aller chercher les paquets (ici `conda-forge`) et pour quel type de plateforme (ici `osx-arm64`).

Vous pouvez facilement ajouter vos dépendances à l'aide de la commande `pixi add`.

```bash
pixi add numpy
```

Si vous retournez dans le fichier `pixi.toml` vous devriez voir l'ajout de `numpy` dans les dépendances avec une version fixée. Un fichier `pixi.lock` a également été créé. Ce fichier contient l'arbre des dépendances permettant de réinstaller à l'identique votre environnement de développement.

Nous souhaiterions à présent que cet environnement soit installable sur différentes plateformes (linux, macos, windows). Nous allons ici ajouter la plateforme `linux-64` directement dans le fichier `pixi.toml`. Avec la commande

```bash
pixi update
```

nous mettons à jour `pixi.lock`.

Pour travailler dans l'environnement, vous disposez de deux commandes `pixi run`pour exécuter une ligne de commande ou `pixi shell` qui peut être vu comme l'équivalent de l'activation de l'environnement pour `mamba`.

:::{exercise}
Utiliser la commande `pixi run` pour voir la version Python installé dans l'environnement.
:::


:::{exercise}
Utiliser la commande `pixi shell` pour activer l'environnement. Jouer dans l'interpréteur Python en important, par exemple, `NumPy`.
:::

Nous ne rentrerons pas plus dans les détails de l'utilisation de `pixi` car ce n'est pas l'objet de cette formation. Vous verrez dans la suite de cette formation d'autres commandes qui pourront vous être utiles.