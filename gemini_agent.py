import os
import re
import google.generativeai as genai
from e2b import Sandbox
from e2b.sandbox.commands.command_handle import CommandExitException

# Configure Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_ai_code(prompt):
    print(f"🧠 Gemini is thinking about: '{prompt}'...")
    
    # Using the Lite model to avoid rate limits
    model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
    
    full_prompt = (
        "You are a Python data assistant. "
        "Write ONLY valid Python code to solve the user's problem. "
        "Do not write explanations. Print the final result. "
        f"User Task: {prompt}"
    )
    
    response = model.generate_content(full_prompt)
    code = response.text
    # Clean up markdown if present
    code = re.sub(r"```python|```", "", code).strip()
    return code

def main():
    print("🤖 Gemini AI Agent Ready.")
    user_task = input("\nWhat should I calculate? \n> ")
    if not user_task: user_task = "Calculate factorial of 100"

    # 1. Get Code
    try:
        code = get_ai_code(user_task)
        print(f"\n📝 Gemini wrote this code:\n{'-'*20}\n{code}\n{'-'*20}\n")
    except Exception as e:
        print(f"❌ Error talking to Gemini: {e}")
        return

    # 2. Run in Sandbox
    print("🚀 Sending to E2B Sandbox...")
    sandbox = Sandbox.create()
    
    try:
        # --- THE FIX IS HERE ---
        # Instead of 'python -c', we write a file. This is safer.
        sandbox.files.write("agent_script.py", code)
        
        # Now we just run the file
        execution = sandbox.commands.run("python agent_script.py")
        
        print(f"\n✅ Final Result from Cloud:\n{execution.stdout}")
        
        if execution.stderr:
            print(f"⚠️ Stderr: {execution.stderr}")
            
    except CommandExitException as e:
        print(f"\n❌ The code failed:\n{e}")
    
    sandbox.kill()

if __name__ == "__main__":
    main()
