# Runtime environment setup in Linux and MacOS

# create and activate a virtual python environment

# Mac
$ python3 -m venv venv
$ . venv/bin/activate

# Windows
py -3 -m venv venv 
venv\Scripts\activate

# install runtime environment

# Mac
$ pip3 install -r requirements.txt

# Windows
# comment uWSGI library
pip3 install -r requirements.txt

# select python: interpreter from view -> command palette in VS Code

# set start up app

$ export FLASK_APP=app.py

# run app

$ flask run

# Using Python environments in VS Code

# https://code.visualstudio.com/docs/python/environments
