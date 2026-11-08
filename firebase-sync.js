// Optional cloud progress sync for Adventure Academy.
// The site keeps working locally if Firebase is unavailable or not configured.
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";
import { getFirestore, doc, getDoc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";

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
const db = getFirestore(app);
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
function saveCloud() {
  if (!currentUser || applyingCloud) return;
  const user = currentUser;
  const data = readLocal();
  pendingWrite = pendingWrite.then(() => setDoc(
    doc(db, "learners", user.uid, "progress", "current"),
    { ...data, updatedAt: serverTimestamp() }
  )).then(() => setStatus("Cloud sync is on. Your progress is backed up to your signed-in account."))
    .catch(error => {
      console.error("Adventure Academy cloud save failed:", error);
      setStatus("Cloud save could not finish. Your progress is still saved on this device.");
    });
}
async function loadCloud(user) {
  currentUser = user;
  setStatus("Signed in. Checking your cloud progress…");
  try {
    const snapshot = await getDoc(doc(db, "learners", user.uid, "progress", "current"));
    const local = readLocal();
    if (snapshot.exists()) {
      const cloud = snapshot.data();
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
    saveCloud();
  } catch (error) {
    applyingCloud = false;
    console.error("Adventure Academy cloud load failed:", error);
    setStatus("Cloud sync is unavailable right now. Your local progress is safe.");
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
