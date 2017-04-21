import warnings
from flask.exthook import ExtDeprecationWarning
warnings.filterwarnings("ignore", category=ExtDeprecationWarning)
from app.create_app import create_app, create_db, create_user
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
        create_db()
    elif len(sys.argv) > 1 and sys.argv[1] == 'create_user':
        create_user()
    else:
        app = create_app()
        app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
