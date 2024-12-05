const openFileBtn = document.getElementById("open_file_btn");
const inputTxt = document.getElementById("input_txt");

const fileInput = document.createElement("input");
fileInput.type = "file";
fileInput.style.display = "none";
fileInput.accept = ".cc, .cpp, .cxx, .c, .c++, .h, .hpp, .hh, .hxx, .h++";

openFileBtn.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      inputTxt.value = e.target.result;
    };
    reader.readAsText(file);
  }
});

const downloadFileBtn = document.getElementById("download_file_btn");
const outputTxt = document.getElementById("output_txt");

downloadFileBtn.addEventListener("click", function () {
  const content = outputTxt.value;

  const blob = new Blob([content], { type: "text/plain" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "translated_code.py";
  link.click();
});




const logTxt = document.getElementById("log_txt");

const translateBtn = document.getElementById("translate_btn");
translateBtn.addEventListener("click", async () => {
  const cppCode = inputTxt.value;

  if (!cppCode.trim()) {
    alert("Введите код на C++!");
    return;
  }


  logTxt.value = "Получение токкенов...";


  try {
    const response = await fetch('http://127.0.0.1:5000/process_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: cppCode })
    });


    if (!response.ok) throw new Error('Ошибка при запросе');

    const result = await response.json();

    logTxt.value += `\nТокенизация успешна:\n${result.processed_text}`;
    if (result.processed_text == null){
      logTxt.value += `\nОшибка токкенизации: tokkens = ${result.processed_text}`;
    }
    else{
      outputTxt.value = result.processed_text;
    }





  } catch (error) {
      console.error('Ошибка:', error);
      alert('Не удалось обработать текст');
  }
















});
