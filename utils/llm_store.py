import os
import json
from openai import OpenAI
import retry
#from filestore import FileStoreState


#state = FileStoreState()

def get_compliation(system_message,user_input,model="gpt-3.5-turbo",is_json_expected=False,api_key=None,num_of_gen=1,temperature=0,top_p=0):
    messages= [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ]
    
    generations = get_chat_compliation(messages,model=model,is_json_expected=is_json_expected,api_key=api_key,num_of_gen=num_of_gen,temperature=temperature,top_p=top_p)

    
    #state.presist_compliation(messages,generations,model)
    return generations


@retry.retry(exceptions=(json.decoder.JSONDecodeError),logger=None,tries=3)
def get_chat_compliation(messages,model="gpt-3.5-turbo", is_json_expected=False, api_key=None,num_of_gen=1,temperature=0,top_p=0):
    if not api_key:
        api_key = os.environ['OPENAI_API_KEY']

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        temperature=temperature,
        top_p=top_p,
        n=num_of_gen
    )

    if is_json_expected:
       if num_of_gen == 1:
           return json.loads(stream.choices[0].message.content.replace("```json","").replace("```",""))
       else:
          return [json.loads(choice.message.content.replace("```json","").replace("```","")) for choice in stream.choices]
       
    if num_of_gen == 1:
       return stream.choices[0].message.content
    else:
       return [choice.message.content for choice in stream.choices]

def have_a_look(image_path, prompt, api_key, model="gpt-4-vision-preview"):
    import requests

    def file_to_bytes(image_path):
        import base64

        """convert file to byte array"""

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    base64_image = file_to_bytes(image_path)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    ).json()

    return response["choices"][0]["message"]["content"]


def experience_chatbot(system_prompt,user_interface,topic,model="gpt-3.5-turbo"):
  cache_key = user_interface.get_cache_key()

  #user_interface.start_bot_session(topic)

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
        "is_all_issue_addressed": "<true if all the issues addressed and this is a goodbye message>",
        "expectation": "<what you expected to learn from the user answer>"
        
    }}
    ```"""
  messages = [
    {"role": "system", "content": system_prompt},
  ] + user_interface.get_chain_message_on_extracted_cv()[1:]

  
  # Keep repeating the following
  #   while True:

    # Request gpt-3.5-turbo for chat completion
  client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

  max_retries = 3
  retry_count = 0

  while retry_count < max_retries:
    try:
            
        stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
        )
        chat_message = json.loads(stream.choices[0].message.content.replace("```json","").replace("```",""))
        user_interface.presist_compliation(messages,chat_message,model,cache_key=cache_key)
        break  # Break out of the loop if successful
    except json.JSONDecodeError as e:
        retry_count += 1
        if retry_count == max_retries:
            raise e
        else:
            user_interface.send_user_message("Bot: ....")
                

  # Print the response and add it to the messages list
  user_interface.send_user_message(f"{chat_message['message']}")
  if str(chat_message['is_all_issue_addressed']).lower() == "true":
      user_interface.set_chain_message_on_extracted_cv(messages,reason="GPT")


  # Prompt user for input
  message = user_interface.get_user_input()

  # Exit program if user inputs "quit"
  if message.lower() == "quit":
      user_interface.set_chain_message_on_extracted_cv(messages,reason="quit")

  # Add each new message to the list
  messages.append({"role": "assistant", "content": json.dumps(chat_message,indent=4)})
  messages.append({"role": "user", "content": message})

 #user_interface.end_bot_session()
  return messages
    

if __name__ == "__main__":
  from .interface import TerminalInterface

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