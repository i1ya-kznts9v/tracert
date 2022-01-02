import socket
import struct

__all__ = ["init_udp_socket", "init_icmp_socket"]


def init_udp_socket(time_to_live):
    """
    Initializes UDP socket
    """

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, time_to_live)

    return udp_socket


def init_icmp_socket(port):
    """
    Initializes ICMP socket
    """

    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    timeout = struct.pack("ll", 5, 0)
    icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

    icmp_socket.bind(("0.0.0.0", port))

    return icmp_socket
