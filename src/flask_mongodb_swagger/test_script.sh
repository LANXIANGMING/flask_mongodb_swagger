. venv/bin/activate
export SECRET_KEY="super secret guy"
export USER_DATABASE_URL="localhost"
export USER_DATABASE_USER=root
export USER_DATABASE_PASSWORD=sdasdeqda
export USER_DATABASE_PORT=27017

python -m unittest test/integration/test_login.py 
