"""
Exam Agent I/O Handler
Manages input/output for exam recommendation agent
"""

import json
import os
from datetime import datetime


class ExamIO:
    """Handles input/output operations for exam agent"""
    
    def __init__(self, input_file: str = "agent_io/exam_input.json", 
                 output_file: str = "agent_io/exam_output.json"):
        self.input_file = input_file
        self.output_file = output_file
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create agent_io directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.input_file), exist_ok=True)
    
    def read_input(self) -> dict:
        """
        Read exam agent input from file
        
        Returns:
            Input configuration dictionary
        """
        try:
            if os.path.exists(self.input_file):
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "Input file not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def write_input(self, profile_data: dict, preferences: dict = None):
        """
        Write input for exam agent
        
        Args:
            profile_data: Student profile dictionary
            preferences: Optional student preferences
        """
        input_data = {
            "timestamp": datetime.now().isoformat(),
            "profile": profile_data,
            "preferences": preferences or {},
            "agent": "exam_recommendation"
        }
        
        with open(self.input_file, 'w', encoding='utf-8') as f:
            json.dump(input_data, f, indent=2, ensure_ascii=False)
    
    def write_output(self, recommendations: dict, metadata: dict = None):
        """
        Write exam recommendations to output file
        
        Args:
            recommendations: Exam recommendations from agent
            metadata: Optional metadata about the recommendation process
        """
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "metadata": metadata or {},
            "agent": "exam_recommendation"
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    def read_output(self) -> dict:
        """
        Read previous exam recommendations
        
        Returns:
            Previous recommendations dictionary
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
    # Test ExamIO
    io = ExamIO()
    
    # Sample input
    profile = {
        "age": 25,
        "education": "Bachelor's in Engineering",
        "interests": "Technical jobs"
    }
    
    io.write_input(profile, {"exam_type": "government"})
    print("Input written successfully")
    
    # Sample output
    recommendations = {
        "exams": [
            {"name": "SSC CGL", "eligibility": "Graduate"}
        ]
    }
    
    io.write_output(recommendations, {"sources": 5})
    print("Output written successfully")
