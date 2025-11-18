# 아키텍처 가이드: AWS 서버 + Vercel

## 🏗️ 전체 구조

```
┌─────────────────┐         ┌──────────────────┐
│   Vercel        │         │   AWS 서버       │
│  (프론트엔드)    │────────▶│  (백엔드 API)    │
│                 │  HTTP   │                  │
│ - 도메인 제공    │  요청   │ - API 서버       │
│ - 정적 파일      │         │ - 텔레그램 알림  │
│ - 폴링 방식      │         │ - 백그라운드 작업│
└─────────────────┘         └──────────────────┘
```

## 📋 구성 요소

### 1. AWS 서버 (백엔드)
- **파일**: `api_server.py`
- **역할**:
  - REST API 제공 (`/api/balances`)
  - 빗썸 API 호출 및 데이터 수집
  - 텔레그램 알림 (백그라운드)
  - CORS 설정으로 Vercel에서 접근 허용

### 2. Vercel (프론트엔드)
- **파일**: `public/index.html`
- **역할**:
  - 웹 UI 제공
  - AWS API 폴링 (1초마다)
  - 도메인 제공 (무료 `.vercel.app` 또는 커스텀 도메인)

---

## 🚀 배포 방법

### AWS 서버 설정

1. **서버 접속**
```bash
ssh -i ~/경로/adam.pem ubuntu@<AWS_SERVER_IP>
```

2. **프로젝트 클론**
```bash
cd ~/project
git clone git@github-bithumb:adam-epiclions/Bithumb-Monitor-nextjs.git
cd Bithumb-Monitor-nextjs
```

3. **패키지 설치**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask-cors  # 추가 필요
```

4. **환경 변수 설정**
```bash
nano .env
```

`.env` 파일:
```env
BITHUMB_ACCESS_KEY_1="..."
BITHUMB_SECRET_KEY_1="..."
... (13개 계정)
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHAT_ID="..."
```

5. **API 서버 실행**
```bash
# 백그라운드 실행
nohup python api_server.py > api.log 2>&1 &

# 또는 systemd 서비스로 등록 (권장)
```

6. **방화벽 설정**
```bash
# 포트 8080 열기
sudo ufw allow 8080/tcp
```

### Vercel 설정

1. **프로젝트 연결**
   - Vercel 대시보드 → Add New Project
   - GitHub 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`

2. **환경 변수 설정**
   - Settings → Environment Variables
   - `API_BASE_URL`: `http://YOUR_AWS_SERVER_IP:8080`

3. **프론트엔드 수정**
   - `public/index.html`에서 `API_BASE_URL` 확인
   - AWS 서버 IP 주소로 변경

4. **배포**
   - GitHub에 푸시하면 자동 배포

---

## 🔧 설정 파일

### `vercel.json` (Vercel용)
```json
{
  "version": 2,
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/index.html"
    }
  ]
}
```

### `api_server.py` (AWS 서버용)
- REST API 엔드포인트 제공
- CORS 설정으로 Vercel 도메인 허용
- 백그라운드 모니터링 및 텔레그램 알림

---

## 🔐 보안 고려사항

1. **AWS 보안 그룹**
   - 포트 8080을 특정 IP만 허용하거나
   - Vercel IP 대역만 허용 (권장)

2. **API 인증** (선택사항)
   - API 키 추가
   - Rate limiting 설정

3. **HTTPS** (권장)
   - AWS 서버에 Nginx + Let's Encrypt 설정
   - 또는 AWS ALB 사용

---

## 📊 데이터 흐름

1. **Vercel 프론트엔드**
   - 1초마다 `GET /api/balances` 호출
   - 받은 데이터로 UI 업데이트

2. **AWS 서버**
   - 백그라운드에서 계속 모니터링
   - 최신 데이터를 메모리에 저장
   - API 요청 시 즉시 반환
   - 5분마다 텔레그램 리포트 전송

---

## ✅ 장점

- ✅ **도메인 불필요**: AWS 서버는 IP만 있으면 됨
- ✅ **Vercel 도메인**: 무료 `.vercel.app` 또는 커스텀 도메인
- ✅ **비용 효율**: AWS 서버는 기존 인프라 활용
- ✅ **확장성**: 프론트엔드와 백엔드 분리
- ✅ **보안**: API 서버는 내부 네트워크에서만 접근 가능

---

## 🔄 업데이트 방법

### AWS 서버 업데이트
```bash
cd ~/project/Bithumb-Monitor-nextjs
git pull origin main
# 프로세스 재시작
pkill -f api_server.py
nohup python api_server.py > api.log 2>&1 &
```

### Vercel 업데이트
- GitHub에 푸시하면 자동 배포

