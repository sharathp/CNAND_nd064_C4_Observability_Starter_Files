# import pymongo

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics


# Export OpenTelemetry Traces/Spans to Jaeger
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = jaeger.JaegerSpanExporter(service_name='nd064course4-backend-service')
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
CORS(app)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)


@app.route('/')
def homepage():
    return "Hello World"


@app.route('/api')
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})


if __name__ == "__main__":
    app.run()
