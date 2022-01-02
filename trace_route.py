import socket
import sys

from file_flush import FileFlush
from socket_utilities import init_udp_socket, init_icmp_socket


def trace_route(dest_name_or_address):
    sys.stdout = FileFlush(sys.stdout)

    port = 55555

    dest_address = None
    try:
        # If dest_name_or_address contains destination address, it will be returned
        dest_address = socket.gethostbyname(dest_name_or_address)
    except socket.error:
        print(f"{dest_name_or_address} is invalid destination name or address\nCheck it and try again")
        exit(1)

    max_route_len = 30
    time_to_live = 1

    print(f"Try to trace route to {dest_name_or_address} ({dest_address}) with max route length {max_route_len}:")

    while True:
        send_socket = init_udp_socket(time_to_live)
        receive_socket = init_icmp_socket(port)

        sys.stdout.write("%d\t" % time_to_live)
        send_socket.sendto(bytes("", "utf-8"), (dest_name_or_address, port))

        attempts = 3
        curr_name = None
        curr_address = None
        node_reached = False
        while not node_reached and attempts > 0:
            try:
                curr_address = receive_socket.recvfrom(512)[1][0]
                node_reached = True

                try:
                    curr_name = socket.gethostbyaddr(curr_address)[0]
                except socket.error:
                    pass

            except socket.error:
                attempts -= 1
                sys.stdout.write("* ")

        send_socket.close()
        receive_socket.close()

        current_host = ""
        if curr_address is not None and curr_name is not None:
            current_host = f"{curr_name} ({curr_address})"
        elif curr_address is not None:
            current_host = f"{curr_address}"
        sys.stdout.write(f"{current_host}\n")

        time_to_live += 1

        if curr_address == dest_address or time_to_live > max_route_len:
            exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        trace_route(sys.argv[1])
    else:
        print("Only one argument is expected\nCheck it and try again")
        exit(1)
