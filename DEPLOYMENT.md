# Deploy AMspeaker to Cloud for Independent Access

To make the Android app work independently (without your computer), deploy the Streamlit app to a cloud service.

## Option 1: Streamlit Cloud (Free & Easiest)

### Step 1: Create GitHub Repository
1. Go to https://github.com and sign in
2. Click "New repository"
3. Name it "amspeaker"
4. Make it Public
5. Click "Create repository"

### Step 2: Push Code to GitHub
```bash
cd c:\streamlit_app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/amspeaker.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/amspeaker`
5. Main file: `app.py`
6. Click "Deploy"

### Step 4: Get Your Cloud URL
After deployment, Streamlit Cloud will give you a URL like:
`https://amspeaker-YOUR_USERNAME.streamlit.app`

### Step 5: Update Android App
1. Edit `android/app/src/main/java/com/amspeaker/app/MainActivity.java`
2. Change the URL to your Streamlit Cloud URL:
```java
private static final String APP_URL = "https://amspeaker-YOUR_USERNAME.streamlit.app";
```

### Step 6: Rebuild APK
```bash
cd android
.\gradlew.bat assembleDebug
```

## Option 2: Railway (Free Tier Alternative)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login
```bash
railway login
```

### Step 3: Initialize Project
```bash
cd c:\streamlit_app
railway init
```

### Step 4: Deploy
```bash
railway up
```

### Step 5: Get URL
Railway will provide a public URL for your app.

## Option 3: Render (Free Tier)

### Step 1: Create render.yaml
```yaml
services:
  - type: web
    name: amspeaker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT
    envVars:
      - key: PORT
        value: 8501
```

### Step 2: Push to GitHub
Follow same steps as Option 1

### Step 3: Connect to Render
1. Go to https://render.com
2. Sign up/login
3. Click "New +"
4. Select "Web Service"
5. Connect your GitHub repository
6. Deploy

## After Deployment

Once you have your cloud URL:
1. Update the Android app with the cloud URL
2. Rebuild the APK
3. Install on your phone
4. The app will now work independently from anywhere!

## Important Notes

- **Streamlit Cloud** is the easiest and recommended option
- Free tiers have limitations (sleep after inactivity, etc.)
- For production, consider paid plans for better performance
- Keep your `.env` file secure (don't commit API keys to GitHub)
