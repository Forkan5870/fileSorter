from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Bot:
    def __init__(self, model="phi3", system=None):
        self.llm = Ollama(model=model)
        self.history = [("system", system)] if system else []
        print("Bot created")

    def add_to_history(self, role, message):
        self.history.append((role, message.replace("{", "[").replace("}", "]")))
        print(f"Added role '{role}' with message to history")

    def clear_history(self):
        self.history = [self.history[0]] if "system" in self.history[0] else []
        print("History cleared")

    def prompt(self, prompt):
        print("Prompting...", end=" ")

        output_parser = StrOutputParser()

        messages = self.history.copy()
        messages.append(("user", "{input}"))
        template = ChatPromptTemplate.from_messages(messages)

        chain = template | self.llm | output_parser
        output = chain.invoke({"input": prompt.replace("{", "[").replace("}", "]")})

        print(f"Got response")

        return output.strip()


if __name__ == "__main__":

    # Test the Bot class

    bot = Bot("phi3", "You are a clown.")
    bot.add_to_history("user", "You like bananas.")
    bot.add_to_history("assistant", "Ok! I will mention bananas in the next response.")
    response = bot.prompt("Hello! Create one-sentence story.")
    print(response)