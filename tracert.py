import io
import socket
import struct
import sys


class FileFlush(io.FileIO):
    def __init__(self, file):
        self.file = file

    def write(self, data):
        self.file.write(data)
        self.file.flush()


sys.stdout = FileFlush(sys.stdout)


def main(ip_or_name):
    port = 57227

    ip = None
    try:
        # If ip_or_name contains destination ip, gethostbyname() will return it
        ip = socket.gethostbyname(ip_or_name)
    except socket.error:
        print()
        exit()

    max_route = 30
    ttl = 1
    while True:
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        timeout = struct.pack("11", 5, 0)
        receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

        receive_socket.bind(("", port))
        sys.stdout.write(" %d   " % ttl)
        send_socket.sendto(bytes("", "utf-8"), (ip_or_name, port))

        current_ip = None
        current_name = None
        interim_point = False
        attempts = 3
        while not interim_point and attempts > 0:
            try:
                current_ip = receive_socket.recvfrom(512)[1][0]
                interim_point = True

                try:
                    current_name = socket.gethostbyaddr(current_ip)[0]
                except socket.error:
                    current_name = current_ip
            except socket.error:
                attempts -= 1
                sys.stdout.write("* ")

        send_socket.close()
        receive_socket.close()

        if not interim_point:
            pass

        if current_ip is not None:
            current_host = "%s (%s)" % (current_name, current_ip)
        else:
            current_host = ""
        sys.stdout.write("%s\n" % current_host)

        ttl += 1

        if current_ip == ip or ttl > max_route:
            break


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Only one argument is expected")
        exit()
