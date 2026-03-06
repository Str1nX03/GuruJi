from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import sys
from src.logger import logging
from src.exception import CustomException
load_dotenv()

def get_llm(api: str | None = os.getenv("GROQ_API_KEY"), model: str | None = "llama-3.3-70b-versatile", temp: float | None = 0.1) -> ChatGroq:
    """
    This function will return the Groq LLM .
    Args:
        api: API Key for the Groq LLM, it extracts the key by default from your `.env` file.
        model: Groq LLM's model name, by default it is set to `llama-3.3-70b-versatile`
        temp: Groq LLM's temperature will determine the randomness of the output, by default it is set to `0.1`.
    Returns:
        LLM: Groq LLM object
    """
    try:

        logging.info("Requesting the LLM object.")

        llm = ChatGroq(
            api_key = api,
            model_name = model,
            temperature = temp)

        logging.info("Successfully got the LLM object.")

        return llm

    except Exception as e:
        raise CustomException(e, sys)