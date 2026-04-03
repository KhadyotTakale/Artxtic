"""Email service — async SMTP via AWS SES."""

from __future__ import annotations

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Send emails via AWS SES SMTP."""

    @staticmethod
    async def send_email(to_email: str, subject: str, html_body: str) -> bool:
        """Send an email via SMTP. Returns True on success."""
        try:
            message = MIMEMultipart("alternative")
            message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(html_body, "html"))

            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
            )
            logger.info("Email sent to %s: %s", to_email, subject)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, str(e))
            return False

    @staticmethod
    async def send_verification_otp(to_email: str, otp: str, name: str | None = None) -> bool:
        """Send OTP verification email."""
        greeting = f"Hi {name}," if name else "Hi,"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto;">
            <h2 style="color: #7c3aed;">Artxtic — Verify Your Email</h2>
            <p>{greeting}</p>
            <p>Your verification code is:</p>
            <div style="
                background: #f3f4f6; border-radius: 8px; padding: 20px;
                text-align: center; font-size: 32px; font-weight: bold;
                letter-spacing: 8px; color: #7c3aed; margin: 20px 0;
            ">{otp}</div>
            <p>This code expires in <strong>{settings.OTP_EXPIRE_MINUTES} minutes</strong>.</p>
            <p>If you didn't request this, you can safely ignore this email.</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
            <p style="color: #9ca3af; font-size: 12px;">© Artxtic — AI Media Generation Platform</p>
        </div>
        """
        return await EmailService.send_email(to_email, "Artxtic — Verify Your Email", html)

    @staticmethod
    async def send_password_reset(to_email: str, reset_token: str, name: str | None = None) -> bool:
        """Send password reset email with a link containing the token."""
        greeting = f"Hi {name}," if name else "Hi,"
        # The frontend should handle the reset page
        reset_url = f"{settings.CORS_ORIGINS[0]}/reset-password?token={reset_token}"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto;">
            <h2 style="color: #7c3aed;">Artxtic — Password Reset</h2>
            <p>{greeting}</p>
            <p>You requested a password reset. Click the button below:</p>
            <div style="text-align: center; margin: 25px 0;">
                <a href="{reset_url}" style="
                    background: #7c3aed; color: white; padding: 12px 32px;
                    border-radius: 8px; text-decoration: none; font-weight: bold;
                ">Reset Password</a>
            </div>
            <p>This link expires in <strong>1 hour</strong>.</p>
            <p>If you didn't request this, you can safely ignore this email.</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
            <p style="color: #9ca3af; font-size: 12px;">© Artxtic — AI Media Generation Platform</p>
        </div>
        """
        return await EmailService.send_email(to_email, "Artxtic — Password Reset", html)
