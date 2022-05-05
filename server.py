import logging
server_logger = logging.getLogger(__name__)
from logger import logger
logger()

from Configs import configuration

config = configuration()
api = config["API"]

from flask import Flask

from routes.user_management.v1 import v1
from controllers.sync_database import create_database
from controllers.sync_database import create_tables

app = Flask(__name__)

create_database()
create_tables()

app.register_blueprint(v1, url_prefix="/v1")

if __name__ == "__main__":
    server_logger.info(f"Running on un-secure port: {api['PORT']}")
    app.run(host=api["HOST"], port=api["PORT"])