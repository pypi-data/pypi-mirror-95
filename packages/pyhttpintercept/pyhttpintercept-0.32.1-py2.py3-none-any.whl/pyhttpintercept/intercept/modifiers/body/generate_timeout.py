# encoding: utf-8

u"""
============================================================
Delays the response for a number of seconds.
------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : wait value in seconds
============================================================
"""

import time
import logging_helper
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    # Setup parameters
    wait = (float(modifier.params)
            if modifier.params
            else 0)  # Set a default timeout

    logging.info(u'Generating timeout for {wait} seconds'
                 .format(wait=wait))

    # Wait
    time.sleep(wait)

    logging.debug(u'Timeout elapsed, continuing...')

    return response
