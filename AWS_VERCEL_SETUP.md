# AWS 서버 + Vercel 설정 가이드

## 🎯 목표

- **AWS 서버**: 백엔드 API + 텔레그램 알림 (도메인 불필요)
- **Vercel**: 프론트엔드 + 도메인 제공

---

## 📋 1단계: AWS 서버 설정

### 1.1 서버 접속 및 프로젝트 클론

```bash
ssh -i ~/경로/adam.pem ubuntu@<AWS_SERVER_IP>
cd ~/project
git clone git@github-bithumb:adam-epiclions/Bithumb-Monitor-nextjs.git
cd Bithumb-Monitor-nextjs
```

### 1.2 패키지 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.3 환경 변수 설정

```bash
nano .env
```

`.env` 파일 내용:
```env
BITHUMB_ACCESS_KEY_1="..."
BITHUMB_SECRET_KEY_1="..."
BITHUMB_ACCESS_KEY_2="..."
BITHUMB_SECRET_KEY_2="..."
... (13개 계정)
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHAT_ID="..."
```

### 1.4 API 서버 실행

```bash
# 백그라운드 실행
nohup python api_server.py > api.log 2>&1 &

# 로그 확인
tail -f api.log
```

### 1.5 방화벽 설정

```bash
# 포트 8080 열기
sudo ufw allow 8080/tcp

# 또는 특정 IP만 허용 (Vercel IP 대역)
# sudo ufw allow from <IP> to any port 8080
```

### 1.6 테스트

```bash
# 서버에서 테스트
curl http://localhost:8080/api/health

# 외부에서 테스트 (AWS 서버 IP 사용)
curl http://<AWS_SERVER_IP>:8080/api/health
```

---

## 📋 2단계: Vercel 설정

### 2.1 프로젝트 연결

1. [Vercel](https://vercel.com) 접속
2. "Add New Project" 클릭
3. GitHub 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`

### 2.2 환경 변수 설정

Vercel 대시보드 → Settings → Environment Variables:

```
API_BASE_URL=http://YOUR_AWS_SERVER_IP:8080
```

> **주의**: AWS 서버 IP 주소를 정확히 입력하세요.

### 2.3 프론트엔드 수정

`public/index.html` 파일에서 AWS 서버 IP 주소 확인:

```javascript
const API_BASE_URL = 'http://YOUR_AWS_SERVER_IP:8080';
```

또는 환경 변수 사용:
```javascript
const API_BASE_URL = process.env.API_BASE_URL || 'http://YOUR_AWS_SERVER_IP:8080';
```

### 2.4 배포

GitHub에 푸시하면 자동 배포:

```bash
git add .
git commit -m "Add AWS + Vercel architecture"
git push origin main
```

### 2.5 도메인 확인

배포 완료 후:
- 자동 도메인: `https://bithumb-monitor-nextjs.vercel.app`
- 커스텀 도메인 연결 가능

---

## 🔧 3단계: 보안 설정 (권장)

### 3.1 AWS 보안 그룹

AWS 콘솔 → EC2 → Security Groups:
- 인바운드 규칙 추가
- 포트: 8080
- 소스: Vercel IP 대역 또는 특정 IP

### 3.2 HTTPS 설정 (선택사항)

AWS 서버에 Nginx + Let's Encrypt 설정:

```bash
# Nginx 설치
sudo apt install nginx

# SSL 인증서 발급 (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## ✅ 4단계: 테스트

1. **AWS 서버 API 테스트**
   ```bash
   curl http://<AWS_SERVER_IP>:8080/api/balances
   ```

2. **Vercel 프론트엔드 접속**
   - 브라우저에서 Vercel 도메인 접속
   - 잔고 데이터가 표시되는지 확인

3. **텔레그램 알림 확인**
   - 5분 후 텔레그램 메시지 확인

---

## 🔄 업데이트 방법

### AWS 서버 업데이트

```bash
cd ~/project/Bithumb-Monitor-nextjs
git pull origin main
pkill -f api_server.py
source venv/bin/activate
nohup python api_server.py > api.log 2>&1 &
```

### Vercel 업데이트

- GitHub에 푸시하면 자동 배포

---

## 🐛 문제 해결

### CORS 오류

`api_server.py`에서 CORS 설정 확인:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://*.vercel.app", "http://localhost:3000"],
        ...
    }
})
```

### 연결 실패

1. AWS 보안 그룹 확인
2. 방화벽 설정 확인
3. API 서버 실행 상태 확인: `ps aux | grep api_server`

### 텔레그램 알림 안 옴

1. `.env` 파일 확인
2. 로그 확인: `tail -f api.log`
3. 텔레그램 봇 토큰 확인

---

## 📊 모니터링

### AWS 서버 로그

```bash
tail -f api.log
```

### Vercel 로그

- Vercel 대시보드 → Functions → Logs

---

## 💡 팁

1. **AWS 서버 IP 변경 시**
   - Vercel 환경 변수 업데이트
   - `public/index.html` 업데이트

2. **자동 재시작**
   - systemd 서비스로 등록 권장
   - 또는 PM2 사용

3. **백업**
   - `.env` 파일 백업 필수
   - GitHub에 올리지 않도록 주의

