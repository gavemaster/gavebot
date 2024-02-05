from gavemaster_py_api_functions import get_best_performing_stock, get_price_change_percentage, get_sport_events_by_date, get_stock_price
import openai
import os   
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from myprompts import interpret_prompt, response_prompt, agent_wikipedia_prompt
from langchain import PromptTemplate
from langchain.chains import SimpleSequentialChain
from typing import Any, List
from pydantic import BaseModel, Field
from langchain.agents import load_tools
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

load_dotenv(find_dotenv())


openai.api_key = os.getenv('OPENAI_API_KEY')



def gavebot_stocks_and_sports(tempature):
    
    class StockPriceCheckInput(BaseModel):
        stockTicker: str = Field(..., description="Stock ticker to check price for")


    class StockPriceTool(BaseTool):
        name = "get_stock_price"
        description = "Useful for when you need to find out the price of a stock. You shoud input the stock ticker used "

        def _run(self, stockTicker: str):
            return get_stock_price(stockTicker)
        def _arun(self, stockTicker: str):
            raise NotImplementedError("This tool does not support async")

        args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput


    class StockChangePercentageCheckInput(BaseModel):
        """input for Stock ticker check. for percentage check"""
        stockTicker: str = Field(..., description="Stock ticker to check price for")
        days_ago: int = Field(..., description="Number of days ago to check price for")


    class StockPercentageChangeTool(BaseTool):
        name = "get_price_change_percentage"
        description = "Useful when you need to find the percentage change of a stock over a period of time"

        def _run(self, stockTicker: str, days_ago: int):
            return get_price_change_percentage(stockTicker, days_ago)
        def _arun(self, stockTicker: str, days_ago: int):
            raise NotImplementedError("This tool does not support async")

        args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput


    class StockBestPerformingInput(BaseModel):
        """input for Stock ticker check. for percentage check"""
        stockTickers: List[str] = Field(..., description="Stock tickers to check price for")
        days_ago: int = Field(..., description="Number of days ago to check price for")

    class StockGetBestPerformingTool(BaseTool):
        name = "get_best_performing_stock"
        description = "Useful when you need to find the best performing stock over a period of time"

        def _run(self, stockTickers: List[str], days_ago: int):
            return get_best_performing_stock(stockTickers, days_ago)
        def _arun(self, stockTickers: List[str], days_ago: int):
            raise NotImplementedError("This tool does not support async")

        args_schema: Optional[Type[BaseModel]] = StockBestPerformingInput

    class SportEventsByDateCheckInput(BaseModel):
        """input for get sport events by date check"""
        sport: str = Field(..., description="Sport to check events for.... given a league sport should be the coressponding sport")
        league: str = Field(..., description="League to check events for.... given the sport league should be the most common league for the sport in the united states")
        days: int = Field(..., description="representing the number of days from today to check events for. negative numbers are in the past, positive numbers are in the future")
        teams: List[str] = Field(..., description="List of teams to filter events by. If none are provided all events will be returned and this list should be empty the team names should be written in there full display name ex. 'Los Angeles Lakers'")
    class SportEventsByDateTool(BaseTool):
        name = "get_sports_events_by_date"
        description = "Useful when you need information on the games for a particular sport League in the undited states ex. leagyes = mlb,nfl,nba,nhl,mls,wnba, mens-college-basketball, womens-college-basketball, mens-college-football"

        def _run(self, sport: str, league: str, days: int, teams: List[str]):
            return get_sport_events_by_date(sport, league, days, teams)
        def _arun(self, sport: str, league: str, days: int, teams: List[str]):
            raise NotImplementedError("This tool does not support async")

        args_schema: Optional[Type[BaseModel]] = SportEventsByDateCheckInput

    tools = [StockPriceTool(), StockPercentageChangeTool(), StockGetBestPerformingTool(), SportEventsByDateTool()]

    llm = ChatOpenAI(temperature=tempature, model="gpt-3.5-turbo-0613")
    open_ai_agent = initialize_agent(tools,
                                    llm,
                                    agent=AgentType.OPENAI_FUNCTIONS,
                                    verbose=True)
        
    return open_ai_agent



def gavebot_simple_sequential(tempature):
    llm = OpenAI(temperature=1.2)

    prompt_interpret = PromptTemplate.from_template(template=interpret_prompt)
    chain_interpret = LLMChain(llm=llm, prompt=prompt_interpret, output_key="interpretation")


     
    prompt_response = PromptTemplate.from_template(input_var="interpretation", template=response_prompt)
    chain_response = LLMChain(llm=llm, prompt=prompt_response)




    overall_chain = SimpleSequentialChain(chains=[chain_interpret, chain_response], verbose=True)

    return overall_chain


def wikiBacked_gavebot(tempature):
    llm = OpenAI(temperature=tempature)
    tools =  load_tools(["wikipedia","llm-math"],
    llm=llm)
    agent=initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    agent.agent.llm_chain.prompt.template = agent_wikipedia_prompt

    return agent

async def run_chain(chain, input, option):
    if option == 'wiki':
        response = chain.run(input=input)
        return response
    else:
        response = chain.run(input=input)
        return response
            
    

async def run_agent(agent, input):
    response = agent(input)
    return response['output']




