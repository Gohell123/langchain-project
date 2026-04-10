from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage
from langsmith import traceable
MAX_ITERATIONS = 7
MODEL="qwen3:1.7b"
MODEL_PROVIDER="ollama"


#------Tools------

@tool
def get_product_price(product_name:str) ->float:
    """Get the price of a product."""
    print(f"Execuiting the tool get_product_price(product={product_name}) ")
    # Simulate getting the price from a database or an API
    price={"laptop":1299.99,"headphone":99.55,"keyboard":55.30}
    return price.get(product_name,0)


@tool
def get_product_discount(price:float,discount_tier:str)->float:
    """Apply a discount tier the price and return the final price
    Available Tiers:gold,silver,bronze"""
    print(f"Execuiting the tool get_product_discount(price={price}, discount_tier={discount_tier})")
    discount_percent={"bronze":5,"silver":10,"gold":15}
    discount=discount_percent.get(discount_tier,0)
    return round(price * (1-discount/100),2)



@traceable(name="Langchain Agent Loop")
def run_agent(query:str):
    tools=[get_product_price,get_product_discount]
    tools_dict={t.name: t for t in tools}
    

    llm=init_chat_model(f"{MODEL_PROVIDER}:{MODEL}",temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    print("Question",{query})
    print("="*60)

    sys_msg = SystemMessage(
    content="""
You are a helpful shopping assistant.

You MUST use tools to answer questions.

TOOLS:
- get_product_price(product_name: string) → returns price
- get_product_discount(price: float, discount_tier: string) → returns final price after discount

STRICT TOOL USAGE RULES:
1. If user asks about a product → ALWAYS call get_product_price first
2. After getting price:
   - If tier is provided → call get_product_discount
   - If tier is missing → ask user for tier
3. NEVER skip tool calls
4. NEVER say "product not available" unless tool returns no result
5. ALWAYS pass correct arguments:
   - product_name must be extracted from user query
   - discount_tier must be one of: bronze, silver, gold (lowercase)

DO NOT answer directly without using tools.

Follow this sequence strictly.
"""
)

    hum_msg=HumanMessage(content=query)

    messages=[sys_msg,hum_msg]


    for i in range(1,MAX_ITERATIONS+1):
        print(f"Iteration:{i}")
        ai_message=llm_with_tools.invoke(messages) 
        
        #ai message will either have tool call or the final content
        tool_calls=ai_message.tool_calls
        print("Tool Calls",tool_calls)


        if not tool_calls:
            print(f"Final Answer:{ai_message.content}")
            return ai_message.content


        # Process only the first tool call
        tool_call=tool_calls[0]
        tool_name=tool_call.get("name")
        tool_args=tool_call.get("args")
        tool_id=tool_call.get("id")


        print(f"Tool Selected {tool_name} with arguments {tool_args }")

        tool_to_use=tools_dict.get(tool_name)
        print("tool_to_use",tool_to_use)

        if tool_to_use is None:
            raise ValueError("Tool name not found")
        observation=tool_to_use.invoke(tool_args)

        print(f"Tool Result {observation}")

        messages.append(ai_message)
        messages.append(ToolMessage(content=str(observation),tool_call_id=tool_id))
    print("Error:Max Iterations reached")
    return None


if __name__=='__main__':
    print("Hello Langchain Agent (.bind tools)")
    result=run_agent("What is the price of a laptop after applying gold discount?")




    
