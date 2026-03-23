from src.agents.tutor_agent import TutorAgent
import os
from dotenv import load_dotenv

load_dotenv()

import json

def test_tutor_agent():
    agent = TutorAgent()
    subject = "Science"
    standard = 3
    topics = ["Photosynthesis"]
    
    print(f"Running TutorAgent for {subject}, Standard {standard}, Topics: {topics}...")
    result = agent.run(subject=subject, standard=standard, topics=topics)
    
    with open("g:/Dravin/Projects/GuruJi/tests/test_results.json", "w") as f:
        json.dump(result, f, indent=4)
    
    print("\nResults saved to tests/test_results.json")

if __name__ == "__main__":
    test_tutor_agent()
