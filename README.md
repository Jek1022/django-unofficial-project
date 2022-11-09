# django-unofficial-project

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/Jek1022/django-unofficial-project.git
    $ cd django-unofficial-project
    
Activate the venv or you may refer to the official documentation for setting up the venv: https://docs.python.org/3.10/tutorial/venv.html
    
    source <my_env_name>/Scripts/activate
    
    
Create a new database "django_unofficial_project" in mysql.

    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
    
    
    
For any issues, please contact Jek.
