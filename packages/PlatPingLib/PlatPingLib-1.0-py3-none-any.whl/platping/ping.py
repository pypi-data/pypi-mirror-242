import subprocess
import platform

def ping_ip(ip_address):
    """
    Pings a given IP address once and returns whether the ping was successful.

    Args:
    ip_address (str): The IP address to ping.

    Returns:
    bool: True if the ping succeeds, False otherwise.
    """
    try:
        if platform.system().lower() == "windows":
            parameters = ['-n', '1', '-w', '1000']
        else:
            parameters = ['-c', '1', '-W', '1']

        response = subprocess.run(
            ['ping'] + parameters + [ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return response.returncode == 0

    except Exception as e:
        print(f"Error pinging: {e}")
        return False
