import autogen
import panel as pn
import openai
import os
import time

config_list = [
    {
        'model': 'gpt-4o',
        'api_key': 'sk-Your_OpenAI_Key',
    }
    ]
gpt4_config = {"config_list": config_list, "temperature":0, "seed": 53}

user_proxy = autogen.UserProxyAgent(
   name="Admin",
   is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
   system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin. 
   Only say APPROVED in most cases, and say EXIT when nothing is to be done further. Do not say others.""",
   code_execution_config=False,
   default_auto_reply="Approved", 
   human_input_mode="NEVER",
   llm_config=gpt4_config,
)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message='''...''',
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    system_message="""..."""
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''...
''',
    llm_config=gpt4_config,
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="...",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="...",
    llm_config=gpt4_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

pn.extension(design="material")

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    user_proxy.initiate_chat(manager, message=contents)

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Send a message!", user="System", respond=False)
chat_interface.servable()

avatar = {user_proxy.name:"👨‍💼", engineer.name:"👩‍💻", scientist.name:"👩‍🔬", planner.name:"🗓", executor.name:"🛠", critic.name:'📝'}

def print_messages(recipient, messages, sender, config):

    chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
    print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")
    return False, None  # required to ensure the agent communication flow continues

user_proxy.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

engineer.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
scientist.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
planner.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

executor.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
critic.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 

