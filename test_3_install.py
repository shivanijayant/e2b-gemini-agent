from e2b import Sandbox

def main():
    print("🛠️  Spinning up standard sandbox...")
    sandbox = Sandbox.create()

    print("   Checking for 'cowsay'...")
    try:
        # This command fails (Exit Code 1) if the tool is missing
        sandbox.commands.run("which cowsay")
    except Exception:
        # We CATCH the error so the script continues
        print("   ✅ 'cowsay' is missing (as expected). Installing now...")

    # Install the tool LIVE
    print("   Running apt-get install (this takes ~15s)...")
    sandbox.commands.run("sudo apt-get update && sudo apt-get install -y cowsay")

    # Verify it works now
    cmd = sandbox.commands.run("/usr/games/cowsay 'I was installed on the fly!'")
    print(cmd.stdout)
    
    sandbox.kill()
    print("✅ Test 3 Complete: Dynamic installation successful.")

if __name__ == "__main__":
    main()
