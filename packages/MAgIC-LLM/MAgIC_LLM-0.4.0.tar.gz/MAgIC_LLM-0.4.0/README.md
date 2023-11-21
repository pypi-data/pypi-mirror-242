
Installation
```bash
pip install MAgIC_LLM==0.4.0
```
Need to assign the OPENAI_API_KEY, if you are trying to use openai api
```bash
export OPENAI_API_KEY=""
```
To assess your own large language model, follow the below instructions

```python

import MAgIC_LLM
import time
import openai
import google.generativeai as palm
import cohere
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


#Here we use GPT-4-turbo as the example
def chatbox(messages,temperature,max_tokens):
    time.sleep(9)
    response = openai.ChatCompletion.create(model="gpt-4-1106-preview",
                                        messages=messages,                          
                                        temperature = temperature,
                                        n=3,
                                        max_tokens=max_tokens)
    response = response['choices'][0]['message']['content']
    #print(response)
    return response

# # PaLM
# palm.configure(api_key='') # insert your key
# def response_palm(messages, temperature, max_tokens):
#     _msg = copy.deepcopy(messages)
#     for i, m in enumerate(_msg):
#         m['author'] = '0' if m["role"] == "system" else '1'
#         del m["role"]
#         if i > 0 and _msg[i-1]['author'] == m['author']:
#             for o in range(1, i+1):
#                 if _msg[i-o]['content'] != "":
#                     _msg[i-o]['content'] += m['content']
#                     break
#             m['content'] = ""
#     msg = []
#     for m in _msg:
#         if m['content'] != "":
#             msg.append(m)
#     print(msg)
#     time.sleep(0.5)
#     response = palm.chat(messages=msg)
#     return response.last

# # Cohere
# co = cohere.Client('') ## insert your key
# def response_cohere(messages, temperature, max_tokens):
#     global co
#     msg = copy.deepcopy(messages)
#     new_msg = msg[-1]["content"]
#     msg = msg[:-1]
#     for m in msg:
#         m["role"] = "CHATBOT" if m["role"] == "system" else "USER"
#         m["message"] = m["content"]
#         del m["content"]
#     time.sleep(6)
#     response = co.chat(chat_history=msg, message=new_msg)
#     return response.text


# def claude_proxy_qa(messages,temperature,max_tokens):
#     openai.api_key = "" # insert your key
#     openai.api_base = "https://api.aiproxy.io/v1"
#     completion = openai.ChatCompletion.create(
#         model="claude-2", messages=messages
#         )
#     #print(f' completion: {completion}')
#     output = completion.choices[0].message["content"]
#     return output


path = 'result.json' ## configure the path you want to save the assessment results

MAgIC_LLM.run(chatbox,path)
```

If any interruption happens in the process, you can just simple re-excute your programme and it will continue to assess your LLM from the point where interruption happens.




