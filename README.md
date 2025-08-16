---
title: LanggraphAgenticAI
emoji: 🐨
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.42.0
app_file: app.py
---
# Agentic AI: Chatbox with Multiple Tools

# Chatbot with Tools

🌐 **Live App:** [https://huggingface.co/spaces/manhtran01/Chatbot_with_Tools](https://huggingface.co/spaces/manhtran01/Chatbot_with_Tools)

## Overview
This project is a Streamlit web application that combines multiple AI tools into a single chat interface to enable a wide range of use cases:

- 🗨️ Basic Chatbot – converse naturally with an AI assistant for general questions or casual interactions.
- 🔍 Chatbot with Web Search Tools – augment AI responses with real-time information from web search, enabling fact-based answers.
- 📰 AI News Summarizer – fetch and summarize the latest AI news, presenting concise and structured summaries in Markdown format.
- ️📑 Blog Generation – generate creative and SEO-friendly blog content based on user-provided topics, fully formatted in Markdown.

The application leverages LangGraph to orchestrate complex workflows, managing both the flow of conversation and interactions with external tools. This modular design allows for:

- Easy integration of new tools and AI capabilities.
- Clear separation of logic for each use case.
- Efficient state management across multiple steps in a conversation.

## Features

- Interactive chat interface powered by Streamlit.
- Dynamic tool invocation, enabling the AI to use external sources for enhanced responses.
- Markdown output for blog posts and news summaries, ready for download.
- Automated deployment to Hugging Face Spaces via GitHub Actions. Any push to the main branch automatically updates the live app.

## Architecture
- Frontend: Streamlit for a responsive web interface.
- Backend: Python modules using LangGraph for workflow orchestration and tool integration.
- External APIs: Web search, news APIs, and LLMs for content generation.
- Deployment: Hugging Face Spaces, keeping the app live and continuously synced with GitHub.

This project is ideal for developers and AI enthusiasts looking to explore multi-tool conversational AI applications, automate content generation, and create interactive AI experiences easily deployable on the web.

## Project Structure
```
├── AINews                # Folder to store AI news markdown summaries
├── app.py                # Main Streamlit app entry point
├── BlogGeneration        # Folder to save generated blog markdown files
├── pyproject.toml        # Project configuration
├── README.md             # Project overview and documentation
├── requirements.txt      # Python dependencies
└── src
    ├── __init__.py
    └── langgraph_agenticai
        ├── __init__.py
        ├── graph
        │   ├── __init__.py
        │   └── graph_builder.py     # Builds graphs for different usecases
        ├── LLMs
        │   ├── __init__.py
        │   └── groqllm.py            # LLM
        ├── main.py                   # Main module for running scripts
        ├── nodes
        │   ├── __init__.py
        │   ├── ai_news_node.py       # Node for fetching and summarizing AI news
        │   ├── basic_chat_node.py    # Node for simple chatbot
        │   ├── blog_generator_node.py   # Node for generating blogs
        │   └── chatbot_with_tools_node.py # Node for chatbot with web search tools
        ├── state
        │   ├── __init__.py
        │   └── state.py                 # State definitions (TypedDicts / Pydantic models)
        ├── tools
        │   ├── __init__.py
        │   └── search_tool.py           # Web search / tool utilities
        └── ui
            ├── __init__.py
            ├── streamlit_ui
            │   ├── display_result.py    # Handles Streamlit display for outputs
            │   └── load_ui.py           # Loads Streamlit UI components
            ├── uiconfigfile.ini         # UI configuration settings
            └── uiconfigfile.py          # Parses and applies UI config

```
## Set Up Instruction

### Step 1: Clone the repository
```
git clone https://github.com/tranminhanh1512/ChatBot_With_Tools.git
cd ChatBot_With_Tools
```
### Step 2: Install dependencies
```
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```
### Step 3: Set up Hugging Face Space and Access Tokens

- Create a new Space on Hugging Face by following their official guide: [Spaces Overview](https://huggingface.co/docs/hub/en/spaces-overview)
- Set up HF_Token: [User access tokens](https://huggingface.co/docs/hub/en/security-tokens)

### Step 4: Sync the repository with Hugging Face Space
- Run following commands in the git root folder:
```
git remote add space https://huggingface.co/spaces/<user_name>/<repo_name>
git push --force space main
```
### Step 5: Set up Github Secrets
```
HF_TOKEN = your_access_token
```
### Step 6: Set up a GitHub Action to push your main branch to Spaces
Create a new GitHub Action in your repository with the following content:

```yaml
name: Sync to Hugging Face hub
on:
  push:
    branches: [main]
  # to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          lfs: true
      - name: Push to hub
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: git push https://HF_USERNAME:$HF_TOKEN@huggingface.co/spaces/HF_USERNAME/SPACE_NAME main
```

Replace `HF_USERNAME` with your username and `SPACE_NAME` with your Space name.

### Step 7: Access Your Live App on Hugging Face Spaces

Once the GitHub Action finishes running, your Streamlit app will be deployed. You can access it directly via your Space URL: `https://huggingface.co/spaces/HF_USERNAME/SPACE_NAME`.

