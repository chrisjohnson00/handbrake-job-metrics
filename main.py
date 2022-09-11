import pygogo as gogo
from metric_collector.metric_collector import MetricCollector
from flask import Flask
from prometheus_client import core, exposition

application = Flask(__name__)

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


@application.route('/')
def hello():
    return "Welcome to the Handbrake Job Exporter.  The metrics can be found on /metrics"


@application.route('/metrics')
def metrics():
    registry = core.CollectorRegistry(auto_describe=False)
    registry.register(MetricCollector())
    return exposition.generate_latest(registry)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080)
