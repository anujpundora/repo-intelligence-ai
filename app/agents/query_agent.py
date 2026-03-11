from app.llm.llm_router import LLMRouter

llm = LLMRouter()

def generate_queries(task):

    prompt = f"""
Generate 4 different search queries to find relevant code for the following task.

Task:
{task}

Return a JSON list of queries.

Example:
["authentication login flask", "session handling flask", "login_required decorator"]
"""
    
    response = llm.generate(prompt)

    try:
        queries = eval(response)
        print(f"Generating queries {queries} for task {task}")
    except:
        queries = [task]

    return queries