from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import PHARMA_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the LLM
#openai
from langchain.chat_models import ChatOpenAI
llm=ChatOpenAI(
    temperature=0.3, 
    model_name="gpt-3.5-turbo"
)

#google genai
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.3
)

# Create the prompt and chain
prompt=PromptTemplate(
    input_variables=["symptoms"],
    template=PHARMA_PROMPT
)
chain=LLMChain(
    llm=llm,
    prompt=prompt
)

# Function to get pharmaceutical advice
def get_pharma_advice(symptoms: str) -> str:
    response = chain.run(symptoms=symptoms)
    return response

# Main interaction loop
if __name__ == "__main__":
    print("🩺 PharmaBot Console \n\nTape 'exit' pour quitter\n")
    while True:
        user_input = input("👤 Décris tes symptômes : ")
        if user_input.lower() == 'exit':
            print("👋 Au revoir!")
            break
        advice = get_pharma_advice(user_input)
        print(f"💊 PharmaBot : {advice}\n")
        print("-*-" * 50)
    