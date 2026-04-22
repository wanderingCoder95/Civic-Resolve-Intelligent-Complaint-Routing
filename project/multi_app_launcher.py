import subprocess
import time
import os
import sys

def launch_instance(port):
    """Launches a single Flask instance in a new console window and returns the process object."""
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    try:
        if os.name == 'nt':
            # CREATE_NEW_CONSOLE ensures it pops up in a new window on Windows
            # and allows us to keep a handle on the process to terminate it later.
            p = subprocess.Popen([sys.executable, app_path, str(port)], 
                               creationflags=0x00000010) # 0x10 is CREATE_NEW_CONSOLE
        else:
            # On Unix-like systems, we just run it in the background
            p = subprocess.Popen([sys.executable, app_path, str(port)])
        return p
    except Exception as e:
        print(f" ❌ Failed to launch: {e}")
        return None

def interactive_launcher():
    start_port = 5000
    # List of tuples: (port, process_object)
    instances = []
    
    print("\n" + "="*45)
    print(" 🚀 Civic Resolve: Smart Multi-App Manager")
    print("="*45)
    print(" Control multiple real-time instances from here.")
    print("-" * 45)

    # Start the first one automatically
    p = launch_instance(start_port)
    if p:
        instances.append((start_port, p))
        print(f" ✅ Started Instance 1: http://127.0.0.1:{start_port}")

    while True:
        active_ports = [str(i[0]) for i in instances]
        print(f"\n [ ACTIVE PORTS: {', '.join(active_ports) if active_ports else 'None'} ]")
        print(" > '+'          : Add new instance (+1)")
        print(" > '- <port>'   : Close specific (e.g., - 5001)")
        print(" > 'killall'    : Close ALL active instances")
        print(" > 'exit'       : Close all and exit program")
        print(" > 'q'          : Exit launcher (leave windows open)")
        
        choice = input("\n Command: ").strip().lower()

        if choice == '+':
            # Determine next port
            next_port = start_port
            existing_ports = [i[0] for i in instances]
            while next_port in existing_ports:
                next_port += 1
                
            p = launch_instance(next_port)
            if p:
                instances.append((next_port, p))
                print(f" ✅ Started Instance: http://127.0.0.1:{next_port}")
            time.sleep(0.5)

        elif choice.startswith('-'):
            try:
                parts = choice.split()
                if len(parts) < 2:
                    print(" ⚠️ Please specify a port. Example: - 5001")
                    continue
                
                target_port = int(parts[1])
                match = next((inst for inst in instances if inst[0] == target_port), None)
                
                if match:
                    match[1].terminate()
                    instances.remove(match)
                    print(f" 🛑 Closed instance on port {target_port}")
                else:
                    print(f" ⚠️ No active instance found on port {target_port}")
            except ValueError:
                print(" ⚠️ Invalid port number.")
            except Exception as e:
                print(f" ⚠️ Error closing instance: {e}")

        elif choice == 'killall':
            print(" 💥 Killing all instances...")
            for _, p in instances:
                p.terminate()
            instances = []
            print(" ✅ All windows closed.")

        elif choice == 'exit':
            print(" 💥 Cleaning up and exiting...")
            for _, p in instances:
                p.terminate()
            break

        elif choice == 'q':
            print("\n 👋 Exiting launcher. Background windows will remain active.")
            break
        else:
            print(" ⚠️ Unknown command. Use +, -, killall, exit, or q.")

if __name__ == "__main__":
    try:
        interactive_launcher()
    except KeyboardInterrupt:
        print("\n\n 👋 Launcher stopped via keyboard.")
