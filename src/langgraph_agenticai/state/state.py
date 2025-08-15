from typing_extensions import TypedDict, List
from typing import Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    """
    Represent the structure of the state of the language model.
    Args:
        TypedDict (_type_): _description_
    """
    messages: Annotated[List,add_messages]