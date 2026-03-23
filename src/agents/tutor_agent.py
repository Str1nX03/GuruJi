from src.logger import logging
from src.exception import CustomException
from src.utils import get_llm
from typing import TypedDict
import sys
from langgraph.graph import StateGraph, START, END
from src.prompts.tutor_agent_prompt import (
    FOUNDATIONAL_LESSON_PROMPT, 
    INTERMEDIATE_LESSON_PROMPT, 
    ADVANCED_LESSON_PROMPT, 
    STUDENT_INSTRUCTIONS_PROMPT
)


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
            
            graph.add_node("generate_lessons", self._generate_lessons)
            graph.add_node("generate_instructions", self._generate_instructions)

            graph.add_edge(START, "generate_lessons")
            graph.add_edge("generate_lessons", "generate_instructions")
            graph.add_edge("generate_instructions", END)

            return graph.compile()

        except Exception as e:

            raise CustomException(e, sys)
        
    def _generate_lessons(self, state: TutorAgentState) -> dict:

        try:

            subject = state["subject"]
            standard = state["standard"]
            topics = state["topics"]
            lessons = []

            if standard <= 4:
                prompt_template = FOUNDATIONAL_LESSON_PROMPT
            elif standard <= 9:
                prompt_template = INTERMEDIATE_LESSON_PROMPT
            else:
                prompt_template = ADVANCED_LESSON_PROMPT
            
            for topic in topics:
                
                prompt = prompt_template.format(
                    subject=subject, 
                    standard=standard, 
                    topic=topic
                )
                response = self.llm.invoke(prompt)
                lessons.append([topic, response.content])
            
            return {"lessons": lessons}

        except Exception as e:

            raise CustomException(e, sys)
        
    def _generate_instructions(self, state: TutorAgentState):

        try:

            subject = state["subject"]
            standard = state["standard"]
            
            prompt = STUDENT_INSTRUCTIONS_PROMPT.format(subject=subject, standard=standard)
            response = self.llm.invoke(prompt)
            
            return {"student_instructions": response.content.strip()}

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