const stations = {
  science: {label:"SCIENCE LAB",title:"A curious question!",description:"Science helps us understand the world by asking questions, observing and testing ideas.",question:"Which part of a plant usually absorbs water from the soil?",options:["The flower","The roots","The leaves"],answer:1,correct:"Correct! Roots absorb water and minerals from the soil.",retry:"Not quite. Think about the part that grows underground."},
  library: {label:"KNOWLEDGE LIBRARY",title:"Words open worlds.",description:"The library is a place to read, research and connect ideas. Every good question can lead to a new discovery.",question:"Which resource helps you find the meaning of an unfamiliar word?",options:["A dictionary","A calculator","A map"],answer:0,correct:"Exactly! A dictionary explains word meanings.",retry:"Try again. Think of a book that explains words."},
  maths: {label:"MATHS GARDEN",title:"Patterns are everywhere.",description:"Mathematics helps us notice patterns, solve problems and make sense of numbers around us.",question:"There are 3 rows with 4 flowers in each row. How many flowers are there?",options:["7 flowers","12 flowers","14 flowers"],answer:1,correct:"That's right! 3 groups of 4 make 12.",retry:"Try again. Add 4 + 4 + 4, or multiply 3 by 4."}
};
const visited = new Set();
const dialog = document.querySelector("#station-dialog");
const count = document.querySelector("#visited-count");
const quiz = document.querySelector("#quiz-area");
document.querySelectorAll(".station").forEach(button => button.addEventListener("click", () => openStation(button.dataset.station)));
const campusSections = [document.querySelector(".hero"), document.querySelector(".campus-section"), document.querySelector(".mission")];
const interior = document.querySelector("#academy-interior");
document.querySelector("#enter-academy").addEventListener("click", () => { campusSections.forEach(section => section.hidden = true); interior.hidden = false; interior.scrollIntoView({behavior:"smooth", block:"start"}); });
document.querySelector("#back-campus").addEventListener("click", () => { interior.hidden = true; campusSections.forEach(section => section.hidden = false); document.querySelector(".campus-section").scrollIntoView({behavior:"smooth", block:"start"}); });
document.querySelectorAll(".room-card").forEach(button => button.addEventListener("click", () => openStation(button.dataset.room)));
document.querySelector(".close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });
function openStation(key) {
  const station = stations[key];
  if (!station) return;
  visited.add(key);
  count.textContent = visited.size;
  document.querySelector("#dialog-eyebrow").textContent = station.label;
  document.querySelector("#dialog-title").textContent = station.title;
  document.querySelector("#dialog-description").textContent = station.description;
  quiz.replaceChildren();
  const question = document.createElement("p");
  question.className = "quiz-question";
  question.textContent = station.question;
  quiz.append(question);
  station.options.forEach((option,index) => {
    const button = document.createElement("button");
    button.className = "quiz-option";
    button.textContent = option;
    button.addEventListener("click", () => {
      quiz.querySelectorAll(".quiz-option").forEach(choice => { choice.disabled = true; });
      feedback.textContent = index === station.answer ? station.correct : station.retry;
      if (index === station.answer) button.style.borderColor = "#399b91";
    });
    quiz.append(button);
  });
  const feedback = document.createElement("p");
  feedback.className = "quiz-feedback";
  feedback.setAttribute("aria-live","polite");
  quiz.append(feedback);
  dialog.showModal();
}