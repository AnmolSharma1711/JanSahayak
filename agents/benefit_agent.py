"""
Missed Benefits Calculator Agent
Estimates potential benefits user might have missed
"""

import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import GROQ_API_KEY


def get_llm():
    """Initialize Groq LLM"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )


def calculate_missed_benefits(profile_data: dict, scheme_recommendations: str) -> dict:
    """
    Calculates potential benefits the user might have missed in the past
    
    Args:
        profile_data: User profile dictionary
        scheme_recommendations: Recommended schemes text
        
    Returns:
        Dictionary with missed benefits calculation
    """
    try:
        llm = get_llm()
        
        profile_str = json.dumps(profile_data, indent=2)
        
        prompt = f"""
You are a financial analyst specializing in Indian government welfare schemes.

Based on the user's profile and recommended schemes, calculate how much money/benefits 
they might have missed in the past 5 years by not applying to eligible schemes.

**USER PROFILE:**
{profile_str}

**RECOMMENDED SCHEMES:**
{scheme_recommendations}

**ANALYSIS REQUIREMENTS:**

1. **Identify Eligible Schemes:**
   - List schemes user was eligible for in past 5 years
   - Consider age, income, education criteria over time

2. **Calculate Monetary Benefits:**
   - One-time payments missed
   - Annual recurring benefits missed
   - Subsidies or discounts not availed
   - Total missed amount (conservative estimate)

3. **Non-Monetary Benefits:**
   - Training opportunities missed
   - Healthcare benefits not utilized
   - Educational scholarships lost
   - Employment opportunities missed

4. **Year-wise Breakdown:**
   - Provide year-wise missed benefit estimate
   - Account for scheme start dates
   - Consider eligibility changes over time

5. **Actionable Insights:**
   - Can any benefits be claimed retroactively?
   - Which schemes should be applied immediately?
   - Priority ranking for current applications

**OUTPUT FORMAT:**

### Total Missed Benefits (Past 5 Years)
- **Monetary Loss:** ₹[Amount]
- **Non-Monetary Loss:** [Description]

### Year-wise Breakdown
**2022:**
- Scheme Name: ₹[Amount] | [Benefit Description]

**2023:**
- Scheme Name: ₹[Amount] | [Benefit Description]

[Continue for all years]

### Retroactive Claims Possible
- List schemes that allow backdated applications
- Required documentation for backdated claims

### Immediate Action Items
1. [Highest priority scheme to apply now]
2. [Second priority scheme]
3. [Third priority scheme]

### Future Projections
If user applies now, estimated benefits over next 5 years: ₹[Amount]

---

**IMPORTANT NOTES:**
- Provide conservative estimates (lower bound)
- Mark assumptions clearly
- Only include verified government schemes
- Consider state-specific schemes based on user's state
- Factor in income bracket changes over time

Proceed with calculation:
"""
        
        messages = [
            SystemMessage(content="You are a financial analyst for government welfare schemes. Provide realistic, conservative estimates."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        
        return {
            "calculation": response.content,
            "profile_considered": profile_data.get('age', 'N/A'),
            "schemes_analyzed": "Available in recommendations"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "calculation": "Unable to calculate missed benefits"
        }


def estimate_future_benefits(profile_data: dict, scheme_recommendations: str, years: int = 5) -> dict:
    """
    Estimates potential benefits over the next N years if user applies now
    
    Args:
        profile_data: User profile dictionary
        scheme_recommendations: Recommended schemes text
        years: Number of years to project (default: 5)
        
    Returns:
        Dictionary with future benefits projection
    """
    try:
        llm = get_llm()
        
        profile_str = json.dumps(profile_data, indent=2)
        
        prompt = f"""
Based on the user's current profile and eligible schemes, estimate the total benefits 
they can receive over the next {years} years if they apply immediately.

**USER PROFILE:**
{profile_str}

**ELIGIBLE SCHEMES:**
{scheme_recommendations}

Provide:
1. Year-wise projected benefits
2. Total estimated benefits over {years} years
3. Required actions to maximize benefits
4. Key deadlines to watch

Return structured calculation with conservative estimates.
"""
        
        messages = [
            SystemMessage(content="You are a financial projection analyst for government schemes."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        
        return {
            "projection": response.content,
            "years_projected": years,
            "profile_age": profile_data.get('age', 'N/A')
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "projection": "Unable to estimate future benefits"
        }


if __name__ == "__main__":
    # Test the agent
    test_profile = {
        "age": 25,
        "income": "300000",
        "caste": "OBC",
        "state": "Maharashtra",
        "education": "Bachelor's in Engineering",
        "employment_status": "Unemployed"
    }
    
    test_schemes = """
    1. PM Kisan Samman Nidhi: ₹6000 per year
    2. Post Matric Scholarship (OBC): ₹5000-10000 per year
    3. Skill Development Scheme: Free training worth ₹20000
    """
    
    result = calculate_missed_benefits(test_profile, test_schemes)
    print(json.dumps(result, indent=2))
