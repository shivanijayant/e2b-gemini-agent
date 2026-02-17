import os
import re
from openai import OpenAI
from e2b import Sandbox
from e2b.sandbox.commands.command_handle import CommandExitException

# Initialize OpenAI
# Ensure you ran: export OPENAI_API_KEY=sk-...
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_code(prompt):
    """Ask GPT-4 to write Python code for a specific task."""
    print(f"🧠 Thinking about: '{prompt}'...")
    
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-3.5-turbo" if you don't have gpt-4
        messages=[
            {"role": "system", "content": "You are a Python data assistant. Write ONLY valid Python code to solve the user's problem. Do not write explanations. Print the final result."},
            {"role": "user", "content": prompt}
        ]
    )
    # Clean up response to get just the code (remove markdown backticks)
    content = response.choices[0].message.content
    code = re.sub(r"```python|```", "", content).strip()
    return code

def main():
    # 1. Get user input
    user_task = input("\n🤖 AI Agent Ready. What should I calculate? \n> ")
    if not user_task:
        user_task = "Calculate the first 10 numbers of the Fibonacci sequence"

    # 2. Get Code from AI
    code = get_ai_code(user_task)
    print(f"\n📝 AI wrote this code:\n{'-'*20}\n{code}\n{'-'*20}\n")

    # 3. Execute in E2B Sandbox
    print("🚀 Running in E2B Sandbox...")
    sandbox = Sandbox.create()
    
    try:
        # Run the AI's code
        execution = sandbox.commands.run(f"python -c \"{code}\"")
        print(f"\n✅ Final Result:\n{execution.stdout}")
        
    except CommandExitException as e:
        print(f"\n❌ The AI's code failed:\n{e}")
        print("(You could now auto-feed this error back to the AI to ask for a fix!)")
    
    sandbox.kill()

if __name__ == "__main__":
    main()
