# desktop-jarvis
 a desktop ai assistant which can take screenshots of your screen and answer questions for you

 ollama and the llava need to already be installed on your computer for the program to work

 the program takes a photo of your screen every time you prompt it by greeting jarvis e.g. "Hey Jarvis". the program then answers your question and can examine the image to answer a question you have relating to the question, but it will ignore the image if it is irrelevant. Currently the image examining is not very good with llava 7b, but this is simply a limitation of the AI model and will likely be fixed with a better model. The program uses text-to-speech to respond to the user, so that the user does not need to read the command line. All of the processing is done locally and the program does not rely on any cloud services.

Vosk is used for speech-to-text.
pyttsx3 is used for text-to-speech.
ollama is used for response generation and it is using the llava model.

necessary modules are as follows:
    vosk
    pyaudio
    ollama
    pillow
    pyttsx3