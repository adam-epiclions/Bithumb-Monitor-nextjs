"""
AWS 서버에서 실행할 API 서버
- REST API 제공 (잔고 데이터)
- 텔레그램 알림 (백그라운드)
- CORS 설정으로 Vercel에서 접근 가능
"""
from flask import Flask, jsonify
from flask_cors import CORS
from balance_monitor import BalanceMonitor
import threading
import logging
import os
import time

# flask-cors 설치 필요: pip install flask-cors

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

app = Flask(__name__)
# CORS 설정: Vercel 도메인에서 접근 허용
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://*.vercel.app", "http://localhost:3000"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

monitor = BalanceMonitor()

# 전역 변수로 최신 잔고 데이터 저장
latest_balances = {}
balance_lock = threading.Lock()

def monitor_balances_background():
    """백그라운드에서 잔고 모니터링 및 텔레그램 알림"""
    global latest_balances
    
    while True:
        try:
            if not monitor.apis:
                logger.warning("등록된 API가 없습니다.")
                import time
                time.sleep(10)
                continue
                
            price_cache = list(monitor.apis.values())[0].get_all_prices()
            current_balances = {}

            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=14) as executor:
                futures = {
                    executor.submit(monitor.get_total_balance, api_name, price_cache): api_name
                    for api_name in monitor.apis
                }

                for future in futures:
                    api_name = futures[future]
                    try:
                        current_balance = future.result()
                        if current_balance is None:
                            continue

                        if monitor.initial_balances.get(api_name) is None:
                            monitor.initial_balances[api_name] = current_balance
                        if monitor.previous_balances.get(api_name) is None:
                            monitor.previous_balances[api_name] = current_balance

                        change = current_balance - monitor.previous_balances[api_name]
                        total_change = current_balance - monitor.initial_balances[api_name]
                        monitor.previous_balances[api_name] = current_balance

                        current_balances[api_name] = {
                            'current_balance': current_balance,
                            'change': change,
                            'total_change': total_change
                        }

                    except Exception as e:
                        logger.warning(f"[{api_name}] 잔고 조회 실패: {str(e)}")

            # 최신 데이터 업데이트
            with balance_lock:
                latest_balances = current_balances.copy()

            # 텔레그램 알림 로직
            import time
            now = time.time()
            if not hasattr(monitor, 'last_report_time'):
                monitor.last_report_time = 0
                
            if now - monitor.last_report_time >= 300:  # 5분마다 리포트
                from balance_monitor import send_telegram_message
                report_lines = ["📊 <b>총 자산 안내</b>\n"]
                first_risk = []
                second_risk = []
                
                for i, name in enumerate(monitor.account_names, start=1):
                    api = f"bithumb_{i}"
                    start = monitor.initial_balances.get(api)
                    current = monitor.previous_balances.get(api)
                    if not start or not current:
                        continue
                    delta = current - start
                    report_lines.append(
                        f"{i}. {name}   시작: {start:,.0f}원   현재: {current:,.0f}원   변화: {delta:+,.0f}원"
                    )

                    기준금액 = 50000000 if i == 1 else 300000000
                    loss_rate = (기준금액 - current) / 기준금액
                    if loss_rate >= 0.15:
                        second_risk.append(f"{i}. {name}   {current:,.0f}원")
                    elif loss_rate >= 0.10:
                        first_risk.append(f"{i}. {name}   {current:,.0f}원")

                send_telegram_message("\n".join(report_lines))
                if first_risk:
                    send_telegram_message("⚠️ 1차 청산위험 (기준 대비 10% 손실)\n" + "\n".join(first_risk))
                if second_risk:
                    send_telegram_message("🚨 2차 청산위험 (기준 대비 15% 손실)\n" + "\n".join(second_risk))
                monitor.last_report_time = now

            time.sleep(1)

        except Exception as e:
            logger.error(f"오류 발생: {str(e)}")
            time.sleep(1)

@app.route('/api/balances', methods=['GET'])
def get_balances():
    """잔고 데이터 API 엔드포인트"""
    with balance_lock:
        return jsonify({
            'success': True,
            'data': latest_balances,
            'timestamp': os.environ.get('LAST_UPDATE_TIME', '')
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'ok',
        'apis_count': len(monitor.apis)
    })

if __name__ == '__main__':
    import os
    
    # 백그라운드 모니터링 스레드 시작
    monitor_thread = threading.Thread(target=monitor_balances_background, daemon=True)
    monitor_thread.start()
    logger.info("백그라운드 모니터링 스레드 시작됨")
    
    # 포트 설정
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"API 서버 시작: http://{host}:{port}")
    logger.info(f"API 엔드포인트: http://{host}:{port}/api/balances")
    
    app.run(debug=False, host=host, port=port)

