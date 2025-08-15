from src.langgraph_agenticai.state.state import State

class ChatbotWithToolsNode:
    """
    Chatbot with tools node class.
    This class integrates a chatbot with tools functionality.
    """
    def __init__(self, model):
        self.llm = model
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node with tools integrated.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> dict:
            """
            Chatbot logic for processing user input and generating a response.
            """
            return {"messages": [llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node