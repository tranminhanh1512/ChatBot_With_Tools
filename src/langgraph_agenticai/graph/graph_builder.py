from langgraph.graph import StateGraph
from langgraph.graph import START,END
from src.langgraph_agenticai.state.state import State, Blog, BlogState
from src.langgraph_agenticai.nodes.basic_chat_node import BasicChatbotNode
from src.langgraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agenticai.nodes.chatbot_with_tools_node import ChatbotWithToolsNode
from src.langgraph_agenticai.nodes.ai_news_node import AINewsNode
from src.langgraph_agenticai.nodes.blog_generator_node import BlogNode
from langgraph.prebuilt import ToolNode, tools_condition

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        self.blog_graph = StateGraph(BlogState)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    def chat_bot_with_tools_build_graph(self):
        """
        Builds a chatbot with tools graph using LangGraph.
        This method initializes a chatbot node with tool integration using the 
        `ChatbotWithToolsNode` class and integrates it into the graph. The 
        chatbot node is set as both the entry and exit point of the graph.
        """

        # Define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define LLM
        llm = self.llm

        # Define the chatbot node with tools
        obj_chatbot_with_node = ChatbotWithToolsNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        # Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        # Add edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):
        """
        Builds an AI news explorer graph using LangGraph.
        This method initializes an AI news explorer node and integrates it into the graph. The AI news
        explorer node is set as both the entry and exit point of the graph.
        """
        ai_news_node = AINewsNode(self.llm)

        # Add nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
        # Add edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def build_topic_graph(self):
        """
        Builds a topic graph for blog creation using LangGraph.
        """
        blog_obj_node = BlogNode(self.llm)
        # Define the topic node
        self.blog_graph.add_node("title_creation",blog_obj_node.title_creation)
        self.blog_graph.add_node("content_creation", blog_obj_node.content_generation)
        self.blog_graph.add_node("save_result", blog_obj_node.save_result)

        # Add edges
        self.blog_graph.add_edge(START, "title_creation")
        self.blog_graph.add_edge("title_creation", "content_creation")
        self.blog_graph.add_edge("content_creation", "save_result")
        self.blog_graph.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph based on the provided use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Tools":
            self.chat_bot_with_tools_build_graph()

        if usecase == "AI News":
            self.ai_news_builder_graph()
        
        if usecase == "Blog Generator":
            self.build_topic_graph()
            return self.blog_graph.compile()
            
        return self.graph_builder.compile()
