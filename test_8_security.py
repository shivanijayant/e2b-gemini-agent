import time
from e2b import Sandbox
from e2b.exceptions import TimeoutException

def main():
    print("🛡️ Starting Security Protocol: Hostile Agent Test")
    
    malicious_code = """
import os

print('🚨 Attempting unauthorized access to /etc/shadow...')
try:
    with open('/etc/shadow', 'r') as f:
        print(f.read())
except PermissionError:
    print('✅ ACCESS DENIED: Host filesystem is isolated and protected.')

print('\\n🚨 Initiating CPU/Memory exhaustion (Fork Bomb)...')
# A classic Python fork bomb that replicates endlessly
try:
    while True:
        os.fork()
except Exception as e:
    pass
"""
    print("🚀 Starting Isolated Sandbox...")
    sandbox = Sandbox.create()
    
    sandbox.files.write("attack.py", malicious_code.strip())
    
    print("⚙️ Executing malicious payload (Waiting 15 seconds for timeout)...")
    
    try:
        # We expect this to time out because the fork bomb never finishes
        execution = sandbox.commands.run("python attack.py", timeout=15)
        print(execution.stdout)
    except TimeoutException:
        print("\n✅ ATTACK NEUTRALIZED: The sandbox successfully contained the infinite loop!")
        print("   The local timeout was reached, and the host machine was completely unaffected.")
        
    sandbox.kill()

if __name__ == "__main__":
    main()
