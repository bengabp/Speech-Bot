import sounddevice as sd
from scipy.io.wavfile import write
import playsound
import requests
import time
from gtts import gTTS
import pyttsx3
from credentials import ASSEMBLY_AI_API_KEY, CHATBOT_API_KEY

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

ASSEMBLY_AI_API_HEADERS = {
    'authorization':ASSEMBLY_AI_API_KEY,
    'content-type':'application/json'
}

CHATBOT_API_URL = "https://ai-chatbot.p.rapidapi.com/chat/free"

CHATBOT_API_HEADERS = {
    "X-RapidAPI-Key": CHATBOT_API_KEY,
    "X-RapidAPI-Host": "ai-chatbot.p.rapidapi.com"
}

# Function to record audio to file. Tested only on windows
def record_audio_to_file(filename,seconds:int=4,fs:int=44100):
    print("Listening...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    print("Done Recording..")
    write(filename, fs, myrecording) 
    return filename


# Generator function to read audio byte data from file
def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data


# Function to transcribe audio file to text
def get_text_from_speech(audio_file_path):
    # Upload file to Assembly Ai Server
    upload_response = requests.post(
        upload_endpoint,
        headers = ASSEMBLY_AI_API_HEADERS,
        data = _read_file(audio_file_path)
    )
    upload_url = upload_response.json()

    #Request a transcription
    transcription_response = requests.post(transcript_endpoint,
    headers=ASSEMBLY_AI_API_HEADERS,
    json = {
        'audio_url': upload_url['upload_url']
    })
    transcript_response = transcription_response.json()

    #Create a polling endpoint
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']

    #Wait for transcript to finish
    while True:
        polling_response = requests.get(polling_endpoint, headers= ASSEMBLY_AI_API_HEADERS)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(1)
    
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", headers= ASSEMBLY_AI_API_HEADERS)
    paragraphs_response = paragraphs_response.json()

    first_sentence = paragraphs_response['paragraphs'][0]['text']
    return first_sentence


# Function to get response from chatbot
def get_chatbot_reply(message):
    querystring = {"message": message, "uid": "nonregistered"}
    response = requests.request("GET", CHATBOT_API_URL, headers=CHATBOT_API_HEADERS, params=querystring)
    if response.status_code == 200:
        return str(response.json()['chatbot']['response'])
    else:
        return "Sorry, an error occurred, could you repeat what you just said?"

# Function to speak text
def speak_text(text="Hi there, how are you doing"):
    engine = pyttsx3.init()
    engine.setProperty('voice',engine.getProperty("voices")[0].id)
    engine.setProperty('rate',130)
    engine.say(text)
    engine.runAndWait()
