import speech_recognition as sr
from gtts import gTTS
import os


def voice_to_ai_voice():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please speak now...")
        audio_data = recognizer.listen(source)

        # Try to recognize the speech in the audio
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Transcribed text: {text}")

            # Convert the transcribed text to AI voice
            tts = gTTS(text=text, lang="en")
            ai_voice_file = "ai_voice_output.mp3"
            tts.save(ai_voice_file)
            print(f"AI voice saved to {ai_voice_file}")

            # Optionally play the AI voice
            # os.system(f"start {ai_voice_file}")

        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


voice_to_ai_voice()
