# Deployment Guide - Stellar Compass

Complete guide for deploying Stellar Compass to production.

## Table of Contents
1. [Quick Deploy (Free Options)](#quick-deploy)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Environment Variables](#environment-variables)
5. [Production Checklist](#production-checklist)

---

## Quick Deploy (Free Options)

### Option 1: Railway (Easiest) 🚂

**Backend:**
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose `stellar-compass` repo
5. Set root directory to `backend`
6. Add environment variables
7. Deploy!

**Frontend:**
1. Use Netlify (see below)

### Option 2: Render.com ⚡

**Backend:**
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Root Directory: `backend`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`
7. Deploy

---

## Backend Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create stellar-compass-api

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set root directory (if needed)
heroku config:set PROJECT_PATH=backend

# Deploy
git subtree push --prefix backend heroku main

# Or deploy from backend folder
cd backend
git init
heroku git:remote -a stellar-compass-api
git add .
git commit -m "Deploy backend"
git push heroku main
```

### Railway Deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Deploy
railway up

# Add domain
railway domain
```

### DigitalOcean App Platform

1. Create account at [digitalocean.com](https://digitalocean.com)
2. Go to Apps → Create App
3. Connect GitHub repo
4. Select `stellar-compass` repo
5. Configure:
   - **Source Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Add environment variables
7. Deploy

### Docker Deployment

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

Build and run:

```bash
cd backend
docker build -t stellar-compass-api .
docker run -p 5000:5000 stellar-compass-api
```

---

## Frontend Deployment

### Netlify (Recommended) 🌐

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod

# Or drag & drop in Netlify UI
# Just drag the 'frontend' folder to netlify.com/drop
```

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### GitHub Pages (Free)

```bash
# Create gh-pages branch
git checkout -b gh-pages

# Copy frontend to root
cp -r frontend/* .

# Update API URL in app.js
# Change: const API_BASE_URL = 'http://localhost:5000/api';
# To: const API_BASE_URL = 'https://your-backend-url.com/api';

# Commit and push
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

Enable in GitHub: Settings → Pages → Source: gh-pages

### Cloudflare Pages

1. Login to [Cloudflare](https://dash.cloudflare.com)
2. Pages → Create a project
3. Connect GitHub
4. Select `stellar-compass` repo
5. Build settings:
   - **Build directory:** `frontend`
   - **Build command:** (leave empty)
6. Deploy

---

## Environment Variables

### Backend Environment Variables

Create `.env` file in `backend/`:

```bash
# Network
STELLAR_NETWORK=mainnet  # or testnet
HORIZON_URL=https://horizon.stellar.org

# Notifications (Optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=noreply@stellarcompass.io

# Security
FLASK_SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.com

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Frontend Environment Variables

Update `frontend/app.js`:

```javascript
// Production API URL
const API_BASE_URL = 'https://your-backend-url.com/api';

// Or use environment detection
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:5000/api'
  : 'https://your-backend-url.com/api';
```

---

## Production Checklist

### Security ✅

- [ ] Change `FLASK_SECRET_KEY` to random value
- [ ] Enable HTTPS (SSL/TLS certificates)
- [ ] Update CORS settings in `app.py`:
  ```python
  CORS(app, origins=['https://your-frontend-domain.com'])
  ```
- [ ] Add rate limiting:
  ```python
  from flask_limiter import Limiter
  limiter = Limiter(app, default_limits=["100 per hour"])
  ```
- [ ] Never commit `.env` file (add to `.gitignore`)
- [ ] Use environment variables for secrets

### Performance ✅

- [ ] Enable gzip compression
- [ ] Add caching headers
- [ ] Minify CSS/JS (optional)
- [ ] Use CDN for static files
- [ ] Set up database connection pooling

### Monitoring ✅

- [ ] Set up error tracking (Sentry)
- [ ] Add logging (Papertrail, Loggly)
- [ ] Monitor uptime (UptimeRobot)
- [ ] Set up analytics (Google Analytics)

### Functionality ✅

- [ ] Test wallet connection in production
- [ ] Verify API endpoints work
- [ ] Test SMS/Email notifications
- [ ] Test on multiple devices
- [ ] Switch to Stellar mainnet (if ready)

### Documentation ✅

- [ ] Update README with production URLs
- [ ] Document API endpoints
- [ ] Create user guide
- [ ] Add troubleshooting section

---

## Custom Domain Setup

### Backend (Heroku Example)

```bash
# Add custom domain
heroku domains:add api.stellarcompass.io

# Get DNS target
heroku domains

# Add CNAME record in your DNS:
# api.stellarcompass.io → your-app.herokuapp.com
```

### Frontend (Netlify Example)

1. Netlify Dashboard → Domain Settings
2. Add custom domain: `stellarcompass.io`
3. Update DNS records (provided by Netlify)
4. Enable HTTPS (automatic with Netlify)

---

## Scaling

### Horizontal Scaling

**Heroku:**
```bash
# Scale to multiple dynos
heroku ps:scale web=3
```

**Docker:**
```bash
# Use docker-compose for multiple instances
docker-compose up --scale api=3
```

### Database

For production, use a managed database:
- **PostgreSQL:** Heroku Postgres, Supabase
- **MongoDB:** MongoDB Atlas
- **Redis:** Redis Cloud (for caching)

---

## Monitoring & Alerts

### Sentry (Error Tracking)

```bash
pip install sentry-sdk[flask]
```

In `app.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### UptimeRobot (Uptime Monitoring)

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitors for:
   - Frontend URL
   - Backend health endpoint
3. Set up alerts (email/SMS)

---

## Troubleshooting

### Backend won't start
- Check logs: `heroku logs --tail`
- Verify requirements.txt has all dependencies
- Check Python version compatibility

### CORS errors
- Update `CORS(app)` to include frontend domain
- Check frontend API_BASE_URL is correct

### Wallet connection fails
- Ensure HTTPS is enabled
- Check browser console for errors
- Verify Freighter is installed

---

## Cost Estimate (Monthly)

**Free Tier:**
- Heroku/Railway/Render: $0 (hobby tier)
- Netlify/Vercel: $0
- **Total: $0/month** ✅

**Paid (Production):**
- Backend: $7-25/month
- Frontend: $0-19/month
- Database: $5-15/month
- Twilio SMS: ~$0.0075/SMS
- **Total: ~$15-60/month**

---

**You're ready to deploy! 🚀**

Need help? Open an issue on GitHub!
