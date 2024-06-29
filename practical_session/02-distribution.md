# Distribuer son application

:::{note} Les objectifs de cette partie
- Comprendre comment créer les différentes versions de son application
- Pouvoir mettre ses versions sur PyPi
- Pouvoir mettre ses versions sur conda
:::

Vous avez deux types de paquets Python

- un paquet que l'on dit pur Python, c'est-à-dire qu'il ne contient pas de partie qui doit être compilée.
- un paquet avec des modules compilés comme ceux vus précédemment avec l'utilisation de `cython`.

Dans le premier cas, la distribution est assez simple puisqu'elle ne dépend que de la version de Python. Le paquet peut s'installer sur n'importe quel système d'exploitation en copiant juste les fichiers Python au bon endroit.

Dans le cas de bout compilé, les choses se compliquent un peu, car il faut fournir des binaires et, par conséquent, il y a une dépendance au système d'exploitation, au compilateur utilisé... En d'autres termes, si vous souhaitez distribuer ce genre de paquet sur tous les systèmes d'exploitation, vous devez les avoir à votre disposition pour pouvoir créer les bons binaires.

Heureusement, vous n'êtes pas obligés d'avoir plusieurs machines pour réaliser cette opération. L'intégration continue peut grandement vous faciliter la vie comme nous le verrons à la fin de cette formation.

Les gestionnaires de paquets dans l'univers Python sont au nombre de deux : pypi et conda. Nous verrons dans la suite comment rendre disponible son application sur ces deux gestionnaires.

## PyPi

Nous allons dans un premier temps nous intéresser à PyPi. Maintenant que nous avons un fichier `pyproject.toml` qui explique comment construire le package ainsi que ces dépendances, nous sommes en mesure de construire des distributions.

:::{attention}
Nous utiliserons dans la suite le package `build` pour créer les différentes versions.
:::

Dans PyPi, elles peuvent être de deux sortes

### Archive et wheel

- `sdist` crée une archive de votre package.

    Lorsqu'un utilisateur utilise `pip` pour l'installer, l'archive est téléchargée puis la commande `pip install` est exécutée comme vu précédemment. La ligne de commande

    ```bash
    python -m build --sdist
    ```

    crée une archive dans le répertoire `dist`.

- `bdist` crée un binaire et est donc spécifique à une plateforme si des modules sont compilés. Ceci permet d'avoir une installation beaucoup plus rapide du fait qu'il n'y a pas de processus de compilation. Ce binaire est appelé `wheels` et est obtenu à partir de la ligne de commande

  ```bash
  python -m build --wheel
  ```

  Il existe plusieurs variantes :

    1. Lorsque le package ne contient que des fichiers Python.

       On a alors dans le répertoire `dist` le fichier `calculator-0.1.1-py3-none-any.whl`.

    2. Lorsque le package contient des fichiers compilés.

       On a alors dans le répertoire `dist` le fichier `calculator-0.1.0-cp312-cp312-macosx_11_0_arm64.whl`. Ce fichier nous renseigne sur la version Python, l'OS et le type d'architecture pour qui est destiné ce binaire. Dans toute autre configuration, le binaire ne sera pas installable.
       Il vous faut donc toutes les variantes pour pouvoir avoir l'ensemble de binaires.

       :::{note}
       C'est là que les systèmes d'intégration entre en jeu et plus particulièrement [github action](https://docs.github.com/fr/actions).

       On pourra regarder notamment [cbuildwhell](https://cibuildwheel.readthedocs.io).
       :::

:::{exercise}
Ajoutez le paquet `build` via la commande `pixi` dans une `feature` que l'on nommera `pypi-release` (voir https://pixi.sh/v0.20.1/reference/cli/#add).
:::

:::{exercise}
Créez l'environnement associé qui portera le nom `publish` (voir https://pixi.sh/latest/reference/cli/#project-environment-add)
:::

:::{exercise}
- Créez une tâche via `pixi` qui construit le paquet via `sdist`
- Créez une tâche via `pixi` qui construit le paquet via `wheel`
:::

:::{note}
Voir https://pixi.sh/latest/reference/cli/#task-add.
:::

:::{exercise}
Testez les deux tâches et vérifiez dans le répertoire `dist` les deux paquets créés.
:::

Maintenant que vous avez les différentes versions, vous pouvez les mettre sur PyPi pour que d'autres personnes puissent utiliser votre application.

### twine

`twine` permet de mettre les distributions créées se trouvant dans le répertoire `dist` sur PyPi. Il existe deux sites

- https://pypi.org/ (le site officiel)
- https://test.pypi.org/ (le site pour faire des tests)

Avant d'utiliser `twine`, il est nécessaire de se créer un compte

- https://pypi.org/account/register/
- https://test.pypi.org/account/register/

Pour mettre l'ensemble des distributions sur

- `pypi.org`

    ```bash
    twine upload dist/*
    ```

- `test.pypi.org`

    ```bash
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    ```

Une fois que vous avez effectué l'upload, vous pouvez rechercher votre application

- `pypi.org`

    ```bash
    pip search calculator
    ```

- `test.pypi.org`

    ```bash
    pip search --index https://testpypi.python.org/pypi calculator
    ```

:::{tip} Configuration de PyPi

Pour éviter de taper son mot de passe à chaque fois, il est possible d'écrire un fichier `~/.pypirc` avec les informations suivantes

```
[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxx

[testpypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxx
```

:::

:::{exercise}
Créez un compte sur https://test.pypi.org/ et un token pour pouvoir uploader des fichiers.
:::

:::{exercise}
Créez un fichier `.pypirc` avec le token créé précédemment.
:::

:::{exercise}
Ecrivez une tâche appelée pypi-upload qui permet de faire les tâches `sdist`et `bdist` et qui utilise `twine` pour uploader les fichiers sur `testpypi`.
:::

:::{exercise}
Testez l'installation du paquet.
:::

:::{caution} Attention
Les noms des paquets sur pypi sont uniques. Il ne peut donc pas y avoir plusieurs projets appelés `splinart`. Vous devez faire en sorte que le paquet que vous allez créer est un nom unique et différentiable.
:::

## conda

Il est également possible de mettre son package sur conda. Comme pour PyPi, il est nécessaire de se créer un compte pour pouvoir avoir sa propre `channel` ([https://anaconda.org/](https://anaconda.org/)).

Il est ensuite nécessaire d'installer différents outils pour pouvoir uploader vos fichiers.

```bash
conda install conda-build anaconda-client
```

Il est possible d'installer des packages qui ne sont pas forcément écrits en Python.

[`conda-forge`](https://conda-forge.org/) est un endroit où l'on peut trouver ces packages.

Le but est d'écrire des recettes permettant de compiler le projet sur différentes plateformes (linux, mac OSX, windows).

Le processus de soumission peut être assez long, c'est pourquoi nous utiliserons notre propre channel dans la suite. Si vous souhaitez mettre vos applications sur `conda-forge` (ce qui est une très bonne idée, car cela offre plus de visibilité que sur sa propre channel), il suffit d'aller ici : [https://conda-forge.org/docs/maintainer/00_intro.html](https://conda-forge.org/docs/maintainer/00_intro.html).

(conda-recipe)=
### Création d'une recette

Pour que conda puisse construire le binaire de votre application, il lui faut plusieurs fichiers que l'on retrouve généralement dans un répertoire `recipes`.

- `meta.yaml`

   Ce fichier définit l'ensemble des méta données de la recette permettant de créer le package conda (voir [https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html))

- `build.sh`

    Ce fichier indique comment construire des parties qui ne peuvent pas être produite par la recette (compilation, ajout de fichiers externes...) pour les systèmes linux et macos.

- `build.bat`

    Ce fichier indique comment construire des parties qui ne peuvent pas être produite par la recette (compilation, ajout de fichiers externes...) pour le système windows.


Nous ne verrons ici que l'écriture d'un fichier `meta.yaml`. Reprenons l'exemple de l'application `calculator` et regardons ce que ça donne

```yaml
{% set name = "calculator" %}
{% set version = "0.1.1" %}

package:
  name: '{{ name|lower }}'
  version: '{{ version }}'

source:
  path: ../

build:
  number: 0
  script: python setup.py install

requirements:
  build:
    - python
    - setuptools
    - cython
  run:
    - python

test:
  imports:
    - calculator

about:
  home: http://github.com/gouarin/calculator
  license: MIT
  description: Simple calculator project

extra:
  recipe-maintainers: Loic Gouarin <loic.gouarin@gmail.com>
```

Une fois les fichiers du répertoire `recipes` sont écrits, il faut exécuter la commande suivante

```bash
conda build recipes
```

À la fin de la procédure, vous devriez voir où il a mis le package en local. Vous pouvez alors essayer de l'installer en faisant

```bash
conda install --use-local calculator
```

:::{exercise}
En s'inspirant de l'exemple du fichier `meta.yaml` précédent, écrivez celui pour le projet `splinart`.
:::

:::{exercise}
Ajoutez une feature qui installe `conda-build` et `anaconda-client` et ajoutez cette feature à l'environnement `publish`.
:::

:::{exercise}
Ajoutez une tâche qui fait l'étape du `conda-build`. Testez localement l'installation de votre application.
:::

:::{caution} Attention
Il n'est pas possible de construire un paquet conda au même niveau que les sources. Or `conda-build` est installé dans l'environnement par `pixi` qui se trouve dans le répertoire `.pixi` au même niveau que les sources. Si vous ne dites rien à `conda-build`, vous aurez un message d'erreur.
Pour corriger ce problème, il vous suffit de spécifier un autre répertoire pour la construction du paquet conda via l'option `-croot`.
:::

### Uploader le paquet

Si tout s'est bien passé, vous pouvez à présent le mettre sur anaconda dans votre channel pour que d'autres puissent l'installer. Il vous faut pour cela `anaconda-client`.

```bash
conda install anaconda-client
```

Vous pouvez maintenant l'uploader.

```bash
anaconda upload /home/loic/miniconda3/conda-bld/linux-64/calculator-0.1.1-py36h585410b_0.tar.bz2
```

:::{exercise}
Ajoutez une tâche qui dépend de la tâche réalisée précédemment pour le `conda-build` et qui transfert le paquet conda sur votre channel.
:::

## Références

- [Python Packaging User Guide](https://packaging.python.org/)
- [Les aventuriers du packaging perdu](https://youtu.be/Y5xMQYw9lls)
- [Inside the Cheeseshop: How Python Packaging Works](https://www.youtube.com/watch?v=AQsZsgJ30AE)
