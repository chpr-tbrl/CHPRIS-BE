import logging
logger = logging.getLogger(__name__)

import os

from datetime import datetime
from datetime import timedelta

from werkzeug.exceptions import InternalServerError

def purge_export(max_days:int) -> None:
    """
    """
    try:
        logger.debug("removing export files older than %d day(s) ..." % max_days)

        export_filepath = os.path.abspath('datasets')
        date_limit = datetime.now() - timedelta(max_days)
        files = os.listdir(export_filepath)

        for file in files:
            file_path = os.path.abspath(os.path.join("datasets", file))
            filetime = datetime.fromtimestamp(os.path.getctime(file_path))
        
            if filetime < date_limit:
                os.remove(file_path)
                logger.info("- '%s' removed. Created: %s" % (file, filetime))

    except Exception as error:
        raise InternalServerError(error) from None