import requests
from bs4 import BeautifulSoup
import time

# --- 수정이 필요한 구간 ---
TOKEN = '복사한_API_토큰'
CHAT_ID = '복사한_채팅_아이디'
URL = "https://www.hongik.ac.kr/kr/newscenter/notice.do"
KEYWORDS = ["교내봉사", "교내 근로", "봉사장학생"]
# -----------------------

def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': message}
    requests.get(api_url, params=params)

last_notice_id = ""

print("홍익대 교내봉사 알리미 작동 중...")

while True:
    try:
        # User-Agent를 넣어야 학교 서버에서 차단될 확률이 낮습니다.
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 홍대 공지 리스트의 첫 번째 게시글 찾기
        first_notice = soup.select_one(".bn-list-common table tbody tr")
        if first_notice:
            title_tag = first_notice.select_one(".bn-title a")
            title = title_tag.text.strip()
            link = "https://www.hongik.ac.kr" + title_tag['href']
            
            # 주소에서 고유 번호 추출
            current_id = link.split('articleNo=')[1].split('&')[0]

            # 새로운 글이고, 키워드가 포함되어 있다면 알림 전송
            if current_id != last_notice_id:
                if any(key in title for key in KEYWORDS):
                    message = f"📢 교내봉사 공지 떴다!\n\n제목: {title}\n링크: {link}"
                    send_telegram(message)
                    print(f"알림 보냄: {title}")
                
                last_notice_id = current_id # 확인한 글 번호 저장

    except Exception as e:
        print(f"오류 발생: {e}")

    time.sleep(600) # 10분마다 체크
