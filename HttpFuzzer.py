# Simple http/s fuzzer with multithreading


import multiprocessing.pool

import requests


# PAYLOAD must be a sequence
URL = "http://blank.chal.imaginaryctf.org/login"
PAYLOAD = range(1, 1000)


# Change this is you need to do some work with a response
def send_request(url, fuzz_value):
    url = url.format(FUZZ=str(fuzz_value))
    response = requests.get(url)
    # if response.status_code != 500:
    print("{RESPONSE_CODE} : {URL}".format(URL=url, RESPONSE_CODE=response.status_code))


with multiprocessing.pool.ThreadPool() as pool:
    async_tasks = []

    for value in PAYLOAD:
        async_task = pool.apply_async(send_request, (URL, value))
        async_tasks.append(async_task)

    for async_task in async_tasks:
        async_task.get()
