from diagrams import Cluster, Diagram
from diagrams.generic.device import Mobile, Tablet
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Kong
from diagrams.programming.framework import FastAPI

with Diagram("Hash Retail Backend API Microservice Architecture", show=False):
    with Cluster("Consumers"):
        consumers = [Tablet(), Mobile()]

    api_gateway = Kong("Kong API Gateway")
    metrics = Prometheus("Prometheus")
    monitoring = Grafana("Grafana")

    consumers >> api_gateway << metrics << monitoring

    with Cluster("API Cluster"):
        api = [
            FastAPI("API Instance"),
            FastAPI("API Instance"),
        ]

    with Cluster("PostgreSQL HA"):
        main = PostgreSQL("Master")
        main - PostgreSQL("Slave")
        api >> main

    aggregator = Fluentd("Fluentd")
    api_gateway >> api >> aggregator << metrics

    with Cluster("External Services"):
        services = Server("gRPC Service")
        services - Server("Private API")
        api >> services
