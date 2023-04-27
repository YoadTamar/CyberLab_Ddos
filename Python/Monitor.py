"""
DDoS Laboratory
Assignment of `Cyber Lab - Defense` course at Ariel-University

this file contains the implementation for `ICMP-Monitoring`.
In our lab, there are `Attacker`, `Target` and `Monitor` machines (docker-compose).
While the `Target` is under the DDoS attack from the `Attacker`, the `Monitor`
should send an ICMP (Internet-Control-Message-Protocol) request and receive an ICMP response,
it should also calculate the RTT (Round-Trip-Time) of the ping-pong.

:version: 1.2
:since: 28/04/2023
:authors: Lior Vinman & Yoad Tamar
"""


import scapy.all as scapy
import time
import sys

MONITOR_ADDR = "10.9.0.5"   # monitor machine ip address
TARGET_ADDR = "10.9.0.3"  # target machine ip address
FILE = "pings_results_p.txt"  # filename of the results file
TIMEOUT = 5  # a timeout after each ping
SUCCESS = 0  # program's success exit code
FAIL = 1  # program's failure exit code


def main():
    seq = avg = 0
    try:
        ip_header = scapy.IP(src=MONITOR_ADDR, dst=TARGET_ADDR)
        icmp_header = scapy.ICMP()
        ping_packet = (ip_header / icmp_header)

        with open(FILE, "w") as file:
            while True:
                before_send = time.time()
                scapy.sr1(ping_packet, verbose=False)
                after_send = time.time()

                avg += (after_send - before_send)

                file.write(f"{seq} {(after_send - before_send)}\n")
                file.flush()

                seq += 1

                time.sleep(TIMEOUT)

    except KeyboardInterrupt:
        print("\nStopping monitor...")

        avg /= seq
        with open(FILE, "a") as file:
            file.write(f"{avg}")
            file.flush()

        sys.exit(SUCCESS)
    except Exception as e:
        print(f"Error: {e}.")
        sys.exit(FAIL)
    finally:
        if file:
            file.close()


if __name__ == "__main__":
    main()
