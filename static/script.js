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
    // Preprocessing code
    const file = audioFileInput.files[0];
    const formData = new FormData();
    formData.append("audio", file);
    fetch("/predict", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        let avg = 0;
        for(let i = 0; i < data.result.length; i++){
          avg = avg + data.result[i];
        }
        avg = avg/data.result.length;
        if(avg >= 0.5)  
          predictionResult.textContent = `Prediction: Real`;
        else 
          predictionResult.textContent = `Prediction: Fake`;
    })
    .catch(error => {
        console.error("Error during prediction:", error);
    });
});
});
