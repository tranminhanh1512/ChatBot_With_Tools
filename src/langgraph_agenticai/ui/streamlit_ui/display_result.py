import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase == "Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
                            
        elif usecase == "Chatbot with Tools":
            # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Starts")
                        st.write(message.content)
                        st.write("Tool Call Ends")
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
        
        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                
                with open(AI_NEWS_PATH, 'r') as f:
                    st.download_button(
                        "💾 Download Summary",
                        f.read(),
                        file_name=AI_NEWS_PATH,
                        mime="text/markdown"
                    )
                st.success(f"✅ Summary saved to {AI_NEWS_PATH}")

        elif usecase == "Blog Generator":
            topic = self.user_message
            with st.spinner("Generating blog... ⏳"):
                try:
                    # Invoke the graph with topic
                    result = graph.invoke({"topic": topic})

                    # Get the saved Markdown file path from state
                    blog_md_path = f"./BlogGeneration/{topic.replace(' ', '_')}_blog.md"

                    # Read the Markdown content
                    with open(blog_md_path, 'r', encoding='utf-8') as f:
                        blog_content = f.read()

                    # Display results in a styled container
                    st.subheader("📝 Generated Blog")
                    st.markdown(blog_content, unsafe_allow_html=True)

                    # Download button
                    st.download_button(
                        label="💾 Download Blog",
                        data=blog_content,
                        file_name=blog_md_path.split("/")[-1],
                        mime="text/markdown"
                    )
                    st.success(f"✅ Blog saved to {blog_md_path}")
                except FileNotFoundError:
                    st.error(f"Blog file not found: {blog_md_path}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
