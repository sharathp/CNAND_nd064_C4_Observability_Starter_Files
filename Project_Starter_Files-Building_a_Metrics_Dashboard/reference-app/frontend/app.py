from flask import Flask, render_template, request

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

# Export OpenTelemetry Traces/Spans to Jaeger
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = jaeger.JaegerSpanExporter(service_name='nd064course4-frontend-service')
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()



@app.route('/')
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()