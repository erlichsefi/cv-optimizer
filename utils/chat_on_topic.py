
from openai import OpenAI
import os
import json


def chatbot(system_prompt,topic):
  print("Start chatting with the bot (type 'quit' to stop)!")
  print(f"Bot: Let's talk about your time at {topic}")
  # Create a list to store all the messages for context

  system_prompt = f"""{system_prompt} \n.
    Response format:
    ```json
    {{
        "question": "the question to ask",
        "message": "the message to send the user, that contains the question. be nice!",
        "expectation": "what you expected to learn from the user answer"
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
                print("Bot: ....")
                

    # Print the response and add it to the messages list
    if chat_message['message'].lower() == "quit":
      break
    print(f"Bot: {chat_message['message']}")

    # Prompt user for input
    message = input("User: ")

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
  chatbot(system_prompt,topic="TEST TOPIC")