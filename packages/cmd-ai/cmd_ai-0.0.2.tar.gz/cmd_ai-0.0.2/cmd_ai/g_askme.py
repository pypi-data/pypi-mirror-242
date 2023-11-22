#!/usr/bin/env python3
'''
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
'''
from cmd_ai.version import __version__
from fire import Fire
from cmd_ai import config
from console import fg
# print("v... unit 'unitname' loaded, version:",__version__)

import datetime as dt
import time
import tiktoken


def num_tokens_from_messages(model="gpt-3.5-turbo-0613"):
#def num_tokens_from_messages(model="gpt-4"):
    """Return the number of tokens used by a list of messages."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(config.messages, model="gpt-3.5-turbo-0613")

    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(config.messages, model="gpt-4")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in config.messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# ===============================================================================================

def g_ask_chat( prompt ,  temp  , model, limit_tokens = 300, total_model_tokens = 4096*2-50 ):
    """
    CORE ChatGPT function
    """
    # global task_assis, limit_tokens

    # ---- if no system present, add it
    if len(config.messages)==0:
        config.messages.append( {"role":"system", "content":config.system_role }  )
    # add the message~
    config.messages.append( {"role":"user","content":prompt} )

    max_tokens = total_model_tokens - num_tokens_from_messages()
    if limit_tokens<max_tokens:
        max_tokens = limit_tokens
    now = dt.datetime.now().replace(microsecond=0)

    print(f"i...  max_tokens= {max_tokens}, model = {model};  task: {now-config.started_task}; total:{now-config.started_total}" )

    # THIS CAN OBTAIN ERROR: enai.error.RateLimitError: Rate limit reached for 10KTPM-200RPM in organization org-YaucYGaAecppFiTrhbnquVvB on tokens per min. Limit: 10000 / min. Please try again in 6ms.
    # token size block it

    waittime = [1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3 ]
    DONE = len(waittime)-1
    responded = False
    while DONE>0: # I forgot to decrease
        DONE-=1
        time.sleep( 1*waittime[0] )
        try:
            # print(messages)
            print(" --> ", end ="" )
            response = config.client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model=model,
                messages=config.messages ,
                temperature=temp,
                max_tokens=max_tokens
            )
            print(" >>OK")
            DONE = 0
            responded = True
            # print(response)
        except Exception as e:
            print("An error occurred:", str(e))
            print(f"i... re-trying {DONE+1}x more time ... after {waittime[0]} seconds ...")
            time.sleep( 1*waittime[0] )
            waittime.pop(0)
            DONE-=1

    #print("i... OK SENT")
    if not responded:
        print("i... NOT RESPONDED  ====================================")
        return None

    #print(type(response))
    #print(str(response))

    resdi = response.choices[0].message.content

    #resdi = json.loads( str(response)  )
    return resdi
    #print(resdi)


    # ========================================================================





def g_askme(prompt ,  temp = 0.0 , model='gpt-4-1106-preview', limit_tokens = 300, total_model_tokens = 4096*2-50 ):

    resdi = g_ask_chat( prompt, temp , model, num_tokens_from_messages()+len(prompt)+600 )

    if resdi is None:
        return None
    return resdi




if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
