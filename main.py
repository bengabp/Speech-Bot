from utils import (record_audio_to_file,
                    get_text_from_speech,
                    get_chatbot_reply,
                    speak_text)
import time


speak_text("Hi, my name is Eva. I am a chatbot designed by Ben")

while True:
    print("Listening...")
    audio_filename = record_audio_to_file("my_message.wav")
    
    print("Got audio message... Transcribing...")
    message = get_text_from_speech(audio_filename)

    print("Transcribed successfully... Getting response")
    bot_response = get_chatbot_reply(message)

    print("Replying user...")
    speak_text(bot_response)

    print("Waiting for some time")
    time.sleep(2)

    print("\n")