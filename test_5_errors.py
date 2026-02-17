from e2b import Sandbox
from e2b.sandbox.commands.command_handle import CommandExitException

def main():
    print("🐛 Starting Debugging Test...")
    sandbox = Sandbox.create()

    # We intentionally write broken code (dividing by zero)
    bad_code = "print(10 / 0)"
    
    print("   Running broken code...")

    try:
        # This will raise an exception because the code fails
        sandbox.commands.run(f"python -c '{bad_code}'")
    
    except CommandExitException as e:
        # ✅ SUCCESS: We caught the error!
        print("\n✅ Test 5 Passed: Error Successfully Captured!")
        print(f"   The Sandbox said: {e}")
        print("   (In a real AI agent, we would send this error back to the LLM to fix the code.)")

    except Exception as e:
        print(f"❌ Unexpected error type: {e}")

    sandbox.kill()

if __name__ == "__main__":
    main()

