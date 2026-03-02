"""
User Profiling Agent
Extracts structured user information for eligibility matching
"""

import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from prompts.profiling_prompt import PROFILING_PROMPT
from config import GROQ_API_KEY


def get_llm():
    """Initialize Groq LLM"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.1  # Low temperature for structured extraction
    )


def extract_json_from_text(text: str) -> dict:
    """Extract JSON from text that might contain markdown or extra content"""
    import re
    
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, text, re.DOTALL)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in text
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None


def run_profiling_agent(user_input: str) -> dict:
    """
    Extracts structured profile information from user input
    
    Args:
        user_input: Raw user input text
        
    Returns:
        Structured profile dictionary
    """
    try:
        llm = get_llm()
        
        prompt = PROFILING_PROMPT.format(user_input=user_input)
        
        messages = [
            SystemMessage(content="You are an expert user profiling agent. Return ONLY a valid JSON object, nothing else."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        
        print(f"\n🤖 LLM Response (first 200 chars): {response.content[:200]}...")
        
        # Extract JSON from response
        profile_data = extract_json_from_text(response.content)
        
        if profile_data:
            # Normalize keys to lowercase with underscores
            normalized_profile = {}
            for key, value in profile_data.items():
                normalized_key = key.lower().replace(' ', '_').replace('-', '_')
                normalized_profile[normalized_key] = value
            
            print(f"✅ Profile extracted: {list(normalized_profile.keys())}")
            return normalized_profile
        else:
            # Fallback: Create basic profile from user input
            print("⚠️ Could not parse JSON, creating basic profile")
            return {
                "user_input": user_input,
                "raw_profile": response.content,
                "note": "Profile extraction incomplete. Using raw input."
            }
    
    except Exception as e:
        print(f"❌ Profiling error: {str(e)}")
        return {
            "error": str(e),
            "user_input": user_input
        }


def validate_profile(profile_data: dict) -> bool:
    """
    Validates that profile has minimum required information
    
    Args:
        profile_data: Profile dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['age', 'state', 'education']
    
    for field in required_fields:
        if field not in profile_data or profile_data[field] == "Not Provided":
            return False
    
    return True


if __name__ == "__main__":
    # Test the agent
    test_input = """
    I am a 25-year-old male from Maharashtra. I completed my Bachelor's in Engineering.
    My family income is around 3 lakh per year. I belong to the OBC category.
    I am currently unemployed and looking for government job opportunities.
    """
    
    result = run_profiling_agent(test_input)
    print(json.dumps(result, indent=2))
