from src.langgraph_agenticai.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    """
    AI News Node class for fetching and processing AI news articles.
    """
    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm
        # Capture steps in this node so that we can show it
        self.state = {}


    def fetch_news(self, state: State) -> dict:
        """
        Fetch AI news articles from Tavily based on the selected time frame.

        Args:
            state: The state dictionary containing 'frequency'.
        
        Returns:
            dict: Updated state with fetched news articles.
        """
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {"daily": "d", "weekly": "w", "monthly": "m", "yearly": "y"}
        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "yearly": 365}

        response = self.tavily.search(
            query = "Top Artificial Intelligence (AI) technology news globally",
            topic = "news",
            time_range = time_range_map[frequency],
            include_answer = "advanced",
            max_results = 20,
            days = days_map[frequency],
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state

    def summarize_news(self, state: State) -> dict:
        """
        Summarize the fetched news articles using the LLM.

        Args:
            state: The state dictionary containing 'news_data'.
        
        Returns:
            dict: Updated state with summarized news.
        """
        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in EST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state

    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state

