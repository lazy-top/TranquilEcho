from langchain.prompts import PromptTemplate
import  ollama
from enum import Enum
from langchain.output_parsers.enum import EnumOutputParser
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# 初始化大型语言模型
llm = Ollama(model="qwen")
    # 定义枚举类
class Choice(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = 'd'
def selector(input: str):
    # 创建枚举输出解析器
    parser = EnumOutputParser(enum=Choice)

    # 创建提示模板
    prompt_template = PromptTemplate.from_template(
        """请你选择一个与用户输入有关的选项:
        "a:用户输入的内容体现了用户想知道有关心理学的知识。\n"
        "b:用户输入的内容体现了用户自身存在心理状态上的疾病。\n"
        "c:用户输入的内容体现了危害自己的内容，就是有可能会产生自残现象。\n"
        "d:都不是。\n"
    > 用户输入: {input}

    Instructions: {instructions}"""
    ).partial(instructions=parser.get_format_instructions())

    # 构建处理链
    chain = prompt_template | llm | parser

    # 调用处理链
    result = chain.invoke({"input": input})
    return result

def control(enum:Enum,input:str):
    if(enum == Choice.A):
        knowledge_base(input)
        
        pass
    if(enum == Choice.B):
        consultants(input)
        
        pass
    if(enum == Choice.C):
        waring(input)
        
        pass
    if(enum == Choice.D):
        
        pass
    
def knowledge_base(input:str):
    return  ''
def consultants(input:str):
    pass
def  waring(input:str):
    return  ''