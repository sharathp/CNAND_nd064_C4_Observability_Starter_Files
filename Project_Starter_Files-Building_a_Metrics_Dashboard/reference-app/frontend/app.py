import logging

from flask import Flask, render_template, request

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_opentracing import FlaskTracing


app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service)
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


jaeger_tracer = init_tracer('nd064course4-frontend-service')
# only trace requests explicitly annotated to be traced, this will prevent tracing "non-functional" requests
# such as prometheus /metrics
tracing = FlaskTracing(jaeger_tracer, False, app)


@app.route('/')
@tracing.trace()
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()