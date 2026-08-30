import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

prompt = """
해외 출장 상황(공항 입국 심사, 호텔 체크인, 바이어 미팅, 프레젠테이션 Q&A, 식사 및 네트워킹 자리)에서 
원어민들이 실제로 가장 많이 쓰는 실용적인 비즈니스 영어 표현 및 회화 10가지를 골라주세요.
각 표현마다 다음 형식을 지켜주세요:
1. 영어 문장
2. 한국어 의미
3. 비즈니스 현장에서의 뉘앙스 또는 활용 팁
이메일 본문으로 보기 편하게 깔끔하게 정리해 주세요.
"""

response = model.generate_content(prompt)
report_content = response.text

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

msg = MIMEMultipart()
msg["Subject"] = "[Daily Business English] 해외 출장 필수 비즈니스 영어 10선"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER
msg.attach(MIMEText(report_content, "plain", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())

print("비즈니스 영어 이메일 발송 완료!")
