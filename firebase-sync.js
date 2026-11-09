// Optional cloud progress sync for Adventure Academy.
// The site keeps working locally if Firebase is unavailable or not configured.
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";
// Firestore is accessed through its HTTPS REST API below to avoid SDK offline-detection failures.

const firebaseConfig = {
  apiKey: "AIzaSyADuJvpPkuaVQG0J8Su84hjV_cwbjwi6Og",
  authDomain: "adventure-academy-822b6.firebaseapp.com",
  projectId: "adventure-academy-822b6",
  storageBucket: "adventure-academy-822b6.firebasestorage.app",
  messagingSenderId: "345746035703",
  appId: "1:345746035703:web:3f430966542464ba8ed4f2"
};
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
const progressKey = "adventure-academy-level-progress";
const profileKey = "adventure-academy-learner-profile";
const rooms = ["science","library","maths","biology","chemistry","physics","geography","history","computing","business","shona","art"];
const avatars = ["🧭","🚀","🦊","🦉","🐼","🦁","🌟","🎨"];
const status = document.querySelector("#cloud-sync-status");
const signIn = document.querySelector("#cloud-sign-in");
const signOutButton = document.querySelector("#cloud-sign-out");
let currentUser = null;
let applyingCloud = false;
let pendingWrite = Promise.resolve();

function setStatus(message) { if (status) status.textContent = message; }
function readLocal() {
  let progress = {}, profile = {};
  try { progress = JSON.parse(localStorage.getItem(progressKey) || "{}") || {}; } catch (_) {}
  try { profile = JSON.parse(localStorage.getItem(profileKey) || "{}") || {}; } catch (_) {}
  const levels = {};
  rooms.forEach(key => {
    const n = Number(progress.levels && progress.levels[key] || 0);
    levels[key] = Number.isInteger(n) ? Math.max(0, Math.min(3, n)) : 0;
  });
  return {
    schemaVersion: 1,
    nickname: typeof profile.nickname === "string" ? profile.nickname.slice(0,20) : "",
    avatar: avatars.includes(profile.avatar) ? profile.avatar : "🧭",
    visited: Array.isArray(progress.visited) ? [...new Set(progress.visited.filter(k => rooms.includes(k)))] : [],
    levels
  };
}
function firestoreValue(value) {
  if (typeof value === "string") return { stringValue: value };
  if (typeof value === "boolean") return { booleanValue: value };
  if (typeof value === "number" && Number.isInteger(value)) return { integerValue: String(value) };
  if (Array.isArray(value)) return { arrayValue: { values: value.map(firestoreValue) } };
  if (value && typeof value === "object") {
    const fields = {};
    Object.entries(value).forEach(([key, item]) => { fields[key] = firestoreValue(item); });
    return { mapValue: { fields } };
  }
  return { nullValue: null };
}
function plainValue(value) {
  if (!value) return null;
  if ("stringValue" in value) return value.stringValue;
  if ("integerValue" in value) return Number(value.integerValue);
  if ("doubleValue" in value) return Number(value.doubleValue);
  if ("booleanValue" in value) return value.booleanValue;
  if ("nullValue" in value) return null;
  if ("arrayValue" in value) return (value.arrayValue.values || []).map(plainValue);
  if ("mapValue" in value) {
    const result = {};
    Object.entries(value.mapValue.fields || {}).forEach(([key, item]) => { result[key] = plainValue(item); });
    return result;
  }
  return null;
}
async function firestoreRequest(user, method, url, body) {
  const token = await user.getIdToken();
  const response = await fetch(url, {
    method,
    headers: { "Authorization": `Bearer ${token}`, ...(body ? { "Content-Type": "application/json" } : {}) },
    ...(body ? { body: JSON.stringify(body) } : {})
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(payload.error?.message || `Firestore HTTP ${response.status}`);
    error.code = payload.error?.status || String(response.status);
    throw error;
  }
  return payload;
}
function documentName(user) {
  return `projects/${firebaseConfig.projectId}/databases/(default)/documents/learners/${user.uid}/progress/current`;
}
async function readCloud(user) {
  const url = `https://firestore.googleapis.com/v1/${documentName(user)}`;
  try {
    const result = await firestoreRequest(user, "GET", url);
    return Object.fromEntries(Object.entries(result.fields || {}).map(([key, value]) => [key, plainValue(value)]));
  } catch (error) {
    if (error.code === "NOT_FOUND" || String(error.message).includes("NOT_FOUND")) return null;
    throw error;
  }
}
async function writeCloud(user, data) {
  const fields = {};
  Object.entries(data).forEach(([key, value]) => { fields[key] = firestoreValue(value); });
  const url = `https://firestore.googleapis.com/v1/projects/${firebaseConfig.projectId}/databases/(default)/documents:commit`;
  await firestoreRequest(user, "POST", url, {
    writes: [{
      update: { name: documentName(user), fields },
      updateTransforms: [{ fieldPath: "updatedAt", setToServerValue: "REQUEST_TIME" }]
    }]
  });
}
function saveCloud() {
  if (!currentUser || applyingCloud) return;
  const user = currentUser;
  const data = readLocal();
  pendingWrite = pendingWrite.then(() => writeCloud(user, data))
    .then(() => setStatus("Cloud sync is on. Your progress is backed up to your signed-in account."))
    .catch(error => {
      console.error("Adventure Academy cloud save failed:", error);
      setStatus("Cloud save failed: " + (error.message || "Please check your connection."));
    });
}
async function loadCloud(user) {
  currentUser = user;
  setStatus("Signed in. Checking your cloud progress…");
  try {
    const cloud = await readCloud(user);
    const local = readLocal();
    if (cloud) {
      const levels = {};
      rooms.forEach(key => {
        const a = Math.max(0, Math.min(3, Number(local.levels[key]) || 0));
        const b = Math.max(0, Math.min(3, Number(cloud.levels && cloud.levels[key]) || 0));
        levels[key] = Math.max(a, b);
      });
      const useLocalProfile = !!local.nickname;
      const merged = {
        schemaVersion: 1,
        nickname: useLocalProfile ? local.nickname : (typeof cloud.nickname === "string" ? cloud.nickname.slice(0,20) : ""),
        avatar: useLocalProfile ? local.avatar : (avatars.includes(cloud.avatar) ? cloud.avatar : "🧭"),
        visited: [...new Set([...local.visited, ...(Array.isArray(cloud.visited) ? cloud.visited.filter(k => rooms.includes(k)) : [])])],
        levels
      };
      applyingCloud = true;
      localStorage.setItem(progressKey, JSON.stringify({ visited: merged.visited, levels: merged.levels }));
      localStorage.setItem(profileKey, JSON.stringify({ nickname: merged.nickname, avatar: merged.avatar }));
      window.dispatchEvent(new CustomEvent("academy:cloud-progress-loaded", { detail: merged }));
      applyingCloud = false;
    }
    await writeCloud(user, readLocal());
    setStatus("Cloud sync is on. Your progress is backed up to your signed-in account.");
  } catch (error) {
    applyingCloud = false;
    console.error("Adventure Academy cloud load failed:", error);
    setStatus("Cloud sync failed: " + (error.message || "Please check your connection."));
  }
}
if (signIn) signIn.addEventListener("click", async () => {
  signIn.disabled = true;
  setStatus("Opening Google sign-in…");
  try { await signInWithPopup(auth, provider); }
  catch (error) {
    console.error("Adventure Academy sign-in failed:", error);
    setStatus(error.code === "auth/unauthorized-domain"
      ? "This website domain is not authorised yet. Follow the Firebase setup guide."
      : "Sign-in did not complete. Your local progress remains available.");
  } finally { signIn.disabled = false; }
});
if (signOutButton) signOutButton.addEventListener("click", async () => {
  try { await signOut(auth); } catch (_) { setStatus("Could not sign out just now."); }
});
onAuthStateChanged(auth, user => {
  currentUser = user;
  if (signIn) signIn.hidden = !!user;
  if (signOutButton) signOutButton.hidden = !user;
  if (user) loadCloud(user);
  else setStatus("Not signed in. Your progress is saved on this device; sign in to sync it.");
});
window.addEventListener("academy:progress-changed", saveCloud);
window.addEventListener("academy:profile-changed", saveCloud);
