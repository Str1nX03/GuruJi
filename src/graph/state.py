import operator
from typing import TypedDict, Annotated, List, Dict, Any, Union
from langchain_core.messages import BaseMessage

class GlobalAgentState(TypedDict):
    """
    The main Graph State and architectural 'Blackboard' of the Multi-Agent System.
    
    This state is passed continuously through the LangGraph nodes. It serves two main purposes:
    1. Maintaining the persistent conversation memory.
    2. Acting as a shared information bus where agents can write variables that downstream agents need to read.
    
    Attributes:
        messages (Annotated[List[BaseMessage], operator.add]): 
            The core conversation memory. 'operator.add' ensures new messages are appended 
            rather than overwriting the entire history.
        next_node (str): 
            The routing directive. Updated primarily by the Supervisor to dictate which agent node executes next.
            
        subject (str): Shared bus variable indicating the current subject.
        standard (int): Shared bus variable indicating the student's academic level.
        major_topic (str): Shared bus variable indicating the overarching topic focus.
        planning (Dict[str, List[str]]): Shared bus variable containing the generated curriculum.
        lessons (Dict[str, str]): Shared bus variable containing generated lesson content.
    """
    messages: Annotated[List[BaseMessage], operator.add]
    next_node: str
    
    subject: str
    standard: int
    major_topic: str
    planning: Dict[str, List[str]]
    lessons: Dict[str, str]

class SupervisorAgentState(TypedDict):
    """
    Local state for the Supervisor/Routing Agent.
    Responsible for maintaining the system's capabilities and routing user requests.
    
    Attributes:
        subjects (List[str]): A list of all available subjects that the AI Tutor is capable of teaching.
        major_topics (Dict[str, List[str]]): A mapping of available subjects (keys) to their corresponding major topics (values).
            Example: {'Mathematics': ['Calculus', 'Linear Algebra'], 'Physics': ['Kinematics', 'Thermodynamics']}
    """
    subjects: List[str]                  # List of subjects that can be taught by the agent
    major_topics: Dict[str, List[str]]   # Subjects (keys) -> Corresponding major topics (values)

class PlanningAgentState(TypedDict, total=False):
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
    syllabus: List[str]                  # Major units that need to be covered
    topics: List[List[str]]              # Nested lists containing topics for each unit
    planning: Dict[str, List[str]]       # Final planning: units (keys) -> subtopics (values)
    standard: int                        # Class/standard the user is currently in
    subject: str                         # The subject being taught (e.g., economics vs data engineering)
    major_topic: str                     # Passed by the supervisor agent

class TutorAgentState(TypedDict, total=False):
    """
    Local state for the core Tutor Agent.
    Responsible for Socratic teaching and delivering the actual lessons.
    
    Attributes:
        planning (Dict[str, List[str]]): The structured curriculum of units and subtopics, provided by the Planning Agent.
        lessons (Dict[str, str]): A mapping of specific subtopics (keys) to their generated, comprehensive lessons (values).
        standard (int): The academic class/standard, provided by the Planning Agent.
        subject (str): The current subject context, provided by the Planning Agent.
    """
    planning: Dict[str, List[str]]       # Final planning of units -> subtopics (Passed by Planning Agent)
    lessons: Dict[str, str]              # Subtopics (keys) -> comprehensive lessons (values)
    standard: int                        # Passed by Planning Agent
    subject: str                         # Passed by Planning Agent     

class ProgressAgentState(TypedDict, total=False):
    """
    Local state for the Progress & Evaluation Agent.
    Responsible for tracking student performance, grading, and identifying weaknesses.
    
    Attributes:
        tests (Dict[str, Dict[int, Union[float, int]]]): 
            A nested dictionary mapping a subject (key) to another dictionary, 
            which maps the student's grade/standard to their final evaluation score.
        remarks (Dict[str, List[Any]]): 
            Evaluation remarks stored by test ID. The value is a list where the 1st item 
            contains identified problems/weaknesses, and the 2nd item is the final score.
    """
    tests: Dict[str, Dict[int, Union[float, int]]]      # subject -> {class/standard: final_score} 
    remarks: Dict[str, List[Any]]                       # test_id -> [problems_identified, final_score, pass/fail]