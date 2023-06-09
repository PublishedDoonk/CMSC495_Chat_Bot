import openai

def generateChatResponse(prompt,key,messages):
    '''This fucntion will pull the user input and send it through the chatbot
    allowing the chatbot to generate a response. It will also receive the openai
    key allowing for the chatbot to make an API call to chatGPT.
    '''
    
    openai.api_key = key
    answer = "working"
    
    if messages == []:
        messages.append({"role": "system", "content": "You are a helpful assistant."})

    messages.append({
        'role': 'user',
        'content': prompt,
    })

    #using try/except blocks to catch potential errors, such as
    #incorrect api keys, disabled web access.
    
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
        messages.append(response['choices'][0]['message'])
    except openai.error.AuthenticationError :
        answer = "You need to enter a valid key!"
    except KeyError:
        answer = "API call failed"
    except openai.error.APIConnectionError:
        answer = "Unable to reach server"

    #returning the chatbot answer to the other chatroom program to be posted
    return (answer, messages)
