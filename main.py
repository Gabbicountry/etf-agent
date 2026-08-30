import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email():
    sender_email = os.environ.get("GMAIL_USER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    wife_email = os.environ.get("WIFE_EMAIL")
    
    # 엔돌핀 넘치는 추천 음악 리스트 (제목과 유튜브 링크)
    music_list = """
    1. 🎵 브루노 마스 - 24K Magic
       https://www.youtube.com/watch?v=UqyT8IEBHBM
    2. 🎵 두아 리파 - Levitating
       https://www.youtube.com/watch?v=TEdELDVzEAo
    3. 🎵 어메이ธ์ - Wake Me Up (Avicii)
       https://www.youtube.com/watch?v=IcrbM1l_BoI
    """
    
    subject = "[모닝 음악] ☀️ 오늘 하루도 화이팅! 엔돌핀 충전 음악 3곡이 도착했습니다."
    body = f"안녕하세요! 세석진님, 혜인님,\n\n매일 아침 활력을 채워줄 오늘의 추천 음악 3곡입니다.\n{music_list}\n\n오늘도 기분 좋은 하루 보내세요!"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    
    # 수신자 설정 (본인과 와이프 모두 포함)
    recipients = [sender_email]
    if wife_email:
        recipients.append(wife_email)
    
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("모닝 음악 메일 전송 성공!")
    except Exception as e:
        print(f"전송 실패: {e}")

if __name__ == "__main__":
    send_email()
