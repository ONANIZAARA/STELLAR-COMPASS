import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import os
from datetime import datetime

class NotificationService:
    def __init__(self):
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_address = os.getenv('EMAIL_ADDRESS', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # Twilio configuration for SMS
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER', '')
        
        # Initialize Twilio client if credentials exist
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None
    
    def send_email(self, to_email, subject, message, html_content=None):
        """Send email notification"""
        try:
            if not self.email_address or not self.email_password:
                print("⚠️ Email credentials not configured")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text version
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
            
            # Add HTML version if provided
            if html_content:
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
            return False
    
    def send_sms(self, to_phone, message):
        """Send SMS notification via Twilio"""
        try:
            if not self.twilio_client:
                print("⚠️ Twilio credentials not configured")
                return False
            
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_phone
            )
            
            print(f"✅ SMS sent to {to_phone} (SID: {message.sid})")
            return True
            
        except Exception as e:
            print(f"❌ SMS error: {str(e)}")
            return False
    
    def send_opportunity_alert(self, user_email, user_phone, opportunity_data):
        """Send alert about new DeFi opportunity"""
        subject = f"🚀 New {opportunity_data['apy']}% APY Opportunity Found!"
        
        message = f"""
Stellar Compass Alert 🌟

New DeFi Opportunity Detected:

Protocol: {opportunity_data['protocol']}
Asset: {opportunity_data['asset']}
APY: {opportunity_data['apy']}%
TVL: ${opportunity_data['tvl']}
Risk: {opportunity_data['risk_score']}

{opportunity_data['description']}

Log in to Stellar Compass to take action!
        """
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #4F46E5;">🚀 New DeFi Opportunity!</h2>
                <div style="background: #F3F4F6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{opportunity_data['protocol']}</h3>
                    <p><strong>Asset:</strong> {opportunity_data['asset']}</p>
                    <p><strong>APY:</strong> <span style="color: #10B981; font-size: 24px;">{opportunity_data['apy']}%</span></p>
                    <p><strong>TVL:</strong> ${opportunity_data['tvl']}</p>
                    <p><strong>Risk Score:</strong> {opportunity_data['risk_score']}</p>
                    <p style="margin-top: 15px;">{opportunity_data['description']}</p>
                </div>
                <a href="http://localhost:8080" style="background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 10px;">
                    View in Stellar Compass
                </a>
            </body>
        </html>
        """
        
        # Send both email and SMS
        email_sent = self.send_email(user_email, subject, message, html_content)
        sms_sent = self.send_sms(user_phone, f"Stellar Compass: {opportunity_data['apy']}% APY opportunity in {opportunity_data['protocol']}! Check your email for details.")
        
        return email_sent or sms_sent
    
    def send_idle_asset_alert(self, user_email, user_phone, idle_value, asset_count):
        """Alert user about idle assets"""
        subject = f"💤 ${idle_value:,.2f} in Idle Assets Detected"
        
        message = f"""
Stellar Compass Alert 🌟

You have {asset_count} idle assets worth ${idle_value:,.2f} that could be earning yield!

These assets are sitting dormant and missing potential earnings.

Log in to see personalized recommendations.
        """
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #F59E0B;">💤 Idle Assets Detected</h2>
                <div style="background: #FEF3C7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 18px;"><strong>{asset_count} assets</strong> worth <strong style="color: #D97706; font-size: 24px;">${idle_value:,.2f}</strong> are sitting idle.</p>
                    <p>These assets could be earning yield in DeFi protocols!</p>
                </div>
                <a href="http://localhost:8080" style="background: #F59E0B; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 10px;">
                    See Recommendations
                </a>
            </body>
        </html>
        """
        
        email_sent = self.send_email(user_email, subject, message, html_content)
        sms_sent = self.send_sms(user_phone, f"Stellar Compass: You have ${idle_value:,.2f} in idle assets. Check your email for opportunities!")
        
        return email_sent or sms_sent
    
    def send_risk_alert(self, user_email, user_phone, protocol_name, risk_type):
        """Alert user about protocol risks"""
        subject = f"⚠️ Risk Alert: {protocol_name}"
        
        message = f"""
Stellar Compass Security Alert 🛡️

Risk detected in {protocol_name}:
{risk_type}

We recommend reviewing your positions immediately.

Log in to Stellar Compass for more details.
        """
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #EF4444;">⚠️ Security Alert</h2>
                <div style="background: #FEE2E2; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #EF4444;">
                    <h3 style="margin-top: 0; color: #991B1B;">{protocol_name}</h3>
                    <p><strong>Risk Type:</strong> {risk_type}</p>
                    <p style="margin-top: 15px;">We recommend reviewing your positions in this protocol immediately.</p>
                </div>
                <a href="http://localhost:8080" style="background: #EF4444; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 10px;">
                    Review Positions
                </a>
            </body>
        </html>
        """
        
        email_sent = self.send_email(user_email, subject, message, html_content)
        sms_sent = self.send_sms(user_phone, f"URGENT - Stellar Compass: Risk detected in {protocol_name}. Check your email immediately!")
        
        return email_sent or sms_sent
    
    def send_price_alert(self, user_email, user_phone, asset, price_change, current_price):
        """Alert user about significant price movements"""
        direction = "📈" if price_change > 0 else "📉"
        subject = f"{direction} {asset} Price Alert: {price_change:+.1f}%"
        
        message = f"""
Stellar Compass Price Alert {direction}

{asset} has moved {price_change:+.1f}%
Current Price: ${current_price:,.4f}

This could affect your portfolio value and yield opportunities.

Log in to review your positions.
        """
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>{direction} Price Movement Alert</h2>
                <div style="background: #F3F4F6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{asset}</h3>
                    <p><strong>Price Change:</strong> <span style="color: {'#10B981' if price_change > 0 else '#EF4444'}; font-size: 24px;">{price_change:+.1f}%</span></p>
                    <p><strong>Current Price:</strong> ${current_price:,.4f}</p>
                </div>
                <a href="http://localhost:8080" style="background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 10px;">
                    View Portfolio
                </a>
            </body>
        </html>
        """
        
        email_sent = self.send_email(user_email, subject, message, html_content)
        sms_sent = self.send_sms(user_phone, f"Stellar Compass: {asset} {price_change:+.1f}% - ${current_price:,.4f}")
        
        return email_sent or sms_sent
