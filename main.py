from metric_collector.metric_collector import MetricCollector
from flask import Flask
from prometheus_client import core, exposition

application = Flask(__name__)


@application.route('/')
def hello():
    return "Welcome to the Handbrake Job Exporter.  The metrics can be found on /metrics"


@application.route('/metrics')
def metrics():
    registry = core.CollectorRegistry(auto_describe=False)
    registry.register(MetricCollector(logger=application.logger))
    return exposition.generate_latest(registry)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080)
