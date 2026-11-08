# Firebase setup for Adventure Academy

Firebase cloud sync is optional. GitHub Pages continues to host the site, and browser-local saving plus JSON backup remain available if Firebase is unavailable.

## Cost guardrails
- Keep the project on the Spark (no-cost) plan.
- Do not link a billing account or upgrade to Blaze.
- Do not enable paid services such as Cloud Functions, phone/SMS authentication, or paid storage.
- Firestore has limited free quotas. If a quota is reached, pause and review usage rather than adding billing.

## What the first version stores
The app stores only a nickname (maximum 20 characters), a built-in avatar, visited room IDs, and lesson levels (0–3). It does not intentionally store a learner's full name, phone number, school, home address, precise location, or date of birth. Google sign-in establishes the account identity; the app does not copy the Google profile name or email into the learner progress document.

## One-time Firebase Console setup
1. Open https://console.firebase.google.com/ and select project `adventure-academy-822b6`.
2. Confirm the project is on the Spark plan. Do not add billing.
3. Open **Build → Authentication → Get started → Sign-in method**.
4. Enable **Google** as a sign-in provider and save.
5. In Authentication settings, open **Authorized domains** and confirm `tawananyashachipiro.github.io` is listed. Add it if it is missing.
6. Open **Build → Firestore Database** and create the database if it does not exist. Choose a region carefully; it cannot be changed later.
7. In Firestore **Rules**, publish the complete contents of this repository's `firestore.rules` file.
8. Wait for GitHub Pages to deploy, open the live site, enter the academy, and select **Sign in with Google**.

## How sync works
- Google sign-in provides a stable Firebase user ID so the same account can sync across devices.
- Progress is stored at `learners/{userId}/progress/current`.
- On sign-in, the app combines local and cloud progress, keeping the highest lesson level per subject and combining visited rooms.
- Changes are sent to Firestore after local saves.
- If sign-in, network access, or Firebase is unavailable, local browser storage and JSON backup continue to work.

## Security notes
The Firestore rules restrict each signed-in account to its own progress document and validate the expected fields. Review and test rules before public launch. Never place service-account private keys, Admin SDK credentials, passwords, or other private secrets in browser code or GitHub. The web configuration identifies the Firebase project; it is not an admin credential. Restrict the API key to required Firebase APIs and review authorised domains.

## Current status
The website code includes optional Google sign-in and Firestore sync. Cloud sync will not become active until Authentication, Firestore, and the rules are configured in Firebase Console. Local saving and downloadable backups remain the fallback.
