# app finnaciera

### run local

1. create virtual enviroment

    ```"python -m venv env" ```

2. isntall dependecias

    ```pip install -r requierement.txt ```

3. run app
    ```
    cd app_finaciera 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver