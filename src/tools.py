import sys
from src.logger import logging
from src.exception import CustomException
from langchain_core.tools import tool
import sympy
from ddgs import DDGS
import io
from contextlib import redirect_stdout

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

        error = CustomException(e, sys)
        logging.error(error)

        return f"Error evaluating math: {str(e)}. Please ensure standard mathematical syntax."

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

        f = io.StringIO()
        with redirect_stdout(f):
            exec(code)

        code_result = f.getvalue()

        if not code_result.strip():
            return "Code executed successfully but returned no output. Did you forget to use print()?"

        logging.info("Successfully executed the python code.")

        return code_result

    except Exception as e:

        error = CustomException(e, sys)
        logging.error(error)

        return f"Python Error: {str(e)}. Please fix your code and try again."

@tool
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

        responses = DDGS().text(query = query, max_results=3)
        
        facts = []
        for response in responses:

            facts.append(response["body"])

        logging.info("Successfully fetched the fact.")

        return "\n".join(facts)

    except Exception as e:

        error = CustomException(e, sys)
        logging.error(error)

        return f"Search Error: {str(e)}. Could not fetch facts at this time."