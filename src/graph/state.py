from typing import TypedDict, List, Dict, Any, Union

class TutorAgentState(TypedDict):
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

class ProgressAgentState(TypedDict):
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