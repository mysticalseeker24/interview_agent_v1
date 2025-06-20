"""

This class will represent the conversational
agent (the interviewer)

"""
# Importing libraries 
import os
import threading
from dotenv import load_dotenv
import pygame
from openai import OpenAI
import anthropic
import json

# Assuming audioToText.py is correctly set up in the sys.path.append('audio-extraction') directory
from audioToText import AudioRecorder, transcribe_audio

class Interviewer:
    def __init__(self, persona):
        load_dotenv()
        self.client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.client_claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.history = []
        self.recorder = AudioRecorder()
        pygame.mixer.init()
        self.playback_finished = threading.Event()
        self.done = False

        # Appending the initial persona
        self.persona = persona

        # Clean up any existing temporary files
        self._cleanup_temp_files()

    def text_to_speech(self, text: str):
        import tempfile
        import time

        # Create a unique temporary file to avoid conflicts
        temp_audio_file = f"interviewer-speech-{int(time.time())}.mp3"

        try:
            speech = self.client_openai.audio.speech.create(model='tts-1', voice='alloy', input=text)
            with open(temp_audio_file, "wb") as f:
                f.write(speech.content)
        except Exception as e:
            print(f"Error generating speech: {e}")
            return

        def play_audio():
            try:
                pygame.mixer.music.load(temp_audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f"Error playing audio: {e}")
            finally:
                # Stop music and unload to release file handle
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                # Clean up the temporary audio file
                self._safe_remove_file(temp_audio_file)
                self.playback_finished.set()

        threading.Thread(target=play_audio).start()
        self.playback_finished.wait()  # Wait here until audio playback is finished

    def text_to_text(self, input_text: str):
        try:
            self.history.append({'role': 'user', 'content': input_text})
            response = self.client_claude.messages.create(
                model='claude-sonnet-4-20250514', max_tokens=1000,
                temperature=0, system=self.persona, messages=self.history
            )
            response_text = response.content[0].text
            self.history.append({'role': 'assistant', 'content': response_text})
            return response_text
        except Exception as e:
            print(f"Error in text-to-text conversion: {e}")
            return "I'm sorry, I didn't catch that."

    def speech_to_text(self):
        self.playback_finished.clear()  # Ensure this is reset before starting playback
        frames = self.recorder.record_until_silence()
        wav_filename = self.recorder.save_recording(frames)
        text = ""
        try:
            text = transcribe_audio(wav_filename)
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            text = ""
        finally:
            # Safe file deletion with retry mechanism
            self._safe_remove_file(wav_filename)
        return text

    def _safe_remove_file(self, filename, max_attempts=5):
        """Safely remove a file with retry mechanism for Windows file locking issues"""
        import time
        for attempt in range(max_attempts):
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(0.1)  # Wait 100ms before retry
                    continue
                else:
                    print(f"Warning: Could not delete temporary file {filename}. It will be cleaned up later.")
            except Exception as e:
                print(f"Warning: Error deleting file {filename}: {e}")
                break

    def _cleanup_temp_files(self):
        """Clean up any existing temporary files"""
        import glob

        # Clean up specific temp files
        temp_files = ["temp.wav", "interviewer-speech.mp3"]
        for temp_file in temp_files:
            self._safe_remove_file(temp_file)

        # Clean up any timestamped audio files
        for audio_file in glob.glob("interviewer-speech-*.mp3"):
            self._safe_remove_file(audio_file)

    def is_done(self, message):
        response = self.client_claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Given this response, {message}, does it seem like the person wants to end the conversation immediately? only give a 'yes' or a 'no' in that exact format"
                        }
                    ]
                }
            ]
        )

        return response.content[0].text.lower() == 'yes'

    def main(self):
        done = False
        while not done:
            self.playback_finished.set()  # Assume playback is finished at the start
            user_speech = self.speech_to_text()
            #user_input = input("Enter something: ")

            if user_speech.strip(' ').lower() == 'i am done.' or self.is_done(user_speech):
                done = True

            response_text = self.text_to_text(user_speech)
            done = self.is_done(response_text)
            print('Recruiter said: ' + response_text)
            self.text_to_speech(response_text)
        
        # Writing to a file
        with open('history1.json','w') as file:
            json.dump(self.history,file,indent=4)

        # Clean up temporary files
        self._cleanup_temp_files()
        print("Interview completed. Temporary files cleaned up.")


if __name__ == '__main__':
    # Adding the persona
    with open('ethan-the-strategic-planner-product-manager-watershed-response-guidelines.txt','r') as file:
        persona = file.read()
    mode = input("Please mention how difficult you want this interview to be (put 'hard', 'medium', or 'easy': ")
    persona += f"Begin the interview. You are the interviewer and I am the interviewee. Please be very concise as the interviewer in your answers but do not skip the formalities. Use this opportunity to pick up on interviewee social cues. keep in mind time is limited and make this interview {mode}"
    interviewer = Interviewer(persona)
    print('Interview is beginning. Say hello!')
    interviewer.main()
