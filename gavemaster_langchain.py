import openai
import os   
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from myprompts import interpret_prompt, response_prompt
from langchain import PromptTemplate
from langchain.chains import SimpleSequentialChain

load_dotenv(find_dotenv())


openai.api_key = os.getenv('OPENAI_API_KEY')





def gavebot_simple_sequential(tempature):
    llm = OpenAI(temperature=1.2)

    prompt_interpret = PromptTemplate.from_template(template=interpret_prompt)
    chain_interpret = LLMChain(llm=llm, prompt=prompt_interpret, output_key="interpretation")


     
    prompt_response = PromptTemplate.from_template(input_var="interpretation", template=response_prompt)
    chain_response = LLMChain(llm=llm, prompt=prompt_response)




    overall_chain = SimpleSequentialChain(chains=[chain_interpret, chain_response], verbose=True)

    return overall_chain



async def run_chain(chain, input):
    response = chain.run(input=input)
    return response
            
    


