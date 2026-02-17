import time
from e2b import Sandbox

def main():
    print("⏱️  Starting timer...")
    start_time = time.time()
    
    # 1. Spin up the sandbox
    sandbox = Sandbox.create() 
    
    # 2. Run a command
    sandbox.commands.run("echo 'Hello World'")
    
    # 3. Kill it
    sandbox.kill()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Test 1 Complete.")
    print(f"⚡ Total Turnaround Time: {duration:.2f} seconds")
    print("(Includes: Cloud Connection -> Boot VM -> Run Code -> Network Return -> Shutdown)")

if __name__ == "__main__":
    main()
