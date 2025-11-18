# Railway 배포 가이드 (권장)

Railway는 WebSocket과 장기 실행 프로세스를 완전히 지원하므로 이 프로젝트에 가장 적합합니다.

## 🚀 배포 단계

### 1. Railway 계정 생성

1. [Railway](https://railway.app) 접속
2. "Start a New Project" 클릭
3. GitHub로 로그인

### 2. 프로젝트 배포

1. "Deploy from GitHub repo" 선택
2. 저장소 선택: `adam-epiclions/Bithumb-Monitor-nextjs`
3. Railway가 자동으로 감지:
   - Python 프로젝트 인식
   - `requirements.txt` 자동 설치
   - `Procfile` 또는 `railway.json` 설정 사용

### 3. 환경 변수 설정

Railway 대시보드 → Variables 탭에서 추가:

```
BITHUMB_ACCESS_KEY_1=...
BITHUMB_SECRET_KEY_1=...
BITHUMB_ACCESS_KEY_2=...
BITHUMB_SECRET_KEY_2=...
... (13개 계정)
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
PORT=8080
```

> **참고**: Railway는 자동으로 `PORT` 환경 변수를 제공하므로 설정할 필요 없습니다.

### 4. 도메인 확인

배포 완료 후:
- 자동 생성된 도메인: `https://your-project.up.railway.app`
- Settings → Generate Domain에서 확인

### 5. 커스텀 도메인 연결 (선택사항)

1. Settings → Domains
2. "Custom Domain" 추가
3. 도메인 입력 (예: `monitor.yourdomain.com`)
4. DNS 설정 안내에 따라 CNAME 레코드 추가
5. SSL 인증서 자동 발급

---

## 🔄 업데이트

GitHub에 푸시하면 자동으로 재배포됩니다:

```bash
git push origin main
```

---

## 💰 가격

- **무료 플랜**: $5 크레딧/월 (충분히 사용 가능)
- **Pro 플랜**: $20/월 (더 많은 리소스)

---

## ✅ 장점

- ✅ WebSocket 완전 지원
- ✅ 장기 실행 프로세스 지원
- ✅ 자동 HTTPS/도메인
- ✅ GitHub 연동 자동 배포
- ✅ 환경 변수 관리 쉬움
- ✅ 로그 확인 쉬움

