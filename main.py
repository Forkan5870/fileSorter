from ollamaBot import Bot

import os
from pathlib import Path
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


def match(text, categories):
    matches = [category for category in categories if category.lower() in text.split("\n")[0].lower()]
    if len(matches) == 1:
        return matches[0]
    matches = [category for category in categories if category.lower() in text.lower()]
    if len(matches) == 1:
        return matches[0]
    else:
        return None


def organize_pdfs(inputDir=os.path.join(os.getcwd(), "input"), outputDir=os.path.join(os.getcwd(), "output"), trainDir=os.path.join(os.getcwd(), "train"), trainedFile=None, model="phi3"):

    categories = {}

    # Step 1: Read through each category, extract text, and update JSON.

    if not trainedFile:

        trainedFile = os.path.join(trainDir, "trained.json")
        if not os.path.exists(trainedFile):
            try:
                with open(trainedFile, 'w') as jsonFile:
                    json.dump({}, jsonFile)
            except OSError as e:
                print(f"Error: Cannot create file '{trainedFile}'. {e}")
                raise

        if not os.path.exists(trainDir):
            raise FileNotFoundError(f"Error: The directory '{trainDir}' does not exist.")
        for category in os.listdir(trainDir):
            categoryDir = os.path.join(trainDir, category)
            if os.path.isdir(categoryDir):
                pdfList = [fileName for fileName in os.listdir(categoryDir) if fileName.lower().endswith('.pdf')]
                if len(pdfList) == 1:
                    pdfPath = os.path.join(categoryDir, pdfList[0])
                    text = extract_text(pdfPath)
                    categories[category] = text

        try:
            with open(trainedFile, 'w') as jsonFile:
                json.dump(categories, jsonFile)
        except OSError as e:
            print(f"Error: Cannot update file '{trainedFile}'. {e}")
            raise

    else:
        if not os.path.exists(trainedFile):
            trainedFile = os.path.join(trainDir, trainedFile)
        try:
            with open(trainedFile, 'r') as jsonFile:
                trainedData = json.load(jsonFile)
                for category, text in trainedData.items():
                    categories[category] = text
        except FileNotFoundError:
            print(f"Error: The file '{trainedFile}' does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file '{trainedFile}' is not a valid JSON file.")

    print("Categories: ", categories)


    # Step 2: "Train" the bot using provided examples

    bot = Bot(model, "Be concise, provide the correct tag, and stop when done.")

    for category, text in categories.items():
        bot.add_to_history("user", f"TASK -> Classify this content:\nCONTENT -> {text}\nSelect the correct category\nCATEGORIES -> {', '.join(categories.keys())}\nOnly respond with one category, then STOP.")
        bot.add_to_history("assistant", category)
    

    # Step 3: Match files in input directory to categories

    if not os.path.exists(inputDir):
        raise FileNotFoundError(f"Error: The directory '{inputDir}' does not exist.")

    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
        except OSError as e:
            print(f"Error: Cannot create directory '{outputDir}': {e}")

    otherDir = os.path.join(outputDir, "Other")
    if not os.path.exists(otherDir):
        try:
            os.mkdir(otherDir)
        except OSError as e:
            print(f"Error creating directory '{otherDir}': {e}")

    for category in categories.keys():
        categoryDir = os.path.join(outputDir, category)
        if not os.path.exists(categoryDir):
            try:
                os.mkdir(categoryDir)
            except OSError as e:
                print(f"Error creating directory '{categoryDir}': {e}")

        
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        if os.path.isfile(filePath) and fileName.endswith('.pdf'):
            text = extract_text(filePath)
            prompt = f"TASK -> Classify this content:\nCONTENT -> {text}\nSelect the correct category\nCATEGORIES -> {', '.join(categories.keys())}\nOnly respond with one category, then STOP."
            response = bot.prompt(prompt)
            bestCategory = match(response, categories)
            print(f"Matched file '{fileName}' to category '{bestCategory}', where the answer was:\n{response}")
            if bestCategory:
                categoryDir = os.path.join(outputDir, bestCategory)
                shutil.move(filePath, os.path.join(categoryDir, fileName))
                print(f"Moved '{fileName}' to '{bestCategory}'")
            else:
                shutil.move(filePath, os.path.join(otherDir, fileName))
                print(f"Moved '{fileName}' to 'Other'")


if __name__ == "__main__":
    organize_pdfs()