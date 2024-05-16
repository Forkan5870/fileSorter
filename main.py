from ollamaBot import Bot

import os
import json
import shutil
import PyPDF2

def extract_text(pdfPath, maxPages=2):
    text = ""
    with open(pdfPath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for pageNum in range(min(maxPages, len(reader.pages))):
            page = reader.pages[pageNum]
            text += page.extract_text()
    return text.replace("\n", " ")


def organize_pdfs(mainDir=os.getcwd()):
    categories = {}
    
    # Step 1: Read through each category, extract text, and update JSON. Store all categories in an array.
    for categoryDir in os.listdir(mainDir):
        if os.path.isdir(os.path.join(mainDir, categoryDir)):
            jsonPath = os.path.join(mainDir, categoryDir, 'data.json')
            pdfPath = None
            for fileName in os.listdir(os.path.join(mainDir, categoryDir)):
                if fileName.endswith('.pdf'):
                    pdfPath = os.path.join(mainDir, categoryDir, fileName)
                    break  # Stop searching once a PDF is found
            if os.path.exists(jsonPath) and pdfPath and len(os.listdir(os.path.join(mainDir, categoryDir))) == 2:
                with open(jsonPath, 'r') as jsonFile:
                    data = json.load(jsonFile)
                    category = data["category"]  # Get the value associated with the key "category"
                    if category:
                        categories[category] = categoryDir
                text = extract_text(pdfPath)
                data["example"] = text
                with open(jsonPath, 'w') as jsonFile:
                    json.dump(data, jsonFile, indent=4)
    
    print("Categories: ", categories)

    # Train the bot
    bot = Bot("phi3", "Be concise, provide the correct tag, and stop when done.")

    for categoryDir in categories.values():
        jsonPath = os.path.join(categoryDir, 'data.json')
        if os.path.exists(jsonPath):
            with open(jsonPath, 'r') as jsonFile:
                data = json.load(jsonFile)
                exampleText = data["example"]
                exampleCategory = data["category"]
                if exampleText and exampleCategory:
                    bot.add_to_history("user", exampleText)
                    bot.add_to_history("assistant", exampleCategory)

    response = bot.prompt("Hello! Create one-sentence story.")
    print(response)
    
    # Step 2: Match files in input directory to categories
    # inputDir = os.path.join(mainDir, "input")
    # for fileName in os.listdir(inputDir):
    #     filePath = os.path.join(inputDir, fileName)
    #     if os.path.isfile(filePath) and fileName.endswith('.pdf'):
    #         text = extract_text(filePath)
    #         introduce = f"TASK -> Classify this content:\nCONTENT -> {text}\nSelect the correct category\nCATEGORIES -> {', '.join(categories.keys())}\nOnly respond with categories, then STOP."
    #         bestCategory = bot.prompt(introduce)
    #         print(f"Matched file '{fileName}' to category '{bestCategory}'")
            # bestCategory = match(text, categories)
            # categoryDir = categories[bestCategory]
            # if not os.path.exists(categoryDir):
            #     os.makedirs(categoryDir)
            # shutil.move(filePath, os.path.join(categoryDir, fileName))
            # print(f"Moved {fileName} to {bestCategory}")

if __name__ == "__main__":
    organize_pdfs()