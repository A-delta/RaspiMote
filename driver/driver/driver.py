# 2021 Adelta
# https://github.com/A-delta


from sys import platform
from os import system, path, chdir, getcwd, getenv, kill
from requests import request
from random import randint
from json import dumps, load
import urllib3, threading, socket
import time
import subprocess, psutil

urllib3.disable_warnings()


class Driver:
    def __init__(self, verbose):

        self.platform = platform
        self.driver_path = path.join(getcwd(), "driver")
        self.verbose = verbose

        self.code = str(randint(0, 9999999))
        self.ip = ''
        self.port = 9876



        self.load_config()

        self.log([self.platform, self.driver_path, self.code, self.ip, self.port])


    def log(self, messages):
        if self.verbose:
            for m in messages:
                print(m)

    def load_config(self):
        """Will check for saved config.
        If none, -> self.configure()"""

        if self.platform == "linux":
            config_folder = "HOME"
        elif self.platform == "win32":
            config_folder = "APPDATA"
        config_path = path.join(getenv(config_folder), ".config", "RaspiMote")

        config_file_path = path.join(config_path, "pi_ip.raspimote")

        if path.isfile(config_file_path):
            pi_ip = open(config_file_path, 'r')
            self.ip = load(pi_ip)["ip"]
            pi_ip.close()
        else:
            self.ip = input("Raspberry Pi's IP address : ")


        with open(config_file_path, 'w') as pi_ip:
            pi_ip.write(dumps({"ip": self.ip, "code": self.code}))


    def establish_connection(self):

        url = f"https://{self.ip}:{self.port}/connect"
        content = {"code": self.code}
        headers = {"Content-Type": "application/json"}
        content = dumps(content)
        connection = request('CONNECT', url, data=content, headers=headers, verify=False)
        return connection.text == "True"


    """def watchdog(self):
        listOfProcessObjects = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])

                if "gunicorn".lower() in pinfo['name'].lower():
                    listOfProcessObjects.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass




        time.sleep(5)
        command = f"ps ax | grep gunicorn | grep {self.port} | awk {'{'}split($0,a,\" \"); print a[1]}}' | head -n 1"
        try:
            output = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            pid = int(e.output)

        while True:
            time.sleep(3)
            try:
                kill(pid, 0)
            except OSError:
                self.log("Server crashed")"""

    def run(self):
        """watchdog = threading.Thread(name="Server Watchdog", target=self.watchdog)
        watchdog.start()"""

        chdir(path.join(self.driver_path, "lan_server"))

        if self.verbose:
            log_level = ''
        else:
            log_level = "--log-level critical"

        if self.platform == "win32":
            print("Only HTTP for the moment.")
            #system('python wsgi_waitress.py')

        elif self.platform == "darwin":
            print("System not supported for the moment.")

        elif self.platform == "linux":
            system(f"gunicorn {log_level} --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:9876 wsgi_gunicorn:app")  # Run the HTTPS server.

        else:
            print("System not supported.")
