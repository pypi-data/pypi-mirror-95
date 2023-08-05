# Koala-Analytics

Python package for fetching metric data from analytics source and pushing them  
to BigQuery.

## Supported analytics sources
* Prometheus

## Not yet implemented sources
* Amplitude
* Influx
* Google Analytics

## Examples
* ### Prometheus

````python
#Imports
from koala_analytics.prometheus_metrics import PrometheusMetrics


# Setting envs:
gcp_creds = {"project_id": "example_project"}
metrics = ["metric_name_example"]
api_url = "https://example_api.example"


# Init
prometheus = koala_analytics.PrometheusMetrics(api_url,
                                               metrics,
                                               table_id,
                                               gcp_creds)


# Fetching and writing to BigQuery
rows = prometheus.get_metrics()
prometheus.insert_rows_bq(table_id=table_id, rows=rows)
````