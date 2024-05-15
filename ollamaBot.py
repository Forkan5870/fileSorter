from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Bot:
    def __init__(self, model="phi3", system=None):
        self.llm = Ollama(model=model)
        self.history = [("system", system)] if system else []
        print("Bot created")

    def addToHistory(self, role, message):
        self.history.append((role, message))
        print(f"Added to history: ({role}: {message})")

    def removeFromHistory(self, index):
        self.history.pop(index)
        print(f"Removed from history index {index}")

    def clearHistory(self):
        self.history = []
        print("History cleared")

    def prompt(self, prompt):
        output_parser = StrOutputParser()

        messages = self.history.copy()
        messages.append(("user", "{input}"))
        template = ChatPromptTemplate.from_messages(messages)

        chain = template | self.llm | output_parser
        output = chain.invoke({"input": prompt })

        print(f"Prompted and got response")

        return output.strip()


if __name__ == "__main__":

    # Test the Bot class

    bot = Bot("phi3", "You are a clown.")
    bot.addToHistory("user", "You like bananas.")
    bot.addToHistory("assistant", "Ok! I will mention bananas in the next response.")
    response = bot.prompt("Hello! Create one-sentence story.")
    print(response)