# Multithreaded http/s fuzzer which uses
# Burp Suite generated curl command as an input


import os
import sys
import pathlib
import multiprocessing.pool

import uncurl
import requests

# Workaround for InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def exit_with_critical_error(error_message):
    print("Critical error: %s" % error_message)
    input("\nPress 'Enter' to continue...")
    sys.exit(EXIT_FAILURE)


def get_request_eval_string():
    path = pathlib.Path(FILE_NAME_REQUEST)
    if not path.exists():
        exit_with_critical_error("Could not find %s" % FILE_NAME_REQUEST)
    else:
        with open(path, "r") as file:
            curl = file.read()
        curl = curl \
            .replace("\\", "") \
            .replace("\n", "") \
            .replace("$", "")
        try:
            request_eval_string = uncurl.parse(curl)
            return request_eval_string
        except SystemExit:
            clear_screen()
            exit_with_critical_error("Could not parse curl command")


def input_payload_choice():
    print(HELP_MESSAGE)
    while True:
        payload_choice = input("Enter payload choice > ").strip()
        if payload_choice not in ALLOWED_PARAMETERS:
            print("Incorrect payload choice")
        else:
            return payload_choice


def input_range():
    def input_range_part(message):
        while True:
            try:
                part = int(input(message))
                return part
            except ValueError:
                print("Range part must be a number")

    start = input_range_part("Enter range start > ")
    end = input_range_part("Enter range end > ")
    step = input_range_part("Enter range step > ")
    return range(start, end, step)


def input_file():
    path = pathlib.Path(FILE_NAME_PAYLOAD)
    if not path.exists():
        exit_with_critical_error("Could not find %s" % FILE_NAME_PAYLOAD)
    else:
        with open(path, "r") as file:
            lines = file.readlines()
        lines = map(lambda x: x.replace("\n", ""), lines)
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: True if x != "" else False, lines)
        return lines


def fuzz(request_eval_string, payload):
    def send_request_and_log(payload_part, log_file):
        to_eval = request_eval_string.replace(FUZZ_KEYWORD, str(payload_part))
        response = eval(to_eval)
        log_message = "{status_code} | {method} | {url}" \
                      "".format(
            status_code=str(response.status_code),
            method=response.request.method,
            url=response.request.url
        )
        log_file.write(log_message + "\n")
        print(log_message)

    with open(FILE_NAME_LOG, "w") as file:
        file.flush()

    print()
    with open(FILE_NAME_LOG, "a") as file:
        tasks = []
        with multiprocessing.pool.ThreadPool() as pool:
            for part in payload:
                task = pool.apply_async(send_request_and_log, (part, file))
                tasks.append(task)

            for task in tasks:
                task.get()


if __name__ == "__main__":
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1
    FILE_NAME_REQUEST = "request.txt"
    FILE_NAME_PAYLOAD = "payload.txt"
    FILE_NAME_LOG = "log.txt"
    FUZZ_KEYWORD = "FUZZ"
    HELP_MESSAGE = (
        "Available parameters:\n"
        "* r | payload from range\n"
        "* f | payload from file"
    )
    ALLOWED_PARAMETERS = [
        "r",
        "f",
    ]

    clear_screen()
    request_eval_string = get_request_eval_string()
    payload_choice = input_payload_choice()
    if payload_choice == "r":
        payload = input_range()
    elif payload_choice == "f":
        payload = input_file()
    fuzz(request_eval_string, payload)
    input("\nPress 'Enter' to continue...")
