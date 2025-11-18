from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template
from flask_socketio import SocketIO
from balance_monitor import BalanceMonitor
import threading
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

app = Flask(__name__)
socketio = SocketIO(app)

monitor = BalanceMonitor()

def monitor_balances():
    """잔고 모니터링 스레드"""
    while True:
        try:
            price_cache = list(monitor.apis.values())[0].get_all_prices()
            current_balances = {}

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

            if current_balances:
                socketio.emit('balance_update', current_balances)

            socketio.sleep(1)

        except Exception as e:
            logger.error(f"오류 발생: {str(e)}")
            socketio.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    import os
    # 포트는 환경 변수에서 가져오거나 기본값 8080 사용
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # ngrok 도메인 (로컬/EC2에서만 사용)
    public_url = os.environ.get('PUBLIC_URL', "https://trusting-kite-sound.ngrok-free.app")
    if public_url:
        logger.info(f"🔗 Public URL: {public_url}")

    monitor_thread = threading.Thread(target=monitor_balances, daemon=True)
    monitor_thread.start()

    socketio.run(app, debug=False, host=host, port=port, allow_unsafe_werkzeug=True)
