# CV Customization Application (Proof of Concept)

This application is a proof of concept intended to demonstrate how you can customize your CV to a specific position.

## Getting Started
- Upload your PDF CV into the sidebar.
- Copy the position details into the sidebar (include only information you would like to optimize your CV based on).
- Select a method (from the sidebar) and move to its page.

## Currently, there are two methods:
1. **Simple Method**: Provide the CV and position when calling the LLM with a single prompt.
    - You can adjust the prompt in the method page.
2. **LLM Agent Method**: Ask an LLM agent to represent the user.
    - You can adjust your intent in the method page.

### Important Note
This application is a proof of concept and does not guarantee accurate results. Use it for experimental purposes only.
Feedback is welcome at erlichsefi@gmail.com.


# Dev
## Setup:
- Setup google sheet service account has stated [here](https://github.com/streamlit/gsheets-connection/blob/main/examples/pages/Service_Account_Example.py)
- Get Open.AI keys [here](https://platform.openai.com/account/api-keys) 