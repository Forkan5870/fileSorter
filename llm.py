from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def promptLLM(prompt, model="llama3", system=False):

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
