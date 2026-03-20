from src.logger import logging
from src.exception import CustomException
from src.utils import get_llm
from typing import TypedDict
import sys
from langgraph.graph import StateGraph, START, END


class TutorAgentState(TypedDict):
    
    topics: list[str]           # list of topics
    lessons: list[list[str]]    # list of lists of lessons
    standard: int               # Standard of the user
    subject: str                # Subject of the user
    student_instructions: str   # Instructions for the student


class TutorAgent:

    def __init__(self):
        self.llm = get_llm(temp=0.1)
        self.graph = self._build_graph()

    def _build_graph(self):

        try:

            graph = StateGraph(TutorAgentState)

            return graph.compile()

        except Exception as e:

            raise CustomException(e, sys)
        
    def _generate_lessons(self, state: TutorAgentState):

        try:

            pass

        except Exception as e:

            raise CustomException(e, sys)
        
    def _generate_instructions(self, state: TutorAgentState):

        try:

            pass

        except Exception as e:

            raise CustomException(e, sys)
        
    def run(self, subject: str, standard: int, topics: list[str]):

        try:

            logging.info("TUTOR AGENT ACTIVATED")

            initial_state = {
                "topics": topics,
                "standard": standard,
                "subject": subject
            }

            final_state = self.graph.invoke(initial_state)

            logging.info("TUTOR AGENT DEACTIVATED")

            return final_state

        except Exception as e:

            raise CustomException(e, sys)