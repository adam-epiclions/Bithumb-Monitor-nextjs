from concurrent.futures import ThreadPoolExecutor
from bithumb_api import BithumbAPI
from datetime import datetime
import requests
import time
import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)
logging.getLogger("urllib3").setLevel(logging.WARNING)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

class BalanceMonitor:
    def __init__(self):
        self.apis = {}
        self.previous_balances = {}
        self.initial_balances = {}
        self.warning_threshold = 50000
        self.logger = logging.getLogger(__name__)
        self.account_names = [
            "정*호", "김*현", "이*우", "김*민", "박*원", "장*민", "김*수",
            "박*영", "이*근", "이*석", "김*옥", "임*희", "이*도"
        ]
        self.last_report_time = 0

        for i in range(1, len(self.account_names) + 1):
            access_key = os.getenv(f'BITHUMB_ACCESS_KEY_{i}')
            secret_key = os.getenv(f'BITHUMB_SECRET_KEY_{i}')
            if access_key and secret_key:
                try:
                    api = BithumbAPI(account_number=i)
                    self.add_api(f"bithumb_{i}", api)
                    self.logger.info(f"계정 {i} API 추가 성공")
                except Exception as e:
                    self.logger.error(f"계정 {i} API 추가 실패: {str(e)}")

    def add_api(self, name, api):
        self.apis[name] = api
        self.previous_balances[name] = None
        self.initial_balances[name] = None

    def get_total_balance(self, api_name, price_cache):
        try:
            api = self.apis[api_name]
            accounts = api.get_accounts()
            total_balance = 0
            for account in accounts:
                currency = account['currency']
                balance = float(account['balance'])
                locked = float(account['locked'])
                total = balance + locked
                if currency == 'KRW':
                    total_balance += total
                else:
                    price = price_cache.get(currency)
                    if price:
                        total_balance += total * price
            return total_balance
        except Exception as e:
            self.logger.error(f"{api_name} 잔고 조회 실패: {str(e)}")
            return None

    def monitor(self):
        while True:
            try:
                current_balances = {}
                sample_api = next(iter(self.apis.values()), None)
                if not sample_api:
                    self.logger.error("등록된 API가 없습니다.")
                    return
                price_cache = sample_api.get_all_prices()

                with ThreadPoolExecutor(max_workers=14) as executor:
                    future_to_api = {
                        executor.submit(self.get_total_balance, f"bithumb_{i}", price_cache): f"bithumb_{i}"
                        for i in range(1, len(self.account_names) + 1)
                        if f"bithumb_{i}" in self.apis
                    }
                    for future in future_to_api:
                        api_name = future_to_api[future]
                        try:
                            balance = future.result()
                            if balance is not None:
                                current_balances[api_name] = balance
                        except Exception as e:
                            self.logger.error(f"{api_name} 잔고 조회 실패: {str(e)}")

                for i in range(1, len(self.account_names) + 1):
                    api_name = f"bithumb_{i}"
                    if api_name not in current_balances:
                        continue
                    balance = current_balances[api_name]
                    if balance is None:
                        continue
                    if self.initial_balances[api_name] is None:
                        self.initial_balances[api_name] = balance
                        self.previous_balances[api_name] = balance
                        self.logger.info(f"\n=== {api_name} 초기 자산 ===")
                        self.logger.info(f"실제 총 자산: {balance:,.0f}원")

                self.logger.info("\n=== 전체 계정 현황 ===")
                for i in range(1, len(self.account_names) + 1):
                    api_name = f"bithumb_{i}"
                    if api_name not in current_balances:
                        continue
                    current_balance = current_balances[api_name]
                    if current_balance is None:
                        continue
                    change = current_balance - self.previous_balances[api_name]
                    total_change = current_balance - self.initial_balances[api_name]

                    if change > 0:
                        self.logger.info(f"[{api_name}] +{change:,.0f}원")
                    elif change < 0:
                        self.logger.info(f"[{api_name}] {change:,.0f}원")
                        if abs(change) >= self.warning_threshold:
                            self.logger.warning(f"⚠️ [{api_name}] 경고: {abs(change):,.0f}원 손실 발생!")
                    else:
                        self.logger.info(f"[{api_name}] 변동 없음")

                    if total_change > 0:
                        self.logger.info(f"[{api_name}] 💰 총 자산: {current_balance:,.0f}원 (+{total_change:,.0f}원)")
                    elif total_change < 0:
                        self.logger.info(f"[{api_name}] 💸 총 자산: {current_balance:,.0f}원 ({total_change:,.0f}원)")
                    else:
                        self.logger.info(f"[{api_name}] 💰 총 자산: {current_balance:,.0f}원 (0원)")

                    # ✅ 여기서 갱신: 변화량 계산 이후
                    self.previous_balances[api_name] = current_balance

                now = time.time()
                if now - self.last_report_time >= 300:
                    report_lines = ["📊 <b>총 자산 안내</b>\n"]
                    first_risk = []
                    second_risk = []
                    for i, name in enumerate(self.account_names, start=1):
                        api = f"bithumb_{i}"
                        start = self.initial_balances.get(api)
                        current = self.previous_balances.get(api)
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
                    self.last_report_time = now

                time.sleep(1)
            except KeyboardInterrupt:
                print("\n모니터링 종료")
                break
            except Exception as e:
                self.logger.error(f"오류 발생: {str(e)}")
                time.sleep(1)

# 로그 포맷 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

if __name__ == "__main__":
    monitor = BalanceMonitor()
    monitor.monitor()
    time.sleep(1)

# 로그 포맷 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

if __name__ == "__main__":
    monitor = BalanceMonitor()
    monitor.monitor()