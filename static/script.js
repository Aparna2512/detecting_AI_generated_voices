document.addEventListener("DOMContentLoaded", () => {
  const audioFileInput = document.getElementById("audio-file");
  const audioPreview = document.getElementById("audio-preview");
  const predictButton = document.getElementById("predict-btn");
  const predictionResult = document.getElementById("prediction-result");

  audioFileInput.addEventListener("change", () => {
    const file = audioFileInput.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      audioPreview.src = e.target.result;
    };

    reader.readAsDataURL(file);
  });

  predictButton.addEventListener("click", () => {
    // Call Flask endpoint to predict
    // You may want to use fetch() or Axios to send the audio file to Flask
    // and receive the prediction result
    predictionResult.textContent = "Prediction: [Human/AI]";
  });
});
