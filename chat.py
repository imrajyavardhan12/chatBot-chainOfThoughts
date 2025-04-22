import json
import openai
import streamlit as st


openai_api_key = st.secrets["OPENAI_API_KEY"]

system_prompt = """
    You are an helpful AI assistant specialized in solving complex problems by breaking them into smaller problems.

    You should solve the problem by thinking 3-4 times and solving in steps

    the steps are user give input, you think, then analyse, and think again and then finally return the output with explanation

    You should follow the steps in given order "Think", "analyse","Think","Output"

    Rules to Follow : 
    1. Perform one step at a time and wait for next input
    2. Follow strict JSON output as per format
    3. carefully analyse the user query

    Output format : 
    {{step : "string", content : "string"}}
    
    Example : 

    Input : what is 4 * 2
    Output : {{ step : "think", content : "the user is asking me to solve 4 * 2"}}
    Output : {{ step : "analyse", content : "I should identity the mathematical operation between the operands which is * which means multiplication"}}
    Output : {{ step : "think", content : "now i have identified the operation i should perform it so the output will be 8"}}
    
    Output : {{ step: "output", content : "the answer is 8 "}}


"""

messages = [{"role":"system", "content":system_prompt}]

st.title("Bharat GPT!")
st.subheader("Proudly made in INDIA")
st.badge("New")

st.divider()

query = st.chat_input("Ask something from Bharat GPT")

if query : 

    messages.append({"role":"user", "content": query})



    while True:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages = messages,
            response_format={"type": "json_object"},
            max_tokens = 200
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({'role':'assistant', 'content' : json.dumps(parsed_response)})

        if parsed_response.get('step') != 'output':
            st.write("🧠 ", parsed_response.get('content'))
            continue

        st.write("🤖 ", parsed_response.get('content'))
        break


