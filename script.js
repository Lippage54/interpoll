let questions = [];
let currentIndex = 0;
let correct = 0;
let wrong = 0;
let selectedOption = null;
const N = 20; // количество вопросов

async function loadQuiz() {
  const res = await fetch("quiz.json");
  const data = await res.json();
  questions = data.sort(() => Math.random() - 0.5).slice(0, N);
  showQuestion();
}

function showQuestion() {
  const q = questions[currentIndex];
  document.getElementById("question").textContent = q.question;
  document.getElementById("result").textContent = "";
  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";
  selectedOption = null;

  const shuffled = [...q.options].sort(() => Math.random() - 0.5);
  shuffled.forEach(opt => {
    const div = document.createElement("div");
    div.className = "option";
    div.textContent = opt;
    div.onclick = () => {
      document.querySelectorAll(".option").forEach(o => o.classList.remove("selected"));
      div.classList.add("selected");
      selectedOption = opt;
    };
    optionsDiv.appendChild(div);
  });

  document.getElementById("confirm").disabled = false;
  document.getElementById("next").disabled = true;
}

document.getElementById("confirm").onclick = () => {
  if (!selectedOption) {
    alert("Сначала выберите вариант ответа!");
    return;
  }

  const q = questions[currentIndex];
  document.querySelectorAll(".option").forEach(div => {
    if (div.textContent === q.answer) {
      div.classList.add("correct");
    }
    if (div.textContent === selectedOption && selectedOption !== q.answer) {
      div.classList.add("wrong");
    }
    div.onclick = null;
  });

  if (selectedOption === q.answer) {
    document.getElementById("result").textContent = "✅ Правильно!";
    document.getElementById("result").style.color = "green";
    correct++;
  } else {
    document.getElementById("result").textContent = "❌ Неправильно! Правильный ответ: " + q.answer;
    document.getElementById("result").style.color = "red";
    wrong++;
  }

  document.getElementById("confirm").disabled = true;
  document.getElementById("next").disabled = false;
};

document.getElementById("next").onclick = () => {
  currentIndex++;
  if (currentIndex < questions.length) {
    showQuestion();
  } else {
    const percent = ((correct / questions.length) * 100).toFixed(2);
    alert(`Правильных: ${correct}\nНеправильных: ${wrong}\nВсего: ${questions.length}\nУспеваемость: ${percent}%`);
    location.reload();
  }
};

loadQuiz();
