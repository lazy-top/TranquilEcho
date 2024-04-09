from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
from langchain_core.messages import AIMessage,SystemMessage
prompt_template = PromptTemplate.from_template(
    """
你是一名功能选择判断器，现在你根据用户输入来判断应该使用那些功能，并且只需要使用:a,b,c...等字母来回答。
你可以选择的字母如下：
         a: 用户输入的内容体现了是专业的心理知识，选择这个来查询专业知识。 
         b: 用户输入的内容体现了心理状态上的疾病，你是专业的心理咨询师，选择这个来提供专业的心理咨询。
         c: 用户输入的内容体现了危害自己的内容，就是有可能会产生自残现象。 
         d: 都不是，选择这个。
           用户输入：{user_input}.
    """
)
prompt=ChatPromptTemplate.format_messages(
       [
        SystemMessage(
            content=(
                "You are a helpful assistant that re-writes the user's text to "
                "sound more upbeat."
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
    
)

input=prompt_template.format(user_input="我想知道什么是焦虑症？")
llm=Ollama(model="qwen")
chain = llm 

r=chain.invoke(input)
print(r)