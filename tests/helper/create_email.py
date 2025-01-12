from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path):
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the body text
    msg.attach(MIMEText(body, "html"))
    msg.attach(MIMEText("Example of plain text that follows.", "plain"))

    # Open the file in bynary
    with open(attachment_path, "rb") as attachment:
        # Add the attachment to the message
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    filename = attachment_path.split("/")[-1]
    # Add header as key/value pair to attachment part
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    # Attach the attachment to the message
    # msg.attach(part)

    # Convert the message to a string
    return msg.as_bytes()


def main():
    # Example usage
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@example.com"
    subject = "Test Email with Attachment"
    body = """
    <html>
    <head></head>
    <body>
        <h1>Hello!</h1>
        <p>This is a test email with an HTML body and an attachment.</p>
        <hr>
        <h2>Mock Replies</h2>
        <div style="border-left: 3px solid #ccc; padding-left: 10px;">
            <p><strong>Reply 1:</strong> Thank you for your email. I will review the attachment shortly.</p>
        </div>
        <div style="border-left: 3px solid #ccc; padding-left: 10px; margin-top: 10px;">
            <p><strong>Reply 2:</strong> I have reviewed the attachment and everything looks good. Let me know if you need anything else.</p>
        </div>
    </body>
    </html>
    """  # noqa: E501
    attachment_path = "tests/data/docx/msft_pr.docx"  # Path to the file you want to attach

    email_bytes = send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path)
    with open("example.eml", "wb") as f:
        f.write(email_bytes)


if __name__ == "__main__":
    main()
