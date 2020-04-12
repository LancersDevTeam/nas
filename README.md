## Overview

A Python template intended for general purpose use, which uses Pipenv for package management.
We use Pipenv for package management.
It also generates documents using Sphinx for the tests folder.
They have also implemented a basic CI using CircleCI.

## How to use

1. Create a GitHub repository.

This time, I created a repository called new_project.
![image](https://user-images.githubusercontent.com/33741792/79072902-785be280-7d1e-11ea-9758-a5aa6ebbbdc9.png)

2. Start a new project based on this repository
```
git clone git@github.com:odrum428/python_setup.git new_poject
cd new_project
git remote set-url origin git@github.com:user_name/new_project.git
git push origin master
```

Now you can create a new project with this repository intact.
Check your GitHub repgitory.

3. install pipenv
```
pip install pipenv
```

finish. enjoy your develop!

bonus
4. using direnv
You can use direnv to automatically switch between Python environments. I highly recommend it, so be sure to include it.bonus
https://github.com/direnv/direnv

## Features.

### Document the contents of the tests/folder
The contents of tests/ are documented using Sphinx. The theme is sphinx_rtd_theme.

### Automatically update the document.
Using Circle CI, any changes to the tests/ folder will be automatically updated. If it has not been updated, the process is skipped.
Build the document in CI and then commit it.

### Keep the code style.
Use isort and flake8 to check the code.

### test is also set up.
We use pytest and Circle CI to process the test code.

## **COPYRIGHT**
MIT licence - Copyright (C) 2020 @odrum428
