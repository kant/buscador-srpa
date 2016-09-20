# Server

```
virtualenv --no-site-packages venv-server
. venv-server/bin/activate
pip install -r requirements.txt

```

## Para desarrollo

```
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run
```

Para levantar un servidor smtp para desarrollo, correr `sudo python -m smtpd -n -c DebuggingServer localhost:25`

Documentaciones relevantes:
- [Flask Mail](https://pythonhosted.org/Flask-Mail/)
- [Flask User](https://pythonhosted.org/Flask-User/)