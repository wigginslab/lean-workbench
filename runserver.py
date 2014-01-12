import os
from lean_workbench import app

def runserver():
	port = int(os.environ.get('port', 8000))
	app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
	runserver()
