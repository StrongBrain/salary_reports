===================
Project description
===================

  - This project reads the data from .csv files and stores it into SQLite database
  - Runs a Flask webserver to make it possible to review stored data via browser
  - Added some basic filters on UI side to filter data by salary

=============
Prerequisites
=============

To start this project under Ubuntu (or EC2 instance with Ubuntu) you'll need:

  - virtualenv (to isolate Python's installed libraries)

===========
Preparation
===========

  - Create your virtual environment (it's recommended to create it
  in the project's directory):

      `virtualenv venv`

  - Activate your virtual environment:

      `. venv/bin/activate`

  - Install required Python's dependencies:

      `pip install -r requirements.txt`

  Well, your environment is ready!

==================================================
Move the data from .csv files into SQLite database
==================================================

  To move all the data from your .csv files stored in `data` folder please run:

    `python create_databases.py`

  If everything is OK, `salaries.sqlite` file will appear in your folder.

============================
Startup your web application
============================

  To start your web application please run:

    `python web_app.py &`

  It starts a webserver on `5000` port.

  To make sure everything works fine, open your browser and check it:

    http://<your_ip_address>:5000

  If you're running this under AWS EC2 instance it requires to open inbound traffic for `5000` port.