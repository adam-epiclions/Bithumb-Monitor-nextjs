"""
Vercel Serverless Function Entry Point
Flask 앱을 Vercel의 serverless function으로 래핑
"""
import sys
import os

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Vercel 환경에서만 모니터 스레드 시작
if os.environ.get('VERCEL'):
    from web_monitor import monitor, monitor_balances
    import threading
    # 모니터 스레드 시작 (한 번만)
    if not hasattr(monitor_balances, '_started'):
        monitor_thread = threading.Thread(target=monitor_balances, daemon=True)
        monitor_thread.start()
        monitor_balances._started = True

from web_monitor import app

# Vercel의 WSGI 어댑터
def wsgi_handler(environ, start_response):
    """Vercel이 호출하는 WSGI 핸들러"""
    return app(environ, start_response)

