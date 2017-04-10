from app.create_app import create_app, create_db
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
        create_db()
    else:
        app = create_app()
        app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
