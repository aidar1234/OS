#!/usr/bin/python3

import os
import signal

import select

produced = 0


def signal_handler(sign, frame):
    global produced
    if sign == signal.SIGUSR1:
        print(f"Produced: {produced}")


def main():
    pid = os.getpid()
    print(f"Started controller with PID: {pid}", flush=True)
    global produced
    signal.signal(signal.SIGUSR1, signal_handler)

    pipe10, pipe02, pipe20 = os.pipe(), os.pipe(), os.pipe()

    p1 = os.fork()

    if p1 == 0:  # Child process P1
        os.close(pipe10[0])
        os.dup2(pipe10[1], 1)
        os.execv("./producer.py", [' '])
    else:  # Parent process P0
        os.close(pipe10[1])
        p2 = os.fork()

        if p2 == 0:  # Child process P2
            os.close(pipe02[1])
            os.close(pipe20[0])
            os.dup2(pipe02[0], 0)
            os.dup2(pipe20[1], 1)
            os.execl("/usr/bin/bc", "bc")
        else:  # Parent process P0
            os.close(pipe02[0])
            os.close(pipe20[1])

            results = []
            while True:
                rlist, _, _ = select.select([pipe10[0]], [], [], 1)
                if rlist:
                    expression = os.read(pipe10[0], 100).decode("utf-8").strip()
                    if not expression:
                        break

                    os.write(pipe02[1], expression.encode("utf-8") + b"\n")
                    produced += 1
                    result = os.read(pipe20[0], 100).decode("utf-8").strip()
                    results.append((expression, result))

                for expression, result in results:
                    print(f"{expression} = {result}")
                results = []


if __name__ == "__main__":
    main()

