from e2b import Sandbox

def main():
    print("🌐 Spinning up sandbox...")
    sandbox = Sandbox.create()

    print("📦 Installing 'requests' library via pip...")
    # AI agents often need to install libraries on the fly
    sandbox.commands.run("pip install requests")

    print("🌍 Testing Internet Access...")
    # We will write a python script inside the sandbox that fetches a URL
    code = """
import requests
print("Requesting google.com...")
response = requests.get('https://www.google.com')
print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.text)} characters")
"""
    # Create the python file
    sandbox.files.write("scraper.py", code)

    # Run it
    execution = sandbox.commands.run("python scraper.py")
    
    print("\n--- Sandbox Output ---")
    print(execution.stdout)
    
    if execution.exit_code == 0:
        print("\n✅ Test 4 Passed: Internet + Pip works.")
    else:
        print(f"\n❌ Failed: {execution.stderr}")

    sandbox.kill()

if __name__ == "__main__":
    main()
