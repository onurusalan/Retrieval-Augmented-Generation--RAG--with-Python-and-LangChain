import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from assistant_instructions import assistant_instructions

# Load environment variables from the .env file
load_dotenv()

# Check for the API key and initialize the client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = OpenAI(api_key=api_key)

# Save user information to a JSON file
def save_lead_to_json(name="", company_name="", phone="", email=""):
    """
    Save customer details to a JSON file.

    Args:
        name (str): Name of the customer.
        company_name (str): Name of the customer's company.
        phone (str): Optional phone number of the customer.
        email (str): Email address of the customer.

    Behavior:
        - Appends the new customer information to a file called 'leads.json'.
        - If the file does not exist, it creates a new one.
        - Prints a success message upon completion.
    """
    file_path = "leads.json"

    # Load existing leads or initialize an empty list
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            leads = json.load(file)
    else:
        leads = []

    # Create a new lead entry
    new_lead = {
        "Name": name,
        "Company Name": company_name,
        "Phone": phone,
        "Email": email
    }
    leads.append(new_lead)

    # Save the updated leads back to the file
    with open(file_path, "w") as file:
        json.dump(leads, file, indent=4)

    print(f"New customer information saved successfully: {new_lead}")