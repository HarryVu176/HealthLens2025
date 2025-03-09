from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('GEMINI_KEY')
client = None
prompts = dict()
promptFormatting = dict()
promptHeader = None

def getPrompt(promptName: str):
    if promptName not in prompts: # Creates an entry in the dict for the formatting
        with open(f"../HealthLens2025/prompts/{promptName}.txt" , "r") as f:
            prompt = f.read()
            prompts[promptName] = prompt

    return prompts[promptName]

# Fn: getFormatting()
# Brief: Pulls the formatting from the
def getFormatting(formatName):
    if formatName not in promptFormatting: # Creates an entry in the dict for the formatting
        with open(f"promptFormats/{formatName}.json", "r") as f:
            format = f.read()
            promptFormatting[formatName] = format

    return promptFormatting[formatName]

def getClient():
    global client
    if not client:
        client = genai.Client(api_key=API_KEY)

    return client

def stripJsonTag(text):
    # Remove ```json and ``` if present
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()  # Remove the first 7 characters (```json) and last 3 (```)
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()  # Remove the first and last 3 characters (```)
    return text

# Fn: prompt()
# Brief: Returns a prompt, with the added header to ensure gemini doesn't add a warning or anything to the text
def textPrompt(text, useHeader = True):
    contents = []
    if useHeader:
        contents = [f"{getPromptHeader()} {text}"]
    else:
        contents = [text]

    response = getClient().models.generate_content(
        model="gemini-2.0-flash",
        contents=contents)

    return stripJsonTag(response.text)

def imagePrompt(text, image):
    response = getClient().models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"{getPromptHeader()} {text}", image])
    return stripJsonTag(response.text)

def getPromptHeader():
    global promptHeader
    if not promptHeader:
        with open(f"promptHeader.txt", "r") as f:
            promptHeader = f.read()
    return promptHeader