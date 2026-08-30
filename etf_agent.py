import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
import yfinance as yf


def get_etf_data():
  tickers = ["SPY", "QQQ", "DIA", "IWM"]
  data_str = ""
  for ticker in tickers:
    etf = yf.Ticker(ticker)
    hist = etf.history(period="5d")
    if not hist.empty:
      latest = hist.iloc[-1]
      prev = hist.iloc[-2] if len(hist) > 1 else latest
      change_pct = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
      data_str += (
          f"- {ticker}: 종가 ${latest['Close']:.2f} (전일 대비"
          f" {change_pct:+.2f}%)\n"
      )
  return data_str


def generate_report(data):
  api_key = os.environ.get("GEMINI_API_KEY")
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  prompt = f"""
    다음은 주요 ETF의 최근 가격 동향 데이터입니다:
    {data}

    이 데이터를 바탕으로 한국 투자자가 이해하기 쉽도록 오늘의 ETF 가격 동향 분석 보고서를 작성해 주세요. 
    주요 변동 요인과 시장 인사이트를 포함하여 깔끔하고 전문적인 어조로 작성해 주세요. (한국어로 작성)
    """
  response = model.generate_content(prompt)
  return response.text


def send_email(content):
  sender_email = os.environ.get("EMAIL_USER")
  sender_password = os.environ.get("EMAIL_PASSWORD")
  receiver_email = sender_email  # 본인 이메일로 수신

  msg = MIMEMultipart()
  msg["Subject"] = "[AI ETF 분석 보고서] 오늘의 시장 동향"
  msg["From"] = sender_email
  msg["To"] = receiver_email

  msg.attach(MIMEText(content, "plain", "utf-8"))

  try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
      server.starttls()
      server.login(sender_email, sender_password)
      server.sendmail(sender_email, receiver_email, msg.as_string())
    print("이메일 전송 성공!")
  except Exception as e:
    print(f"이메일 전송 실패: {e}")


if __name__ == "__main__":
  data = get_etf_data()
  report = generate_report(data)
  send_email(report)
