QR Code Creation and Tracking Service
=====================================

Summary
--------
This project is a web application built on Django and MySQL. If you are familiar with Django and setting up a MySQL database, the install should be straight forward.
Feel free to fork the codebase and use for personal or commercial use. See MIT License for more information.

Demo
-----
A working demo can be viewed at http://qrtrace.com

Getting Started
----------------
Section 1 - Installation
- install mysql-server, virtualenv
- in terminal at project's root, execute `virtualenv env`
- in terminal at project's root, execute `source env/bin/activate`
- in project's root, execute `pip install -r pip-requirements.txt`

Section 2 - Configuration
- copy web/conf/settings.example.py web/settings.py
- create mysql database
- add mysql credentials at appropriate section in web/settings.py
- add SECRET_KEY at appropriate line in web/settings.py
- in project's root, execute `python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser`

Section 3 - Starting Server
- to start server, in project's root, execute `python manage.py runserver`
- to access website, visit http://localhost:8000 in your browser

Section 4 - Post Configuration
- visit http://localhost:8000/admin and login with your superuser email and password
- click on Sites and change the example.com record display name and domain name to 'localhost'