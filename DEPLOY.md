# 배포 가이드

## 🚀 서버 배포 (EC2)

### 1. 서버 접속

```bash
ssh -i ~/경로/adam.pem ubuntu@<서버 퍼블릭 IP>
```

### 2. 프로젝트 클론

```bash
# 프로젝트 디렉토리로 이동
cd ~/project

# GitHub에서 클론 (SSH 사용)
git clone git@github-bithumb:adam-epiclions/Bithumb-Monitor-nextjs.git
cd Bithumb-Monitor-nextjs
```

> **참고**: 서버에서도 SSH 키 설정이 필요합니다. 서버의 `~/.ssh/config`에 동일한 설정을 추가하세요.

### 3. 가상환경 설정 및 패키지 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
# .env 파일 생성
nano .env
```

`.env` 파일 내용:
```env
BITHUMB_ACCESS_KEY_1="..."
BITHUMB_SECRET_KEY_1="..."
# ... (13개 계정)
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHAT_ID="..."
```

### 5. ngrok 설정 (고정 도메인 사용 시)

```bash
# ngrok 설정 파일 생성
mkdir -p ~/.config/ngrok
nano ~/.config/ngrok/ngrok.yml
```

`~/.config/ngrok/ngrok.yml`:
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

### 6. 실행

```bash
# ngrok 실행 (백그라운드)
nohup ngrok start --all > ngrok.log 2>&1 &

# 웹 모니터 실행
nohup python web_monitor.py > web.log 2>&1 &

# 잔고 모니터 실행
nohup python balance_monitor.py > balance.log 2>&1 &
```

또는 스크립트 사용:
```bash
chmod +x start_monitor.sh
./start_monitor.sh
```

### 7. 프로세스 확인

```bash
# 실행 중인 프로세스 확인
ps aux | grep python
ps aux | grep ngrok

# 로그 확인
tail -f web.log
tail -f balance.log
```

---

## 🔄 업데이트 방법

서버에서 프로젝트를 업데이트하려면:

```bash
cd ~/project/Bithumb-Monitor-nextjs
git pull origin main

# 프로세스 재시작
pkill -f web_monitor.py
pkill -f balance_monitor.py

# 다시 실행
source venv/bin/activate
./start_monitor.sh
```

---

## 📝 서버 SSH 설정 (처음 한 번만)

서버에서도 GitHub에 접속하려면 SSH 키를 설정해야 합니다:

1. 서버에서 SSH 키 생성:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_bithumb -C "server@yourdomain.com"
```

2. 공개키를 GitHub에 등록:
```bash
cat ~/.ssh/id_ed25519_bithumb.pub
```

3. 서버의 `~/.ssh/config` 설정:
```bash
nano ~/.ssh/config
```

추가:
```
Host github-bithumb
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_bithumb
```

