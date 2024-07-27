import ollama

response = ollama.chat(model='phi3', messages=[
    {
        'role': 'user',
        'content': 'Hey Jarvis, how do i improve the sentence I am a good person (give only 1 suggestion to the question)'
    }
])

print(response['message']['content'])