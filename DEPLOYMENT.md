# Real Estate Investment Dashboard — Deployment Guide

## Overview

This Streamlit app is now multi-market (DC Metro + Miami-Fort Lauderdale) and ready for online deployment.

**⚠️ Important**: Cloudflare Pages is designed for static sites and doesn't natively support Streamlit. We have three deployment options:

---

## Option 1: Vercel (Recommended) + Cloudflare DNS

Vercel has excellent Streamlit support and integrates seamlessly with Cloudflare DNS.

### Setup Steps

1. **Push to GitHub**
   ```bash
   cd /Users/rug/Dropbox/Camera\ Uploads/Claude\ Work/Personal/US\ Real\ Estate/Real\ estate\ dashboard
   git init
   git add .
   git commit -m "Multi-market real estate dashboard (DC + Miami)"
   git remote add origin https://github.com/YOUR_USERNAME/real-estate-dashboard.git
   git push -u origin main
   ```

2. **Create Vercel Project**
   - Go to https://vercel.com
   - Click "New Project"
   - Import the GitHub repo
   - Framework: "Other" (Streamlit)
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --logger.level=error`

3. **Configure Vercel for Streamlit**
   - Add `vercel.json` to root:
   ```json
   {
     "buildCommand": "pip install -r requirements.txt",
     "outputDirectory": "./",
     "env": {
       "PYTHONUNBUFFERED": "1"
     }
   }
   ```

4. **Point Cloudflare DNS to Vercel**
   - In Cloudflare dashboard:
     - Add CNAME record pointing to your Vercel domain
     - Or use Vercel's assigned domain as-is
   - Example: `re-dashboard.pages.dev` → Cloudflare CNAME

### Pros
- ✓ Free tier available
- ✓ Easy GitHub integration
- ✓ Auto-deploys on push
- ✓ Works well with Cloudflare DNS
- ✓ Custom domains supported

### Cons
- Streamlit performance on serverless is slower than dedicated hosting

---

## Option 2: Streamlit Community Cloud (Easiest)

Official Streamlit hosting — no configuration needed.

### Setup Steps

1. **Push to GitHub** (same as Option 1, steps 1)

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect GitHub repo
   - Select:
     - Repository: your real-estate-dashboard repo
     - Branch: main
     - Main file path: app.py
   - Click Deploy

3. **Custom Domain with Cloudflare**
   - Note your Streamlit Cloud URL (e.g., `abc123.streamlit.app`)
   - In Cloudflare: Create CNAME pointing to Streamlit Cloud URL
   - Enable Flexible SSL (Streamlit provides cert)

### Pros
- ✓ Official Streamlit solution
- ✓ Zero configuration
- ✓ Free tier available
- ✓ Best Streamlit performance

### Cons
- Limited customization
- Slower cold starts on free tier

---

## Option 3: Railway / Render (Self-Hosted)

These platforms support Streamlit on containers.

### Railway Example

1. Push to GitHub
2. Go to https://railway.app
3. New Project → Deploy from GitHub
4. Select your repo
5. Add environment:
   ```
   PORT=8501
   ```
6. Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Pros
- ✓ Good performance
- ✓ Reasonable pricing
- ✓ Full control

### Cons
- Paid tier required (no free tier)

---

## Cloudflare Configuration (All Options)

After deploying to Vercel, Streamlit Cloud, or Railway, configure Cloudflare:

### Step 1: Add DNS Record

| Type | Name | Content | TTL |
|---|---|---|---|
| CNAME | re-dashboard | `your-deployment-url` | Auto |

Example: `re-dashboard.yoursite.com` → `abc123.streamlit.app`

### Step 2: SSL/TLS Settings

- **SSL/TLS Mode**: Full (Strict) if using Cloudflare cert
- **Always Use HTTPS**: On
- **HSTS**: Enable for security

### Step 3: Page Rules (Optional)

```
URL: re-dashboard.yoursite.com/*
Cache Level: Bypass (Streamlit needs dynamic content)
Browser Cache TTL: Respect Existing Headers
```

### Step 4: Security

- **Bot Fight Mode**: On (basic)
- **Challenge (CAPTCHA)**: Optional
- **Rate Limiting**: Optional (to prevent abuse)

---

## Testing Local Deployment

Before deploying, test locally:

```bash
cd Real\ estate\ dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Visit `http://localhost:8501` and test:
- ✓ Market selector (DC Metro ↔ Miami)
- ✓ All pages load
- ✓ Data filters work
- ✓ Charts render

---

## Recommended: Streamlit Cloud + Cloudflare

**Simplest approach:**

1. Deploy to Streamlit Cloud (click → done)
2. Get URL: `https://your-app.streamlit.app`
3. Add Cloudflare CNAME: `re-dashboard.yourdomain.com` → Streamlit URL
4. Enable Cloudflare SSL/TLS

**Total time**: ~5 minutes

---

## Monitoring & Updates

### Auto-Deploy (GitHub)
- Streamlit Cloud auto-deploys on `main` push
- Vercel auto-deploys on `main` push
- Just `git push` to update

### Manual Check
- Streamlit Cloud: https://share.streamlit.io/deployments
- Vercel: https://vercel.com/deployments
- Railway: https://railway.app/deployments

### Environment Variables
If needed later, add secrets:
- Streamlit Cloud: Secrets tab in settings
- Vercel: Environment Variables in settings
- Railway: Variables in service settings

---

## Current Data Status

✓ DC Metro data: Complete (2012–present)
✓ Miami-Fort Lauderdale data: Complete (21,180 properties)
✓ Market configs: Defined (market_config.py)
✓ Multi-market support: Implemented

**Data updates**: Rerun Python scripts to refresh Redfin data

---

## Next Steps

After deployment:

1. Test all pages work with market selector
2. Verify data loads for both markets
3. Check performance (should be <3s per page)
4. Set up monitoring/alerts if needed
5. Add custom domain via Cloudflare
6. Share URL with investors/colleagues

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'market_config'"**
- Ensure `market_config.py` is in same directory as `app.py`
- Check requirements.txt includes all dependencies

**Pages won't load**
- Verify data files exist in `data/` directory
- Check file paths in `market_config.py`
- Review Streamlit logs

**Slow performance**
- Use Streamlit Cloud (free tier) — better performance than Vercel serverless
- Add `@st.cache_data` to slow-loading functions

---

## Contact / Support

For issues:
1. Check Streamlit Community: https://discuss.streamlit.io
2. Review app logs in deployment dashboard
3. Test locally first before troubleshooting

---

**Deployment ready!** Choose your platform above and follow the steps. Streamlit Cloud is recommended for fastest setup.
