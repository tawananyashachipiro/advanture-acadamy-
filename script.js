const stations = {
  science: {
    label: "SCIENCE LAB",
    title: "A curious question!",
    description: "Science helps us understand the world by asking questions, observing and testing ideas.",
    question: "Which part of a plant usually absorbs water from the soil?",
    options: ["The flower", "The roots", "The leaves"],
    answer: 1,
    correct: "Correct! Roots absorb water and minerals from the soil.",
    retry: "Not quite. Think about the part that grows underground."
  },
  library: {
    label: "KNOWLEDGE LIBRARY",
    title: "Words open worlds.",
    description: "The library is a place to read, research and connect ideas. Every good question can lead to a new discovery.",
    question: "Which resource helps you find the meaning of an unfamiliar word?",
    options: ["A dictionary", "A calculator", "A map"],
    answer: 0,
    correct: "Exactly! A dictionary explains word meanings.",
    retry: "Try again. Think of a book that explains words."
  },
  maths: {
    label: "MATHS GARDEN",
    title: "Patterns are everywhere.",
    description: "Mathematics helps us notice patterns, solve problems and make sense of numbers around us.",
    question: "There are 3 rows with 4 flowers in each row. How many flowers are there?",
    options: ["7 flowers", "12 flowers", "14 flowers"],
    answer: 1,
    correct: "That's right! 3 groups of 4 make 12.",
    retry: "Try again. Add 4 + 4 + 4, or multiply 3 by 4."
  }
};

const STORAGE_KEY = "adventure-academy-progress";
const visited = new Set();
const completed = new Set();

function loadProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    (Array.isArray(saved.visited) ? saved.visited : []).forEach(key => {
      if (stations[key]) visited.add(key);
    });
    (Array.isArray(saved.completed) ? saved.completed : []).forEach(key => {
      if (stations[key]) completed.add(key);
    });
  } catch (error) {
    console.warn("Could not load saved academy progress.", error);
  }
}

function saveProgress() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      visited: [...visited],
      completed: [...completed]
    }));
  } catch (error) {
    console.warn("Could not save academy progress.", error);
  }
}

const dialog = document.querySelector("#station-dialog");
const count = document.querySelector("#visited-count");
const quiz = document.querySelector("#quiz-area");
const interior = document.querySelector("#academy-interior");
const campusSections = [
  document.querySelector(".hero"),
  document.querySelector(".campus-section"),
  document.querySelector(".mission")
];

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
  document.querySelector(".campus-section").scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}

function openStation(key) {
  const station = stations[key];
  if (!station || !dialog || !quiz) return;

  visited.add(key);
  saveProgress();
  updateProgress();

  document.querySelector("#dialog-eyebrow").textContent = station.label;
  document.querySelector("#dialog-title").textContent = station.title;
  document.querySelector("#dialog-description").textContent = station.description;
  quiz.replaceChildren();

  const question = document.createElement("p");
  question.className = "quiz-question";
  question.textContent = station.question;
  quiz.append(question);

  const feedback = document.createElement("p");
  feedback.className = "quiz-feedback";
  feedback.setAttribute("aria-live", "polite");

  station.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "quiz-option";
    button.textContent = option;

    button.addEventListener("click", () => {
      if (completed.has(key)) return;

      if (index === station.answer) {
        completed.add(key);
        saveProgress();
        quiz.querySelectorAll(".quiz-option").forEach(choice => {
          choice.disabled = true;
        });
        button.setAttribute("aria-pressed", "true");
        button.classList.add("is-correct");
        feedback.textContent = station.correct + " Challenge completed!";
        updateProgress();
        const guideMessage = document.querySelector("#guide-message");
        if (guideMessage) guideMessage.textContent = "Brilliant work! You earned a discovery badge. Choose another room or ask me for your next mission.";
      } else {
        button.classList.add("is-incorrect");
        feedback.textContent = station.retry;
        button.setAttribute("aria-pressed", "false");
      }
    });

    quiz.append(button);
  });

  if (completed.has(key)) {
    quiz.querySelectorAll(".quiz-option").forEach(choice => {
      choice.disabled = true;
    });
    feedback.textContent = "You've already completed this challenge. Great work!";
  }

  quiz.append(feedback);

  if (typeof dialog.showModal === "function") {
    if (!dialog.open) dialog.showModal();
  } else {
    dialog.setAttribute("open", "");
  }
}

document.querySelector("#enter-academy").addEventListener("click", showInterior);
document.querySelector("#back-campus").addEventListener("click", showCampus);

document.querySelector("#next-mission").addEventListener("click", () => {
  const nextKey = Object.keys(stations).find(key => !completed.has(key));
  const guideMessage = document.querySelector("#guide-message");
  if (!nextKey) {
    if (guideMessage) guideMessage.textContent = "Amazing explorer! You have earned all three discovery badges. More adventures are coming soon.";
    return;
  }
  if (guideMessage) guideMessage.textContent = "Let's explore the " + stations[nextKey].label.toLowerCase() + "! Complete its challenge to earn a badge.";
  openStation(nextKey);
});

document.querySelectorAll(".station").forEach(button => {
  button.addEventListener("click", () => openStation(button.dataset.station));
});

document.querySelectorAll(".room-card").forEach(button => {
  button.addEventListener("click", () => openStation(button.dataset.room));
});

document.querySelector(".close").addEventListener("click", () => {
  if (typeof dialog.close === "function") dialog.close();
  else dialog.removeAttribute("open");
});

dialog.addEventListener("click", event => {
  if (event.target === dialog && typeof dialog.close === "function") {
    dialog.close();
  }
});

dialog.addEventListener("cancel", event => {
  event.preventDefault();
  if (typeof dialog.close === "function") dialog.close();
});

loadProgress();
updateProgress();
