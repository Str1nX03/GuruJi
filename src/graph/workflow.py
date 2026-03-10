import sys
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from src.logger import logging
from src.exception import CustomException
from src.graph.state import GlobalAgentState

class Workflow:
    """
    The main Multi-Agent Workflow class.
    Encapsulates the routing logic, agent nodes, and graph compilation.
    """
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self):
        """
        Builds and compiles the LangGraph Multi-Agent StateMachine.
        """
        try:

            logging.info("Compiling the LangGraph StateMachine...")

            graph = StateGraph(GlobalAgentState)

            graph.add_node("supervisor", self._supervisor_node)
            graph.add_node("planner", self._planning_node)
            graph.add_node("tutor", self._tutor_node)
            graph.add_node("progress", self._progress_node)

            graph.add_edge(START, "supervisor")
            graph.add_conditional_edges(
                "supervisor",
                self.route_from_supervisor,
                {
                    "planner": "planner",
                    "progress": "progress",
                    "tutor": "tutor",
                    END: END
                }
            )

            graph.add_edge("planner", END)
            graph.add_edge("tutor", END)
            graph.add_edge("progress", END)

            logging.info("Successfully compiled the LangGraph Workflow.")

            return graph.compile()

        except Exception as e:
            
            raise CustomException(e, sys)
    
    def _supervisor_node(self, state: GlobalAgentState) -> dict:

        logging.info("--- SUPERVISOR NODE (STUB) ---")

        return {}

    def _planning_node(self, state: GlobalAgentState) -> dict:

        logging.info("--- PLANNING NODE (STUB) ---")

        return {}

    def _tutor_node(self, state: GlobalAgentState) -> dict:

        logging.info("--- TUTOR NODE (STUB) ---")

        return {}

    def _progress_node(self, state: GlobalAgentState) -> dict:

        logging.info("--- PROGRESS NODE (STUB) ---")

        return {}
    
    def route_from_supervisor(self, state: GlobalAgentState) -> str:
        """
        Reads the 'next_node' from the state blackboard and tells LangGraph where to go.
        """
        next_node = state.get("next_node", "tutor_agent")
        
        if next_node == "planning_agent":
            return "planning_node"
        elif next_node == "progress_agent":
            return "progress_node"
        elif next_node == "FINISH":
            return END
        else:
            return "tutor_node"
    
    def run_workflow(self, user_message: str) -> dict:
        """
        Initiates the workflow by passing the user's message into the graph.
        """
        try:
            logging.info(f"Running workflow for user message: '{user_message}'")
            
            initial_state = {
                "messages": [HumanMessage(content=user_message)]
            }
            
            final_state = self.graph.invoke(initial_state)
            
            logging.info("Workflow execution completed successfully.")

            return final_state
            
        except Exception as e:

            raise CustomException(e, sys)