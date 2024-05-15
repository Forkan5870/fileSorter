from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# This function is a simplified version of the Bot class from ollamaBot.py

def promptLLM(prompt, model="llama2", system=False):

    output_parser = StrOutputParser()

    llm = Ollama(model=model)

    if system:
        template = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("user", "{input}"),
            ]
        )
    else:
        template = ChatPromptTemplate.from_messages(
            [
                ("user", "{input}"),
            ]
        )

    chain = template | llm | output_parser
    output = chain.invoke({"input": prompt })

    print(output.strip())


promptLLM("Hello! Create a one-sentence story.")