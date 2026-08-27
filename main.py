import os
import feedparser
import requests
import json
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai

# ==========================================
# [설정] 환경 변수에서 값 가져오기
# ==========================================
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 검색할 키워드
KEYWORDS = ["방산", "자동차"]
MAX_ARTICLES_PER_KEYWORD = 5

# Gemini API 설정
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # 빠르고 가벼운 gemini-1.5-flash 모델 사용
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def get_google_news_rss(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:MAX_ARTICLES_PER_KEYWORD]

def summarize_text(title, description):
    if not model:
        soup = BeautifulSoup(description, "html.parser")
        text = soup.get_text()
        return text if text else "요약 정보를 가져올 수 없습니다."

    prompt = f"""
    다음 뉴스 기사의 제목과 내용을 바탕으로 핵심 내용을 한국어로 3줄 요약해주세요.
    
    제목: {title}
    내용: {description}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"요약 중 오류 발생: {e}")
        return "요약 생성 실패"

def send_discord_webhook(keyword, articles):
    today = datetime.now().strftime("%Y-%m-%d")
    
    embeds = []
    for article in articles:
        title = article.title
        link = article.link
        pub_date = article.published
        summary = summarize_text(title, article.get("description", ""))

        embed = {
            "title": title,
            "url": link,
            "color": 3447003 if keyword == "방산" else 15105570,
            "fields": [
                {
                    "name": "📝 핵심 요약",
                    "value": summary,
                    "inline": False
                }
            ],
            "footer": {
                "text": f"발행일시: {pub_date}"
            }
        }
        embeds.append(embed)

    payload = {
        "content": f"📢 **[{today}] '{keyword}' 관련 주요 뉴스 Top {len(articles)}**",
        "embeds": embeds
    }

    headers = {"Content-Type": "application/json"}
    if DISCORD_WEBHOOK_URL:
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        if response.status_code in [200, 204]:
            print(f"[{keyword}] 뉴스 디스코드 전송 완료!")
        else:
            print(f"디스코드 전송 실패: {response.status_code}, {response.text}")
    else:
        print("DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")

def main():
    for keyword in KEYWORDS:
        print(f"'{keyword}' 뉴스 수집 및 요약 시작...")
        articles = get_google_news_rss(keyword)
        if articles:
            send_discord_webhook(keyword, articles)
        else:
            print(f"'{keyword}' 관련 뉴스를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
