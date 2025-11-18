# Bithumb Balance Monitor

빗썸 거래소의 다중 계정 자산을 실시간으로 통합 모니터링할 수 있는 웹 애플리케이션입니다.

## ✅ 주요 기능

- **13개 빗썸 계정 자산 실시간 확인**
- **총 자산 기준 손실 알림 (10%, 15%) 텔레그램 전송**
- **초기 대비 변화량 추적**
- **WebSocket 기반 실시간 가격 반영**
- **ngrok 고정 도메인 연동으로 외부 접속 가능**

---

> **💡 Git/SSH 설정이 필요하신가요?**  
> 각 폴더별로 다른 GitHub 계정을 사용하는 방법은 상위 폴더의 [README.md](../README.md)를 참고하세요.

---

## 📦 설치 및 실행

### 1. 서버 접속 (EC2 예시)

```bash
ssh -i ~/경로/adam.pem ubuntu@<서버 퍼블릭 IP>
```

> `.pem` 파일은 반드시 퍼미션이 `chmod 400` 으로 제한되어야 합니다.

---

### 2. 프로젝트 업로드 또는 복제

#### Git 사용 시
```bash
git clone <repository-url>
cd Bithumb-Balance-Monitor-master
```

#### 로컬 파일 업로드 (SCP)
```bash
scp -i ~/경로/adam.pem web_monitor.py ubuntu@<서버IP>:~/project/Bithumb-Balance-Monitor-master/
```

---

### 3. 가상환경 세팅 및 패키지 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4. `.env` 환경 설정

`.env` 파일을 생성하여 다음 형식으로 API 키와 텔레그램 설정을 추가합니다.

```env
BITHUMB_ACCESS_KEY_1="..."
BITHUMB_SECRET_KEY_1="..."
...
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHAT_ID="..."
```

---

### 5. `ngrok` 설정 (고정 도메인 사용 시)

#### `~/.config/ngrok/ngrok.yml` 예시:
```yaml
region: ap
version: '2'
authtoken: <YOUR_TOKEN>
tunnels:
  web-monitor:
    proto: http
    addr: 8080
    subdomain: trusting-kite-sound
```

---

### 6. 실행 방법

#### ① `ngrok` 실행
```bash
ngrok start --all
```

#### ② 웹 모니터 실행 (백그라운드)
```bash
nohup python web_monitor.py > web.log 2>&1 &
```

#### ③ 잔고 텔레그램 모니터 실행
```bash
nohup python balance_monitor.py > balance.log 2>&1 &
```

---

## 📡 웹 접속

브라우저에서 아래 주소 접속:

```
https://trusting-kite-sound.ngrok-free.app
```

---

## 🛠 운영 명령어

### 실행 중 프로세스 확인
```bash
ps aux | grep python
```

### 특정 프로세스 종료 (예: web_monitor.py)
```bash
kill <PID>
```

### 로그 보기
```bash
tail -n 30 web.log
tail -n 30 balance.log
```

---

## 🖥 자동 실행 스크립트 예시

`start_monitor.sh`:

```bash
#!/bin/bash
source venv/bin/activate
nohup python web_monitor.py > web.log 2>&1 &
nohup python balance_monitor.py > balance.log 2>&1 &
```

실행:
```bash
chmod +x start_monitor.sh
./start_monitor.sh
```
