import speech_recognition as sr
import openai, os
import re, argparse
from pythonosc import udp_client
import json, requests
from pydub import AudioSegment, playback

# Define a function.
def SendExpOSC(i):
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=9000, help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/avatar/parameters/Expressions", i)
def SendStaOSC(i):
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=9000, help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/avatar/parameters/Status", i)

while True:
    # Listen to the voice.
    SendStaOSC(1)
    listener = sr.Recognizer()
    Suc = False
    while not Suc:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                voice = listener.listen(source)
                voice_text = listener.recognize_google(voice, language="ja-JP")
                print(voice_text)
                Suc = True
        except:
            print('Trying again...')
    Suc = False

    # Accessing OpenAI API.
    SendStaOSC(2)
    print("Connecting OpenAI API...")
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Sakura, an expressive 10-year-old Japanese girl. She has pink hair color, cat ears, and is bright and cheerful. You must not speak any English and must speak only Japanese."},
            {"role": "system", "content": "As the emotion switches, indicate the type and intensity of the emotion with a command."},
            {"role": "system", "content": "The types of emotions are Happy, Angry, Sad, and Surprised, expressed in five levels of intensity."},
            {"role": "system", "content": "The command must be prefixed to the sentence and must be in English."},
            {"role": "system", "content": "Examples of commands are [Happy:2], [Angry:5], [Sad:1], [Surprised:3]."},
            {"role": "user", "content": voice_text},
        ],
    )
    AI_text = response.choices[0]["message"]["content"].strip()
    print("Successful ChatGPT Process\n" + AI_text)

    # Analyze sentences and separate them into emotions and sentences.
    p_text = AI_text.split('[')
    if p_text[0] == '':
        del p_text[0]
    ln = 0
    for i in p_text:
        if ']' in i:
            p_text[ln] = '[' + i
        ln += 1
    Exp = []
    Sen = []
    for i in p_text:
        if '[' in i:
            Exp.append(re.findall("\[([^\[\]]+)\]", i)[0])
            Sen.append(re.findall("\[[^\]]*\](.*)", i)[0])
        else:
            Exp.append('[:]')
            Sen.append(i)

    # Change the character's facial expression and have COEIROINK read it.
    for i in range(len(Exp)):    
        speaker_id = 0
        response = requests.post(
            "http://localhost:50031/audio_query",
            params={
                'text': Sen[i],
                'speaker': speaker_id,
                'core_version': '0.0.0'
            })
        query = response.json()
        response = requests.post(
            'http://localhost:50031/synthesis',
            params={
                'speaker': speaker_id,
                'core_version': "0.0.0",
                'enable_interrogative_upspeak': 'true'
            },
            data=json.dumps(query))
        SendStaOSC(3)
        try:
            match re.findall(r"[^:]+(?=:)", Exp[i])[0]:
                case 'Happy':
                    SendExpOSC(1)
                case 'Angry':
                    SendExpOSC(2)
                case 'Sad':
                    SendExpOSC(3)
                case 'Surprised':
                    SendExpOSC(4)
                case _:
                    SendExpOSC(0)
        except (IndexError):
            SendStaOSC(4)
        playback.play(AudioSegment(response.content,
            sample_width=2, frame_rate=44100, channels=1))
    
    SendExpOSC(0)