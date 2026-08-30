import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

prompt = """
전 세계의 가장 뜨거운 글로벌 경제 핫이슈 3가지를 엄선하여 요약해 주세요.
각 이슈마다 다음 형식을 지켜주세요:
1. 이슈 제목 (핵심 요약)
2. 주요 내용 및 배경 설명
3. 글로벌 경제에 미치는 영향 또는 시사점
이메일 본문으로 보기 편하게 깔끔하게 정리해 주세요.
"""

response = model.generate_content(prompt)
report_content = response.text

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
WIFE_EMAIL = os.environ.get("WIFE_EMAIL")

recipients = [EMAIL_USER, WIFE_EMAIL]

msg = MIMEMultipart()
msg["Subject"] = "[Daily Global Economy] 오늘의 글로벌 핫이슈 경제뉴스 3선"
msg["From"] = EMAIL_USER
msg["To"] = ", ".join(recipients)
msg.attach(MIMEText(report_content, "plain", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, recipients, msg.as_string())

print("경제 뉴스 이메일 다중 발송 완료!")
