# Vercel 배포 가이드

## ⚠️ 중요 사항

이 프로젝트는 **Flask + SocketIO (WebSocket)**를 사용하므로 Vercel의 Serverless 환경에서는 제한이 있습니다.

### Vercel의 제약사항:
- WebSocket 연결이 제한적일 수 있음
- 장기 실행되는 백그라운드 스레드가 제한될 수 있음
- Serverless Functions는 요청 시에만 실행됨

---

## 🚀 Vercel 배포 방법

### 1. Vercel 계정 생성 및 프로젝트 연결

1. [Vercel](https://vercel.com)에 가입/로그인
2. "Add New Project" 클릭
3. GitHub 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`
4. 프로젝트 설정:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (비워둠)
   - **Output Directory**: (비워둠)

### 2. 환경 변수 설정

Vercel 대시보드 → Settings → Environment Variables에서 추가:

```
BITHUMB_ACCESS_KEY_1=...
BITHUMB_SECRET_KEY_1=...
BITHUMB_ACCESS_KEY_2=...
BITHUMB_SECRET_KEY_2=...
... (13개 계정)
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### 3. 배포

GitHub에 푸시하면 자동으로 배포됩니다:

```bash
git push origin main
```

### 4. 도메인 확인

배포 완료 후:
- 자동 생성된 도메인: `https://bithumb-monitor-nextjs.vercel.app`
- 또는 커스텀 도메인 연결 가능

---

## 🔄 대안: Railway 또는 Render (권장)

WebSocket과 장기 실행이 필요한 경우, 다음 플랫폼을 권장합니다:

### Railway 배포

1. [Railway](https://railway.app) 가입
2. "New Project" → "Deploy from GitHub repo"
3. 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`
4. 환경 변수 설정
5. 자동으로 도메인 제공: `https://your-project.railway.app`

**Railway 장점:**
- WebSocket 완전 지원
- 장기 실행 프로세스 지원
- 무료 플랜 제공
- 자동 HTTPS/도메인

### Render 배포

1. [Render](https://render.com) 가입
2. "New Web Service" → GitHub 저장소 연결
3. 설정:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_monitor.py`
4. 환경 변수 설정
5. 자동 도메인 제공: `https://your-project.onrender.com`

---

## 📝 추천 방법

**도메인 접속이 목적이라면:**

1. **Railway 사용 (가장 권장)**
   - WebSocket 완전 지원
   - 무료 플랜
   - 자동 HTTPS/도메인

2. **Render 사용**
   - 무료 플랜 (15분 비활성 시 슬립)
   - WebSocket 지원

3. **Vercel 사용 (제한적)**
   - SocketIO가 제대로 작동하지 않을 수 있음
   - 정적 페이지는 잘 작동

---

## 🔗 커스텀 도메인 연결

모든 플랫폼에서 커스텀 도메인 연결이 가능합니다:

1. 도메인 구매 (예: Namecheap, GoDaddy)
2. 플랫폼 대시보드에서 도메인 추가
3. DNS 설정 (플랫폼이 안내)
4. SSL 자동 인증서 발급

