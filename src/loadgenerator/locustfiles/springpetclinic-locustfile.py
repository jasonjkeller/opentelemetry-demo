from locust import task, run_single_user, between
from locust import FastHttpUser

from opentelemetry import context, baggage, trace
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

exporter = OTLPMetricExporter(insecure=True)
set_meter_provider(MeterProvider([PeriodicExportingMetricReader(exporter)]))

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

# Instrumenting manually to avoid error with locust gevent monkey
Jinja2Instrumentor().instrument()
RequestsInstrumentor().instrument()
SystemMetricsInstrumentor().instrument()
URLLib3Instrumentor().instrument()


class PetClinicUser(FastHttpUser):
    host = "http://localhost:8087"

    @task(1)
    def get_home(self):
        self.client.get("/")

    @task(2)
    def get_error(self):
        self.client.get("/oups")

    @task(3)
    def get_vets(self):
        self.client.get("/vets.html")

    @task(4)
    def get_vets_page_2(self):
        self.client.get("/vets.html?page=2")

    @task(5)
    def get_find_owners(self):
        self.client.get("/owners/find")

    @task(6)
    def post_add_owner(self):
        # FIXME POST not working
        self.client.post("/owners/new?firstName=Bo&lastName=Diddley&address=123+St.&city=Chicago&telephone=1234567890")

    @task(7)
    def get_owner(self):
        self.client.get("/owners/1")


if __name__ == "__main__":
    run_single_user(PetClinicUser)
