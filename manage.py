from lean_workbench import app
from lean_workbench.core import db
import sys

if len(sys.argv) > 1:
	cmd = sys.argv[1]
	if cmd == "syncdb":
		db.create_all()
	if cmd == "dropdb":
		db.drop_all()
