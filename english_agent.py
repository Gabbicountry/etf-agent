Python
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

prompt = """
미국 원어민들이 일상생활과 비즈니스에서 가장 자주 사용하는 실용적인 영어 회화 표현 10가지를 골라주세요.
각 표현마다 다음 형식을 지켜주세요:
1. 영어 문장
2. 한국어 의미
3. 간단한 뉘앙스 또는 활용 팁
이메일 본문으로 보기 편하게 깔끔하게 정리해 주세요.
"""

response = model.generate_content(prompt)
report_content = response.text

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

msg = MIMEMultipart()
msg["Subject"] = "[Daily English] 오늘의 미국 원어민 필수 표현 10선"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER
msg.attach(MIMEText(report_content, "plain", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())

print("영어 표현 이메일 발송 완료!")
