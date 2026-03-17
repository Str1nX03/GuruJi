import sys
from langgraph.graph import StateGraph, START, END
from src.logger import logging
from src.exception import CustomException
from src.utils import get_llm
from src.prompts.planning_agent_prompt import PLANNING_SYSTEM_PROMPT
from src.tools import fetch_fact
from typing import TypedDict

class PlanningAgentState(TypedDict):
    """
    Local state for the Planning Agent.
    Responsible for generating and structuring the curriculum.
    
    Attributes:
        syllabus (List[str]): Major units or overarching themes that need to be covered.
        topics (List[List[str]]): Nested lists containing specific topics broken down for each unit.
        planning (Dict[str, List[str]]): The final, structured curriculum mapping units (keys) to their subtopics (values).
        standard (int): The academic class, grade, or standard the user is currently in.
        subject (str): The specific subject being taught (e.g., to differentiate 'data collection' in Economics vs. Data Engineering).
        major_topic (str): The primary topic area assigned to this agent by the Supervisor.
    """
    generic_data: list[str]              # General Data about the subject with respect to the topic and standard of the user
    topics: list[str]                    # Nested lists containing topics for each unit
    standard: int                        # Class/standard the user is currently in
    subject: str                         # The subject being taught (e.g., economics vs data engineering)
    major_topic: str                     # Passed by the user

class PlanningAgent:
    def __init__(self):

        self.llm = get_llm(temp=0.1)
        self.graph = self._build_graph()

    def _build_graph(self):

        try:

            graph = StateGraph(PlanningAgentState)

            graph.add_node("fetch_data", self._fetch_data)
            graph.add_node("plan_topics", self._plan_topics)

            graph.add_edge(START, "fetch_data")
            graph.add_edge("fetch_data", "plan_topics")
            graph.add_edge("plan_topics", END)

            return graph.compile()

        except Exception as e:
            
            raise CustomException(e, sys)

    def _fetch_data(self, state: PlanningAgentState) -> dict:

        try:

            logging.info(f"Planner searching DuckDuckGo")

            standard = state["standard"]
            subject = state["subject"]
            major_topic = state["major_topic"]

            query = f"Syllabus for {subject} for {major_topic} in class {standard} in 2026"
            
            generic_data = fetch_fact(query)

            logging.info(f"Planner found {len(generic_data)} data on the syllabus")
            
            return {"generic_data": generic_data}
            
        except Exception as e:
            
            raise CustomException(e, sys)

    def _plan_topics(self, state: PlanningAgentState) -> dict:
        try:
            
            logging.info("Planning a curriculum")

            generic_data = state["generic_data"]
            standard = state["standard"]
            subject = state["subject"]
            major_topic = state["major_topic"]

            topic_plan_prompt = PLANNING_SYSTEM_PROMPT.format(
                subject=subject,
                standard=standard,
                major_topic=major_topic,
                generic_data=generic_data
            )

            topics = self.llm.invoke(topic_plan_prompt).content
            topics = list(topics.split("\n"))

            un_char = ["", " ", "  ", "   ", "    "]
            for res in topics:
                while res in un_char:
                    topics.remove(res)
            
            logging.info("Planning curriculum completed")
            
            return {"topics": topics}
        
        except Exception as e:

            raise CustomException(e, sys)

    def run(self, subject: str, major_topic: str, standard: int) -> dict:

        try:

            logging.info("PLANNING AGENT ACTIVATED")
            
            initial_state = {
                "subject": subject,
                "standard": standard,
                "major_topic": major_topic
            }
            
            final_state = self.graph.invoke(initial_state)

            logging.info("PLANNING AGENT DEACTIVATED")
            
            return final_state
            
        except Exception as e:
            
            raise CustomException(e, sys)