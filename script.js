const stations = {
  science: { label: "SCIENCE LAB", title: "Science Lab discovery challenge", description: "Explore scientific questions and discoveries.", question: "Which part of a plant absorbs most water from soil?", options: ["Flower","Roots","Stem"], answer: 1, correct: "Roots absorb water and minerals from the soil.", retry: "Not quite. Try again, and think about the lesson topic." },
  library: { label: "KNOWLEDGE LIBRARY", title: "Knowledge Library discovery challenge", description: "Build reading, research and vocabulary skills.", question: "Which reference book explains the meanings of words?", options: ["Atlas","Dictionary","Almanac"], answer: 1, correct: "A dictionary explains word meanings.", retry: "Not quite. Try again, and think about the lesson topic." },
  maths: { label: "MATHS GARDEN", title: "Maths Garden discovery challenge", description: "Solve number problems and discover patterns.", question: "There are 3 rows with 4 flowers in each. How many flowers?", options: ["7","12","14"], answer: 1, correct: "3 × 4 = 12 flowers.", retry: "Not quite. Try again, and think about the lesson topic." },
  biology: { label: "BIOLOGY", title: "Biology discovery challenge", description: "Explore living things, cells and ecosystems.", question: "What is the basic unit of life?", options: ["Cell","Rock","Cloud"], answer: 0, correct: "The cell is the basic unit of life.", retry: "Not quite. Try again, and think about the lesson topic." },
  chemistry: { label: "CHEMISTRY", title: "Chemistry discovery challenge", description: "Discover matter, elements and reactions.", question: "What is the chemical symbol for water?", options: ["CO₂","H₂O","O₂"], answer: 1, correct: "Water is H₂O: two hydrogen atoms and one oxygen atom.", retry: "Not quite. Try again, and think about the lesson topic." },
  physics: { label: "PHYSICS", title: "Physics discovery challenge", description: "Investigate forces, energy, light and motion.", question: "What force pulls objects towards Earth?", options: ["Friction","Magnetism","Gravity"], answer: 2, correct: "Gravity attracts objects towards Earth.", retry: "Not quite. Try again, and think about the lesson topic." },
  geography: { label: "GEOGRAPHY", title: "Geography discovery challenge", description: "Explore maps, landscapes, climate and people.", question: "Which imaginary line divides Earth into Northern and Southern Hemispheres?", options: ["Equator","Prime Meridian","Tropic of Cancer"], answer: 0, correct: "The Equator divides the Northern and Southern Hemispheres.", retry: "Not quite. Try again, and think about the lesson topic." },
  history: { label: "HISTORY", title: "History discovery challenge", description: "Study people, events and the past.", question: "What do historians study?", options: ["Future predictions","Evidence about the past","Weather patterns"], answer: 1, correct: "Historians use evidence to understand the past.", retry: "Not quite. Try again, and think about the lesson topic." },
  computing: { label: "COMPUTER SCIENCE", title: "Computer Science discovery challenge", description: "Learn algorithms, data and digital thinking.", question: "What is an algorithm?", options: ["A computer screen","A step-by-step set of instructions","A type of battery"], answer: 1, correct: "An algorithm is a step-by-step set of instructions.", retry: "Not quite. Try again, and think about the lesson topic." },
  business: { label: "BUSINESS STUDIES", title: "Business Studies discovery challenge", description: "Explore enterprise, money and decision-making.", question: "What is profit?", options: ["Money left after costs are subtracted from revenue","All money spent","The number of customers"], answer: 0, correct: "Profit is revenue minus costs.", retry: "Not quite. Try again, and think about the lesson topic." },
  shona: { label: "SHONA", title: "Shona discovery challenge", description: "Grow Shona vocabulary, reading and language skills.", question: "What is the Shona greeting commonly used for 'Good morning'?", options: ["Masikati","Mangwanani","Manheru"], answer: 1, correct: "Mangwanani is a common Shona greeting for good morning.", retry: "Not quite. Try again, and think about the lesson topic." },
  art: { label: "ART AND DESIGN", title: "Art and Design discovery challenge", description: "Explore colour, drawing, design and creativity.", question: "Which are the three traditional primary colours in paint?", options: ["Red, yellow and blue","Green, orange and purple","Black, white and grey"], answer: 0, correct: "Red, yellow and blue are the traditional primary colours in paint.", retry: "Not quite. Try again, and think about the lesson topic." }
};

const STORAGE_KEY = "adventure-academy-progress";
const visited = new Set();
const completed = new Set();

function loadProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    (Array.isArray(saved.visited) ? saved.visited : []).forEach(key => { if (stations[key]) visited.add(key); });
    (Array.isArray(saved.completed) ? saved.completed : []).forEach(key => { if (stations[key]) completed.add(key); });
  } catch (error) { console.warn("Could not load saved academy progress.", error); }
}
function saveProgress() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ visited: [...visited], completed: [...completed] })); }
  catch (error) { console.warn("Could not save academy progress.", error); }
}
const dialog = document.querySelector("#station-dialog");
const count = document.querySelector("#visited-count");
const quiz = document.querySelector("#quiz-area");
const interior = document.querySelector("#academy-interior");
const campusSections = [document.querySelector(".hero"), document.querySelector(".campus-section"), document.querySelector(".mission")];
function updateProgress() {
  count.textContent = String(visited.size);
  const completedCount = document.querySelector("#completed-count");
  if (completedCount) completedCount.textContent = String(completed.size);
  Object.keys(stations).forEach(key => {
    const badge = document.querySelector("#badge-" + key);
    if (!badge) return;
    badge.classList.toggle("is-earned", completed.has(key));
    const status = badge.querySelector("b");
    if (status) status.textContent = completed.has(key) ? "EARNED ✓" : "LOCKED";
  });
}
function showInterior() {
  campusSections.forEach(section => { section.hidden = true; });
  interior.hidden = false;
  interior.scrollIntoView({ behavior: "smooth", block: "start" });
}
function showCampus() {
  interior.hidden = true;
  campusSections.forEach(section => { section.hidden = false; });
  document.querySelector(".campus-section").scrollIntoView({ behavior: "smooth", block: "start" });
}
function openStation(key) {
  const station = stations[key];
  if (!station || !dialog || !quiz) return;
  visited.add(key); saveProgress(); updateProgress();
  document.querySelector("#dialog-eyebrow").textContent = station.label;
  document.querySelector("#dialog-title").textContent = station.title;
  document.querySelector("#dialog-description").textContent = station.description;
  quiz.replaceChildren();
  const question = document.createElement("p"); question.className = "quiz-question"; question.textContent = station.question; quiz.append(question);
  const feedback = document.createElement("p"); feedback.className = "quiz-feedback"; feedback.setAttribute("aria-live", "polite");
  station.options.forEach((option, index) => {
    const button = document.createElement("button"); button.type = "button"; button.className = "quiz-option"; button.textContent = option;
    button.addEventListener("click", () => {
      if (completed.has(key)) return;
      if (index === station.answer) {
        completed.add(key); saveProgress();
        quiz.querySelectorAll(".quiz-option").forEach(choice => { choice.disabled = true; });
        button.setAttribute("aria-pressed", "true"); button.classList.add("is-correct");
        feedback.textContent = station.correct + " Challenge completed!"; updateProgress();
        const guideMessage = document.querySelector("#guide-message");
        if (guideMessage) guideMessage.textContent = "Excellent work! You earned a badge. Choose another subject to keep learning.";
      } else {
        button.classList.add("is-incorrect"); button.setAttribute("aria-pressed", "false");
        feedback.textContent = station.retry;
      }
    });
    quiz.append(button);
  });
  if (completed.has(key)) {
    quiz.querySelectorAll(".quiz-option").forEach(choice => { choice.disabled = true; });
    feedback.textContent = "You've already completed this challenge. Great work!";
  }
  quiz.append(feedback);
  if (typeof dialog.showModal === "function") { if (!dialog.open) dialog.showModal(); }
  else dialog.setAttribute("open", "");
}
document.querySelector("#enter-academy").addEventListener("click", showInterior);
document.querySelector("#back-campus").addEventListener("click", showCampus);
document.querySelector("#next-mission").addEventListener("click", () => {
  const nextKey = Object.keys(stations).find(key => !completed.has(key));
  const guideMessage = document.querySelector("#guide-message");
  if (!nextKey) { if (guideMessage) guideMessage.textContent = "Amazing explorer! You have earned all twelve discovery badges."; return; }
  if (guideMessage) guideMessage.textContent = "Your next mission is " + stations[nextKey].label + ". Complete its challenge to earn a badge.";
  openStation(nextKey);
});
document.querySelectorAll(".station, .room-card").forEach(button => {
  button.addEventListener("click", () => openStation(button.dataset.station || button.dataset.room));
});
document.querySelector(".close").addEventListener("click", () => {
  if (typeof dialog.close === "function") dialog.close(); else dialog.removeAttribute("open");
});
dialog.addEventListener("click", event => { if (event.target === dialog && typeof dialog.close === "function") dialog.close(); });
dialog.addEventListener("cancel", event => { event.preventDefault(); if (typeof dialog.close === "function") dialog.close(); });
loadProgress(); updateProgress();
