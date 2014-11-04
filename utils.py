#!/usr/bin/python3

import subprocess

import asyncio
import tornado.concurrent


def coroutine(func):
    func = asyncio.coroutine(func)

    def decorator(*args, **kwargs):
        future = tornado.concurrent.Future()

        def future_done(f):
            try:
                future.set_result(f.result())
            except Exception as e:
                future.set_exception(e)
        asyncio.async(func(*args, **kwargs)).add_done_callback(future_done)
        return future
    return decorator


def create_self_signed_cert(CERT_FILE, KEY_FILE):

    cmd = """openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
             -subj '/C=aa/ST=aa/L=aa/O=aa/CN=aa' -keyout {0} -out {1}""".format(
        KEY_FILE, CERT_FILE
    )
    subprocess.check_call(cmd, shell=True)
