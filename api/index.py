"""
Vercel Serverless Function Entry Point
Flask 앱을 Vercel의 serverless function으로 래핑
"""
import sys
import os

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_monitor import app

# Vercel은 이 handler를 사용합니다
def handler(request):
    return app(request.environ, request.start_response)

# Vercel의 WSGI 어댑터를 위해
def wsgi_handler(environ, start_response):
    return app(environ, start_response)

