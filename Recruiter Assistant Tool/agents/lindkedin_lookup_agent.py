from typing import Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain import hub, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool

from tools.tools import get_profile_url


def lookup(name: str) -> dict[str, Any]:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """
    Given the full name and data: {name_of_person}, I want you to get me a link to their Linkedin profile page.
    Your answer should contain only a URL
    """

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="Useful for when you need to get the Linkedin page URL ",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_excecutor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    result = agent_excecutor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linked_profile_url = result
    return linked_profile_url
