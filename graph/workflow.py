"""
LangGraph Workflow
Orchestrates multi-agent system using LangGraph
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator


class AgentState(TypedDict):
    """
    State object that gets passed between agents
    Contains all intermediate and final results
    """
    # Input
    user_input: str
    user_interests: list  # ['schemes', 'exams']
    
    # Profiling Agent Output
    profile: dict
    
    # Scheme Agent Output
    scheme_recommendations: str
    
    # Exam Agent Output
    exam_recommendations: str
    
    # Benefit Agent Output
    missed_benefits: str
    
    # Final Output
    final_output: dict
    
    # Error tracking
    errors: Annotated[list, operator.add]


def profiling_node(state: AgentState) -> dict:
    """
    Node: User Profiling Agent
    Extracts structured profile from user input
    """
    from agents.profiling_agent import run_profiling_agent
    
    try:
        # Check if we already have a structured profile (from form)
        existing_profile = state.get("profile", {})
        
        # If we have useful profile data already, skip LLM profiling
        useful_fields = [k for k in existing_profile.keys() if k not in ['raw_profile', 'user_input', 'error', 'note'] and existing_profile[k] not in ['Not Provided', 'N/A', '', None]]
        
        if len(useful_fields) >= 3:
            print("\n✅ Using pre-extracted profile data (skipping LLM profiling)")
            return {"profile": existing_profile}
        
        print("\n🔍 Running Profiling Agent...")
        user_input = state.get("user_input", "")
        profile = run_profiling_agent(user_input)
        
        # Merge with existing profile if available
        if existing_profile:
            profile = {**profile, **existing_profile}  # existing_profile takes precedence
        
        if "error" in profile and len(profile) <= 2:  # Only error and maybe user_input
            print("❌ Profile extraction failed, using fallback data")
            return {
                "profile": existing_profile if existing_profile else {},
                "errors": ["Profiling failed: " + profile.get("error", "Unknown error")]
            }
        
        print("✅ Profile extracted successfully")
        return {"profile": profile}
        
    except Exception as e:
        print(f"❌ Profiling Agent Error: {str(e)}")
        existing_profile = state.get("profile", {})
        return {
            "profile": existing_profile if existing_profile else {},
            "errors": [f"Profiling: {str(e)}"]
        }


def scheme_node(state: AgentState) -> dict:
    """
    Node: Scheme Recommendation Agent
    Recommends government schemes based on profile
    """
    from agents.scheme_agent import run_scheme_agent
    
    try:
        # Check if user wants scheme recommendations
        interests = state.get("user_interests", ["schemes", "exams"])
        if "schemes" not in interests:
            print("\n⏭️ Skipping Scheme Agent (not requested)")
            return {"scheme_recommendations": "Not requested by user"}
        
        print("\n🏛️ Running Scheme Recommendation Agent...")
        profile = state.get("profile", {})
        
        # Check if profile has useful data (at least 2 fields with actual values)
        useful_fields = [k for k in profile.keys() 
                        if k not in ['raw_profile', 'user_input', 'error', 'note'] 
                        and profile[k] not in ['Not Provided', 'N/A', '', None]]
        
        if not profile or len(useful_fields) < 2:
            print(f"⚠️ Limited profile data ({len(useful_fields)} fields), will rely more on web search")
        else:
            print(f"✅ Profile has {len(useful_fields)} useful fields")
        
        result = run_scheme_agent(profile, use_web_search=True)
        print("✅ Scheme recommendations generated")
        return {"scheme_recommendations": result.get("recommendations", "")}
        
    except Exception as e:
        print(f"❌ Scheme Agent Error: {str(e)}")
        return {
            "scheme_recommendations": f"Error generating recommendations: {str(e)}",
            "errors": [f"Scheme: {str(e)}"]
        }


def exam_node(state: AgentState) -> dict:
    """
    Node: Exam Recommendation Agent
    Recommends competitive exams based on profile
    """
    from agents.exam_agent import run_exam_agent
    
    try:
        # Check if user wants exam recommendations
        interests = state.get("user_interests", ["schemes", "exams"])
        if "exams" not in interests:
            print("\n⏭️ Skipping Exam Agent (not requested)")
            return {"exam_recommendations": "Not requested by user"}
        
        print("\n🎓 Running Exam Recommendation Agent...")
        profile = state.get("profile", {})
        
        # Check if profile has useful data
        useful_fields = [k for k in profile.keys() if k not in ['raw_profile', 'user_input', 'error', 'note']]
        
        if not profile or len(useful_fields) < 2:
            print("⚠️ Insufficient profile data, using web search only")
            # Still try with whatever we have
        
        result = run_exam_agent(profile, use_web_search=True)
        print("✅ Exam recommendations generated")
        return {"exam_recommendations": result.get("recommendations", "")}
        
    except Exception as e:
        print(f"❌ Exam Agent Error: {str(e)}")
        return {
            "exam_recommendations": f"Error generating recommendations: {str(e)}",
            "errors": [f"Exam: {str(e)}"]
        }


def benefit_node(state: AgentState) -> dict:
    """
    Node: Missed Benefits Calculator Agent
    Calculates potential missed benefits
    """
    from agents.benefit_agent import calculate_missed_benefits
    
    try:
        print("\n💰 Running Benefit Calculator Agent...")
        profile = state.get("profile", {})
        scheme_recommendations = state.get("scheme_recommendations", "")
        
        if not profile or not scheme_recommendations:
            print("⚠️ Insufficient data for benefit calculation")
            return {"missed_benefits": "Insufficient data"}
        
        result = calculate_missed_benefits(profile, scheme_recommendations)
        print("✅ Benefit calculation completed")
        return {"missed_benefits": result.get("calculation", "")}
        
    except Exception as e:
        print(f"❌ Benefit Agent Error: {str(e)}")
        return {
            "missed_benefits": "",
            "errors": [f"Benefit: {str(e)}"]
        }


def output_node(state: AgentState) -> dict:
    """
    Node: Final Output Compiler
    Compiles all agent outputs into final response
    """
    print("\n📊 Compiling Final Output...")
    
    final_output = {
        "user_profile": state.get("profile", {}),
        "scheme_recommendations": state.get("scheme_recommendations", ""),
        "exam_recommendations": state.get("exam_recommendations", ""),
        "missed_benefits_analysis": state.get("missed_benefits", ""),
        "errors": state.get("errors", [])
    }
    
    print("✅ Final output ready")
    
    return {"final_output": final_output}


def build_workflow():
    """
    Builds the LangGraph workflow
    
    Returns:
        Compiled workflow graph
    """
    # Create workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("profiling", profiling_node)
    workflow.add_node("scheme", scheme_node)
    workflow.add_node("exam", exam_node)
    workflow.add_node("benefit", benefit_node)
    workflow.add_node("output", output_node)
    
    # Set entry point
    workflow.set_entry_point("profiling")
    
    # Define edges (workflow flow)
    # Step 1: Profiling runs first
    workflow.add_edge("profiling", "scheme")
    workflow.add_edge("profiling", "exam")
    
    # Step 2: Both scheme and exam converge to benefit (runs after both complete)
    workflow.add_edge("scheme", "benefit")
    workflow.add_edge("exam", "benefit")
    
    # Step 3: Benefit goes to output
    workflow.add_edge("benefit", "output")
    
    # Set finish point
    workflow.add_edge("output", END)
    
    # Compile workflow
    return workflow.compile()


def run_workflow(user_input: str, user_interests: list = None, structured_profile: dict = None) -> dict:
    """
    Runs the complete multi-agent workflow
    
    Args:
        user_input: Raw user input text
        user_interests: List of interests ['schemes', 'exams']
        structured_profile: Pre-extracted profile data from form (optional)
        
    Returns:
        Final compiled output dictionary
    """
    print("="*60)
    print("🚀 Starting JanSahayak Multi-Agent System")
    print("="*60)
    
    if user_interests:
        print(f"🎯 User Interests: {', '.join(user_interests)}")
    
    if structured_profile:
        print("📋 Using structured profile data from form")
    
    # Build workflow
    app = build_workflow()
    
    # Initialize state
    initial_state = {
        "user_input": user_input,
        "user_interests": user_interests or ["schemes", "exams"],
        "profile": structured_profile if structured_profile else {},
        "errors": []
    }
    
    # Run workflow
    result = app.invoke(initial_state)
    
    print("\n" + "="*60)
    print("✅ Workflow Completed")
    print("="*60)
    
    return result.get("final_output", {})


if __name__ == "__main__":
    # Test workflow
    test_input = """
    I am a 25-year-old male from Maharashtra. I completed my Bachelor's in Engineering.
    My family income is around 3 lakh per year. I belong to the OBC category.
    I am currently unemployed and looking for government job opportunities.
    I am interested in technical positions and government jobs.
    """
    
    result = run_workflow(test_input)
    
    print("\n📄 Final Result:")
    print("="*60)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
