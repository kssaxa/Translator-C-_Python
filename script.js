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





const translateBtn = document.getElementById("translate_btn");
translateBtn.addEventListener("click", async () => {
//   const textarea = inputTxt
  const cppCode = inputTxt.value;

  if (!cppCode.trim()) {
    alert("Введите код на C++!");
    return;
  }

  const apiUrl = "https://6741de41e4647499008f0f47.mockapi.io/api/v1/code";

  const data = {
    cpp_code: cppCode,
  };

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      alert(`Код успешно отправлен! ID записи: ${result.id}`);
      inputTxt.value = "";
    } else {
      alert(`Ошибка при отправке: ${response.status}`);
    }
  } catch (error) {
    alert(`Ошибка: ${error.message}`);
  }
});
