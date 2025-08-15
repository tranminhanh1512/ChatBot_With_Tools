from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns a list of tools to be used in the chatbot.
    """
    api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=2,doc_content_chars_max=500)
    arxiv=ArxivQueryRun(api_wrapper=api_wrapper_arxiv)

    api_wrapper_wiki=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=500)
    wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

    tavily_search = TavilySearchResults(max_results=2)
    tools = [arxiv, wiki, tavily_search]
    return tools

def create_tool_node(tools):
    """
    Creates a ToolNode with the provided tools.
    """
    tool_node = ToolNode(tools=tools)
    return tool_node