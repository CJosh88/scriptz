__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

def define_agents(llm):
    if not llm:
        st.error("Please provide a valid OpenAI API key.")
        return []

    agents = [
        Agent(
            role='Product Owner',
            backstory='''You are a product owner responsible for managing the product backlog and ensuring it aligns with business strategy.
            You work closely with stakeholders to understand their needs and prioritize features accordingly.
            You are skilled in agile processes and collaborate with the development team to deliver successful products.
            ''',
            goal="Create and refine the product backlog, ensuring it aligns with business needs and stakeholder expectations. Generate high-quality user stories, epics, and backlog items that drive product success.",
            llm=llm,
            callbacks=[MyCustomHandler("Product Owner", avatar_urls[0])]
        ),
        Agent(
            role='Solution Architect',
            backstory='''You are a solution architect with a strong technical background in IT areas such as architecture, infrastructure, and cloud development.
            You design and manage technical solutions to solve business problems, ensuring alignment with corporate strategy.
            You possess excellent communication and analytical skills, working closely with enterprise and software architects, business analysts, and project teams.
            ''',
            goal="Design and document technical solutions through artifacts like solution designs, BRDs, and technical specifications. Ensure these solutions align with business needs and drive product innovation.",
            llm=llm,
            callbacks=[MyCustomHandler("Solution Architect", avatar_urls[1])]
        ),
        Agent(
            role='Designer',
            backstory='''You are a graphic designer who enjoys branding and design overall.
            You aim to be very good at your job, stay up-to-date with design skills, and contribute meaningfully to your team or agency.
            You focus on creating cool designs that make stakeholders and clients happy, while also understanding the business side of design.
            ''',
            goal="Create high-quality wireframes, prototypes, and visual designs that meet business needs and delight stakeholders. Ensure designs are user-centric and align with product goals.",
            llm=llm,
            callbacks=[MyCustomHandler("Designer", avatar_urls[2])]
        ),
        Agent(
            role='Developer',
            backstory='''You are a developer who collaborates with the product owner to write user stories and tasks during sprints.
            You are skilled in software development and work closely with the product owner to deliver features that meet business needs.
            You are open to feedback and willing to iterate on your work based on refinement discussions.
            ''',
            goal="Write high-quality code that meets the requirements outlined in user stories and tasks. Ensure code is testable, maintainable, and aligns with the overall product vision.",
            llm=llm,
            callbacks=[MyCustomHandler("Developer", avatar_urls[3])]
        ),
        Agent(
            role='Scrum Master',
            backstory='''You are a Scrum Master who facilitates agile processes and ensures the Scrum framework is followed.
            You work closely with the product owner, development team, and stakeholders to ensure efficient product delivery.
            You are skilled in conflict resolution and team collaboration, driving continuous improvement in the Scrum team.
            ''',
            goal="Facilitate agile processes, ensure Scrum framework adherence, and drive continuous improvement in the Scrum team. Generate artifacts like sprint backlogs, burndown charts, and increment definitions to support team efficiency.",
            llm=llm,
            callbacks=[MyCustomHandler("Scrum Master", avatar_urls[4])]
        )
    ]

    return agents

def main():
    st.title("💬 AI Project Agents/Assistants")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What tasks do you want us to perform?"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if "agents" not in st.session_state:
        st.session_state.agents = define_agents(llm)

    if "task_descriptions" not in st.session_state:
        st.session_state.task_descriptions = []

    with st.expander("Describe the challenge/project", expanded=True):
        task_description = st.text_area("Description", key="task_description")
        expected_output = st.text_input(f"Expected Output", key=f"expected_output")
        
        if st.button("Submit", key="add_task"):
            if task_description and expected_output:
                st.session_state.task_descriptions.append((task_description, expected_output))
                tasks = [Task(description=task_description, expected_output=expected_output)]
                
                st.warning("Working...")
                
                project_crew = Crew(
                    tasks=tasks,
                    agents=st.session_state.agents,
                    manager_llm=llm,
                    process=Process.hierarchical
                )
                
                # Adding debug logging
                logging.debug(f'Tasks: {tasks}')
                logging.debug(f'Agents: {st.session_state.agents}')

                try:
                    final = project_crew.kickoff()
                    result = f"## Here is the Final Result \n\n {final}"
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    st.chat_message("assistant").write(result)
                    st.success("Task complete")
                except IndexError as e:
                    st.error(f"An error occurred: {e}")
                    logging.error(f"Error during kickoff: {e}")

if __name__ == "__main__":
    main()

