import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()
from logger import baseLogger
baseLogger(args.logs or "info")

from Configs import baseConfig

config = baseConfig()
api = config["API"]

from flask import Flask
from flask_cors import CORS

from routes.data_collector.v1 import v1 as data_collector_api_v1
from routes.admin.v1 import v1 as admin_v1

from controllers.sync_database import create_database
from controllers.sync_database import create_tables

app = Flask(__name__)
CORS(app)

create_database()
create_tables()

app.register_blueprint(data_collector_api_v1, url_prefix="/v1")
app.register_blueprint(admin_v1, url_prefix="/v1/admin")

if __name__ == "__main__":
    app.logger.info("Running on un-secure port: %s" % api["PORT"])
    app.run(host=api["HOST"], port=api["PORT"])