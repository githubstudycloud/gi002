#!/usr/bin/env python3
"""
Flask Web服务 - 提供API接口触发百度搜索
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from baidu_search import BaiduSearchAutomation

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/web_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('WebService')

# 创建Flask应用
app = Flask(__name__)

# 全局自动化实例（每次请求创建新的）
automation = None


@app.route('/')
def index():
    """首页"""
    return jsonify({
        'service': 'Chrome Selenium自动化服务',
        'version': '1.0.0',
        'endpoints': {
            '/': 'API首页',
            '/health': '健康检查',
            '/search': '触发百度搜索 (GET/POST)',
            '/search?keyword=关键词': '搜索指定关键词'
        },
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'chrome-automation',
        'timestamp': datetime.now().isoformat(),
        'chrome_available': os.path.exists('/usr/bin/google-chrome'),
        'chromedriver_available': os.path.exists('/usr/local/bin/chromedriver')
    })


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    触发百度搜索

    参数:
        keyword: 搜索关键词（可选，默认"茶叶"）

    示例:
        GET  /search
        GET  /search?keyword=Python
        POST /search -d '{"keyword": "Selenium"}'
    """
    # 获取关键词
    if request.method == 'POST':
        data = request.get_json() or {}
        keyword = data.get('keyword', '茶叶')
    else:
        keyword = request.args.get('keyword', '茶叶')

    logger.info(f"收到搜索请求，关键词: {keyword}")

    # 创建自动化实例
    automation = BaiduSearchAutomation(logger=logger)

    try:
        # 执行搜索
        result = automation.search_baidu(keyword)

        # 返回结果
        if result['success']:
            logger.info(f"搜索成功: {keyword}")
            return jsonify({
                'success': True,
                'message': '搜索完成',
                'data': result
            }), 200
        else:
            logger.error(f"搜索失败: {result.get('error')}")
            return jsonify({
                'success': False,
                'message': '搜索失败',
                'error': result.get('error'),
                'data': result
            }), 500

    except Exception as e:
        error_msg = f"服务器错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({
            'success': False,
            'message': error_msg,
            'error': str(e)
        }), 500

    finally:
        # 关闭浏览器
        automation.close()


@app.route('/test', methods=['GET'])
def test():
    """快速测试接口"""
    logger.info("执行快速测试")

    try:
        # 测试Chrome是否可用
        import subprocess
        chrome_version = subprocess.check_output(['google-chrome', '--version'], text=True).strip()
        driver_version = subprocess.check_output(['chromedriver', '--version'], text=True).strip()

        return jsonify({
            'success': True,
            'message': '测试通过',
            'chrome_version': chrome_version,
            'chromedriver_version': driver_version,
            'python_version': sys.version,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"测试失败: {e}")
        return jsonify({
            'success': False,
            'message': '测试失败',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # 确保日志目录存在
    os.makedirs('/app/logs', exist_ok=True)
    os.makedirs('/app/screenshots', exist_ok=True)

    # 启动Flask应用
    port = int(os.getenv('APP_PORT', 8080))
    logger.info(f"启动Flask服务在端口 {port}")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    )
