import sshtunnel
from django.db.backends.signals import connection_created
from django.dispatch import receiver

def start_ssh_tunnel():
    """Starts an SSH tunnel."""
    sshtunnel.SSH_TIMEOUT = 10.0
    sshtunnel.TUNNEL_TIMEOUT = 10.0

    tunnel = sshtunnel.SSHTunnelForwarder(
        # removed here
    )
    tunnel.start()
    return tunnel

# Initialize the SSH tunnel and update settings dynamically
ssh_tunnel = start_ssh_tunnel()
TUNNEL_PORT = ssh_tunnel.local_bind_port

# Stop the tunnel when the app is closed
import atexit
atexit.register(ssh_tunnel.stop)
