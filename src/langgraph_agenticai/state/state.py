from typing_extensions import TypedDict, List
from typing import Annotated
from langgraph.graph import add_messages
from pydantic import BaseModel, Field

class State(TypedDict):
    """
    Represent the structure of the state of the language model.
    Args:
        TypedDict (_type_): _description_
    """
    messages: Annotated[List,add_messages]

class Blog(BaseModel):
    """
    Represent the structure of the blog.
    Args:
        BaseModel (_type_): _description_
    """
    title: str = Field(description = "The title of the blog post")
    content: str = Field(description = "The content of the blog post")

class BlogState(TypedDict):
    topic: str
    blog: Blog
    current_language: str