import warnings
from flask.exthook import ExtDeprecationWarning
warnings.filterwarnings("ignore", category=ExtDeprecationWarning)
from app.create_app import create_app, create_db, create_user, list_users, add_user_role, remove_user_role
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
        create_db()
    elif len(sys.argv) > 1 and sys.argv[1] == 'list_users':
        list_users()
    elif len(sys.argv) > 1 and sys.argv[1] == 'create_user':
        create_user()
    elif len(sys.argv) > 1 and sys.argv[1] == 'add_user_role':
        add_user_role()
    elif len(sys.argv) > 1 and sys.argv[1] == 'remove_user_role':
        remove_user_role()
    else:
        app = create_app()
        app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
