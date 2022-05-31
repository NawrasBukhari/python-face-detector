from tzlocal import get_localzone
from datetime import datetime
import yagmail


def send_mail():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    local_timezone = get_localzone()
    mail_from = 'aues2022@gmail.com'
    mail_password = ''
    mail_to = 'nawrasbukhari@hotmail.com'
    mail_subject = 'MOTION DETECTED'
    mail_body = f"""
    <h2 style="color: red;">Motion Detected: The motion was detected at: {current_time} in {local_timezone} timezone</h2>
    """
    yag = yagmail.SMTP(mail_from, mail_password)
    video_name = ['output.avi']
    yag.send(
        to=mail_to,
        subject=mail_subject,
        contents=mail_body,
        attachments=video_name
    )
