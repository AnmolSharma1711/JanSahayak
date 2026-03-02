"""
Benefit Agent I/O Handler
Manages input/output for missed benefits calculator agent
"""

import json
import os
from datetime import datetime


class BenefitIO:
    """Handles input/output operations for benefit calculator agent"""
    
    def __init__(self, input_file: str = "agent_io/benefit_input.json", 
                 output_file: str = "agent_io/benefit_output.json"):
        self.input_file = input_file
        self.output_file = output_file
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create agent_io directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.input_file), exist_ok=True)
    
    def read_input(self) -> dict:
        """
        Read benefit calculator input from file
        
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
    
    def write_input(self, profile_data: dict, scheme_recommendations: str, years: int = 5):
        """
        Write input for benefit calculator
        
        Args:
            profile_data: User profile dictionary
            scheme_recommendations: Eligible schemes text
            years: Number of years to calculate (default: 5)
        """
        input_data = {
            "timestamp": datetime.now().isoformat(),
            "profile": profile_data,
            "scheme_recommendations": scheme_recommendations,
            "calculation_years": years,
            "agent": "benefit_calculator"
        }
        
        with open(self.input_file, 'w', encoding='utf-8') as f:
            json.dump(input_data, f, indent=2, ensure_ascii=False)
    
    def write_output(self, calculation: dict, metadata: dict = None):
        """
        Write benefit calculation to output file
        
        Args:
            calculation: Missed benefits calculation
            metadata: Optional metadata about calculation
        """
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "calculation": calculation,
            "metadata": metadata or {},
            "agent": "benefit_calculator"
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    def read_output(self) -> dict:
        """
        Read previous benefit calculations
        
        Returns:
            Previous calculations dictionary
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
    # Test BenefitIO
    io = BenefitIO()
    
    # Sample input
    profile = {
        "age": 25,
        "income": "300000"
    }
    
    schemes = "PM Kisan: ₹6000/year"
    
    io.write_input(profile, schemes, years=5)
    print("Input written successfully")
    
    # Sample output
    calculation = {
        "total_missed": "₹30,000",
        "breakdown": {"2022": "₹6000", "2023": "₹6000"}
    }
    
    io.write_output(calculation)
    print("Output written successfully")
