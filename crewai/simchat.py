import streamlit as st
import time
import random 

def type_message(message):
    for char in message:
        # Append the character to the existing text
        st.session_state['text'] += char
        # Update the placeholder with the new text
        st.session_state['input_text'].markdown(st.session_state['text'])
        # Wait a bit before typing the next character
        time.sleep(0.005)  # Adjust typing speed as needed
    # Add some space after the message
    st.session_state['text'] += '\n\n'

def main():
    st.set_page_config(page_title="Simulated Chat")
        # Define paths to local avatar images for each role
    avatars = {
        "Product Owner": "avatar_po.webp",
        "Client": "avatar_cl.webp",
        "Scrum Master": "avatar_sm.webp",
        "UX Designer": "avatar_ux.webp",
    }

    typing_speed = 0.003  # Constant typing speed, adjust as needed
    pause_probability = 0.03  # Probability of a pause at any character
    max_pause_duration = 0.5  # Maximum duration of a pause, adjust as needed

    
    RFP = """Project Brief: \
    
    **Development of a Staff Resourcing and Operational Dashboard** <br>
    
    **Project Title**: Acme Operational Insights Dashboard <br>

    ### Introduction
    Acme Industries is committed to enhancing operational efficiencies <br>    
    and strategic decision-making through improved visibility into staff resourcing <br>
    deployments, and key operational metrics. This project brief outlines  <br>
    the development of an integrated dashboard designed to provide <br>
    real-time insights into these critical areas, enabling more <br>
    informed management and optimization of our staffing solutions. <br>

    ### Background
    In the dynamic environment of corporate staffing, the ability  <br>
    to access and analyze real-time data related to staff allocation, <br>
    project deployments, and operational performance is crucial. The Acme <br>
    Operational Insights Dashboard aims to centralize this data, providing <br>
    a comprehensive view that supports strategic planning and day-to-day management.<br>

    ### Project Need/Demand
    - **Enhanced Visibility:** Centralize data from various sources <br>
    to provide a holistic view of staff resourcing and operational metrics.<br>
    - **Real-Time Insights:** Enable real-time tracking of staff <br>
    deployments, availability, and project status to facilitate agile <br>
    decision-making. <br>
    - **Performance Monitoring:** Incorporate key performance indicators <br>
    (KPIs) to monitor and evaluate operational efficiency and staff productivity.<br>

    ### Objectives
    - Develop a user-friendly, interactive dashboard that <br>
    integrates data from multiple sources. <br>
    - Provide real-time visibility into staff  <br>
    allocations, project deployments, and availability.<br>
    - Enable tracking of operational KPIs to assess <br>
    performance and identify areas for improvement.

    ### Scope of Work
    - **Data Integration:** Aggregate data from HR systems,<br>
      project management tools, and other relevant sources to <br>
      feed into the dashboard.<br>
    - **Dashboard Development:** Design and develop an interactive<br>
      dashboard that provides a comprehensive view of staff resourcing, <br>
      deployments, and operational metrics.<br>
    - **User Access Management:** Implement access controls to ensure <br>
    data security and relevancy for different user roles within the organization.

    ### Expectations from the Project Team
    - **Cross-functional Collaboration:** Work closely with the client admin <br>
    to ensure comprehensive data integration and alignment with business needs. <br>
    - **Technical Expertise:** Utilize advanced data analytics and visualization <br> 
    tools to create an intuitive and informative dashboard.<br>
    - **User-Centric Design:** Focus on usability and user experience <br>
    to ensure the dashboard is accessible and valuable to a wide range of stakeholders.

    ### Key Deliverables
    - A fully functional operational insights dashboard, accessible <br>
    to authorized users across the organization.<br>
    - Documentation detailing dashboard features, data sources, <br>
    and user instructions.<br> A training program for stakeholders to ensure effective utilization of the dashboard.

    ### Resources and Budget <br>
    - Outline of required resources, including personnel <br>
    (data analysts, developers, UI/UX designers), software, and any third-party services.<br>
    - A detailed budget that encompasses all projected costs <br>
    associated with the development, deployment, and maintenance of the dashboard.

    ### Risks and Mitigation Strategies
    - Identification of potential risks, such as data integration <br>
    challenges or delays in development, along with corresponding mitigation strategies.<br>

    ### Approval and Review Process
    - Define a structured approval process for key development milestones <br>
      and establish regular review sessions with stakeholders to ensure alignment <br>
      with business objectives.<br>

    The successful development and implementation of the Acme Operational Insights Dashboard <br>
    will empower our organization with the data-driven insights needed to optimize <br>
    staffing strategies, improve operational efficiencies, and drive better business <br>
    outcomes. This project represents a strategic investment in our operational capabilities <br>
      and a commitment to fostering a culture of transparency and continuous improvement.

    """

    chat_log = [
        ("Client", f"Hi crew, here is the project brief:"),
        ("Client", f"{RFP}"),
        ("Product Owner", "Client, a question: Could you provide more detailed information on the specific data sources you intend for us to integrate with the dashboard? Additionally, are there any specific KPIs you're looking to track beyond the general operational efficiency and staff productivity metrics mentioned in the brief? This clarity will help us ensure that the dashboard aligns perfectly with your operational goals and data analysis needs. Furthermore, understanding the priority of these data sources and KPIs will assist us in planning the development phases accordingly, ensuring we focus on the most critical aspects first. Lastly, could you specify any particular user roles within your organization that should have differentiated access to the dashboard? This information is crucial for implementing effective access controls and user management features."),
        ("Client", "Thank you for reaching out for more detailed information. To ensure the dashboard aligns with our operational goals and data analysis needs, here are the specifics:..."),
        ("Client", """1. **Data Sources to Integrate:** HR Management System (HRMS):** For real-time staffing deployments, employee ratings, and availability. \**Project Management Tools:** To track ongoing projects, associated staff, and their productivity metrics. \**Financial System:** For budget allocations, payroll data, and cost analysis related to staffing.**Customer Feedback System:** To integrate staff performance ratings from client feedback.2. **Key Performance Indicators (KPIs):****Staff Utilization Rate:** To measure the percentage of time staff are working on billable projects versus available time.**Project Delivery Success Rate:** The percentage of projects completed on time and within budget.**Employee Satisfaction Score:** Based on internal surveys to gauge staff morale and engagement.**Client Satisfaction Score:** Derived from customer feedback on staff performance and project outcomes.**Cost Efficiency:** Analysis of staffing costs against revenue generated from projects.**User Roles and Access Controls:****Executive Access:** Full dashboard access, including financial data and strategic KPIs.**Project Manager Access:** Limited to project-related data, staff assignments, and productivity metrics.**HR Access:** Access to HRMS data, including staffing deployments, employee ratings, and availability.**Finance Access:** Limited to financial data, including payroll, budget allocations, and cost analysis. Our priority is to first integrate the HRMS and Project Management Tools to get a clear view of our staffing deployments and their productivity. Following that, integrating the Financial System and Customer Feedback System will be crucial for a holistic view of operational efficiency. We believe that focusing on these areas will significantly enhance our operational efficiency and staff productivity. Please let us know if you need further details or clarifications."""),
        ("Product Owner", "With the detailed information provided by the client, including specifics on data sources to integrate (HR Management System, Project Management Tools, Financial System, and Customer Feedback System), Key Performance Indicators (Staff Utilization Rate, Project Delivery Success Rate, Employee Satisfaction Score, Client Satisfaction Score, Cost Efficiency), and user roles and access controls (Executive, Project Manager, HR, Finance), we have a clear roadmap to proceed with the development of the Acme Operational Insights Dashboard. The priority will be to first integrate the HRMS and Project Management Tools, followed by the Financial System and Customer Feedback System, aligning with the client's operational goals and ensuring effective planning and execution of the project phases."),
        ("Product Owner", "UX Designer, Task: Please collaborate with the snr developer and create user stories and acceptance criteria for the Acme Operational Insights Dashboard..."),
        ("UX Designer", "Sure! Below are the user stories and acceptance criteria for the Acme Operational Insights Dashboard, structured in a 2-column table format for clarity:..."),
        ("UX Designer", """
         
            User Story 1: "As an Executive, I want to view a dashboard that integrates data from HRMS and Project Management Tools so that I can monitor staff utilization rates and project delivery success rates in real-time" [Acceptance Criteria: - Dashboard integrates data seamlessly from HRMS and Project Management Tools.; - Real-time updates on staff utilization rates and project delivery success rates are visible.; - Data accuracy is validated against source systems.]. 
         
            User Story 2: "As a Project Manager, I want to access project-specific performance metrics, including staff utilization and project delivery success rates, to ensure my projects are on track" [Acceptance Criteria: - Access control allows Project Managers to view data related to their projects only.; - Project-specific metrics are accurately displayed.; - The dashboard updates in real-time to reflect current project statuses.]

            User Story 3: "As an HR Professional, I want to view employee satisfaction scores alongside staff utilization rates to better understand how workload impacts employee morale" [Acceptance Criteria: - Employee satisfaction scores are accurately imported from the HR Management System.; - Correlation between staff utilization rates and employee satisfaction is visually represented.; - HR professionals have the ability to filter and analyze data based on different departments or teams.]

            User Story 4: "As a Finance Professional, I want to analyze cost efficiency alongside project delivery success rates to assess the financial health of projects" [Acceptance Criteria: - Integration with the Financial System allows for real-time tracking of project costs.; - Dashboard provides tools for comparing cost efficiency with project delivery success rates.; - Finance professionals can generate reports for further analysis.]

            User Story 5: "As an Executive, I want to view client satisfaction scores to gauge the overall success of our projects and operational efficiency" [Acceptance Criteria: - Client satisfaction scores are accurately imported from the Customer Feedback System.; - The dashboard allows for comparison between client satisfaction scores and project delivery success rates.; - Executives can view trends over time to assess improvements or declines in satisfaction.]
            
         """),
        ("Product Owner", "Thanks. Scrum Master, a task for you: Estimate a week by week sprint plan over 4 months for the development of the Acme Operational Insights Dashboard..."),
        ("Scrum Master", "To estimate a week by week sprint plan over 4 months for the development of the Acme Operational Insights Dashboard, we'll follow the Scrum framework, breaking down the project into two-week sprints...Given the project's scope and the priority integrations, here's a high-level plan:"),
        ("Scrum Master", """*Sprint 1 & 2: Project Kickoff and Setup**
        - Activities: Team kickoff, setup development environments, review user stories and acceptance criteria, and finalize the Definition of Done (DoD).
        - Goals: Ensure all team members are aligned, environments are ready for development, and the team has a clear understanding of the project requirements.

        **Sprint 3 & 4: HR Management System Integration**
        - Activities: Develop and test the integration with the HR Management System to pull data related to Staff Utilization Rate and Employee Satisfaction Score.
        - Goals: Successfully integrate the HR system and display the KPIs on the dashboard for the HR and Executive roles.

        **Sprint 5 & 6: Project Management Tools Integration**
        - Activities: Develop and test the integration with Project Management Tools to monitor Project Delivery Success Rate.
        - Goals: Integrate project management tools and ensure KPIs are accurately reflected on the dashboard for Project Managers and Executives.

        **Sprint 7 & 8: Financial System Integration**
        - Activities: Integrate the Financial System to track Cost Efficiency.
        - Goals: Ensure financial data is accurately pulled into the dashboard and accessible by the Finance and Executive roles.

        **Sprint 9 & 10: Customer Feedback System Integration**
        - Activities: Integrate the Customer Feedback System to monitor Client Satisfaction Score.
        - Goals: Display customer feedback metrics on the dashboard for Executive and Project Manager roles.

        **Sprint 11 & 12: Access Controls and User Roles**
        - Activities: Implement access controls and ensure dashboard views are tailored to different user roles.
        - Goals: Each user role (Executive, Project Manager, HR, and Finance) should see relevant data and KPIs according to their access level.

        **Sprint 13 & 14: Testing and Quality Assurance**
        - Activities: Conduct comprehensive testing, including user acceptance testing (UAT) with the UX Designer's guidance.
        - Goals: Ensure the dashboard is bug-free, meets all acceptance criteria, and aligns with user-centric design principles.

        **Sprint 15 & 16: Final Touches and Project Wrap-up**
        - Activities: Address any remaining feedback, conduct final testing, and prepare for project handover.
        - Goals: Ensure the dashboard is ready for deployment, and all project documentation is complete.

        Throughout the project, regular sprint reviews and retrospectives will be conducted to ensure continuous improvement and alignment with the client's operational goals. This plan is flexible and may be adjusted based on feedback and any emerging requirements. """)
            ]

    # for role, message in chat_log:
    #     # Create a placeholder for each message
    #     placeholder = st.empty()

    #     # Simulate typing by progressively displaying the message
    #     for i in range(1, len(message) + 1):
    #         placeholder.markdown(f"**{role}:** {message[:i]}")
    #         delay = random.uniform(0.005, 0.001)  # Adjust the range as needed
    #         time.sleep(delay)

    #     # To avoid a long wait, remove the character-by-character update and display the full message
    #     placeholder.markdown(f"**{role}:** {message}")
    #     time.sleep(1)  # Adjust the pause between messages as needed

    for role, message in chat_log:
        placeholder = st.empty()

        # Get the local file path for the current role's avatar
        avatar_path = avatars.get(role, "")

        # Use the `st.image` function to display the avatar next to the message
        col1, col2 = st.columns([1, 5])

        with col1:
            if avatar_path:  # Check if the avatar path is not empty
                st.image(avatar_path, width=70)  # Adjust width as needed

        with col2:
            # Simulate typing by progressively displaying the message
            for i in range(1, len(message) + 1):
                placeholder.markdown(f"**{role}:** {message[:i]}")
                
                time.sleep(typing_speed)  # Constant typing speed

                # Randomly decide whether to introduce a pause
                if random.random() < pause_probability:
                    time.sleep(random.uniform(0.2, max_pause_duration)) 

            # Display the full message after the typing simulation
            placeholder.markdown(f"**{role}:** {message}")
            time.sleep(1)  # Pause between messages, adjust as needed


main()