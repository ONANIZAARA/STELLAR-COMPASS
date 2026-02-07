# 🚀 Quick Start Guide - Stellar Compass

Get up and running in 5 minutes!

## ⚡ Super Quick Start (3 Steps)

### 1️⃣ Install Freighter Wallet
- Go to [freighter.app](https://www.freighter.app/)
- Install the browser extension
- Create or import your Stellar wallet

### 2️⃣ Start the Application

**On Mac/Linux:**
```bash
cd stellar-compass
bash start.sh
```

**On Windows:**
```bash
cd stellar-compass
start.bat
```

### 3️⃣ Open Your Browser
- Visit: `http://localhost:8080`
- Click "Connect Wallet"
- Approve in Freighter
- Done! 🎉

---

## 📋 What You'll See

Once connected, the AI agents will:
- ✅ Scan your wallet for idle assets
- 📊 Find best yield opportunities
- 🤖 Start monitoring 24/7
- 🔔 Send you alerts

---

## 🔧 Troubleshooting

**Backend won't start?**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend won't open?**
```bash
cd frontend
python -m http.server 8080
# Then visit http://localhost:8080
```

**Wallet won't connect?**
- Make sure Freighter is installed
- Refresh the page
- Check browser console (F12) for errors

---

## 📱 Enable SMS Alerts (Optional)

1. Sign up for free [Twilio account](https://www.twilio.com/try-twilio)
2. Get your credentials
3. Create `backend/.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number
   ```
4. Restart backend
5. Add your phone number in app settings

---

## 🌐 Deploy to Internet (Free)

**Backend:**
1. Create account on [railway.app](https://railway.app)
2. Click "Deploy from GitHub"
3. Select your repo
4. Set root directory: `backend`
5. Deploy!

**Frontend:**
1. Create account on [netlify.com](https://netlify.com)
2. Drag & drop `frontend` folder
3. Done! You'll get a URL like: `your-app.netlify.app`

---

## 📚 Next Steps

- ✅ Connect your wallet
- ✅ Explore the dashboard
- ✅ Check your alerts
- ✅ Set up notifications
- ✅ Deploy to production
- ✅ Star the repo on GitHub! ⭐

---

## 💡 Tips

1. **Use Testnet First** - Switch Freighter to testnet for testing
2. **Check Alerts** - Refresh every few minutes to see new alerts
3. **Adjust Risk** - Change risk tolerance in settings
4. **Monitor Multiple Wallets** - Disconnect and reconnect different wallets

---

## 🆘 Need Help?

- 📖 Read the full [README.md](README.md)
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deploy
- 🐛 Open an issue on GitHub
- 💬 Join our Discord (coming soon)

---

**Happy DeFi-ing! 🌟**
