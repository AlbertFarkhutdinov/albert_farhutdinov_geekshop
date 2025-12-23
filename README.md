# albert_farhutdinov_geekshop

The training project on Django from [geekbrains.ru](https://geekbrains.ru/)
implemented by Albert Farkhutdinov.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

This project is implemented on Python 3.13.
It is recommended to run it in its own virtual environment.

Follow these steps to set up the project on your machine.

### 1. Clone the repository
Start by cloning the repository and navigating to the project directory:
```bash
git clone https://github.com/AlbertFarkhutdinov/albert_farhutdinov_geekshop.git
cd albert_farhutdinov_geekshop
```

### 2. Set Up a Virtual Environment & Install dependencies

Using a virtual environment is essential for isolating dependencies 
and maintaining a clean development setup. 

`uv` is a fast, modern Python package manager 
that handles both dependency installation and virtual environment creation.

To install `uv`, see [the documentation](https://docs.astral.sh/uv/).

After installing `uv`, install the project dependencies.

```bash
uv sync --frozen
```
This will automatically create a virtual environment 
and install all the packages 
listed in the `pyproject.toml` file within that environment.

`--frozen` allows to run installation without updating the `uv.lock` file.

Instead of checking if the lockfile is up-to-date,
uses the versions in the lockfile as the source of truth.
If the lockfile is missing, uv will exit with an error.
If the `pyproject.toml` includes changes to dependencies 
that have not been included in the lockfile yet,
they will not be present in the environment.

### 3. Prepare the Django project

3.1. Apply migrations:

```bash
python src/shop/manage.py makemigrations
python src/shop/manage.py migrate
```

3.2. Fill SQLite database.

```bash
python src/shop/manage.py fill_db
```

3.3. Also, you need access the Internet to display fonts correctly.

## Usage

You can run the following command in terminal from root directory to start a project:

```bash
python src/shop/manage.py runserver
```

Also. you can change directory to bat/ and use run.bat:

```bash
cd src/shop/bat
run
```
	
Now that the server’s running, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) with your Web browser.  
