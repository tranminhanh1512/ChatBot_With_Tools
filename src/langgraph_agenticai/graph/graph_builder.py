from langgraph.graph import StateGraph
from langgraph.graph import START,END
from src.langgraph_agenticai.state.state import State
from src.langgraph_agenticai.nodes.basic_chat_node import BasicChatbotNode
from src.langgraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agenticai.nodes.chatbot_with_tools_node import ChatbotWithToolsNode
from langgraph.prebuilt import ToolNode, tools_condition

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

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

    def setup_graph(self, usecase: str):
        """
        Sets up the graph based on the provided use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Tools":
            self.chat_bot_with_tools_build_graph()

        return self.graph_builder.compile()
