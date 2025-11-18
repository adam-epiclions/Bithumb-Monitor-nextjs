# Vercel 배포 가이드 (유료 플랜)

## ✅ Vercel 유료 플랜 장점

- **더 긴 실행 시간**: 최대 60초 (무료: 10초)
- **더 많은 메모리**: 최대 3GB (무료: 1GB)
- **더 나은 성능**: 프리미엄 인프라
- **무제한 함수 실행**: 무료 플랜의 제한 없음
- **우선 지원**: 빠른 응답 시간

## ⚠️ 중요 사항

이 프로젝트는 **Flask + SocketIO (WebSocket)**를 사용합니다.

### Vercel 유료 플랜에서:
- ✅ 더 긴 실행 시간으로 백그라운드 작업 가능
- ✅ 더 많은 메모리로 안정적인 실행
- ⚠️ WebSocket은 여전히 제한적일 수 있음 (폴링 방식으로 대체 가능)

---

## 🚀 Vercel 배포 방법

### 1. Vercel 계정 생성 및 유료 플랜 구독

1. [Vercel](https://vercel.com)에 가입/로그인
2. **Settings → Billing**에서 유료 플랜 구독
   - **Pro**: $20/월 (권장)
   - **Enterprise**: 맞춤 가격
3. "Add New Project" 클릭
4. GitHub 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`
5. 프로젝트 설정:
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

### 4. 함수 설정 확인

Settings → Functions에서 확인:
- **Max Duration**: 60초 (유료 플랜)
- **Memory**: 1024MB (필요시 증가 가능)

### 5. 도메인 확인

배포 완료 후:
- 자동 생성된 도메인: `https://bithumb-monitor-nextjs.vercel.app`
- 또는 커스텀 도메인 연결 가능 (Settings → Domains)

### 6. 커스텀 도메인 연결 (선택사항)

1. Settings → Domains
2. "Add Domain" 클릭
3. 도메인 입력 (예: `monitor.yourdomain.com`)
4. DNS 설정 안내에 따라 레코드 추가
5. SSL 인증서 자동 발급

---

## 🔧 최적화 팁

### 함수 메모리 증가
`vercel.json`에서 메모리 설정 조정:
```json
"functions": {
  "api/index.py": {
    "maxDuration": 60,
    "memory": 2048  // 2GB로 증가
  }
}
```

### 환경 변수 최적화
- 프로덕션 환경 변수는 Production에만 설정
- 개발용은 Preview/Development에 설정

---

## 📊 모니터링

Vercel 대시보드에서 확인 가능:
- 함수 실행 시간
- 메모리 사용량
- 에러 로그
- 트래픽 통계

---

## 🔄 대안: Railway 또는 Render

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

