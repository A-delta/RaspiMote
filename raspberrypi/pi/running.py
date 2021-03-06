from threading import Thread
from time import sleep, time
import datetime
from subprocess import run
from requests import post, codes, exceptions as requests_exceptions
from json import dumps


class Mixin:
    def ping_server(self):
        while True:
            sleep(9)
            if self.verbose:
                run("vcgencmd measure_temp".split())

                start = time()

            content = dumps({"code": self.code, "request": {"type": "ping"}})
            try:
                response = post(self.server_url, data=content, headers=self.request_headers, verify=False)
                if self.verbose:
                    self.log(f"[PING] {self.term_ok_green}{str(time() - start)} s{self.term_endc}\n")
            except Exception as error:
                self.log(f"{self.term_fail}[FAIL] Retrying in 5s{self.term_endc}")
                sleep(5)
                try:
                    response = post(self.server_url, data=content, headers=self.request_headers, verify=False)
                except:
                    self.log(f"{self.term_fail}[FAIL] Restarting connection procedure{self.term_endc}")
                    break
        self.server_url = f'{self.ip}:9876/action'
        self.establish_connection()

    def show_connection(self):
        if self.display_info:
            for _ in range(3):
                self.success_led.on()
                sleep(0.1)
                self.success_led.off()
                self.error_led.on()
                sleep(0.1)
                self.error_led.off()

    def show_success(self):
        if self.display_info:
            self.success_led.on()
            sleep(0.1)
            self.success_led.off()
            sleep(0.1)
            self.success_led.on()
            sleep(0.1)
            self.success_led.off()

    def show_error(self):
        if self.display_info:
            self.error_led.on()
            sleep(0.1)
            self.error_led.off()
            sleep(0.1)
            self.error_led.on()
            sleep(0.1)
            self.error_led.off()

    def event_button(self, button):
        pin = self.pins[self.buttons.index(button)]
        self.log(f"Button{pin}")
        self.send_data({"code": self.code, "request": {"type": "button", "pin": pin, "value": 1}})

    def send_data(self, data):
        r = Thread(name='Request', target=self.send_request, args=[data])
        r.start()

    def send_request(self, data):
        if not self.ready:
            self.log(f"{self.term_fail}Error. Request not sent : program not ready.{self.term_endc}")
            t = Thread(name='Blink LED', target=self.show_error)
            t.start()
            return

        if self.verbose:
            start = time()
        else:
            start = 0

        content = dumps(data)

        try:
            r = post(self.server_url, data=content, headers=self.request_headers, verify=False)
        except Exception as error:
            print(f"{self.term_fail}{error}{self.term_endc}")
            print(f"{self.term_fail}Server not responding, driver might have stopped or encountered error{self.term_endc}")
            self.log(f"{self.term_fail}Error. at {self.term_bold}{datetime.datetime.now().time()}{self.term_endc}")
            error_LED_thread = Thread(name='Blink LED', target=self.show_error)
            error_LED_thread.start()
            # self.reconnect()
            return

        if r.status_code == codes.ok:
            self.log(f"Sent. at {self.term_bold}{datetime.datetime.now().time()}{self.term_endc}")
            info_LED_thread = Thread(name='Blink LED', target=self.show_success)
        else:
            self.log(f"{self.term_fail}Error. at {term_bold}{datetime.datetime.now().time()}{self.term_endc}")
            info_LED_thread = Thread(name='Blink LED', target=self.show_error)

        self.log(f"Answered in {str(time() - start)} at {self.term_bold}{datetime.datetime.now().time()}{self.term_endc}\n")
        info_LED_thread.start()