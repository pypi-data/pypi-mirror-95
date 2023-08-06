# Splunk Handler

**Splunk Handler is a Python Logger for sending logged events to an installation of Splunk Enterprise.**

*This logger requires the destination Splunk Enterprise server to have enabled and configured the [Splunk HTTP Event Collector](http://dev.splunk.com/view/event-collector/SP-CAAAE6M).*

## A Note on Using with AWS Lambda

[AWS Lambda](https://aws.amazon.com/lambda/) has a custom implementation of Python Threading, and does not signal when the main thread exits. Because of this, it is possible to have Lambda halt execution while logs are still being processed. To ensure that execution does not terminate prematurely, Lambda users will be required to invoke splunk_handler.force_flush directly as the very last call in the Lambda handler, which will block the main thread from exiting until all logs have processed.
~~~python
from splunk_handler import force_flush

def lambda_handler(event, context):
    do_work()
    force_flush()  # Flush logs in a blocking manner
~~~

## Introduction

This package is based on the splunk_handler of [Zach Tylor](https://github.com/zach-taylor/splunk_handler).
The adjustment in this package enables json format in event that sent to spunk. Additionally, it is designed to
suit logging of [zuul components](https://zuul-ci.org/docs/zuul/discussion/components.html). Thus, the source-type
will reflect the zuul service and the event will contains eventId and buildId within zuul log.

## Installation

Pip:

    pip install splunk_handler_zuul

Manual:

    python setup.py install

## Usage

    from splunk_handler import SplunkHandler

Then use it like any other regular Python [logging handler](https://docs.python.org/2/howto/logging.html#handlers).

Example:

~~~python
    import logging
    from splunk_handler import SplunkHandler
    splunk = SplunkHandler(
        host='splunk.example.com',
        port='8088',
        token='851A5E58-4EF1-7291-F947-F614A76ACB21',
        index='main',
        record_format=True # will make the output as json
        #allow_overrides=True # whether to look for _<param in log data (ex: _index)
        #debug=True # whether to print module activity to stdout, defaults to False
        #flush_interval=15.0, # send batch of logs every n sec, defaults to 15.0, set '0' to block thread & send immediately
        #force_keep_ahead=True # sleep instead of dropping logs when queue fills
        #hostname='hostname', # manually set a hostname parameter, defaults to socket.gethostname()
        #protocol='http', # set the protocol which will be used to connect to the splunk host
        #proxies={
        #           'http': 'http://10.10.1.10:3128',
        #           'https': 'http://10.10.1.10:1080',
        #         }, set the proxies for the session request to splunk host
        #
        #queue_size=5000, # a throttle to prevent resource overconsumption, defaults to 5000, set to 0 for no max
        #record_format=True, whether the log format will be json
        #retry_backoff=1, the requests lib backoff factor, default options will retry for 1 min, defaults to 2.0
        #retry_count=5, number of retry attempts on a failed/erroring connection, defaults to 5
        #source='source', # manually set a source, defaults to the log record.pathname
        #sourcetype='sourcetype', # manually set a sourcetype, defaults to 'text'
        #verify=True, # turn SSL verification on or off, defaults to True
        #timeout=60, # timeout for waiting on a 200 OK from Splunk server, defaults to 60s
    )

    logging.getLogger('').addHandler(splunk)

    logging.warning('hello!')
~~~

### Logging Config

Sometimes it's a good idea to create a logging configuration using a Python dict
and the `logging.config.dictConfig` function. This method is used by default in Django.

Here is an example dictionary config and how it might be used in a settings file:

~~~python
import os

# Splunk settings
SPLUNK_HOST = os.getenv('SPLUNK_HOST', 'splunk.example.com')
SPLUNK_PORT = int(os.getenv('SPLUNK_PORT', '8088'))
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN', '851A5E58-4EF1-7291-F947-F614A76ACB21')
SPLUNK_INDEX = os.getenv('SPLUNK_INDEX', 'main')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(created)f %(exc_info)s %(filename)s %(funcName)s %(levelname)s %(levelno)s %(lineno)d %(module)s %(message)s %(pathname)s %(process)s %(processName)s %(relativeCreated)d %(thread)s %(threadName)s'
        }
    },
    'handlers': {
        'splunk': {
            'level': 'DEBUG',
            'class': 'splunk_handler.SplunkHandler',
            'formatter': 'json',
            'host': SPLUNK_HOST,
            'port': SPLUNK_PORT,
            'token': SPLUNK_TOKEN,
            'index': SPLUNK_INDEX,
            'sourcetype': 'json',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'splunk'],
            'level': 'DEBUG'
        }
    }
}
~~~

Here is an example file config, and how it might be used in a config file:

~~~
[loggers]
keys=root

[handlers]
keys=consoleHandler,splunkHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=%(loglevel)s
handlers=consoleHandler,splunkHandler

[handler_consoleHandler]
class=StreamHandler
level=%(loglevel)s
formatter=simpleFormatter
args=(sys.stdout,)

[handler_splunkHandler]
class=splunk_handler.SplunkHandler
level=%(loglevel)s
formatter=simpleFormatter
args=('my-splunk-host.me.com', '', os.environ.get('SPLUNK_TOKEN_DEV', 'changeme'), 'my_index')
kwargs={'url':'https://my-splunk-host.me.com/services/collector/event', 'verify': False, 'record_format': True}

[formatter_simpleFormatter]
class=pythonjsonlogger.jsonlogger.JsonFormatter
format=%(asctime)s %(levelname)s %(name)s %(message)s

~~~

## License

This project is licensed under the terms of the [MIT license](http://opensource.org/licenses/MIT).
