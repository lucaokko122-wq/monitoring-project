#!/usr/bin/env python3
"""
Простое тестовое приложение, которое отдает метрики Prometheus
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            # Генерируем простые метрики Prometheus
            metrics = f'''# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{{method="GET",status="200"}} {random.randint(100, 1000)}

# HELP app_uptime_seconds Application uptime in seconds
# TYPE app_uptime_seconds gauge
app_uptime_seconds {int(time.time() - start_time)}

# HELP memory_usage_bytes Simulated memory usage
# TYPE memory_usage_bytes gauge
memory_usage_bytes {random.randint(1000000, 50000000)}

# HELP cpu_usage_percent Simulated CPU usage
# TYPE cpu_usage_percent gauge
cpu_usage_percent {random.uniform(1.0, 80.0):.2f}
'''

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(metrics.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
            <html>
            <head><title>Test Application</title></head>
            <body>
            <h1>Test Application is running!</h1>
            <p>Metrics available at: <a href="/metrics">/metrics</a></p>
            </body>
            </html>
            ''')


if __name__ == '__main__':
    start_time = time.time()
    server = HTTPServer(('0.0.0.0', 8080), MetricsHandler)
    print('Starting test application on port 8080...')
    print('Metrics: http://localhost:8080/metrics')
    server.serve_forever()