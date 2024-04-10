from langchain.prompts import PromptTemplate
import  ollama
from enum import Enum
from langchain.output_parsers.enum import EnumOutputParser
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
# 初始化大型语言模型
llm = Ollama(model="qwen")
consultants_chain=llm | prompt
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
def knowledge_base(input:str):
    
    return  ''
def chat_with_consultants(input:str):
    

    pass

def pdf_to_text(pdf_path:str):
    loader = PyPDFLoader(pdf_path)
import arxiv
def arxiv_search(query: str):
    # 设置搜索参数
    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate.descending  # 按提交日期降序排列
    )

    # 存储结果为字典列表
    results_dict_list = []
    for result in search.results():
        paper_info = {
            'entry_id': result.entry_id,
            'title': result.title,
            'summary': result.summary or "No summary provided",  # 防止摘要为空
            'authors': [author.name for author in result.authors],
        }
        results_dict_list.append(paper_info)

    return results_dict_list
    