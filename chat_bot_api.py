import openai

openai.api_key = #enter you own api key


def generateChatResponse(prompt):
    messages = []
    messages.append({"role": "system", "content": "You area a helpful assistant."})

    question = {}
    question['role'] = 'user'
    question['content'] = prompt
    messages.append(question)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)

    try:
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    except:
        answer = "Oh no! Something went wrong!"

    return answer
