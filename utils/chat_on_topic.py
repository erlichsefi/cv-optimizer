
from openai import OpenAI
import os
import json

# Load your API key from an environment variable or secret management service
api_key = os.environ['OPENAI_API_KEY']

def chatbot(system_prompt,topic):
  print("Start chatting with the bot (type 'quit' to stop)!")
  print(f"Bot: Let's talk about your time at {topic}")
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": system_prompt},
  ]

  # Keep repeating the following
  while True:

    # Request gpt-3.5-turbo for chat completion
    client = OpenAI(api_key=api_key)
    
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
    print(f"Bot: {chat_message['message']}")

    # Prompt user for input
    message = input("User: ")

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      break

    # Add each new message to the list
    messages.append({"role": "assistant", "content": json.dumps(chat_message,indent=4)})
    messages.append({"role": "user", "content": message})
    

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

    Response format:
    ```json
    {{
    "question": "the question to ask",
    "message": "the message to send the user, that contains the question. be nice!",
    "expectation": "what you expected to learn from the user answer"
    }}
    ```
    only one question at a time.
    """
  chatbot(system_prompt,topic="TEST TOPIC")