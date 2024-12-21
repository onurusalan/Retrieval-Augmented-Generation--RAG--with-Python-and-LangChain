import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from custom_functions import save_lead_to_json  # For saving user information
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

# Load API keys from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found! Please check your .env file.")

# Initialize the ChatGPT model
chat_model = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# Prompt Template for conversation
template = """
You are an expert assistant for a project called "NeoTerra," a futuristic and fully sustainable city plan.
Details about NeoTerra are provided below:
{context}

Engage with the user based on this context and assist them with NeoTerra-related questions.
"""

# NeoTerra Information Context
context = """
NeoTerra is a futuristic city plan designed to address major issues in modern urban areas.
The project aims to create a self-sustaining city that integrates smart technologies while being environmentally
and human-friendly. It focuses on critical areas such as energy, water, food production, and urbanization.

NeoTerra's features include:
1. Future-designed green roofs: Solar panels, rainwater harvesting systems, and small-scale greenhouses.
2. Vertical farming towers: 20-30 story farming towers with automated irrigation and lighting systems.
3. Solar-powered smart streetlights: Equipped with air quality and motion sensors.
4. Roads with in-motion charging: Energy transfer for electric vehicles while driving.
5. Autonomous delivery drones: Powered by solar panels and advanced navigation systems.

Project goals: Minimize the environmental, economic, and social impacts of urbanization, improve the quality of life,
and promote a sustainable lifestyle.
"""

# Memory management for storing conversation history
memory = ConversationBufferMemory(return_messages=True)

# Function to handle user queries
def ask_neo_terra(question):
    try:
        # Create a system message with the NeoTerra context
        system_message = SystemMessage(content=context)

        # Retrieve previous messages from memory
        previous_messages = memory.chat_memory.messages

        # Create a user message with the current query
        user_message = HumanMessage(content=question)

        # Combine messages for the chat model
        messages = [system_message] + previous_messages + [user_message]

        # Get the response from the chat model
        response = chat_model(messages)

        # Add the user's query and the model's response to memory
        memory.chat_memory.add_user_message(question)
        memory.chat_memory.add_ai_message(response.content)

        return response.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main program loop
if __name__ == "__main__":
    print("Welcome to the NeoTerra Assistant!")
    print("Type 'exit', 'quit', or 'çık' to leave the program.")

    while True:
        user_input = input("\nQuestion: ")
        if user_input.lower() in ["çık", "exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input.lower().startswith("kayıt"):
            # Capture user information and save it to a JSON file
            print("Please enter customer information:")
            name = input("Name: ")
            company_name = input("Company Name: ")
            email = input("Email: ")
            phone = input("Phone (optional): ")
            save_lead_to_json(name=name, company_name=company_name, phone=phone, email=email)
        else:
            # Process the user's query
            answer = ask_neo_terra(user_input)
            print(f"NeoTerra: {answer}")