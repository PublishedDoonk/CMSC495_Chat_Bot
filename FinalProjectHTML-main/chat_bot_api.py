import openai

def generateChatResponse(prompt,key):
    
    openai.api_key = key
    answer = "working"

    messages = []
    messages.append({"role": "system", "content": "You area a helpful assistant."})

    question = {}
    question['role'] = 'user'
    question['content'] = prompt
    messages.append(question)
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    except openai.error.AuthenticationError :
        answer = "You need to enter a valid key!"
    except KeyError:
        answer = "API call failed"
    except openai.error.APIConnectionError:
        answer = "Unable to reach server"

    return answer
