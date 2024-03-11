import streamlit as st
from io import BytesIO
import numpy as np
import soundfile as sf


# Audio recording function in the frontend
def record():
    st.write("## Record your voice")
    record_btn = st.button("Record")
    stop_btn = (
        st.empty()
    )  # Placeholder for stop button, to be shown only during recording
    audio_player = (
        st.empty()
    )  # Placeholder for the audio player, to be shown after recording

    if record_btn:
        stop_btn.button("Stop")  # Show the stop button

        # JavaScript to handle voice recording
        js_code = """
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    const mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();

                    const audioChunks = [];
                    mediaRecorder.addEventListener("dataavailable", event => {
                        audioChunks.push(event.data);
                    });

                    const stopButton = document.getElementById("stopButton");
                    stopButton.onclick = () => {
                        mediaRecorder.stop();
                        stream.getTracks().forEach(track => track.stop());  // Stop the media stream
                    };

                    mediaRecorder.addEventListener("stop", () => {
                        const audioBlob = new Blob(audioChunks);
                        const audioUrl = URL.createObjectURL(audioBlob);
                        const audio = new Audio(audioUrl);
                        const play = () => {
                            audio.play();
                        };

                        // Post the audio URL to Streamlit for playback
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: audioUrl
                        }, '*');

                        const fd = new FormData();
                        fd.append('audio', audioBlob);
                        fetch('/upload_audio', { method: 'POST', body: fd });
                    });
                });
        """
        st.components.v1.html(
            f"<script>{js_code}</script><button id='stopButton' style='display:none;'></button>",
            height=0,
        )

        # Receive the audio URL from JavaScript and display the audio player
        audio_url = st.session_state.get("last_audio_url", "")
        if audio_url:
            audio_player.audio(audio_url, format="audio/wav")


# Endpoint for processing uploaded audio
@st.experimental_singleton
def process_audio(uploaded_file):
    if uploaded_file is not None:
        # Convert the uploaded audio to an array
        file_buffer = BytesIO(uploaded_file.getvalue())
        data, samplerate = sf.read(file_buffer)
        audio_array = np.array(data)

        # Here, you would add your model prediction code
        # For this example, we'll just return a dummy response
        prediction = "Real"  # This should be replaced with actual model prediction

        return prediction


# Main app interface
def main():
    st.title("Voice Authenticity Checker")
    record()

    uploaded_file = st.file_uploader("Or upload an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        prediction = process_audio(uploaded_file)
        st.write(f"Prediction: {prediction}")


if __name__ == "__main__":
    main()
