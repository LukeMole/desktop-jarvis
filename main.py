import vosk
import pyaudio
import json
import os

#necessary to not get ssl errors when downloading vosk model
import certifi
import ssl

# Import the ollama module for chat
import ollama

# Use image grab and time to take a screenshot and name it with the date/time
from PIL import ImageGrab
import time


# Set the default SSL context to use the certifi bundle
# this allows files to be downloaded without errors
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_unverified_context

image_name = ''

# Get the current directory name and make the screenshots folder if it doesn't exist
cur_dir = os.path.dirname(__file__)
if os.path.exists(f'{cur_dir}/screenshots') == False:
    os.mkdir(f'{cur_dir}/screenshots')


def take_screenshot():
    global image_name
    current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    image_name = current_time + '.png'
    screenshot = ImageGrab.grab()

    screenshot.save(f'{cur_dir}/screenshots/{image_name}')


def get_output(recognised_text, image_name):
    prompt = recognised_text.split('jarvis')[1]
    prompt = prompt.strip()

    print(prompt)
    print('')

    #opens the image and sends it to the ollama chatbot, prompt is also engineered to streamline responses
    with open(f'{cur_dir}/screenshots/{image_name}', 'rb') as file:
        response = ollama.chat(model='llava', messages=[
            {
                'role': 'user',
                'content': f'Hey Jarvis, {prompt} (give only 1 suggestion to the question) (if the image does not relate to the question, please ignore it)',
                'images': [file.read()]
            }
        ])

        print(response['message']['content'])


def listen():
    global ssl_context
    global image_name

    #model_path = f'{cur_dir}/vosk-model-en-us-0.22'
    
    #file gets saved to /Users/user/cache/vosk/
    model = vosk.Model(lang='en-us', model_name='vosk-model-en-us-0.22')
    rec = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()

    # find all devices and list them
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        #if the device is an input device print it
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192,
                    input_device_index=1 #sets microphone to desired device
                    )
    
    while True:
        # infinite loop to listen to users microphone
        # if user says "hey jarvis" then it will take a screenshot and send the picture and what the user says
        # to the ollama chatbot
        recognised_text = ''
        data = stream.read(8192, exception_on_overflow=False)

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            recognised_text = res['text']
            #print(recognised_text)

        if 'terminate' in recognised_text.lower():
            print('Terminating...')
            break
        
        # a is included as sometimes hey is caught as a
        greetings = ['hey', 'hello', 'hi', 'a']
        if [greeting for greeting in greetings if f'{greeting} jarvis' in recognised_text.lower()]:
            stream.stop_stream()
            take_screenshot()
            get_output(recognised_text, image_name)
            try: 
                stream.start_stream()
            except:
                print('Error starting stream')
                listen()

if __name__ == '__main__':
    listen()