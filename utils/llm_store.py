import os
import json
from openai import OpenAI
import retry
from filestore import cache_chat,get_cache_key
from interface import TerminalInterface,UserInterface

@retry.retry(exceptions=(json.decoder.JSONDecodeError))
def get_compliation(system_message, user_input, is_json_expected=False, api_key=None,num_of_gen=1,temperature=0):
    if not api_key:
        api_key = os.environ['OPENAI_API_KEY']

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        stream=False,
        temperature=temperature,
        n=num_of_gen
    )

    if is_json_expected:
       
       if num_of_gen == 1:
           return json.loads(stream.choices[0].message.content.replace("```json","").replace("```",""))
       else:
          return[json.loads(choice.message.content.replace("```json","").replace("```","")) for choice in stream.choices ]
    return stream



def experience_chatbot(system_prompt,user_interface:UserInterface,topic):
  cache_key = get_cache_key()

  user_interface.send_user_message("Start chatting with the bot (type 'quit' to stop)!")
  user_interface.send_user_message(f"Bot: focusing on >>{topic}<<")
  # Create a list to store all the messages for context

  system_prompt = f"""{system_prompt} \n.
    Response format:
    ```json
    {{
        "issues_addressed":[
          // list of all inforamtion already gained.
        ],
        "information_gain": "<the information you would like to retrive>",
        "is_followup": "<is this message a followup to complted previous messages",
        "message": "<the message to send the user to obtain the information. be nice!>",
        "is_all_issue_adressed": "<true if all the issues addressed and this is a goodbye message>",
        "expectation": "<what you expected to learn from the user answer>"
        
    }}
    ```"""
  messages = [
    {"role": "system", "content": system_prompt},
  ]

  

  # Keep repeating the following
  while True:

    # Request gpt-3.5-turbo for chat completion
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            cache_chat(messages,cache_key)
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            chat_message = json.loads(stream.choices[0].message.content.replace("```json","").replace("```",""))
            break  # Break out of the loop if successful
        except json.JSONDecodeError as e:
            retry_count += 1
            if retry_count == max_retries:
                raise e
            else:
                user_interface.send_user_message("Bot: ....")
                

    # Print the response and add it to the messages list
    user_interface.send_user_message(f"{chat_message['message']}")
    if str(chat_message['is_all_issue_adressed']).lower() == "true":
      break
    

    # Prompt user for input
    message = user_interface.get_user_input()

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      break

    # Add each new message to the list
    messages.append({"role": "assistant", "content": json.dumps(chat_message,indent=4)})
    messages.append({"role": "user", "content": message})
  return messages
    

if __name__ == "__main__":
  experience_test = {
         "title": "AI Researcher", 
        "company": "Ariel University", 
        "location": "Ariel",
        "start_date": "Nov 2016", 
        "end_date": "Oct 2018", 
        "responsibilities": [
            "Machine learning for football match violence prediction", 
            "Classi\ufb01cation and enrichment of encrypted tra\ufb03c using Machine Learning algorithms"
        ], 
    "keywords": []
    },
  system_prompt = f"""
    You are interviewing me about this period in my life:
    {json.dumps(experience_test,indent=4)}
    You Goal is to asses what skills I've gained during this time.
    When you think that you've understood the skill set I've gained you can respond with 'quit'.
    only one question at a time.
    """
  terminal_interface = TerminalInterface()
  experience_chatbot(system_prompt,terminal_interface,topic="TEST TOPIC")