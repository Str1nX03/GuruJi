import sys
from src.logger import logging
from src.exception import CustomException
from langchain_core.tools import tool
import sympy
from ddgs import DDGS

@tool
def evaluate_math(expression: str) -> str:
    """
    Evaluates a given math expression and returns the mathematical result as a string.
    Args:
        expression (str): The math expression to be evaluated. Example: `3 * 5` is correct but not `3 x 5`.
    Returns:
        str: The result of the math expression as a string.
    """
    try:

        logging.info("Evaluating the math expression.")

        expr = sympy.sympify(expression)
        result = str(expr.evalf())

        logging.info("Successfully evaluated the math expression.")

        return result

    except Exception as e:

        raise CustomException(e, sys)

@tool
def python_executor(code: str) -> str:
    """
    Executes a given python code and returns the python code result as a string.
    Args:
        code (str): The python code to be executed. Example: `print("Hello World")` is correct.
    Returns:
        str: The result of the python code as a string.
    """
    try:

        logging.info("Executing the python code.")

        code_result = exec(code)

        logging.info("Successfully executed the python code.")

        return code_result

    except Exception as e:

        raise CustomException(e, sys)

def fetch_fact(query: str) -> str:
    """
    Fetches facts from the internet using the DDGS API.
    Args:
        query: The query to fetch facts from.
    Returns:
        str: A list of facts as strings.
    """
    try:

        logging.info("Fetching the fact.")

        responses = DDGS().text(query = query, max_results=4)
        
        facts = []
        for response in responses:

            facts.append(response["body"])

        logging.info("Successfully fetched the fact.")

        return facts

    except Exception as e:

        raise CustomException(e, sys)