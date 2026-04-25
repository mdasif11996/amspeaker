# AMspeaker Android App

This is an Android WebView application that wraps the AMspeaker Streamlit web app.

## Prerequisites

- Android Studio (latest version)
- JDK 8 or higher
- Android SDK (API 24+)

## Setup Instructions

### 1. Update App URL

Edit `app/src/main/java/com/amspeaker/app/MainActivity.java` and change the `APP_URL` constant to your server URL:

```java
private static final String APP_URL = "http://192.168.29.96:8504"; // Change to your server URL
```

For production, use your deployed server URL (e.g., `https://your-server.com`).

### 2. Open in Android Studio

1. Open Android Studio
2. Select "Open an Existing Project"
3. Navigate to the `android` folder in this project
4. Click "OK"

### 3. Build the APK

#### Using Android Studio:
1. Click **Build** > **Build Bundle(s) / APK(s)** > **Build APK(s)**
2. Wait for the build to complete
3. Click **locate** in the notification to find the APK
4. The APK will be in: `app/build/outputs/apk/debug/app-debug.apk`

#### Using Command Line:
```bash
cd android
./gradlew assembleDebug
```

The APK will be in: `app/build/outputs/apk/debug/app-debug.apk`

### 4. Build Release APK (for distribution)

#### Using Android Studio:
1. Click **Build** > **Generate Signed Bundle / APK**
2. Select **APK** and click **Next**
3. Create a new keystore or use an existing one
4. Select **release** build variant
5. Click **Finish**

#### Using Command Line:
```bash
cd android
./gradlew assembleRelease
```

Note: You'll need to configure signing in `app/build.gradle` for release builds.

## Install on Android Device

### Option 1: USB Debugging
1. Enable USB debugging on your Android device
2. Connect device via USB
3. In Android Studio, click **Run** or use:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Option 2: Direct APK Transfer
1. Copy the APK file to your device
2. Enable "Install from Unknown Sources" in device settings
3. Open the APK file and install

## App Permissions

The app requires the following permissions:
- **INTERNET** - To load the web app
- **ACCESS_NETWORK_STATE** - To check network connectivity
- **RECORD_AUDIO** - For voice input functionality
- **MODIFY_AUDIO_SETTINGS** - For audio configuration
- **WRITE_EXTERNAL_STORAGE** - For caching
- **READ_EXTERNAL_STORAGE** - For reading cached data

## Troubleshooting

### Blank Screen
- Check that the server URL is correct and accessible
- Ensure the Streamlit app is running on the specified URL
- Check internet connection on the device

### Microphone Not Working
- Ensure microphone permission is granted in app settings
- Check that the device has a working microphone
- Verify the web app's voice input is functioning

### Build Errors
- Ensure Android SDK is properly installed
- Update Android Studio to the latest version
- Run `./gradlew clean` to clean the build cache

## Customization

### Change App Name
Edit `app/src/main/AndroidManifest.xml`:
```xml
android:label="Your App Name"
```

### Change App Icon
Replace the icon files in `app/src/main/res/mipmap-*` directories.

### Change Theme Colors
Edit `app/src/main/res/values/colors.xml` and `themes.xml`.

## Production Deployment

For production deployment:
1. Use HTTPS for the app URL
2. Sign the APK with a proper keystore
3. Upload to Google Play Store following their guidelines
4. Consider using a proper backend hosting service

## Server Requirements

The Streamlit app must be:
- Running on a publicly accessible server (or local network for testing)
- Configured to accept connections from your device
- Using a stable URL (not localhost for production)

## License

This Android wrapper is part of the AMspeaker project.
