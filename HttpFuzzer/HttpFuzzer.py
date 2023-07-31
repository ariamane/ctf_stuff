# Multithreaded http/s fuzzer which uses
# Burp Suite generated curl command as an input


import os
import io
import cmd
import time
import string
import random
import pathlib
import tkinter
import tkinter.filedialog
import multiprocessing.pool

import uncurl
import requests

# Workaround for InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_current_time():
    struct_time = time.localtime(time.time())
    return "{day}.{month}.{year} {hour}:{minutes}:{seconds}" \
           "".format(
        day=str(struct_time.tm_mday),
        month=str(struct_time.tm_mon),
        year=str(struct_time.tm_year),
        hour=str(struct_time.tm_hour),
        minutes=str(struct_time.tm_min),
        seconds=str(struct_time.tm_sec)
    )


def random_string(length):
    abc = string.ascii_letters
    return "".join(random.choices(abc, k=length))


def is_text_file(var):
    return isinstance(var, io.TextIOBase)


def is_iterable(var):
    return hasattr(var, "__iter__")


class HttpFuzzerCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()

        self.prompt = "cmD > "
        self.intro = "Welcome to HTTP Fuzzer. Type \"help\" for available commands."

        # This word is replaced with payload values in requests
        self.fuzz_keyword = "FUZZ"
        self.log_filename = "%s.txt" % random_string(16)

        self.request_value = None
        self.payload_value = None

        self.menu = (
                "HTTP Fuzzer Menu\n"
                + self.ruler * 40 + "\n" +
                "Request :  {request_value}\n"
                "Payload :  {payload_value}\n"
                + self.ruler * 40
        )

    # ---- Available commands ----
    def do_request(self, line):
        file = tkinter.filedialog.askopenfile(
            title="Select curl-containing file",
            initialdir=pathlib.Path(__file__).parent,
            filetypes=(
                (
                    ("All curl files", "*.txt;*.sh;*.req;*.curl"),
                    ("Curl text files", "*.txt"),
                    ("Curl script files", "*.sh"),
                    ("Curl request files", "*.req"),
                    ("Curl-containing files", "*.curl"),
                )
            )
        )
        if not is_text_file(file):
            if not file:
                print("You haven't chosen a file")
            else:
                print("Provided file is not a text file")
        else:
            with file:
                content = file.read()
            curl = content \
                .replace("\\", "") \
                .replace("\n", "") \
                .replace("$", "")
            try:
                eval_string = uncurl.parse(curl)
                self.request_value = eval_string
                self.output_menu()
                print("Set request value successfully")
            except SystemExit:
                self.output_menu()
                print("Could not parse curl-containing file")

    def do_payload(self, line):
        args = line.strip().split(" ")
        if args[0] == "range":
            if len(args) != 4:
                print("Incorrect arguments")
            else:
                try:
                    start, end, step = map(int, args[1:])
                    self.payload_value = range(start, end + 1, step)
                    self.output_menu()
                    print("Set payload value successfully")
                except ValueError:
                    print("Range parts must be numbers")
        elif args[0] == "file":
            file = tkinter.filedialog.askopenfile(
                title="Select payload file",
                initialdir=pathlib.Path(__file__).parent,
                filetypes=(
                    (
                        ("Payload text files", "*.txt"),
                    )
                )
            )
            if not is_text_file(file):
                if not file:
                    print("You haven't chosen a file")
                else:
                    print("Provided file is not a text file")
            else:
                with file:
                    lines = file.readlines()
                lines = map(lambda x: x.strip().replace("\n", ""), lines)
                lines = filter(lambda x: True if x else False, lines)
                self.payload_value = tuple(lines)
                self.output_menu()
                print("Set payload successfully")
        else:
            print("Incorrect arguments")

    def do_run(self, line):
        if not isinstance(self.request_value, str) or not is_iterable(self.payload_value):
            print("Request or Payload are unset")
        else:
            log_file = open(self.log_filename, "a")

            def auxiliary(part):
                eval_string = self.request_value.replace(self.fuzz_keyword, str(part))
                response = eval(eval_string)
                message = "{time} | {status_code} | {method} | {url}" \
                          "".format(
                    time=get_current_time(),
                    status_code=str(response.status_code),
                    method=str(response.request.method),
                    url=str(response.request.url)
                )
                log_file.write(message + "\n")
                print(message)

            print()
            with multiprocessing.pool.ThreadPool() as pool:
                tasks = list()
                for part in self.payload_value:
                    task = pool.apply_async(auxiliary, (part,))
                    tasks.append(task)
                for task in tasks:
                    task.get()
            print()

    # ---- Auxiliary subroutines ----
    def output_menu(self):
        menu = self.menu.format(
            request_value=str(type(self.request_value)),
            payload_value=str(type(self.payload_value))
        )
        clear_screen()
        print(menu)

    # ---- Overwritten CMD methods ----
    def emptyline(self):
        pass

    def precmd(self, line):
        self.output_menu()
        return super().precmd(line)

    def preloop(self):
        self.output_menu()


if __name__ == "__main__":
    tkinter.Tk().withdraw()
    HttpFuzzerCmd().cmdloop()
