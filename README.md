# Daily-Article

구글 뉴스(Google News RSS)를 활용하여 특정 키워드의 최신 기사를 수집하고, 구글 Gemini AI로 3줄 요약하여 디스코드(Discord)로 매일 자동 전송하는 파이썬 프로그램

## 🌟 주요 기능 (Features)
- **자동 뉴스 수집**: 지정한 키워드(예: 방산, 자동차)에 대한 최신 뉴스를 구글 뉴스 RSS에서 크롤링 없이 빠르고 안정적으로 수집합니다.
- **AI 3줄 요약**: Google Gemini API(gemini-1.5-flash)를 활용해 기사 본문을 파악하고 핵심 내용을 한국어로 3줄 요약합니다.
- **디스코드 웹훅 연동**: 깔끔한 임베드(Embed) 메시지 형태로 디스코드 채널에 기사 제목, 요약, 링크를 자동 전송합니다.
- **서버리스 자동화**: GitHub Actions를 통해 개인 서버나 PC를 켜둘 필요 없이 매일 지정된 시간에 자동으로 실행됩니다.

## 🛠️ 기술 스택 (Tech Stack)
- **Language**: Python 3.10
- **AI**: Google Gemini API (`google-generativeai`)
- **Libraries**: `feedparser`, `requests`, `beautifulsoup4`
- **Automation**: GitHub Actions

## 🚀 설정 및 실행 방법 (Getting Started)

### 1. 사전 준비
- **Discord Webhook URL**: 알림을 받을 디스코드 채널 설정에서 웹훅을 생성하고 URL을 복사합니다.
- **Google Gemini API Key**: [Google AI Studio](https://aistudio.google.com/)에서 무료 API 키를 발급받습니다.

### 2. GitHub Actions 자동화 설정 (권장)
이 저장소를 본인의 GitHub에 업로드한 후, 환경 변수(Secrets)를 설정해야 자동화가 작동합니다.
1. GitHub 저장소의 `Settings` -> `Secrets and variables` -> `Actions`로 이동합니다.
2. `New repository secret`을 클릭하여 아래 두 가지 키를 등록합니다:
   - `DISCORD_WEBHOOK_URL` : 복사한 디스코드 웹훅 주소
   - `GEMINI_API_KEY` : 발급받은 제미나이 API 키
3. `.github/workflows/daily_news.yml` 파일에 설정된 시간(기본: 한국 시간 매일 아침 8시)에 자동으로 코드가 실행됩니다.

### 3. 로컬 환경에서 수동 실행하기
본인의 PC에서 바로 실행해보고 싶다면 아래 명령어를 사용하세요.

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경 변수 설정 (Mac/Linux 기준)
export DISCORD_WEBHOOK_URL="당신의_디스코드_웹훅_주소"
export GEMINI_API_KEY="당신의_제미나이_API_키"

# (Windows 명령 프롬프트의 경우)
# set DISCORD_WEBHOOK_URL=당신의_디스코드_웹훅_주소
# set GEMINI_API_KEY=당신의_제미나이_API_키

# 3. 코드 실행
python main.py
```

## 📝 사용자 정의 (Customization)
`main.py` 파일 내의 `KEYWORDS` 리스트를 수정하여 원하는 주제의 뉴스를 받아볼 수 있습니다.
```python
# 예시: 다른 관심사로 변경
KEYWORDS = ["인공지능", "부동산", "스타트업"]
```
