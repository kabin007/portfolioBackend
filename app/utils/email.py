import smtplib
from email.message import EmailMessage
import asyncio
import logging
from app.config import settings

# Set up logging
logger = logging.getLogger(__name__)

async def send_email(to: str, subject: str, body: str):

    try:
        # Create message
        message = EmailMessage()
        message["From"] = settings.smtp_user
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        
        def send_sync_email():
            """Synchronous email sending function"""
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(message)
        
        # Run email sending in executor to avoid blocking
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, send_sync_email)
        
        logger.info(f"Email sent successfully to {to}")
        return {"success": True, "message": "Password reset email has been sent successfully"}
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {e}")
        return {"success": False, "message": "Email authentication failed"}
        
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"Recipients refused: {e}")
        return {"success": False, "message": "Invalid recipient email address"}
        
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"SMTP server disconnected: {e}")
        return {"success": False, "message": "Email server connection failed"}
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return {"success": False, "message": "Failed to send email"}