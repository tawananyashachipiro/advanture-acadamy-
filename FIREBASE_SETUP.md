# Firebase setup for Adventure Academy (zero-cost preparation)

This repository is designed to stay on GitHub Pages. Firebase is an optional next step for syncing learner progress between devices.

## Cost guardrails

- Keep the Firebase project on the Spark (no-cost) plan.
- Do not link a billing account or upgrade to Blaze during setup.
- Do not enable paid services such as Cloud Functions, phone/SMS authentication, or paid storage.
- Firestore has a limited free quota. If it is reached, pause and review usage rather than adding billing.
- GitHub Pages remains the website host; Firebase is only for learner progress when configured.

A parent or guardian should create and manage the Google/Firebase project and review its settings. Do not share account passwords, private keys, or service-account files in chat or commit them to this repository.

## What the first version will store

Only the minimum learning data:
- A nickname (maximum 20 characters)
- One of the academy's built-in avatars
- Which of the 12 rooms have been visited
- Progress level (0–3) in each room

Do not collect a learner's full name, home address, phone number, school, precise location, or date of birth in this first version.

## Setup steps for the parent or guardian

1. Open https://console.firebase.google.com/ using the adult-managed Google account.
2. Create a project named Adventure Academy.
3. If asked about Google Analytics, it can be left off for this first version.
4. Confirm the project is on Spark. Do not add a payment method or upgrade the plan.
5. Open Build → Firestore Database and create the database. Choose a location carefully because the location cannot be changed later.
6. Open the Firestore Rules tab. Copy the complete contents of the repository's firestore.rules file into the editor and publish them.
7. Stop there. Do not enable sign-in providers yet. We will choose an age-appropriate, guardian-managed sign-in approach before enabling accounts.

Official console: https://console.firebase.google.com/

## What happens next

After the adult-managed project and rules are ready, we can add the Firebase web configuration and a small optional sync adapter. The current browser-based saving and JSON backup will remain as a fallback. The site must continue to work when Firebase is not configured or the network is unavailable.

Firebase web configuration identifies the project; it is not an admin credential. Never use a service-account private key or Admin SDK secret in browser code.

## Important status

Firebase is not connected yet. The site continues to save progress in the current browser and supports downloading/restoring a backup. These files prepare and protect the database setup; they do not create a Firebase project or deploy rules automatically.
