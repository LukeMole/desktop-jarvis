import vosk
import pyaudio
import json
import os
import certifi
import ssl
import ollama
from PIL import ImageGrab



# Set the default SSL context to use the certifi bundle
# this allows files to be downloaded without errors
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_unverified_context


def take_screenshot():
    screenshot = ImageGrab.grab()

    screenshot.save('image.jpg')


def get_output(recognised_text, image_name):
    cur_dir = os.path.dirname(__file__)
    prompt = recognised_text.split('hey jarvis')[1]
    prompt = prompt.strip()

    print(prompt)
    print('')

    with open(f'{cur_dir}/{image_name}', 'rb') as file:
        response = ollama.chat(model='llava', messages=[
            {
                'role': 'user',
                'content': f'Hey Jarvis, {prompt} (give only 1 suggestion to the question)',
                'images': [file.read()]
            }
        ])

        print(response['message']['content'])


def listen():
    global ssl_context

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
        recognised_text = ''
        data = stream.read(8192, exception_on_overflow=False)

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            recognised_text = res['text']
            print(recognised_text)

        if 'terminate' in recognised_text.lower():
            print('Terminating...')
            break

        if 'hey jarvis' in recognised_text.lower():
            stream.stop_stream()
            take_screenshot()
            get_output(recognised_text, 'image.jpg')
            stream.start_stream()


if __name__ == '__main__':
    listen()