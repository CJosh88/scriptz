import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import time 
if 'stage' not in st.session_state:
    st.session_state.stage = 1

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://www.iqbusiness.net/ai-lab',
    'Report a bug': "https://www.iqbusiness.net/ai-lab"
    }
)

st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage > 0 :

    st.title("Create a new AI CV-screening pipeline below")
    st.divider()

    st.markdown('Choose/Create a job specification for the position')

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        b1 = st.button('Use a predefined job specification',on_click=set_state, args=[2])
    with col2:
        b2 = st.button('Upload my own job specification',on_click=set_state, args=[3])

    if st.session_state.stage == 2:
        container = st.container(border=True)

        s1 = st.selectbox(label='Choose a job role to view one of expertly crafted templates', options=['','Software Engineer', 'Project Manager'])

        if s1=='Software Engineer':
            st.markdown('''Responsibilities: 
                    As a Software Engineer at [Company Name], you will be responsible for: 
                    Collaborating with cross-functional teams to design, develop, and maintain software applications and systems for our clients. 
                    Utilizing your expertise in AI/ML, full-stack development, or another relevant area to create innovative solutions that drive business growth and success for our clients.
                    Analyzing client requirements and providing technical guidance on the most effective approach to meet their needs.
                    Developing and implementing software components and features based on predefined specifications and guidelines.
                    Ensuring the quality and performance of the developed software through thorough testing and debugging.
                    Collaborating with other engineers and participating in code reviews to ensure adherence to best practices and standards.
                    Staying up-to-date with the latest industry trends and technologies to ensure our clients receive the most advanced and efficient solutions.
                    Providing technical support and assistance to clients during the implementation and integration phases of the software.
                    Collaborating with project managers and contributing to the estimation, planning, and execution of projects.
                    Mentoring and guiding junior team members, helping them improve their skills and grow professionally.  
                    ''')
            
            st.markdown('''**Requirements**:
                    To be considered for this role, you should possess the following qualifications:
                    Bachelor's degree in Computer Science, Engineering, or a related field; Master's degree preferred.
                    Proven experience as a software engineer or developer, with a strong background in AI/ML, full-stack development, or another relevant area.
                    Proficiency in at least one programming language, such as Python, Java, C++, or JavaScript.
                    Strong knowledge of software engineering principles and best practices.
                    Experience with agile methodologies and version control systems, such as Git.
                    Excellent problem-solving and analytical skills.
                    Strong communication and interpersonal skills, with the ability to work effectively in a team environment.
                    Self-motivated, detail-oriented, and able to manage multiple tasks simultaneously.
                    Familiarity with cloud platforms, such as AWS, Azure, or Google Cloud, is a plus.''')
            
            SE_df = pd.DataFrame({'Criteria': ['Experience', 'Technical Skills', 'Agile Methodologies', 'Version Control Systems',\
                                                'Problem Solving', 'Communication Skills', 'Teamwork', 'Time Management', 'Adaptability', \
                                                    'Familiarity with Cloud Platforms'],
                                    'Low scoring attributes': ['0-2 years of experience', 'Basic understanding of programming languages', \
                                                    'Unfamiliar with agile methodologies and version control systems', 'Inexperienced with version control systems', \
                                                        'Weak problem-solving abilities', 'Ineffective written and verbal communication skills', \
                                                            'Difficulty working well in a team environment', 'Poor task prioritization and missed deadlines', \
                                                                'Limited capacity to adapt to new situations and learn new skills', \
                                                                    'No knowledge or experience with cloud platforms like AWS, Azure, or Google Cloud'],
                                    'High scoring attributes': ['10+ years of experience', 'Mastery of multiple programming languages', \
                                                     'Expertise in agile methodologies and version control systems', 'Extensive experience with version control systems', \
                                                        'Exceptional problem-solving abilities', 'Superior written and verbal communication skills',\
                                                              'Excellent teamwork skills', 'Outstanding time management skills',\
                                                                  'Extraordinary adaptability and continuous learning',\
                                                                      'Comprehensive knowledge and experience with cloud platforms like AWS, Azure, or Google Cloud'],
                                    'Weighting': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],})
            
            edited_df  = st.data_editor(data=SE_df,width=1500)

            # Check if there are any blank or empty space cells in the criteria, low anchors, and high anchor columns
            def check_empty_spaces(row):
                return row['Criteria'].replace(' ', '') == '' or \
                    row['Low scoring attributes'].replace(' ', '') == '' or \
                    row['High scoring attributes'].replace(' ', '') == ''

            sub = st.button(label='Click to proceed to the next step')

            if sub:
                # Calculate the sum of the weightings
                total_score = edited_df['Weighting'].sum()
                # Check for missing criteria
                empties = edited_df.apply(check_empty_spaces, axis=1).any()

                if total_score != 100 and empties==False:
                    st.write("Oops, looks like the weightings don't sum to 100%. Please check above and try again.")

                elif total_score == 100 and empties==True:
                    st.write("Oops, looks like the one or more criteria or achors are empty. Please check above and try again")
                
                elif total_score != 100 and empties==True:
                    st.write("Oops, looks the weightings don't sum to 100, and one or more criteria or achors are empty. Please check above and try again")

                elif total_score == 100 and empties==False:                    
                    with st.spinner('Please wait...'):
                        time.sleep(3)
                    switch_page('Results')            
                    st.session_state.stage = 4


    elif st.session_state.stage == 3:
        container2 = st.container(border=True)
        st.file_uploader(label='Upload the job spec for our AI to convert to a scoring matrix', accept_multiple_files=False, type='pdf')


