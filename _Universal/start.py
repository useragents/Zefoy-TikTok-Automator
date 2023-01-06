# Linux and cloud machine compatible code (Removes update_title for linux)

try:
    import requests, ctypes, time, os, threading, platform
    from colorama import Fore
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")

ascii_text = """
           _   _ _    _        _    
          | | (_) |  | |      | |   
          | |_ _| | _| |_ ___ | | __
          | __| | |/ / __/ _ \| |/ /
          | |_| |   <| || (_) |   < 
           \__|_|_|\_\\__\___/|_|\ _\\
  """

# Platform checks
if platform.system() == "Windows":
    windows = True
    clear = "cls"
if platform.system() == "Linux":
    linux = True
else:
    clear = "clear"

class tiktok:

    def __init__(self):
        self.lock = threading.Lock()
        self.checking = True
        self.usernames = []
        self.unavailable = 0
        self.available = 0
        self.counter = 0
    
    def safe_print(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()
    
    def print_console(self, status, arg, color = Fore.RED):
        self.safe_print(f"       {Fore.WHITE}[{color}{status}{Fore.WHITE}] {arg}")
    
    # Categorize the usernames into available and unavailable containers (Files)
    def check_username(self, username):
        if username.isdigit():
            self.unavailable += 1
            self.print_console("Unavailable", username)
            return
        with requests.Session() as session:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "content-type": "application/json"
            }
            r = session.head("https://www.tiktok.com/@{}".format(username), headers = headers)
            if r.status_code == 200:
                self.unavailable += 1
                self.print_console("Unavailable", username)
            elif r.status_code == 404:
                self.available += 1
                self.print_console("Available or Banned", username, Fore.GREEN)
                with open("Available.txt", "a") as f:
                        f.write(username + "\n")
    
    # Load usernames from .txt file
    def load_usernames(self):
        if not os.path.exists("usernames.txt"):
            self.print_console("Console", "File usernames.txt not found")
            time.sleep(10)
            os._exit(0)
        with open("usernames.txt", "r", encoding = "UTF-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                self.usernames.append(line)
            if not len(self.usernames):
                self.print_console("Console", "No usernames loaded in usernames.txt")
                time.sleep(10)
                os._exit(0)

    # This function glues every function together into a loop (Very fast)
    def main(self):
        os.system(clear)
        if windows == "True":
            ctypes.windll.kernel32.SetConsoleTitleW("TikTok Username Checker | Developed by @useragents on Github")
        print(Fore.RED + ascii_text)
        self.load_usernames()
        threads = int(input(f"       {Fore.WHITE}[{Fore.RED}Console{Fore.WHITE}] Threads: "))
        print()
        if threads >= 5: #To prevent ratelimits
            threads = 5
        
        def thread_starter():
            self.check_username(self.usernames[self.counter])
        while self.checking:
            if threading.active_count() <= threads:
                try:
                    threading.Thread(target = thread_starter).start()
                    self.counter += 1
                except:
                    pass
                if len(self.usernames) <= self.counter:
                    self.checking = None

obj = tiktok()
obj.main()
input()


# OPEN SOURCE IS THE BEST SOURCE
