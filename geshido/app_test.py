__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import re
import time
import random
import streamlit as st
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from crewai_tools import WebsiteSearchTool
import base64
from PIL import Image

# page config
st.set_page_config(page_title='Geshidocon Agent Demo',
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items={
                    'Get help': 'https://www.iqbusiness.net/ai-lab'
                   }
                  )

# Sidebar for API key input
st.sidebar.title("Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key:
    st.session_state["OPENAI_API_KEY"] = openai_api_key

# Initialize LLM only if the API key is provided
if openai_api_key:
    st.session_state.llm = ChatOpenAI(openai_api_key=st.session_state["OPENAI_API_KEY"],
                     model="gpt-4o-mini",
                     temperature=0,
                     max_tokens=None)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# List of avatars
# avatar_urls = [
#     "https://cdn-icons-png.flaticon.com/128/4150/4150773.png",
#     "https://cdn-icons-png.flaticon.com/128/4150/4150647.png",
#     "https://cdn-icons-png.flaticon.com/128/4150/4150659.png",
#     "https://cdn-icons-png.flaticon.com/128/4150/4150664.png",
#     "https://cdn-icons-png.flaticon.com/128/4150/4150843.png"
# ]


# Randomly assign avatars to agents
# random.shuffle(avatar_urls)

class MyCustomHandler(BaseCallbackHandler):

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name).write(outputs['output'])


def define_agents():
    agents = []
    for i in range(3):
        with st.expander(f"Define Agent {i+1}", expanded=(i == 0)):
            role = st.text_input(f"Agent {i+1} Role", key=f"role_{i}")
            backstory = st.text_area(f"Agent {i+1} Backstory", key=f"backstory_{i}")
            goal = st.text_input(f"Agent {i+1} Goal", key=f"goal_{i}")

            if role and backstory and goal:
                # # Initialize the specific tool if the role is "product owner"
                # tools = []
                # if role.lower() == "product owner":
                #     tool_roadmap = WebsiteSearchTool(website='https://www.romanpichler.com/blog/prioritising-a-product-backlog-when-everything-is-important/')
                #     tools.append(tool_roadmap)

                agent = Agent(
                    role=role,
                    backstory=backstory,
                    goal=goal,
                    llm= st.session_state.llm,
                    max_iter=3,
                    verbose=False,
                    # tools=tools,  # Include tools here
                    callbacks=[MyCustomHandler(role)]
                )

                agents.append(agent)
                # Save agent to session state
                st.session_state[f"agent_{i}"] = {"role": role, "backstory": backstory, "goal": goal}
    return agents

def main():
    
    #set_background("geshido/bk.jpg")
    
    st.header("💬 Using AI Agents in the product delivery lifecycle")
    st.write('')
    st.subheader('An IQbusiness AI Lab demo', divider='rainbow')
    st.write('')
    st.write('')
    st.write('')
 
    st.sidebar.write("Role: Specifies the agent's job within the groupchat, such as the Client, Product Owner or UI/UX Designer")
    st.sidebar.write("Backstory: Provides depth to the agent's persona, enriching its motivations and engagements within the crew")
    st.sidebar.write("Goal: Defines what the agent aims to achieve, in alignment with its role and the overarching objectives of the crew")

    opening = """Welcome! Let's get started by creating your AI product delivery team. First, enter your OpenAI API key in the sidebar on the left <--  \n\nThen enter the Role
          (e.g. Client, Product Owner, Scrum-master, Solutions Architect/Technical Lead,Lead UI/UX Designer, Lead Data Scientist),
          Backstory, & overall (broad) Goal, for each agent. You can create up to 3 AI agents in your product team.
          \n\nFinally, define the tasks you want each of them to complete. Note that these tasks may be delegated by/to other members of your AI team.
          """
  
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content":opening}]

    if "task_descriptions" not in st.session_state:
        st.session_state["task_descriptions"] = []

    if "define_tasks_clicked" not in st.session_state:
        st.session_state["define_tasks_clicked"] = False

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # with st.chat_message("assistant"):
    #   message_placeholder = st.empty()
    #   assistant_response = opening
  
      # Simulate stream of response with milliseconds delay
      # full_response = ""
      # for chunk in re.split(r'(\s+)', assistant_response):
      #     full_response += chunk + " "
      #     time.sleep(0.04)
      #     message_placeholder.markdown(full_response + "▌")

    st.write('')
    st.write('')
    st.write('')

    agents = define_agents()
       
    if st.button("Define Tasks"):
        st.session_state["define_tasks_clicked"] = True

    if st.session_state["define_tasks_clicked"]:
      
        task_descriptions = []
        for i in range(3):
            if f"agent_{i}" in st.session_state:
                agent_data = st.session_state[f"agent_{i}"]
                agent = Agent(
                    role=agent_data["role"],
                    backstory=agent_data["backstory"],
                    goal=agent_data["goal"],
                    max_iter=3,
                    verbose=False,
                    llm=st.session_state.llm,
                    # tools = agent_data["tool"],
                    callbacks=[MyCustomHandler(agent_data["role"])]
                )
                with st.expander(f"Define Task for {agent.role}", expanded=True):
                    task_description = st.text_area(f"Task Description for {agent.role}", key=f"task_description_{i}")
                    expected_output = st.text_input(f"Desired Output/Artefacts for {agent.role}", key=f"expected_output_{i}")

                    if task_description and expected_output:
                        task_descriptions.append((task_description, agent, expected_output))
                        # Save task descriptions to session state
                        st.session_state["task_descriptions"].append((task_description, agent_data, expected_output))
        
        if st.button("Run Tasks"):
          
            tasks = [
                Task(description=td, agent=Agent(
                    role=a["role"],
                    backstory=a["backstory"],
                    goal=a["goal"],
                    llm=st.session_state.llm,
                    callbacks=[MyCustomHandler(a["role"])]
                ), expected_output=eo)
                for td, a, eo in st.session_state["task_descriptions"]
            ]
        
           
            project_crew = Crew(
                tasks=tasks,
                agents=agents,
                manager_llm=st.session_state.llm,
                full_output=True,
                memory=True,
                process=Process.hierarchical,
                #planning=True
            )

            final = project_crew.kickoff()

            result = f"## Here is the Final Result \n\n {final}"
            st.session_state.messages.append({"role": "assistant", "content": result})
            st.chat_message("assistant").write(result)

if __name__ == "__main__":
    main()
