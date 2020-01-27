# albert_farhutdinov_geekshop

Welcome! My name is Albert Farhutdinov. This is my realization of training project on Django from [geekbrains.ru](https://geekbrains.ru/). 

## Requirements

1. Before you start, make sure that you have Python 3.7 or later versions. Input this command into terminal:

		python --version

2. Install the necessary libraries in your environment:

		pip install -r requirements.txt
	
3. Apply migrations:

		python manage.py migrate

4. Fill SQLite database.

		python manage.py fill_db

5. Also, you need access the Internet to display fonts correctly.

## Start

You can run the following command in terminal from root directory to start a project:

	python manage.py runserver
	
Also. you can change directory to bat/ and use run.bat:

	cd bat
	run
	
Now that the server’s running, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) with your Web browser.  
