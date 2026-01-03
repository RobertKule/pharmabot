from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import PHARMA_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Configure the LLM (Gemini – gratuit)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


# Prompt
prompt = PromptTemplate(
    input_variables=["symptoms"],
    template=PHARMA_PROMPT
)

# ✅ Nouvelle chain (LangChain v1+)
chain = prompt | llm


def get_pharma_advice(symptoms: str) -> str:
    response = chain.invoke({"symptoms": symptoms})
    return response.content


if __name__ == "__main__":
    print("🩺 PharmaBot Console")
    print("Tape 'exit' pour quitter\n")

    while True:
        user_input = input("👤 Décris tes symptômes : ")

        if user_input.lower() == "exit":
            print("👋 Au revoir!")
            break

        advice = get_pharma_advice(user_input)
        print("\n💊 PharmaBot :")
        print(advice)
        print("-" * 50)
