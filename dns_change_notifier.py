import time
import subprocess
import schedule
import smtplib
import os

from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime, timedelta
from schedule import repeat, every


load_dotenv()
today = datetime.today()
TIME_LIMIT = today + timedelta(hours=48) # DNS change shouldn't take longer than 48h

DOMAIN = os.getenv("DOMAIN")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSCODE = os.getenv("SMTP_PASSCODE")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")


@repeat(every(5).minutes.until(TIME_LIMIT))
def check_dns() -> None:
	if dns_has_changed():
		print("DNS changed, notify")
		new_dns_values = "\n".join(os.getenv("NEW_DNS_VALUES").split(","))
		send_email_alert(f"The DNSs of the domain {DOMAIN} have changed.\nNew nameservers:\n{new_dns_values}")
		schedule.clear()


def send_email_alert(body: str) -> None:
	msg = EmailMessage()
	msg.set_content(body)
	msg["subject"] = "DNS have changed"
	msg["to"] = NOTIFICATION_EMAIL
	msg["from"] = SMTP_USER

	with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as srv:
		srv.starttls()
		srv.login(SMTP_USER, SMTP_PASSCODE)
		srv.send_message(msg)
		srv.quit()


def dns_has_changed() -> bool:
	result = subprocess.run([f"dig NS {DOMAIN} +short"], shell=True, capture_output=True, text=True)
	stdout = result.stdout.strip()
	dns_values = stdout.split('\n')
	# THE FOLLOWING VARIABLE WAS USED TO MOCK AS IF THE DNSs HAD CHANGED
	# dns_values = os.getenv("NEW_DNS_VALUES").split(",")

	new_dns_values = os.getenv("NEW_DNS_VALUES").split(",")
	original_dns_values = os.getenv("ORIGINAL_DNS_VALUES").split(",")

	all_previous_dns_match = all([dns_value in original_dns_values for dns_value in dns_values])
	all_new_dns_match = all([new_dns_value in new_dns_values for new_dns_value in dns_values])

	return not all_previous_dns_match and all_new_dns_match


def main() -> None:
	while len(schedule.get_jobs()):
         schedule.run_pending()
         time.sleep(300)

if __name__ == "__main__":
	main()

