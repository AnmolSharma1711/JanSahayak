"""
User Profiling Prompt Template
Extracts structured user information for eligibility matching
"""

PROFILING_PROMPT = """
Extract user information from the input below and return ONLY a JSON object (no markdown, no explanations).

Use these exact keys:
{
  "name": "user's name or 'Not Provided'",
  "age": "age in years or 'Not Provided'",
  "gender": "Male/Female/Other or 'Not Provided'",
  "state": "Indian state or 'Not Provided'",
  "education": "highest qualification or 'Not Provided'",
  "income": "annual family income or 'Not Provided'",
  "caste": "General/SC/ST/OBC/EWS or 'Not Provided'",
  "employment_status": "Student/Employed/Unemployed/Self-employed or 'Not Provided'",
  "occupation": "current job/field or 'Not Provided'",
  "skills": "skills or 'Not Provided'",
  "interests": "interests or 'Not Provided'",
  "disability_status": "Yes/No or 'Not Provided'",
  "family_size": "number of members or 'Not Provided'",
  "bpl_status": "Yes/No or 'Not Provided'"
}

RULES:
1. Return ONLY the JSON object above with actual extracted values
2. Use "Not Provided" for missing information
3. Do not add any text before or after the JSON
4. Do not use markdown code blocks
5. Extract only explicitly stated information

User Input:
{user_input}
"""
