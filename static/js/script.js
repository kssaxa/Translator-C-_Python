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
    outputTxt.value = '';
    return;
  }


  logTxt.value = "Получение токкенов...";

  try {

    const response = await fetch(`/process_text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({ text: cppCode })
    });


    if (!response.ok) throw new Error('Ошибка при запросе');

    const result = await response.json();


    if (result.tokkens == null){
      logTxt.value += `\nОшибка токкенизации: tokkens = ${result.tokkens}`;
      outputTxt.value = '';
    }
    else{
      logTxt.value += `\n Токенизация успешна:\n${result.tokkens}`;
      logTxt.value += `\n Построение дерева:\n${result.tree}`;

      if(result.semanalize == 1){
        logTxt.value += `\n Семантический анализ прошел успешно!:\n`;

        outputTxt.value = result.code;
      }
      else{
        logTxt.value += `\n Семантический анализ завершился с ошибкой!:\n`;
        alert('Ошибка семантического анализа');
        outputTxt.value = '';
      }

    }

  } catch (error) {
      console.error('Ошибка:', error);
      logTxt.value += `\nОшибка токкенизации: ${error}`;
      alert('Не удалось обработать текст');
  }

});
