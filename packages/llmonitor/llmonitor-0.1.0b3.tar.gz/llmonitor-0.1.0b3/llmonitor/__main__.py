from . import chain, LLMonitorCallbackHandler, identify, tags
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI

llm = OpenAI(temperature=0, callbacks=[LLMonitorCallbackHandler()])


@chain("Oh yeah!", user_id="1234", tags=["tag1", "tag2"])
def main(input):
    # llm("What is the square root of 4?")
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    handler = LLMonitorCallbackHandler()

    agent.run(
        "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?",
        callbacks=[handler],
        metadata={
            "agentName": "GirlfriendAge",  # you can assign a custom agent name in the metadata
        },
    )
    return "Fuck yeah"


if __name__ == "__main__":
    main("Yeah baby!")
    llm("Hello world")
