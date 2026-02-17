import os
import re
import google.generativeai as genai
from e2b import Sandbox

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
# Using Gemini 2.0 Flash for its strong reasoning capabilities
MODEL_NAME = 'models/gemini-2.0-flash'

def get_ai_code(prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    full_prompt = (
        "You are an expert Data Scientist. Write ONLY valid Python code to solve the task. "
        "Do not write explanations or markdown. "
        f"Task: {prompt}"
    )
    response = model.generate_content(full_prompt)
    return re.sub(r"```python|```", "", response.text).strip()

def main():
    print(f"📊 Starting Multi-Step Data Science Benchmark with {MODEL_NAME}")
    
    prompt = (
        "1. Generate a pandas DataFrame with 100 rows of synthetic data. "
        "Columns should be 'System_Load_Percent' (0-100) and 'Data_Retrieval_Time_ms'. "
        "Create a positive linear relationship with some random noise. "
        "2. Use scikit-learn to perform a linear regression predicting Retrieval Time based on System Load. "
        "3. Save the regression coefficient and the R-squared score to a file named 'model_metrics.txt'. "
        "4. Print 'Data pipeline complete.' to the console."
    )
    
    print("🚀 Starting Sandbox...")
    sandbox = Sandbox.create()
    
    print("📦 Installing heavy dependencies (pandas, scikit-learn)...")
    sandbox.commands.run("pip install pandas scikit-learn")
    
    print("🧠 Generating data pipeline code...")
    try:
        code = get_ai_code(prompt)
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        sandbox.kill()
        return

    sandbox.files.write("pipeline.py", code)
    
    print("⚙️ Running complex regression analysis...")
    execution = sandbox.commands.run("python pipeline.py")
    
    if execution.exit_code == 0:
        print("✅ Pipeline executed successfully!")
        
        print("⬇️ Extracting model metrics from the cloud...")
        try:
            metrics = sandbox.files.read("model_metrics.txt")
            print(f"\n--- Model Results ---\n{metrics.strip()}")
        except Exception as e:
            print(f"❌ Failed to extract file: {e}")
    else:
        print(f"❌ Pipeline failed. Error:\n{execution.stderr}")
        
    sandbox.kill()

if __name__ == "__main__":
    main()
