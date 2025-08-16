from src.langgraph_agenticai.state.state import BlogState

class BlogNode:
    """
    A class to generate blog posts based on a given topic and language.
    """

    def __init__(self, llm):
        self.llm = llm
        self.state = {}

    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """
                You are an expert blog content writer. Use Markdown formatting. Generate
                a blog title for the {topic}. This title should be creative and SEO friendly
            """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            # Update both self.state and the incoming state
            self.state["topic"] = state["topic"]
            self.state["blog"] = {"title": response.content}
            state["blog"] = {"title": response.content}
            return state

    def content_generation(self, state: BlogState):
        if "topic" in self.state and "blog" in self.state:
            system_prompt = """You are an expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=self.state["topic"])
            response = self.llm.invoke(system_message)

            self.state["blog"]["content"] = response.content
            state["blog"]["content"] = response.content  # propagate to state
            return self.state

    def save_result(self, state: BlogState):
        if "blog" not in state or not state["blog"]:
            raise ValueError("No blog content found in state. Generate content first.")

        topic = state.get("topic", "untitled")
        blog_title = state["blog"]["title"]
        blog_content = state["blog"]["content"]

        filename = f"./BlogGeneration/{topic.replace(' ', '_')}_blog.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {blog_title}\n\n")
            f.write(blog_content)

        self.state["filename"] = filename
        state["filename"] = filename  # propagate to state
        return self.state
