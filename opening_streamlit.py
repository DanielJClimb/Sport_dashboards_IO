# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:59:06 2024
"""

import subprocess
import sys
import os
import socket


def find_free_port():
    """Znajduje wolny port i zwraca go jako liczbę."""
    sock = socket.socket()
    sock.bind(('', 0))        # system przydziela wolny port
    port = sock.getsockname()[1]
    sock.close()
    return port


print("Please wait, while SCOS app is opening...")

# Znajdź wolny port
free_port = find_free_port()
print(f"Opening SCOS app on port {free_port}...")

# Ścieżka do Twojej aplikacji Streamlit
script_path = os.path.join(os.path.dirname(__file__), "titlepage.py")

# Uruchom Streamlit na znalezionym porcie
subprocess.run([
    sys.executable, "-m", "streamlit", "run", script_path,
    "--server.port", str(free_port)
])

