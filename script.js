const stations = {
  science: { label:"SCIENCE LAB", title:"Science Lab", lessons:[
    {title:"Plants and their parts",intro:"Plants have parts that work together. Roots take in water and minerals, stems support the plant, and leaves help make food.",question:"Which plant part absorbs water from the soil?",options:["Flower","Roots","Fruit"],answer:1,explain:"Roots absorb water and minerals from the soil."},
    {title:"A fair test",intro:"A fair test changes one factor at a time and keeps other conditions the same. This helps us see what caused a result.",question:"To test whether light affects plant growth, what should stay the same?",options:["The amount of water","The amount of light","The result"],answer:0,explain:"Keep water the same while changing the light. That makes the comparison fair."},
    {title:"Living things",intro:"Living things carry out life processes such as nutrition, growth, respiration, and responding to their surroundings.",question:"Which is a life process?",options:["Rusting","Growth","Melting ice"],answer:1,explain:"Growth is one of the processes carried out by living things."}
  ]},
  library: { label:"KNOWLEDGE LIBRARY", title:"Knowledge Library", lessons:[
    {title:"Using a dictionary",intro:"A dictionary gives word meanings, pronunciation and sometimes examples. Words are usually arranged alphabetically.",question:"Where would you look to find the meaning of 'curious'?",options:["Dictionary","Atlas","Timetable"],answer:0,explain:"A dictionary explains the meaning of words."},
    {title:"Finding reliable information",intro:"Good research uses trustworthy sources. Check who created the information, when it was published and whether evidence is provided.",question:"Which is the strongest sign of a reliable information source?",options:["It has lots of bright colours","It names its author and gives evidence","It makes a surprising claim"],answer:1,explain:"Named authors and evidence help readers check information."},
    {title:"Main ideas",intro:"The main idea is the most important point in a passage. Supporting details explain or give examples of that point.",question:"What does a supporting detail do?",options:["Explains the main idea","Changes the topic","Always gives a new title"],answer:0,explain:"Supporting details add information that helps explain the main idea."}
  ]},
  maths: { label:"MATHS GARDEN", title:"Maths Garden", lessons:[
    {title:"Multiplication groups",intro:"Multiplication is a quick way to add equal groups. Three groups of four can be written as 3 × 4.",question:"There are 3 rows with 4 flowers in each. How many flowers are there?",options:["7","12","14"],answer:1,explain:"3 × 4 = 12 flowers."},
    {title:"Fractions",intro:"A fraction describes equal parts of a whole. The denominator tells how many equal parts make the whole.",question:"If a pizza is cut into 4 equal slices, what fraction is one slice?",options:["1/2","1/3","1/4"],answer:2,explain:"One out of four equal slices is one quarter, or 1/4."},
    {title:"Number patterns",intro:"A number pattern follows a rule. Look at how the numbers change to find the next term.",question:"What comes next: 5, 10, 15, 20, ...?",options:["22","25","30"],answer:1,explain:"The pattern adds 5 each time, so the next number is 25."}
  ]},
  biology: { label:"BIOLOGY", title:"Biology", lessons:[
    {title:"Cells: the building blocks",intro:"All living organisms are made of cells. Some organisms have one cell, while plants and animals have many cells.",question:"What is the basic unit of life?",options:["Cell","Rock","Cloud"],answer:0,explain:"The cell is the basic unit of life."},
    {title:"Plant and animal cells",intro:"Plant cells have a cell wall, cell membrane, cytoplasm and usually a large permanent vacuole. Many also contain chloroplasts.",question:"Which structure is found in plant cells but not animal cells?",options:["Cytoplasm","Cell membrane","Cell wall"],answer:2,explain:"A cell wall supports and strengthens plant cells."},
    {title:"Food chains",intro:"A food chain shows how energy passes between organisms. Green plants are producers because they make their own food using light.",question:"What is the role of a producer in a food chain?",options:["Make its own food","Hunt every animal","Break down rocks"],answer:0,explain:"Producers, such as green plants, make food using light energy."}
  ]},
  chemistry: { label:"CHEMISTRY", title:"Chemistry", lessons:[
    {title:"Elements and compounds",intro:"An element contains one type of atom. A compound contains two or more different elements chemically joined.",question:"Which formula represents water?",options:["CO₂","H₂O","O₂"],answer:1,explain:"Water is H₂O: hydrogen and oxygen chemically combined."},
    {title:"States of matter",intro:"Matter commonly exists as solids, liquids and gases. Their particles are arranged and move differently.",question:"Which state has a fixed volume but takes the shape of its container?",options:["Solid","Liquid","Gas"],answer:1,explain:"A liquid has a fixed volume but flows to fit its container."},
    {title:"Separating mixtures",intro:"Filtration separates an insoluble solid from a liquid. The liquid passes through the filter while the solid is trapped.",question:"Which method can separate sand from water?",options:["Filtration","Magnetism","Freezing"],answer:0,explain:"Sand is trapped by filter paper while water passes through."}
  ]},
  physics: { label:"PHYSICS", title:"Physics", lessons:[
    {title:"Forces around us",intro:"A force is a push or pull. Forces can change an object's speed, direction or shape.",question:"What force pulls objects towards Earth?",options:["Friction","Magnetism","Gravity"],answer:2,explain:"Gravity attracts objects towards Earth."},
    {title:"Energy changes",intro:"Energy can be transferred from one form to another. A lamp transfers electrical energy into light and thermal energy.",question:"Which energy change happens in a simple lamp?",options:["Electrical to light and heat","Sound to chemical","Heat to nuclear"],answer:0,explain:"A lamp uses electrical energy and produces light and heat."},
    {title:"Simple circuits",intro:"A simple electric circuit needs a complete conducting path. A switch can open or close that path.",question:"What happens when a switch opens a circuit?",options:["Current stops flowing","The battery grows","The wires disappear"],answer:0,explain:"An open circuit breaks the path, so current cannot flow."}
  ]},
  geography: { label:"GEOGRAPHY", title:"Geography", lessons:[
    {title:"Our planet",intro:"The Equator is an imaginary line around the middle of Earth. It separates the Northern and Southern Hemispheres.",question:"Which line divides Earth into Northern and Southern Hemispheres?",options:["Equator","Prime Meridian","Tropic of Cancer"],answer:0,explain:"The Equator divides the Northern and Southern Hemispheres."},
    {title:"Reading maps",intro:"Maps use symbols, a key and a scale. A compass direction helps describe where places are located.",question:"What does a map key explain?",options:["The age of the map","The meaning of map symbols","Tomorrow's weather"],answer:1,explain:"A map key explains what the symbols and colours represent."},
    {title:"Weather and climate",intro:"Weather describes short-term atmospheric conditions. Climate describes the usual pattern of weather in a place over a long period.",question:"Which statement describes climate?",options:["It is raining this morning","The usual conditions over many years","The wind changed an hour ago"],answer:1,explain:"Climate is the long-term pattern of weather in a region."}
  ]},
  history: { label:"HISTORY", title:"History", lessons:[
    {title:"Evidence from the past",intro:"Historians use evidence such as letters, photographs, objects and buildings to investigate the past.",question:"What do historians study?",options:["Future predictions","Evidence about the past","Only weather patterns"],answer:1,explain:"Historians investigate the past using evidence."},
    {title:"Primary sources",intro:"A primary source comes from the time being studied. Examples include a diary, a photograph or an official record from that period.",question:"Which is a primary source for studying an event?",options:["A diary written by a witness at the time","A modern fictional story","A recent summary with no sources"],answer:0,explain:"A witness's diary from the time is a primary source."},
    {title:"Timelines",intro:"A timeline places events in chronological order, from earlier to later. It helps us understand sequence and change.",question:"What does chronological order mean?",options:["Alphabetical order","Order by importance","Order by date"],answer:2,explain:"Chronological order arranges events by the dates they happened."}
  ]},
  computing: { label:"COMPUTER SCIENCE", title:"Computer Science", lessons:[
    {title:"Algorithms",intro:"An algorithm is a clear sequence of steps for solving a problem or completing a task.",question:"What is an algorithm?",options:["A computer screen","A step-by-step set of instructions","A type of battery"],answer:1,explain:"An algorithm is a step-by-step set of instructions."},
    {title:"Input, process, output",intro:"A computer system receives input, processes it according to instructions and produces output.",question:"In a calculator, what is pressing 2 + 3?",options:["Input","Output","Storage"],answer:0,explain:"Pressing the keys supplies input to the calculator."},
    {title:"Staying safe online",intro:"Protect personal information, use strong unique passwords and ask a trusted adult for help if something online feels unsafe.",question:"What should you do with your password?",options:["Post it publicly","Share it with strangers","Keep it private"],answer:2,explain:"Keep passwords private and never post them publicly."}
  ]},
  business: { label:"BUSINESS STUDIES", title:"Business Studies", lessons:[
    {title:"Revenue and profit",intro:"Revenue is money earned from sales. Profit is what remains when costs are subtracted from revenue.",question:"What is profit?",options:["Revenue minus costs","All money spent","The number of customers"],answer:0,explain:"Profit = revenue − costs."},
    {title:"Needs and wants",intro:"Needs are essentials such as food, water and shelter. Wants are things people would like but can live without.",question:"Which is usually a basic need?",options:["A new video game","Clean drinking water","Designer accessories"],answer:1,explain:"Clean drinking water is essential for life."},
    {title:"Customers and value",intro:"Businesses aim to understand customers and offer useful products or services. Customer feedback can help improve quality.",question:"Why might a business ask customers for feedback?",options:["To ignore their views","To improve its products or service","To stop planning"],answer:1,explain:"Feedback helps a business understand what is working and what could improve."}
  ]},
  shona: { label:"SHONA", title:"Shona", lessons:[
    {title:"Mangwanani",intro:"Shona greetings can change depending on the time of day. 'Mangwanani' is commonly used to greet someone in the morning.",question:"Which greeting means 'Good morning'?",options:["Masikati","Mangwanani","Manheru"],answer:1,explain:"Mangwanani is a common greeting for good morning."},
    {title:"Everyday words",intro:"Learning everyday vocabulary helps you describe people and things. 'Mvura' means water in Shona.",question:"What does 'mvura' mean?",options:["Water","Book","House"],answer:0,explain:"Mvura means water."},
    {title:"Simple sentences",intro:"A simple sentence communicates a complete idea. In Shona, 'Ndinoda kuverenga' means 'I like to read'.",question:"What does 'Ndinoda kuverenga' mean?",options:["I am going home","I like to read","It is raining"],answer:1,explain:"Ndinoda kuverenga means I like to read."}
  ]},
  art: { label:"ART AND DESIGN", title:"Art and Design", lessons:[
    {title:"Primary colours",intro:"In traditional paint mixing, red, yellow and blue are taught as primary colours. They can be mixed to make other colours.",question:"Which are the traditional primary colours in paint?",options:["Red, yellow and blue","Green, orange and purple","Black, white and grey"],answer:0,explain:"Red, yellow and blue are the traditional primary colours in paint."},
    {title:"Elements of design",intro:"Line, shape, colour, texture, form and space are elements artists use to create visual work.",question:"Which design element describes how a surface feels or looks like it feels?",options:["Texture","Volume","Speed"],answer:0,explain:"Texture describes the surface quality of an artwork."},
    {title:"Planning a design",intro:"A design brief explains the purpose and audience of a project. Sketches help explore ideas before making a final design.",question:"What is a useful first step before creating a poster?",options:["Ignore the audience","Understand the purpose and audience","Choose random words"],answer:1,explain:"Knowing the purpose and audience helps guide design choices."}
  ]}
};

const STORAGE_KEY = "adventure-academy-level-progress";
const visited = new Set();
const levels = Object.fromEntries(Object.keys(stations).map(key => [key, 0]));
const completed = new Set();
function loadProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (saved && typeof saved === "object") {
      (Array.isArray(saved.visited) ? saved.visited : []).forEach(key => { if (stations[key]) visited.add(key); });
      Object.keys(stations).forEach(key => {
        const value = Number(saved.levels && saved.levels[key]);
        levels[key] = Number.isFinite(value) ? Math.max(0, Math.min(3, Math.floor(value))) : 0;
        if (levels[key] >= 3) completed.add(key);
      });
    } else {
      const old = JSON.parse(localStorage.getItem("adventure-academy-progress") || "{}");
      (Array.isArray(old.visited) ? old.visited : []).forEach(key => { if (stations[key]) visited.add(key); });
      (Array.isArray(old.completed) ? old.completed : []).forEach(key => { if (stations[key]) levels[key] = 1; });
    }
  } catch (error) { console.warn("Could not load saved academy progress.", error); }
}
function saveProgress() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify({visited:[...visited],levels})); window.dispatchEvent(new Event("academy:progress-changed")); }
  catch (error) { console.warn("Could not save academy progress.", error); }
}
const dialog = document.querySelector("#station-dialog");
const count = document.querySelector("#visited-count");
const quiz = document.querySelector("#quiz-area");
const interior = document.querySelector("#academy-interior");
const campusSections = [document.querySelector(".hero"),document.querySelector(".campus-section"),document.querySelector(".mission")];
let activeKey = null;
function updateProgress() {
  count.textContent = String(visited.size);
  document.querySelector("#completed-count").textContent = String(completed.size);
  const lessonTotal = Object.values(levels).reduce((sum, level) => sum + level, 0);
  const percent = Math.round((lessonTotal / 36) * 100);
  document.querySelector("#lessons-completed").textContent = String(lessonTotal);
  document.querySelector("#subjects-mastered").textContent = String(completed.size);
  document.querySelector("#lessons-remaining").textContent = String(36 - lessonTotal);
  document.querySelector("#overall-percent").textContent = percent + "% COMPLETE";
  document.querySelector("#overall-progress").setAttribute("aria-valuenow", String(lessonTotal));
  document.querySelector("#overall-progress-fill").style.width = percent + "%";
  Object.keys(stations).forEach(key => {
    const badge = document.querySelector("#badge-" + key);
    if (!badge) return;
    badge.classList.toggle("is-earned", completed.has(key));
    const status = badge.querySelector("b");
    if (status) status.textContent = completed.has(key) ? "EARNED ✓" : "LEVEL " + levels[key] + "/3";
    const card = document.querySelector('.room-card[data-room="' + key + '"]');
    if (card) {
      let progress = card.querySelector(".room-progress");
      if (!progress) { progress = document.createElement("small"); progress.className = "room-progress"; card.append(progress); }
      progress.textContent = completed.has(key) ? "SUBJECT MASTERED ✓" : "LEVEL " + (levels[key] + 1) + " OF 3";
    }
  });
}
function showInterior() {
  campusSections.forEach(section => { section.hidden = true; });
  interior.hidden = false;
  interior.scrollIntoView({behavior:"smooth",block:"start"});
}
function showCampus() {
  interior.hidden = true;
  campusSections.forEach(section => { section.hidden = false; });
  document.querySelector(".campus-section").scrollIntoView({behavior:"smooth",block:"start"});
}
function showLesson(key) {
  const subject = stations[key];
  const level = levels[key];
  if (level >= 3) {
    quiz.replaceChildren();
    const done = document.createElement("p"); done.className = "quiz-feedback"; done.textContent = "You have completed all three levels in this subject. Your discovery badge is earned!";
    quiz.append(done);
    return;
  }
  const lesson = subject.lessons[level];
  document.querySelector("#dialog-eyebrow").textContent = subject.label + " · LEVEL " + (level + 1) + " OF 3";
  document.querySelector("#dialog-title").textContent = lesson.title;
  document.querySelector("#dialog-description").textContent = lesson.intro;
  quiz.replaceChildren();
  const question = document.createElement("p"); question.className = "quiz-question"; question.textContent = lesson.question; quiz.append(question);
  const feedback = document.createElement("p"); feedback.className = "quiz-feedback"; feedback.setAttribute("aria-live","polite");
  lesson.options.forEach((option,index) => {
    const button = document.createElement("button"); button.type = "button"; button.className = "quiz-option"; button.textContent = option;
    button.addEventListener("click", () => {
      if (button.disabled) return;
      if (index !== lesson.answer) {
        button.classList.add("is-incorrect"); feedback.textContent = "Not quite. Read the lesson again and try another answer."; return;
      }
      quiz.querySelectorAll(".quiz-option").forEach(choice => { choice.disabled = true; });
      button.classList.add("is-correct");
      levels[key] = Math.min(3, levels[key] + 1);
      if (levels[key] >= 3) completed.add(key);
      saveProgress(); updateProgress();
      feedback.textContent = lesson.explain + (levels[key] >= 3 ? " Subject mastered! You earned its discovery badge." : " Level complete! Your next lesson is ready.");
      const next = document.createElement("button"); next.type = "button"; next.className = "lesson-next";
      next.textContent = levels[key] >= 3 ? "FINISH SUBJECT ✓" : "CONTINUE TO LEVEL " + (levels[key] + 1) + " →";
      next.addEventListener("click", () => {
        if (levels[key] >= 3) { if (typeof dialog.close === "function") dialog.close(); else dialog.removeAttribute("open"); }
        else showLesson(key);
      });
      quiz.append(feedback,next);
      const guide = document.querySelector("#guide-message");
      if (guide) guide.textContent = levels[key] >= 3 ? "Brilliant work! You mastered " + subject.label + " and earned its badge. Pick another subject." : "Well done! You unlocked the next lesson in " + subject.label + ". Keep going!";
    });
    quiz.append(button);
  });
  quiz.append(feedback);
}
function openStation(key) {
  if (!stations[key]) return;
  activeKey = key;
  visited.add(key); saveProgress(); updateProgress();
  showLesson(key);
  if (typeof dialog.showModal === "function") { if (!dialog.open) dialog.showModal(); }
  else dialog.setAttribute("open","");
}
document.querySelector("#enter-academy").addEventListener("click",showInterior);
document.querySelector("#back-campus").addEventListener("click",showCampus);
document.querySelector("#next-mission").addEventListener("click",() => {
  const nextKey = Object.keys(stations).find(key => levels[key] < 3);
  const guide = document.querySelector("#guide-message");
  if (!nextKey) { if (guide) guide.textContent = "Amazing explorer! You have mastered all twelve subjects and earned every badge."; return; }
  if (guide) guide.textContent = "Your next mission is " + stations[nextKey].label + ", Level " + (levels[nextKey] + 1) + ".";
  openStation(nextKey);
});
document.querySelectorAll(".station, .room-card").forEach(button => button.addEventListener("click",() => openStation(button.dataset.station || button.dataset.room)));
document.querySelector(".close").addEventListener("click",() => { if (typeof dialog.close === "function") dialog.close(); else dialog.removeAttribute("open"); });
dialog.addEventListener("click",event => { if (event.target === dialog && typeof dialog.close === "function") dialog.close(); });
dialog.addEventListener("cancel",event => { event.preventDefault(); if (typeof dialog.close === "function") dialog.close(); });
const profileForm = document.querySelector("#profile-form");
const profileName = document.querySelector("#profile-name");
const profileAvatar = document.querySelector("#profile-avatar");
const profileSubtitle = document.querySelector("#profile-subtitle");
const profileFeedback = document.querySelector("#profile-feedback");
const profileStorageKey = "adventure-academy-learner-profile";
function loadProfile() {
  try {
    const saved = JSON.parse(localStorage.getItem(profileStorageKey) || "{}");
    const nickname = typeof saved.nickname === "string" ? saved.nickname.slice(0,20) : "";
    const avatar = ["🧭","🚀","🦊","🦉","🐼","🦁","🌟","🎨"].includes(saved.avatar) ? saved.avatar : "🧭";
    document.querySelector("#learner-nickname").value = nickname;
    document.querySelector("#learner-avatar").value = avatar;
    renderProfile(nickname, avatar);
  } catch (error) { renderProfile("", "🧭"); }
}
function renderProfile(nickname, avatar) {
  profileName.textContent = nickname ? "Welcome, " + nickname + "!" : "Welcome, Explorer!";
  profileAvatar.textContent = avatar;
  profileSubtitle.textContent = "Your learning journey is saved on this device.";
}
profileForm.addEventListener("submit", event => {
  event.preventDefault();
  const nickname = document.querySelector("#learner-nickname").value.trim().replace(/\s+/g, " ").slice(0,20);
  const avatar = document.querySelector("#learner-avatar").value;
  try {
    localStorage.setItem(profileStorageKey, JSON.stringify({nickname, avatar}));
    window.dispatchEvent(new Event("academy:profile-changed"));
    renderProfile(nickname, avatar);
    profileFeedback.textContent = "Profile saved on this device.";
  } catch (error) {
    profileFeedback.textContent = "This browser could not save your profile. Your lessons can still be explored.";
  }
});

const exportButton = document.querySelector("#export-progress");
const importInput = document.querySelector("#import-progress");
const backupFeedback = document.querySelector("#backup-feedback");
function makeBackup() {
  const profile = JSON.parse(localStorage.getItem(profileStorageKey) || "{}");
  return {format:"adventure-academy-backup",version:1,createdAt:new Date().toISOString(),profile,progress:{visited:[...visited],levels:{...levels}}};
}
exportButton.addEventListener("click", () => {
  try {
    const blob = new Blob([JSON.stringify(makeBackup(), null, 2)], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url; link.download = "adventure-academy-backup.json";
    document.body.append(link); link.click(); link.remove(); URL.revokeObjectURL(url);
    backupFeedback.textContent = "Backup downloaded. Keep that file somewhere safe.";
  } catch (error) {
    backupFeedback.textContent = "The backup could not be created in this browser.";
  }
});
importInput.addEventListener("change", () => {
  const file = importInput.files && importInput.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(String(reader.result || ""));
      if (!data || data.format !== "adventure-academy-backup" || data.version !== 1 ||
          !data.progress || !Array.isArray(data.progress.visited) ||
          !data.progress.levels || typeof data.progress.levels !== "object") throw new Error("Invalid backup");
      const validVisited = data.progress.visited.filter(key => stations[key]);
      const restoredLevels = {};
      Object.keys(stations).forEach(key => {
        const value = Number(data.progress.levels[key] || 0);
        if (!Number.isInteger(value) || value < 0 || value > 3) throw new Error("Invalid lesson progress");
        restoredLevels[key] = value;
      });
      const savedProfile = data.profile && typeof data.profile === "object" ? data.profile : {};
      const nickname = typeof savedProfile.nickname === "string" ? savedProfile.nickname.trim().replace(/\s+/g," ").slice(0,20) : "";
      const allowedAvatars = ["🧭","🚀","🦊","🦉","🐼","🦁","🌟","🎨"];
      const avatar = allowedAvatars.includes(savedProfile.avatar) ? savedProfile.avatar : "🧭";
      if (!window.confirm("Restore this backup? It will replace the progress currently saved in this browser.")) {
        backupFeedback.textContent = "Restore cancelled. Your current progress is unchanged.";
        importInput.value = ""; return;
      }
      visited.clear(); validVisited.forEach(key => visited.add(key));
      Object.keys(stations).forEach(key => { levels[key] = restoredLevels[key]; });
      completed.clear(); Object.keys(stations).forEach(key => { if (levels[key] === 3) completed.add(key); });
      saveProgress();
      localStorage.setItem(profileStorageKey, JSON.stringify({nickname,avatar}));
      window.dispatchEvent(new Event("academy:profile-changed"));
      renderProfile(nickname,avatar);
      document.querySelector("#learner-nickname").value = nickname;
      document.querySelector("#learner-avatar").value = avatar;
      updateProgress();
      backupFeedback.textContent = "Backup restored successfully on this device.";
    } catch (error) {
      backupFeedback.textContent = "That file is not a valid Adventure Academy backup. Your saved progress was not changed.";
    }
    importInput.value = "";
  };
  reader.onerror = () => { backupFeedback.textContent = "The selected file could not be read."; importInput.value = ""; };
  reader.readAsText(file);
});


window.addEventListener("academy:cloud-progress-loaded", event => {
  const data = event.detail || {};
  visited.clear();
  (Array.isArray(data.visited) ? data.visited : []).forEach(key => { if (stations[key]) visited.add(key); });
  Object.keys(stations).forEach(key => {
    const value = Number(data.levels && data.levels[key] || 0);
    levels[key] = Number.isFinite(value) ? Math.max(0, Math.min(3, Math.floor(value))) : 0;
  });
  completed.clear();
  Object.keys(stations).forEach(key => { if (levels[key] >= 3) completed.add(key); });
  const nickname = typeof data.nickname === "string" ? data.nickname.slice(0,20) : "";
  const avatar = ["🧭","🚀","🦊","🦉","🐼","🦁","🌟","🎨"].includes(data.avatar) ? data.avatar : "🧭";
  document.querySelector("#learner-nickname").value = nickname;
  document.querySelector("#learner-avatar").value = avatar;
  renderProfile(nickname, avatar);
  updateProgress();
});

loadProfile(); loadProgress(); updateProgress();
