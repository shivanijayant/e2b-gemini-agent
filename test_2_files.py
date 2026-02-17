from e2b import Sandbox
import os

def main():
    # Create a dummy "sensitive" file locally
    with open("confidential.txt", "w") as f:
        f.write("SecretCode: 999-888-777")

    print("🔒 Uploading secure file...")
    sandbox = Sandbox.create()
    
    # Upload to the sandbox's temporary memory
    with open("confidential.txt", "rb") as f:
        sandbox.files.write("/tmp/secret.txt", f)

    # Verify the file is there by reading it via shell
    cmd = sandbox.commands.run("cat /tmp/secret.txt")
    print(f"   Remote file content: {cmd.stdout}")

    # Process it (Example: Extract just the number)
    sandbox.commands.run("grep -o '999-888-777' /tmp/secret.txt > /tmp/processed.txt")

    # Download the result
    result = sandbox.files.read("/tmp/processed.txt")
    print(f"✅ Processed Result: {result}")

    sandbox.kill()
    os.remove("confidential.txt")

if __name__ == "__main__":
    main()
