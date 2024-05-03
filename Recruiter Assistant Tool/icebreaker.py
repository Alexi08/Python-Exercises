import os
from typing import Tuple

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from agents.lindkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import PersonIntel, person_intel_parser


def ice_break(name: str) -> Tuple[PersonIntel, str]:

    linkedin_profile_url = linkedin_lookup_agent(name=name)

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url["output"]
    )

    prompt_data = {"information": linkedin_data}

    summary_template = """
    Given the LinkedIn {information} about a person, I want you too create:
    1. A short summary
    2. Two interesting facts about them
    \n{format_instructions}

    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    prompt_text = summary_prompt_template

    """Temperature decides how creative langauge model is. Higher is more creative"""
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.invoke({"information": linkedin_data})
    return person_intel_parser.parse(result["text"]), linkedin_data.get(
        "profile_pic_url"
    )


if __name__ == "__main__":
    load_dotenv()
    print("Hello Langchain")
    result = ice_break(name="Harrison Chase")
    print(result)
