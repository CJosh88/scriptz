import sys
import time
import os
import re
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o')

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    openai_api_version="2023-05-15",
)

from crewai_tools import SerperDevTool, WebsiteSearchTool

search_tool = SerperDevTool(
    config=dict(
        llm=dict(
            provider="azure_openai",
            config=dict(
                model='gpt-4',
            ),
        ),
        embedder=dict(
            provider="azure_openai",
            config=dict(
                model='text-embedding-ada-002',
            ),
        ),
    )
)

#to keep track of tasks performed by agents
task_values = []

def create_crewai_setup(objective):
    if not llm or not getattr(llm, 'model_name', None):
        print(dir(llm))
        raise ValueError("Language model (llm) is not properly initialized.")
    
    print(f"LLM model name: {llm.model_name}")

    # Define Agents
    economist = Agent(
        role="Economist",
        goal=f"Analyze global trends in relation to economic trends",
        backstory=f"Expert at analysing global economic and market trends. Always use the provided search tool to research",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    occupational_expert = Agent(
        role="Occupational Hazard Specialist",
        goal=f"Analyse global trends in occupational health and safety and related compensation and rehabilitation practices.",
        backstory=f"Expert in Occupational Injuries and Diseases Compensation, Occupational Health and Safety, Early Return to Work, and Rehabilitation Trends Globally",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    medical_expert = Agent(
        role="Medical Administrative Expert",
        goal=f"To review trends in medical benefits administration both globally and within South Africa.",
        backstory=f"Seasoned expert at understanding and comparing medical administration and cost strategies",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    # Define Tasks
    task1 = Task(
        description=f"{objective}. Current month is August 2024.",
        expected_output="Detailed report as requested",
        agent=economist,
    )

    # Create and Run the Crew
    product_crew = Crew(
        agents=[economist, occupational_expert, medical_expert],
        tasks=[task1],
        manager_llm=llm,
        verbose=2,
        memory=True,
        process=Process.hierarchical,
    )

    crew_result = product_crew.kickoff()
    return crew_result

class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']
        self.color_index = 0

    def write(self, data):
        if data is None:
            return

        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        if not cleaned_data:
            return

        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Economist" in cleaned_data:
            cleaned_data = cleaned_data.replace("Economist", f":{self.colors[self.color_index]}[Economist]")
        if "Occupational Hazard Specialist" in cleaned_data:
            cleaned_data = cleaned_data.replace("Occupational Hazard Specialist", f":{self.colors[self.color_index]}[Occupational Hazard Specialist]")
        if "Medical Administrative Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("Medical Administrative Expert", f":{self.colors[self.color_index]}[Medical Administrative Expert]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

def run_crewai_app():
    st.title("AI Research Assistants")
    
    instructions = st.text_input("Enter a research question here")

    if st.button("Run Analysis"):
        stopwatch_placeholder = st.empty()
        start_time = time.time()
        with st.expander("Processing!"):
            sys.stdout = StreamToExpander(st)
            with st.spinner("Generating Results"):
                crew_result = create_crewai_setup(instructions)

        end_time = time.time()
        total_time = end_time - start_time
        stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

        st.header("Tasks:")
        st.table({"Tasks": task_values})

        st.header("Results:")
        st.markdown(crew_result)

if __name__ == "__main__":
    run_crewai_app()
