from langchain.output_parsers.enum import EnumOutputParser

import re
from langchain_community.llms import Ollama
from enum import Enum

llm=Ollama(model="qwen")
class Choise(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = 'd'
from langchain.prompts import PromptTemplate
parser = EnumOutputParser(enum=Choise)

from langchain_core.prompts import PromptTemplate

prompt_1 = PromptTemplate.from_template(
    """请你选择一个与用户输入有关的选项:
                "a:用户输入的内容体现了用户想知道有关心理学的知识。\n"
                "b:用户输入的内容体现了用户自身存在心理状态上的疾病。\n"
                "c:用户输入的内容体现了危害自己的内容，就是有可能会产生自残现象。\n"
                "d:都不是。\n"
> 用户输入: {person}

Instructions: {instructions}"""
).partial(instructions=parser.get_format_instructions())
chain = prompt_1 | llm | parser

r=chain.invoke({"person": "我想知道心理疾病的知识"})
print(r)
from langchain_core.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
prompt=ChatPromptTemplate.from_messages(
       [
        SystemMessage(
            content=(
                "你是一个专门用于选择选项的机器人。\n "
                "你有4个选项，你只需要选择一个,而且你必须选择一个，无论用户输入什么内容。\n"
                "选项如下:\n"
                "a:用户输入的内容体现了用户想知道有关心理学的知识。\n"
                "b:用户输入的内容体现了用户自身存在心理状态上的疾病。\n"
                "c:用户输入的内容体现了危害自己的内容，就是有可能会产生自残现象。\n"
                "d:都不是。\n"
                "你的回答应该类似于: "
                "选项:a"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
    
)
r=prompt.format_messages(text="我有点心理疾病")
print(r)

r=llm.invoke(r)
#判断r中是否有a字母，无论大小写
if re.search(r'[aA]', r):
    print("选择了a")
    pass
#判断r中是否有b字母，无论大小写
if re.search(r'[bB]', r):
    print("选择了b")
    pass

#判断r中是否有c字母，无论大小写
if re.search(r'[cC]', r):
    print("选择了c")
    pass

#判断r中是否有d字母，无论大小写
if re.search(r'[dD]', r):
    print("选择了d")
    pass
print(r)
