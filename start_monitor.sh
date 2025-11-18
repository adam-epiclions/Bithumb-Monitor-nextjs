#!/bin/bash

# 가상환경 활성화
source ~/venv/bin/activate

# 작업 디렉토리 이동
cd ~/project/Bithumb-Balance-Monitor-master

# ngrok 실행 (고정 도메인 config 기반)
nohup ~/.config/ngrok/ngrok start --all > ngrok.log 2>&1 &

# 웹 모니터 실행
nohup python web_monitor.py > web.log 2>&1 &
