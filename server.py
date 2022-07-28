import ssl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()
from logger import baseLogger
baseLogger(args.logs or "info")

from Configs import baseConfig

config = baseConfig()
api = config["API"]
SSL = config["SSL_API"]
export = config["EXPORT"]

from flask import Flask
from flask import send_from_directory
from flask_cors import CORS

from routes.data_collector.v1 import v1 as data_collector_api_v1
from routes.admin.v1 import v1 as admin_v1

from controllers.sync_database import create_database
from controllers.sync_database import create_tables
from controllers.sync_database import create_super_admin
from controllers.SSL import isSSL

from schemas.migration import migrate_labs

app = Flask(__name__)

CORS(
    app,
    origins=api["ORIGINS"],
    supports_credentials=True,
)

create_database()
create_tables()

migrate_labs()

create_super_admin()

app.register_blueprint(data_collector_api_v1, url_prefix="/v1")
app.register_blueprint(admin_v1, url_prefix="/v1/admin")

@app.route("/downloads/<path:path>")
def downloads(path):
    app.logger.debug("Requesting %s download ..." % path)
    return send_from_directory(directory="%s/datasets" % export["PATH"], path=path)

checkSSL = isSSL(path_crt_file=SSL["CERTIFICATE"], path_key_file=SSL["KEY"], path_pem_file=SSL["PEM"])

if __name__ == "__main__":
    if checkSSL:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(SSL["CERTIFICATE"], SSL["KEY"])

        app.logger.info("Running on secure port: %s" % SSL['PORT'])
        app.run(host=api["HOST"], port=SSL["PORT"], ssl_context=context)
    else:
        app.logger.info("Running on un-secure port: %s" % api['PORT'])
        app.run(host=api["HOST"], port=api["PORT"])