#Developed by github.com/useragents
#This script was made for educational purposes. I am not responsible for your actions using this script. This code is a few months old, hence why it may not appear as professional but still works to this day.
try:
    from selenium import webdriver
    import time, os, ctypes, requests
    from colorama import Fore, init
    import warnings, selenium, platform
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")

input("\nPress ENTER to start.\nThe owner of this bot @useragents does NOT OWN the SITE zefoy.com\nThis is simply an automator ONLY.")
init(convert = True, autoreset = True)
warnings.filterwarnings("ignore", category=DeprecationWarning)

clear = "clear"
if platform.system() == "Windows":
    clear = "cls"

os.system(clear)

ascii_text = f"""{Fore.RED}
                ████████▀▀▀████
                ████████────▀██
                ████████──█▄──█
                ███▀▀▀██──█████
                █▀──▄▄██──█████
                █──█████──█████
                █▄──▀▀▀──▄█████
                ███▄▄▄▄▄███████ github.com/useragents
"""

class automator:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.xpaths = {
            "followers": "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button",
            "likes": "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button",
            "views": "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button",
            "shares": "/html/body/div[4]/div[1]/div[3]/div/div[5]/div/button"
        }
        try:
            self.driver = webdriver.Chrome(options = options)
        except Exception as e:
            self.error(f"Error trying to load web driver: {e}")
        self.status = {}
        self.sent = 0
        self.cooldowns = 0
        self.ratelimits = 0

    def check_status(self):
        for xpath in self.xpaths:
            value = self.xpaths[xpath]
            element = self.driver.find_element_by_xpath(value)
            if not element.is_enabled():
                self.status.update({xpath: "[OFFLINE]"})
            else:
                self.status.update({xpath: ""})
    
    def check_for_captcha(self):
        while True:
            try:
                if "Enter the word" not in self.driver.page_source:
                    return
            except:
                return
            os.system(clear)
            print(ascii_text)
            print(f"{self.console_msg('Error')} Complete the CAPTCHA in the driver.")
            time.sleep(1)

    def console_msg(self, status):
        colour = Fore.RED
        if status == "Success":
            colour = Fore.GREEN
        return f"                {Fore.WHITE}[{colour}{status}{Fore.WHITE}]"
    
    def update_ascii(self):
        options = f"""
{self.console_msg("1")} Follower Bot {Fore.RED}{self.status["followers"]}
{self.console_msg("2")} Like Video Bot {Fore.RED}{self.status["likes"]}
{self.console_msg("3")} View Bot {Fore.RED}{self.status["views"]}
{self.console_msg("4")} Share Bot {Fore.RED}{self.status["shares"]}
        """
        return ascii_text + options
    
    def check_url(self, url):
        return True

    def convert(self, min, sec):
        seconds = 0
        if min != 0:
            answer = int(min) * 60
            seconds += answer
        seconds += int(sec) + 15
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[4]/div[{div}]/div/div/h4"
        try:
            element = self.driver.find_element_by_xpath(remaining)
        except:
            return None, None
        if "READY" in element.text:
            return True, True
        if "seconds for your next submit" in element.text:
            output = element.text.split("Please wait ")[1].split(" for")[0]
            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration = self.convert(minutes, seconds)
            return sleep_duration, output
        return element.text, None
    
    def update_cooldown(self, sleep_time, bot, rl = False):
        cooldown = sleep_time
        while True:
            time.sleep(1)
            try:
                cooldown -= 1
            except TypeError:
                break
            self.update_title(bot, cooldown, rl)
            if cooldown == 0:
                break
    
    def wait_for_ratelimit(self, arg, div):
        time.sleep(1)
        duration, output = self.check_submit(div)
        if duration == True:
            return
        if output == None:
            time.sleep(0.7)
            self.wait_for_ratelimit(arg, div)
        self.cooldowns += 1
        self.update_cooldown(duration, arg)

    def send_bot(self, video_url, bot, div):
        try:
            self.driver.find_element_by_xpath(self.xpaths[bot]).click()
            time.sleep(0.5)
        except:
            pass
        enter_link_xpath = f"/html/body/div[4]/div[{div}]/div/form/div/input" 
        link = self.driver.find_element_by_xpath(enter_link_xpath)
        link.clear()
        link.send_keys(video_url)
        self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/form/div/div/button").click() #Search button
        time.sleep(0.8)
        send_button_xpath = f"/html/body/div[4]/div[{div}]/div/div/div[1]/div/form/button"
        try:
            self.driver.find_element_by_xpath(send_button_xpath).click() 
        except selenium.common.exceptions.NoSuchElementException:
            self.wait_for_ratelimit(bot, div)
            self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/form/div/div/button").click() #Search button
            time.sleep(0.8)
            self.driver.find_element_by_xpath(send_button_xpath).click()
        time.sleep(3)
        try:
            s = self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/div/span")
            if "Too many requests" in s.text:
                self.ratelimits += 1
                self.update_cooldown(50, bot, True)
                self.send_bot(video_url, bot, div)
            elif "sent" in s.text:
                sent = 100
                if bot == "likes":
                    try:
                        sent = int(s.text.split(" Hearts")[0])
                    except IndexError:
                        sent = 30
                if bot == "views":
                    sent = 2500
                if bot == "shares":
                    sent = 500
                self.sent += sent
            else:
                print(s.text)
        except:
            self.sent += sent
        self.update_title(bot, "0")
        self.wait_for_ratelimit(bot, div)
        self.send_bot(video_url, bot, div)

    def update_title(self, bot, remaining, rl = False):
        if clear == "cls":
            os.system(clear)
            ctypes.windll.kernel32.SetConsoleTitleW(f"TikTok AIO | Sent: {self.sent} | Cooldown: {remaining}s | Developed by @useragents on Github")
            print(ascii_text)
            print(self.console_msg(self.sent) + f" Sent {bot}")
            rl_cooldown = "0"
            cooldown = "0"
            if rl:
                rl_cooldown = remaining
            else:
                cooldown = remaining
            print(self.console_msg(self.cooldowns) + f" Cooldowns {Fore.WHITE}[{Fore.RED}{cooldown}s{Fore.WHITE}]")
            print(self.console_msg(self.ratelimits) + f" Ratelimits {Fore.WHITE}[{Fore.RED}{rl_cooldown}s{Fore.WHITE}]")

    def main(self):
        if clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW("TikTok AIO | Developed by @useragents on Github")
        self.driver.get("https://zefoy.com/")
        time.sleep(2)
        if "502 Bad Gateway" in self.driver.page_source:
            os.system(clear)
            print(ascii_text)
            input(f"{self.console_msg('Error')} This website does not allow VPN or proxy services.")
            os._exit(0)
        self.check_for_captcha()
        self.check_status()
        self.start()
    
    def error(self, error):
        print(ascii_text)
        print(f"{self.console_msg('Error')} {error}")
        time.sleep(5)
        os._exit(0)
    
    def start(self):
        os.system(clear)
        print(self.update_ascii())
        try:
            option = int(input(f"                {Fore.RED}> {Fore.WHITE}"))
        except ValueError:
            self.start()
        if option == 1:
            if self.status["followers"] != "":
                return self.start()
            div = 2
            ver = "followers"
            username = str(input(f"\n{self.console_msg('Console')} TikTok Username: @"))
            print()
            self.send_bot(username, ver, div)
            return
        elif option == 2:
            if self.status["likes"] != "":
                return self.start()
            div = 3
            ver = "likes"
        elif option == 3:
            if self.status["views"] != "":
                return self.start()
            div = 5
            ver = "views"
        elif option == 4:
            if self.status["shares"] != "":
                return self.start()
            div = 6
            ver = "shares"
        else:
            return self.start()
        video_url = str(input(f"\n{self.console_msg('Console')} Video URL: "))
        print()
        check = self.check_url(video_url)
        if not check:
            return self.error("This URL does not exist.")
        self.send_bot(video_url, ver, div)

obj = automator()
obj.main()
