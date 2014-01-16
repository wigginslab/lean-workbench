import os
from main import app_factory
import config

app = app_factory(config.Dev)
if __name__ == "__main__":
	app.run()
