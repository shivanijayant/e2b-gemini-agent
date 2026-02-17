import os
import re
import google.generativeai as genai
from e2b import Sandbox
from e2b.sandbox.commands.command_handle import CommandExitException

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = 'models/gemini-2.0-flash-lite'

def get_ai_code(prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    full_prompt = (
        "You are a Python expert. Write ONLY valid Python code to solve the user's problem. "
        "Do not write explanations. "
        f"Task: {prompt}"
    )
    response = model.generate_content(full_prompt)
    return re.sub(r"```python|```", "", response.text).strip()

def main():
    print(f"🤖 Starting Self-Healing Agent with {MODEL_NAME}")
    
    base_prompt = (
        "Write a Python script that imports the library `quantum_flux_matrix` "
        "and prints the result of `quantum_flux_matrix.stabilize()`. "
        "Assume the library is already installed."
    )
    
    current_prompt = base_prompt
    max_retries = 3
    
    print("🚀 Starting Sandbox...")
    sandbox = Sandbox.create()
    
    for attempt in range(1, max_retries + 1):
        print(f"\n--- Attempt {attempt} ---")
        print("🧠 Generating code...")
        
        try:
            code = get_ai_code(current_prompt)
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            break

        sandbox.files.write("script.py", code)
        
        print("⚙️ Running code in E2B...")
        
        try:
            # THIS is where we catch the crash!
            execution = sandbox.commands.run("python script.py")
            print(f"✅ Success on attempt {attempt}!")
            print(f"Output: {execution.stdout}")
            break
            
        except CommandExitException as e:
            # We catch the E2B exception, extract the error, and keep the script alive
            error_msg = str(e)
            print(f"❌ Execution failed! The sandbox caught this error:\n{error_msg.strip()}")
            
            if attempt < max_retries:
                print("🔄 Feeding the error back to Gemini so it can self-heal...")
                current_prompt = f"{base_prompt}\n\nThe previous code failed with this error:\n{error_msg}\n\nPlease provide the corrected Python code. If the library cannot be found, define a mock version of it in the script so it runs successfully."
            else:
                print("🛑 Max retries reached.")

    sandbox.kill()

if __name__ == "__main__":
    main()
