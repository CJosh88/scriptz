__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import random
import streamlit as st
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from crewai_tools import WebsiteSearchTool

# Sidebar for API key input
st.sidebar.title("Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize LLM only if the API key is provided
if openai_api_key:
    llm = ChatOpenAI(openai_api_key=openai_api_key,
                     model="gpt-4o-mini",
                     temperature=0,
                     max_tokens=None)

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


class StreamToExpander:
    
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Product Owner" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("Product Owner", f":{self.colors[self.color_index]}[Product Owner]")
        if "Scrum-master" in cleaned_data:
            cleaned_data = cleaned_data.replace("Scrum-master", f":{self.colors[self.color_index]}[Scrum-master]")
        if "Technical lead" in cleaned_data:
            cleaned_data = cleaned_data.replace("Technical lead", f":{self.colors[self.color_index]}[Technical lead]")
        if "Business stakeholder" in cleaned_data:
            cleaned_data = cleaned_data.replace("Business stakeholder", f":{self.colors[self.color_index]}[Business stakeholder]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

# class MyCustomHandler(BaseCallbackHandler):

#     def __init__(self, agent_name: str, avatar_url: str) -> None:
#         self.agent_name = agent_name
#         self.avatar_url = avatar_url

#     def on_chain_start(
#         self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
#     ) -> None:
#         st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
#         st.chat_message("assistant").write(inputs['input'])

#     def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
#         st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
#         st.chat_message(self.agent_name, avatar=self.avatar_url).write(outputs['output'])

# def define_agents():
#     agents = []
#     for i in range(2):
#         with st.expander(f"Define Agent {i+1}", expanded=(i == 0)):
#             # name = st.text_input(f"Agent {i+1} Name", key=f"name_{i}")
#             role = st.text_input(f"Agent {i+1} Role", key=f"role_{i}")
#             backstory = st.text_area(f"Agent {i+1} Backstory", key=f"backstory_{i}")
#             goal = st.text_input(f"Agent {i+1} Goal", key=f"goal_{i}")

#             if role and backstory and goal:
#                 agent = Agent(
#                     role=role,
#                     backstory=backstory,
#                     goal=goal,
#                     llm=llm,
#                     callbacks=[MyCustomHandler(role)]
#                 )
#                 agents.append(agent)
#                 # Save agent to session state
#                 st.session_state[f"agent_{i}"] = {"role": role, "backstory": backstory, "goal": goal}
#     return agents

def define_agents():
    agents = []
    for i in range(2):
        with st.expander(f"Define Agent {i+1}", expanded=(i == 0)):
            role = st.text_input(f"Agent {i+1} Role", key=f"role_{i}")
            backstory = st.text_area(f"Agent {i+1} Backstory", key=f"backstory_{i}")
            goal = st.text_input(f"Agent {i+1} Goal", key=f"goal_{i}")

            if role and backstory and goal:
                # # Initialize the specific tool if the role is "product owner"
                # tools = []
                # if role.lower() == "product owner":
                #     tool_roadmap = WebsiteSearchTool(website='https://www.romanpichler.com/blog/10-tips-creating-agile-product-roadmap/')
                #     tools.append(tool_roadmap)

                agent = Agent(
                    role=role,
                    backstory=backstory,
                    goal=goal,
                    llm=llm,
                    #tools=tools,  # Include tools here
                    #callbacks=[MyCustomHandler(role)]
                )

                agents.append(agent)
                # Save agent to session state
                st.session_state[f"agent_{i}"] = {"role": role, "backstory": backstory, "goal": goal}
    return agents

def main():
    st.title("💬 AI Agents - Product Roadmap and Backlog generation/simulation")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Describe your product strategy below"}]

    if "task_descriptions" not in st.session_state:
        st.session_state["task_descriptions"] = []

    if "define_tasks_clicked" not in st.session_state:
        st.session_state["define_tasks_clicked"] = False

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    agents = define_agents()
       
    if st.button("Define Tasks"):
        st.session_state["define_tasks_clicked"] = True

    if st.session_state["define_tasks_clicked"]:
        task_descriptions = []
        for i in range(2):
            if f"agent_{i}" in st.session_state:
                agent_data = st.session_state[f"agent_{i}"]
                agent = Agent(
                    role=agent_data["role"],
                    backstory=agent_data["backstory"],
                    goal=agent_data["goal"],
                    llm=llm,
                    #callbacks=[MyCustomHandler(agent_data["role"])]
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
                    llm=llm,
                    #callbacks=[MyCustomHandler(a["role"])]
                ), expected_output=eo)
                for td, a, eo in st.session_state["task_descriptions"]
            ]
        
        # if st.button("Run Tasks"):
        #     avatar_index = 0  # Initialize the counter
        
        #     tasks = [
        #         Task(
        #             description=td,
        #             agent=Agent(
        #                 role=a["role"],
        #                 backstory=a["backstory"],
        #                 goal=a["goal"],
        #                 llm=llm,
        #                 #callbacks=[MyCustomHandler(a["role"], avatar_urls[avatar_index % 5])]
        #             ),
        #             expected_output=eo
        #         )
        #         for td, a, eo in st.session_state["task_descriptions"]
        #     ]
        
        #     avatar_index = (avatar_index + 1) % 5  # Increment and cycle the counter
            
            project_crew = Crew(
                tasks=tasks,
                agents=agents,
                manager_llm=llm,
                process=Process.hierarchical
            )
            final = project_crew.kickoff()
            
            with st.expander("Processing!"):
                sys.stdout = StreamToExpander(st)
            
            result = f"## Here is the Final Result \n\n {final}"
            st.session_state.messages.append({"role": "assistant", "content": result})
            st.chat_message("assistant").write(result)

if __name__ == "__main__":
    main()

