import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

def send_email():
    # 등록하신 시크릿 이름(EMAIL_USER, EMAIL_PASSWORD)에 맞게 수정
    sender_email = os.environ.get("EMAIL_USER")
    app_password = os.environ.get("EMAIL_PASSWORD")
    wife_email = os.environ.get("WIFE_EMAIL")
    
    if not sender_email or not app_password:
        print("❌ 에러: EMAIL_USER 또는 EMAIL_PASSWORD 시크릿을 불러오지 못했습니다.")
        sys.exit(1)
        
    music_list = """
    1. 🎵 브루노 마스 - 24K Magic
       https://www.youtube.com/watch?v=UqyT8IEBHBM
    2. 🎵 두아 리파 - Levitating
       https://www.youtube.com/watch?v=TEdELDVzEAo
    3. 🎵 아비치 - Wake Me Up
       https://www.youtube.com/watch?v=IcrbM1l_BoI
    """
    
    subject = "[모닝 음악] ☀️ 오늘 하루도 화이팅! 엔돌핀 충전 음악 3곡이 도착했습니다."
    body = f"안녕하세요!\n\n매일 아침 활력을 채워줄 오늘의 추천 음악 3곡입니다.\n{music_list}\n\n오늘도 기분 좋은 하루 보내세요!"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    
    recipients = [sender_email]
    if wife_email:
        recipients.append(wife_email)
    
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        print(f"📧 이메일 발송 시도 중... (발신자: {sender_email})")
        print(f"📬 수신자 목록: {recipients}")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("✨ 이메일 전송 성공!")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_email()
