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



  logTxt.value = "Получение токкенов...\n";
  // try{
  //   const response = await fetch('/get_tokkens', {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',},
  //     body: JSON.stringify({ code: cppCode })
  //   });
  //   if (!response.ok) throw new Error('Ошибка при запросе');
  //   const tokens = await response.json();

  //   if ( tokens.tokens_error == false){
  //     logTxt.value += `Токены получены:\n${tokens.tokens.join('\n')}\n`;
  //     try{
  //       logTxt.value += "Построение дерева...\n";
  //       const response2 = await fetch('/get_tree', {
  //         method: 'POST',
  //         headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',},
  //         body: JSON.stringify({ tokkens: tokens.tokens })
  //       });
  //       if (!response2.ok) throw new Error('Ошибка при запросе');
  //       const tree = await response2.json();
  //       logTxt.value += `Дерево построено:\n${tree.tree}\n`;
  //     } catch (error){
  //       logTxt.value += `Ошибка при построении дерева: ${error.message}\n`
  //       return;
  //     }
  //   }




  // } catch (error){
  //     logTxt.value += `Ошибка при получении токенов: ${error.message}\n`
  //     return;
  // }






  // try{
  //   logTxt.value += "Проверка семантики...\n";
  //   const response4 = await fetch('/check_semantics', {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',},
  //     body: JSON.stringify({ tree })
  //   });
  // } catch(error){}

  // try{
  //   logTxt.value += "Трансляция...\n";
  //   const response2 = await fetch('/translate_code', {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',},
  //     body: JSON.stringify({ tokens })
  //   });
  //   if (!response2.ok) throw new Error('Ошибка при трансляции');
  //   const translatedCode = await response2.text();
  //   logTxt.value += "Трансляция завершена\n";
  //   outputTxt.value = translatedCode;

  // } catch (error){
  //   logTxt.value += `Ошибка: ${error.message}\n`
  // }








  try {
    const response = await fetch(`/process_text`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',},
        body: JSON.stringify({ text: cppCode })
    });
    if (!response.ok) throw new Error('Ошибка при запросе');
    const result = await response.json();

    if (result.tokens_error != "None"){
      logTxt.value += `\nОшибка токкенизации: tokkens = ${result.tokens_error}`;
      outputTxt.value = '';
    }
    else{
      logTxt.value += `\n Токенизация успешна:\n${result.tokens}\n`;
      logTxt.value += `\n Построение дерева...\n`;

      if ((result.parser_error != null)|| (result.ast_error != null)|| (result.gener_error != null)){
        if ((result.tree_error != "None")) logTxt.value += `\nОшибка построения дерева: ${result.tree_error}\n`;
        logTxt.value += `\nОшибка парсера:${result.parser_error}\n`;
        logTxt.value += `\nОшибка АСД:${result.ast_error}\n`;
        logTxt.value += `\nОшибка генератора:${result.gener_error}\n`;


        outputTxt.value = '';
      }
      else{
        logTxt.value += `\nДерево успешно построено:\n${result.tree}\n`;

        logTxt.value += `\nАнализ семантики...\n`;
        if(result.semanalize == 1){
          logTxt.value += `\n Семантический анализ прошел успешно!\n`;
          outputTxt.value = result.code;
        }
        else{
          logTxt.value += `\n Семантический анализ завершился с ошибкой!${result.semanalize_error}\n`;
          outputTxt.value = '';
        }
      }
    }
  } catch (error) {
      alert('Не удалось обработать текст');
      logTxt.value = ``;
      outputTxt.value = '';
  }
});
