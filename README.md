# Speech-Bot
Speech to text chatbot that uses the assembly ai api and chatbot api to communicate in real time with a user.
To run this project successfully , you will need to create an account on assembly ai and get you api key. Also you will need to search for the chatbot api on rapid api and get an apikey.

## Development Stages

+ ### Getting audio data form the microphone
    This is the first stage where we are getting audio data from the microphone.
    I have used the [sounddevice](https://pypi.org/project/sounddevice/) python library to store the audio data from the microphone into a media file
    The function `record_audio_to_file("my_message.wav")` initiates a sound recorder and writes speech from microphone to the file.
    
    
+ ### Transcribing Audio 
    Here I have used the [Assembly Ai](https://www.assemblyai.com/) speech to text api to upload and transcribe 
    the input data from the microphone which has been saved in a media file.
    Remember to get your apikey on assembly ai website if you want to run this project.
    The function `get_text_from_speech(audio_filename)` returns a text format of the audio data.
    
 + ### Generating ChatBot Ai Resonse
    Here the chatbot api from rapidapi was used to get chatbot responses.
    The function `get_chatbot_reply(message)` returns a chatbot response.
    
 + ### Replying the user
    In order to send audio data back to the user, the [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) text to speech python library was used.
    The funciton `speak_text(bot_response)` sends an audio reply.
    
    
  #### If you have any questions, feel free to message [me](https://t.me/bengabp) on telegram.
