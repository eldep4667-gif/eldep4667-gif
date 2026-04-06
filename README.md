# NEXUS Trading Dashboard

Modern Streamlit trading dashboard with:

- TradingView live chart
- pair-aware market news
- confluence-based analysis engine
- mobile-friendly web access

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy online with Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload this project to the repository root.
3. Go to Streamlit Community Cloud.
4. Choose `New app`.
5. Select your GitHub repository.
6. Set:
   - Main file path: `app.py`
   - Python version: `3.11`
7. In app `Secrets`, add any optional keys from `.streamlit/secrets.toml.example`.
8. Deploy the app.

After deployment, the app gets a permanent public link that works from phone or desktop without running the code locally.

## Optional secrets

The app works without paid APIs, but news quality improves when you add one or both:

- `GNEWS_API_KEY`
- `NEWSAPI_KEY`

## Mobile usage

- Open the deployed link from your phone browser.
- Use `Add to Home Screen` to make it behave like an app shortcut.

## Notes

- This is a hosted web app, not a native Android/iPhone app package.
- For a real Play Store / App Store app, the next step would be building a mobile client on top of this logic.
