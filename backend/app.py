"""
Stellar Compass - Universal DeFi Assistant Backend
Serves both frontend and API endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from stellar_sdk import Server, Asset
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Load environment variables
load_dotenv()

# Get the parent directory (project root)
BASE_DIR = Path(__file__).parent.parent

# Initialize Flask app with frontend folder
app = Flask(__name__, 
            static_folder=str(BASE_DIR / 'frontend'),
            static_url_path='')
CORS(app)

# Stellar network configuration
HORIZON_URL = "https://horizon.stellar.org"
horizon = Server(HORIZON_URL)

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
USER_EMAIL = os.getenv('USER_EMAIL')

# SMS configuration (optional)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
USER_PHONE = os.getenv('USER_PHONE')

print("🚀 Starting Stellar Compass API Server...")
print("📡 API available at: http://localhost:5000")
print("🌐 CORS enabled for frontend requests")
print("\n🔔 Notifications Status:")
print(f"   📧 Email: {'✅ Enabled' if EMAIL_ADDRESS and EMAIL_PASSWORD else '❌ Not configured'}")
print(f"   📱 SMS: {'✅ Enabled' if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else '❌ Not configured'}")
print(f"\n💡 Connected to Stellar {HORIZON_URL}")
print(f"📁 Serving frontend from: {BASE_DIR / 'frontend'}")
print("-" * 50)


# ============================================
# FRONTEND SERVING ROUTES
# ============================================

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory(str(BASE_DIR / 'frontend'), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static frontend files"""
    try:
        return send_from_directory(str(BASE_DIR / 'frontend'), path)
    except:
        # If file not found, return index.html (for SPA routing)
        return send_from_directory(str(BASE_DIR / 'frontend'), 'index.html')


# ============================================
# HELPER FUNCTIONS
# ============================================

def send_email(subject, body_html):
    """Send email notification"""
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not USER_EMAIL:
            print("⚠️  Email not configured in .env file")
            return False

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = USER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body_html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent: {subject}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        return False


def send_sms(message):
    """Send SMS notification via Twilio"""
    try:
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            print("⚠️  SMS not configured in .env file")
            return False

        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=USER_PHONE
        )

        print(f"✅ SMS sent: {message.sid}")
        return True

    except ImportError:
        print("⚠️  Twilio not installed. Run: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ SMS failed: {str(e)}")
        return False


# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Stellar Compass API',
        'network': HORIZON_URL
    })


@app.route('/api/notify-connection', methods=['POST'])
@app.route('/notify-connection', methods=['POST'])
def notify_connection():
    """Send notification when wallet connects"""
    try:
        data = request.json
        public_key = data.get('publicKey')
        wallet_type = data.get('walletType', 'unknown')

        wallet_names = {
            'freighter': '🚀 Freighter',
            'albedo': '⭐ Albedo',
            'rabet': '🐰 Rabet',
            'xbull': '🐂 xBull',
            'manual': '🦞 Manual (Lobstr/Other)'
        }

        wallet_display = wallet_names.get(wallet_type, wallet_type.capitalize())

        print(f"\n🔔 Wallet Connected: {wallet_display}")
        print(f"   Address: {public_key[:8]}...{public_key[-8:]}")

        # Send email notification
        email_subject = f"🌟 Stellar Compass: Wallet Connected Successfully"
        email_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #667eea;">🎉 Wallet Connected Successfully!</h2>
                    
                    <div style="background-color: #e8f5e9; padding: 20px; border-left: 4px solid #4caf50; margin: 20px 0;">
                        <p><strong>Wallet Type:</strong> {wallet_display}</p>
                        <p><strong>Public Key:</strong> {public_key[:8]}...{public_key[-8:]}</p>
                        <p><strong>Network:</strong> Stellar Mainnet</p>
                    </div>
                    
                    <h3 style="color: #333;">What's Next?</h3>
                    <ul style="color: #666;">
                        <li>✅ Your portfolio is being analyzed</li>
                        <li>✅ DeFi opportunities are loading</li>
                        <li>✅ Real-time tracking is active</li>
                    </ul>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <p style="margin: 0;"><strong>💡 Pro Tip:</strong> Check your dashboard regularly for new DeFi opportunities!</p>
                    </div>
                    
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        This notification was sent by Stellar Compass DeFi Assistant.
                    </p>
                </div>
            </body>
        </html>
        """

        send_email(email_subject, email_body)

        # Send SMS notification (if configured)
        sms_message = f"Stellar Compass: {wallet_display} connected successfully! Address: {public_key[:8]}...{public_key[-8:]}"
        send_sms(sms_message)

        return jsonify({
            'success': True,
            'message': 'Notifications sent',
            'wallet_type': wallet_type
        })

    except Exception as e:
        print(f"❌ Notification error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/portfolio/<public_key>', methods=['GET'])
@app.route('/portfolio/<public_key>', methods=['GET'])
def get_portfolio(public_key):
    """Get portfolio for a Stellar account"""
    try:
        print(f"\n🔍 Fetching portfolio for: {public_key[:8]}...{public_key[-8:]}")

        # Load account from Stellar
        account = horizon.accounts().account_id(public_key).call()

        balances = account['balances']
        total_value = 0
        active_assets = []
        idle_assets = []

        # Process balances
        for balance in balances:
            asset_code = balance.get('asset_code', 'XLM')
            asset_balance = float(balance['balance'])

            # Simplified value calculation (you can integrate real price APIs)
            if asset_code == 'XLM':
                # Approximate XLM price (update with real API)
                asset_value = asset_balance * 0.10
            else:
                asset_value = 0  # Would need price oracle

            total_value += asset_value

            balance['value'] = asset_value

            # Categorize assets (simplified logic)
            if asset_balance > 0:
                active_assets.append(balance)
            else:
                idle_assets.append(balance)

        portfolio_data = {
            'public_key': public_key,
            'balances': balances,
            'total_value': total_value,
            'active_assets': active_assets,
            'idle_assets': idle_assets,
            'sequence': account['sequence']
        }

        print(f"✅ Portfolio loaded: {len(balances)} assets, ${total_value:.2f} total value")

        # Send portfolio notification
        send_portfolio_notification(public_key, portfolio_data)

        return jsonify(portfolio_data)

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Portfolio error: {error_msg}")
        return jsonify({
            'error': error_msg,
            'public_key': public_key
        }), 400


def send_portfolio_notification(public_key, portfolio):
    """Send notification with portfolio summary"""
    try:
        total_value = portfolio.get('total_value', 0)
        num_assets = len(portfolio.get('balances', []))

        email_subject = f"📊 Your Stellar Portfolio Summary"
        email_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #667eea;">📊 Portfolio Analysis Complete</h2>
                    
                    <div style="background-color: #e3f2fd; padding: 20px; border-left: 4px solid #2196f3; margin: 20px 0;">
                        <h3 style="color: #333; margin-top: 0;">Portfolio Summary</h3>
                        <p><strong>Total Value:</strong> ${total_value:.2f}</p>
                        <p><strong>Total Assets:</strong> {num_assets}</p>
                        <p><strong>Active Assets:</strong> {len(portfolio.get('active_assets', []))}</p>
                        <p><strong>Idle Assets:</strong> {len(portfolio.get('idle_assets', []))}</p>
                    </div>
                    
                    <h3 style="color: #333;">Your Assets</h3>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        """

        # Add asset details
        for balance in portfolio.get('balances', [])[:5]:  # Show first 5 assets
            asset_code = balance.get('asset_code', 'XLM')
            asset_balance = balance.get('balance', '0')
            email_body += f"""
                        <p style="margin: 10px 0;">
                            <strong>{asset_code}:</strong> {float(asset_balance):.4f}
                        </p>
            """

        if len(portfolio.get('balances', [])) > 5:
            email_body += f"<p style='color: #666;'>...and {len(portfolio.get('balances', [])) - 5} more assets</p>"

        email_body += """
                    </div>
                    
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Portfolio data fetched from Stellar Horizon.
                    </p>
                </div>
            </body>
        </html>
        """

        send_email(email_subject, email_body)

    except Exception as e:
        print(f"⚠️  Portfolio notification failed: {str(e)}")


@app.route('/api/opportunities/<public_key>', methods=['GET'])
@app.route('/opportunities/<public_key>', methods=['GET'])
def get_opportunities(public_key):
    """Get DeFi opportunities for account"""
    try:
        print(f"\n🔍 Finding opportunities for: {public_key[:8]}...{public_key[-8:]}")

        # Example opportunities (replace with real DeFi protocol integrations)
        opportunities = [
            {
                'title': 'Aqua Liquidity Rewards',
                'description': 'Provide liquidity to AMM pools and earn AQUA rewards',
                'apy': '12.5',
                'risk': 'Medium',
                'platform': 'Aquarius',
                'action_url': 'https://aqua.network'
            },
            {
                'title': 'Ultra Stellar Staking',
                'description': 'Stake your XLM and earn passive rewards',
                'apy': '5.2',
                'risk': 'Low',
                'platform': 'Ultra Stellar',
                'action_url': 'https://ultrastellar.com'
            },
            {
                'title': 'Stellar X Trading Fees',
                'description': 'Earn trading fees by providing liquidity on StellarX',
                'apy': '8.7',
                'risk': 'Medium',
                'platform': 'StellarX',
                'action_url': 'https://www.stellarx.com'
            }
        ]

        print(f"✅ Found {len(opportunities)} opportunities")

        # Send opportunities notification
        send_opportunities_notification(public_key, opportunities)

        return jsonify({
            'public_key': public_key,
            'opportunities': opportunities,
            'count': len(opportunities)
        })

    except Exception as e:
        print(f"❌ Opportunities error: {str(e)}")
        return jsonify({
            'error': str(e),
            'opportunities': []
        }), 400


def send_opportunities_notification(public_key, opportunities):
    """Send notification about available opportunities"""
    try:
        if not opportunities:
            return

        email_subject = f"🚀 {len(opportunities)} DeFi Opportunities Available"
        email_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #667eea;">🚀 DeFi Opportunities for You</h2>
                    
                    <p style="color: #666;">We found {len(opportunities)} opportunities to earn yield on your assets:</p>
        """

        for opp in opportunities[:3]:  # Show top 3
            email_body += f"""
                    <div style="background-color: #f5f5f5; padding: 20px; margin: 15px 0; border-left: 4px solid #4caf50; border-radius: 5px;">
                        <h3 style="color: #333; margin-top: 0;">{opp.get('title', 'Opportunity')}</h3>
                        <p style="color: #666;">{opp.get('description', '')}</p>
                        <div style="display: flex; gap: 20px; margin-top: 10px;">
                            <span style="color: #4caf50; font-weight: bold;">APY: {opp.get('apy', 'N/A')}%</span>
                            <span style="color: #ff9800;">Risk: {opp.get('risk', 'N/A')}</span>
                        </div>
                        {f'<a href="{opp.get("action_url", "")}" style="color: #667eea; text-decoration: none;">Learn More →</a>' if opp.get('action_url') else ''}
                    </div>
            """

        email_body += """
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Always do your own research before investing in DeFi protocols.
                    </p>
                </div>
            </body>
        </html>
        """

        send_email(email_subject, email_body)

    except Exception as e:
        print(f"⚠️  Opportunities notification failed: {str(e)}")


@app.route('/api/test-notification', methods=['GET'])
@app.route('/test-notification', methods=['GET'])
def test_notification():
    """Test endpoint to verify notifications work"""
    try:
        email_sent = send_email(
            "🧪 Test Notification from Stellar Compass",
            """
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4caf50;">✅ Test Successful!</h2>
                    <p>If you're reading this, your email notifications are working perfectly!</p>
                </body>
            </html>
            """
        )

        sms_sent = send_sms("Test notification from Stellar Compass - Your SMS is working!")

        return jsonify({
            'success': True,
            'email_sent': email_sent,
            'sms_sent': sms_sent
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n✅ Server ready! Press Ctrl+C to stop.\n")
    app.run(host='0.0.0.0', port=5000, debug=True)