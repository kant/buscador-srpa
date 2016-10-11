# Server

Instalación de dependencias 
```
sudo apt-get install git-all python-pip python-dev build-essential sqlite3 libsqlite3-dev
pip install virtualenv
git clone https://github.com/datosgobar/text-classifier.git
cd text-classifier/server/
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

```

## Para desarrollo

Levantar el server:
```
cd text-classifier/server/
. venv/bin/activate
python main.py
```

Para levantar un servidor smtp para desarrollo, correr `sudo python -m smtpd -n -c DebuggingServer localhost:25`

Documentaciones relevantes:
- [Flask Mail](https://pythonhosted.org/Flask-Mail/)
- [Flask User](https://pythonhosted.org/Flask-User/)
- [Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/)
- [Flask Babel](https://pythonhosted.org/Flask-Babel/)
- [Flask WTF](http://flask.pocoo.org/docs/0.11/patterns/wtforms/)
- [Poncho](http://argob.github.io/poncho/)