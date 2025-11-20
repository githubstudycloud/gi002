#!/usr/bin/env python3
"""
简单的健康检查HTTP服务
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """健康检查请求处理器"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'status': 'healthy',
                'service': 'chrome-automation',
                'timestamp': str(self.date_time_string())
            }

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """自定义日志"""
        logger.info("%s - %s" % (self.address_string(), format % args))


def main():
    """启动健康检查服务"""
    port = 8080
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"健康检查服务启动在端口 {port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("健康检查服务停止")
        server.shutdown()


if __name__ == '__main__':
    main()
