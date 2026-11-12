# AI Industrial Safety PWA

## Added
- Installable PWA manifest and app icon
- Standalone app display on supported browsers
- Service worker with basic app-shell offline caching
- Install prompt on supported browsers; iOS Add to Home Screen guidance
- Vercel static-hosting configuration

## Publish
1. Put the contents of this project folder in a GitHub repository. Ensure `index.html` and `vercel.json` are at the repository root.
2. Import the repository into Vercel and deploy as a static site (no build command; use the web root as output).
3. Test the generated HTTPS URL in a private/incognito browser and on a phone.
4. Android/desktop: use the browser Install option. iPhone/iPad: Safari Share → Add to Home Screen.

## Scope and safety
This is a PWA, not a native App Store/Google Play package. The existing AI and wearable values remain demo values unless real services/devices are connected. The service worker caches the app shell, not live data. Do not expose any development Edge API publicly; production integration needs authentication, authorization, TLS, rate limiting, validation and audit logging.
