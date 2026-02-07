# Stellar Compass 🌟

**AI-Powered DeFi Assistant for Stellar Network**

Stellar Compass is an intelligent DeFi portfolio manager that automatically detects idle crypto assets, finds the best yield opportunities, and sends real-time alerts via SMS, email, and push notifications.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

 Features

Core Functionality
- ** Idle Asset Detection** - Automatically scans for crypto sitting dormant for 30+ days
- ** Smart Yield Matching** - Personalized recommendations based on your holdings
- ** AI Agent Monitoring** - 6 autonomous agents running 24/7
- ** Risk Intelligence** - Protocol safety scores and risk assessment
- ** Auto-Rebalancing** - Portfolio drift detection and optimization
- ** Yield Harvesting** - Tracks unclaimed rewards across protocols
- ** Multi-Channel Alerts** - SMS, Email, and Push notifications

### AI Agents
1. **Idle Asset Monitor** - Scans every 5 mins for dormant assets
2. **Opportunity Scout** - Finds new yield opportunities and APY spikes
3. **Risk Monitor** - Watches for protocol risks and security issues
4. **Auto Rebalancer** - Detects portfolio drift and suggests rebalancing
5. **Yield Harvester** - Tracks unclaimed rewards
6. **Price Movement Agent** - Monitors significant price changes

##  Tech Stack

### Frontend
- HTML5 / CSS3 / JavaScript
- Freighter Wallet Integration
- Responsive Design

### Backend
- Python 3.9+
- Flask (REST API)
- Stellar SDK
- Multi-threaded AI Agents

### Blockchain
- Stellar Network
- Horizon API
- Freighter Wallet

## Prerequisites

Before you begin, ensure you have:
- **Python 3.9+** installed
- **Node.js** (optional, for development server)
- **Git** for version control
- **Freighter Wallet** browser extension ([Install here](https://www.freighter.app/))

##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/stellar-compass.git
cd stellar-compass
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# No build step required - pure HTML/CSS/JS
# Just open index.html in a browser or use a local server
```

##  Running the Application

### Start Backend Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### Start Frontend

#### Option 1: Simple HTTP Server (Python)
```bash
cd frontend
python -m http.server 8080
```

Visit `http://localhost:8080` in your browser

#### Option 2: Live Server (VS Code Extension)
- Install "Live Server" extension in VS Code
- Right-click `index.html` and select "Open with Live Server"

#### Option 3: Direct File Access
- Simply open `frontend/index.html` in your browser
- Note: Some features may require a local server

## 🔌 Connecting Your Wallet

1. Install [Freighter Wallet](https://www.freighter.app/) browser extension
2. Create or import your Stellar wallet
3. Open Stellar Compass in your browser
4. Click "Connect Wallet" button
5. Approve the connection in Freighter
6. Your dashboard will activate automatically!

## 📁 Project Structure

```
stellar-compass/
├── frontend/
│   ├── index.html          # Main UI
│   ├── styles.css          # Styling
│   └── app.js              # Frontend logic
├── backend/
│   ├── app.py              # Flask API server
│   ├── stellar_horizon.py  # Blockchain interaction
│   ├── stellar_defi_algorithms.py  # Core algorithms
│   ├── stellar_ai_agents.py        # AI agent system
│   └── requirements.txt    # Python dependencies
└── README.md
```

## 🔑 API Endpoints

### Portfolio Analysis
```http
POST /api/portfolio/analyze
Content-Type: application/json

{
  "wallet_address": "GXXX...",
  "risk_tolerance": "moderate"
}
```

### Initialize AI Agents
```http
POST /api/agents/initialize
Content-Type: application/json

{
  "wallet_address": "GXXX...",
  "settings": {
    "emailNotifications": true,
    "smsNotifications": true,
    "phoneNumber": "+256XXXXXXXXX",
    "riskTolerance": "moderate"
  }
}
```

### Get Alerts
```http
GET /api/alerts/{wallet_address}
```

### Update Settings
```http
POST /api/settings/update
Content-Type: application/json

{
  "wallet_address": "GXXX...",
  "settings": {...}
}
```

## 🧪 Testing

### Test with Stellar Testnet

1. Switch Freighter to Testnet
2. Get testnet XLM from [Stellar Laboratory](https://laboratory.stellar.org/#account-creator?network=test)
3. Connect wallet and test features

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

## 🌐 Deployment

### Deploy Backend (Heroku)

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create stellar-compass-api

# Deploy
git push heroku main

# Set environment variables
heroku config:set STELLAR_NETWORK=mainnet
```

### Deploy Frontend (Netlify/Vercel)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod
```

## 🔐 Security

- **Never commit private keys** - Use environment variables
- **Use HTTPS** in production
- **Validate all user inputs** on the backend
- **Rate limit API requests** to prevent abuse
- **Enable CORS** only for trusted domains in production

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📱 SMS Integration (Optional)

To enable SMS alerts, sign up for [Twilio](https://www.twilio.com/) and add:

```python
# backend/.env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [Stellar](https://stellar.org) blockchain
- Uses [Freighter Wallet](https://freighter.app)
- Inspired by the DeFi community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/stellar-compass/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/stellar-compass/discussions)
- **Email**: support@stellarcompass.io (update with your email)

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] More DeFi protocols
- [ ] Advanced analytics dashboard
- [ ] Tax reporting integration
- [ ] Multi-wallet support
- [ ] Social features (share strategies)

---

**Made with ❤️ for the Stellar community**
