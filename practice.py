from langchain.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from langchain.chat_models import init_chat_model


MAX_ITERATIONS=5
MODEL_PROVIDER="OLLAMA"
MODEL="QWEN"

@tool
def create_tool1(arg1:str)--> str:
    pass

@tool
def create_tool2(arg:str) -> float:
    pass


def agent_loop(query:str):
    print(query)
    tools=[create_tool1,create_tool1]
    tools_dict={t.name:t for t in tools}

    llm=init_chat_model(model_provider=MODEL_PROVIDER,model=MODEL)
    llm_with_tools=llm.bind_tools(tool)


    sys_msg=SystemMessage(content="""You are helping agent.""")
    hum_msg=HumanMessage(content=query)
    messages=[sys_msg,hum_msg]


    for i in range(1,MAX_ITERATIONS+1):
        ai_message=llm_with_tools.invoke(messages)
        tool_calls=ai_message.tool_calls

        if not tool_calls:
            return f"Final Answer:{ai_message.content}"
        
        tool_call=tool_calls[0]
        tool_name=tool_calls.get("name")
        tool_args=tool_calls.get("args")
        tool_id=tool_calls.get("id")

        tool_to_use=tools_dict.get(tool_name)
        observation=tool_to_use.invoke(tool_args)

        messages.append(ai_message)
        messages.append(ToolMessage(content=observation,tool_call_id=tool_id))





if __name__=='__main__':
    result=agent_loop("""What is the weather in japan?""")





