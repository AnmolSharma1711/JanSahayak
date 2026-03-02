"""
JanSahayak - Multi-Agent Government Intelligence System
Main entry point for the application
"""

import json
import os
from datetime import datetime
from graph.workflow import run_workflow
from agent_io.profiling_io import ProfilingIO
from agent_io.scheme_io import SchemeIO
from agent_io.exam_io import ExamIO
from agent_io.benefit_io import BenefitIO


def save_results(result: dict, output_dir: str = "outputs"):
    """
    Save final results to JSON file
    
    Args:
        result: Final output dictionary
        output_dir: Directory to save results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    return filename


def print_summary(result: dict):
    """
    Print a formatted summary of results
    
    Args:
        result: Final output dictionary
    """
    print("\n" + "="*70)
    print("📊 JANSAHAYAK - RESULTS SUMMARY")
    print("="*70)
    
    # Profile Summary
    profile = result.get("user_profile", {})
    print("\n👤 USER PROFILE:")
    print("-" * 70)
    if isinstance(profile, dict) and "error" not in profile:
        for key, value in profile.items():
            if key not in ["raw_profile", "user_input"]:
                print(f"  • {key.replace('_', ' ').title()}: {value}")
    else:
        print("  ⚠️ Profile extraction failed")
    
    # Scheme Recommendations
    print("\n🏛️ GOVERNMENT SCHEMES:")
    print("-" * 70)
    schemes = result.get("scheme_recommendations", "")
    if schemes and schemes != "Profile unavailable":
        print(schemes[:500] + "..." if len(schemes) > 500 else schemes)
    else:
        print("  ⚠️ No scheme recommendations available")
    
    # Exam Recommendations
    print("\n🎓 COMPETITIVE EXAMS:")
    print("-" * 70)
    exams = result.get("exam_recommendations", "")
    if exams and exams != "Profile unavailable":
        print(exams[:500] + "..." if len(exams) > 500 else exams)
    else:
        print("  ⚠️ No exam recommendations available")
    
    # Benefit Analysis
    print("\n💰 MISSED BENEFITS ANALYSIS:")
    print("-" * 70)
    benefits = result.get("missed_benefits_analysis", "")
    if benefits and benefits != "Insufficient data":
        print(benefits[:500] + "..." if len(benefits) > 500 else benefits)
    else:
        print("  ⚠️ Benefit analysis unavailable")
    
    # Errors
    errors = result.get("errors", [])
    if errors:
        print("\n⚠️ ERRORS ENCOUNTERED:")
        print("-" * 70)
        for error in errors:
            print(f"  • {error}")
    
    print("\n" + "="*70)


def interactive_mode():
    """
    Interactive mode for user input
    """
    print("\n" + "="*70)
    print("🙏 WELCOME TO JANSAHAYAK")
    print("Multi-Agent Government Intelligence System")
    print("="*70)
    print("\nPlease provide your details for personalized recommendations.")
    print("Include information about:")
    print("  • Age, Gender, State of residence")
    print("  • Income, Caste/Category")
    print("  • Education qualification")
    print("  • Employment status")
    print("  • Career interests (for exam recommendations)")
    print("\nEnter 'quit' to exit.")
    print("-" * 70)
    
    while True:
        print("\n📝 Enter your details (or 'quit' to exit):")
        
        # Get multi-line input
        lines = []
        while True:
            line = input()
            if line.lower() == 'quit':
                print("\n👋 Thank you for using JanSahayak!")
                return
            if line.lower() == 'done' or (line == '' and lines):
                break
            lines.append(line)
        
        user_input = '\n'.join(lines)
        
        if not user_input.strip():
            print("⚠️ No input provided. Please try again.")
            continue
        
        # Run workflow
        try:
            result = run_workflow(user_input)
            
            # Print summary
            print_summary(result)
            
            # Save results
            save_results(result)
            
            # Ask if user wants to continue
            print("\n" + "-" * 70)
            cont = input("Would you like another analysis? (yes/no): ")
            if cont.lower() not in ['yes', 'y']:
                print("\n👋 Thank you for using JanSahayak!")
                break
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with different input.")


def file_mode(input_file: str):
    """
    Process input from file
    
    Args:
        input_file: Path to input text file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            user_input = f.read()
        
        print(f"\n📄 Processing input from: {input_file}")
        
        result = run_workflow(user_input)
        print_summary(result)
        save_results(result)
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """
    Main entry point
    """
    import sys
    
    if len(sys.argv) > 1:
        # File mode
        input_file = sys.argv[1]
        file_mode(input_file)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
