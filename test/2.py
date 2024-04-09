from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


r=get_word_length.invoke("abc")
print(r)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
prompt.format(input="What is the capital of France?")
llm=Ollama(model="qwen")
r=llm.invoke(prompt)
print(r)



