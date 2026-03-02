"""
Profiling Agent I/O Handler
Manages input/output for user profiling agent
"""

import json
import os
from datetime import datetime


class ProfilingIO:
    """Handles input/output operations for profiling agent"""
    
    def __init__(self, input_file: str = "agent_io/profiling_input.json", 
                 output_file: str = "agent_io/profiling_output.json"):
        self.input_file = input_file
        self.output_file = output_file
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create agent_io directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.input_file), exist_ok=True)
    
    def read_input(self) -> dict:
        """
        Read profiling agent input from file
        
        Returns:
            Raw user input dictionary
        """
        try:
            if os.path.exists(self.input_file):
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "Input file not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def write_input(self, user_input: str, documents: list = None):
        """
        Write raw user input for profiling
        
        Args:
            user_input: Raw text input from user
            documents: Optional list of uploaded documents
        """
        input_data = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "documents": documents or [],
            "agent": "user_profiling"
        }
        
        with open(self.input_file, 'w', encoding='utf-8') as f:
            json.dump(input_data, f, indent=2, ensure_ascii=False)
    
    def write_output(self, profile_data: dict, confidence: dict = None):
        """
        Write extracted profile to output file
        
        Args:
            profile_data: Structured profile data
            confidence: Optional confidence scores for extracted fields
        """
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "profile": profile_data,
            "confidence": confidence or {},
            "agent": "user_profiling"
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    def read_output(self) -> dict:
        """
        Read extracted profile
        
        Returns:
            Structured profile dictionary
        """
        try:
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "Output file not found"}
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    # Test ProfilingIO
    io = ProfilingIO()
    
    # Sample input
    user_text = "I am 25 years old from Maharashtra, OBC category, income 3 lakh."
    io.write_input(user_text, documents=["resume.pdf"])
    print("Input written successfully")
    
    # Sample output
    profile = {
        "age": 25,
        "state": "Maharashtra",
        "caste": "OBC",
        "income": "300000"
    }
    
    io.write_output(profile, confidence={"age": 1.0, "state": 1.0})
    print("Output written successfully")
