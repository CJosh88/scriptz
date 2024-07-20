import streamlit as st
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

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
    for i in range(5):
        with st.expander(f"Define Agent {i+1}", expanded=(i == 0)):
            name = st.text_input(f"Agent {i+1} Name")
            role = st.text_input(f"Agent {i+1} Role")
            backstory = st.text_area(f"Agent {i+1} Backstory")
            goal = st.text_input(f"Agent {i+1} Goal")

            if name and role and backstory and goal:
                agent = Agent(
                    role=role,
                    backstory=backstory,
                    goal=goal,
                    llm=llm,
                    callbacks=[MyCustomHandler(name)]
                )
                agents.append(agent)
    return agents

def main():
    st.title("💬 CrewAI Writing Studio")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What blog post do you want us to write?"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    agents = define_agents()

    if st.button("Define Tasks"):
        task_descriptions = []
        for i, agent in enumerate(agents):
            with st.expander(f"Define Task for {agent.role}", expanded=True):
                task_description = st.text_area(f"Task Description for {agent.role}")
                expected_output = st.text_input(f"Expected Output for {agent.role}")

                if task_description and expected_output:
                    task_descriptions.append((task_description, agent, expected_output))
        
        if st.button("Run Tasks"):
            tasks = [
                Task(description=td, agent=a, expected_output=eo)
                for td, a, eo in task_descriptions
            ]
            project_crew = Crew(
                tasks=tasks,
                agents=agents,
                manager_llm=llm,
                process=Process.hierarchical
            )
            final = project_crew.kickoff()
            result = f"## Here is the Final Result \n\n {final}"
            st.session_state.messages.append({"role": "assistant", "content": result})
            st.chat_message("assistant").write(result)

if __name__ == "__main__":
    main()
