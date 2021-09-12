import logging

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
# from opentelemetry import trace
# from opentelemetry.exporter import jaeger
# from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.sdk.trace import TracerProvider
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_opentracing import FlaskTracing
from requests_opentracing import SessionTracing


app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
CORS(app)
# FlaskInstrumentor().instrument_app(app)
# RequestsInstrumentor().instrument()


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


jaeger_tracer = init_tracer('nd064course4-trial-service')
# only trace requests explicitly annotated to be traced, this will prevent tracing "non-functional" requests
# such as prometheus /metrics
tracing = FlaskTracing(jaeger_tracer, False, app)


@app.route('/')
@tracing.trace()
def homepage():
    return render_template("main.html")
    with tracer.start_span('get-python-jobs') as span:
        homepages = []
        traced_session = SessionTracing(jaeger_tracer)
        res = traced_session.get('https://jobs.github.com/positions.json?description=python')
        span.set_tag('first-tag', len(res.json()))
        for result in res.json():
            try:
                homepages.append(requests.get(result['company_url']))
            except:
                return "Unable to get site for %s" % result['company']

    return jsonify(homepages)


if __name__ == "__main__":
    app.run(debug=True,)