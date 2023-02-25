#!/bin/python

import random
import speech_recognition as sr
import pronouncing as pro
from playsound import playsound
import os
import wave

# workaround because playsound has trouble with path.
# get the path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# change the working directory to the script directory
os.chdir(script_dir)


# List of words to choose from
words = ['Hello', 'You', 'test', 'orange', 'grape']

# Choose a random word from the list
chosen_word = random.choice(words)

# Initialize the recognizer
r = sr.Recognizer()

# initialize cmu
pro.init_cmu()

# workaround for getting pronunciations, method is missing
def get_phonetic(word : str) -> str:
    word_lower = word.lower()
    res =  [ i for i in pro.pronunciations if i[0]==word_lower]
    if len(res) == 0:
        return ""
    else:
        return res[0][1]

# Use the microphone as the audio source
#playsound("beep-01a.wav")
with sr.Microphone() as source:
    # Prompt the user to say the chosen word
    print(f"Say {chosen_word} ")
    audio = r.listen(source)
    
# write audio to a WAV file
with open("audio.wav", "wb") as f:
    f.write(audio.get_wav_data())

print("let's check for what I heard: ")
playsound("audio.wav")

# Recognize speech using PocketSphinx
try:
    # Use PocketSphinx to recognize speech
    spoken_word = r.recognize_sphinx(audio)
    # Get the phonetic representation of the correct word
    correct_pronunciation = get_phonetic(chosen_word)
    # Get the phonetic representation of the spoken word
    spoken_pronunciation = get_phonetic(spoken_word)
    # Compare the two phonetic representations to determine correctness
    if correct_pronunciation == spoken_pronunciation:
        print("Correct!")
    else:
        print("Incorrect.")
        print(f"The correct pronunciation is: {correct_pronunciation}, you said :{spoken_pronunciation} for \'{spoken_word}\'")
except sr.UnknownValueError:
    print("Sorry, I didn't catch that. Please try again.")
except sr.RequestError:
    print("Sorry, my speech recognition service is down.")
