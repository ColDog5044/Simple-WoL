"""
Wake-on-LAN network functionality.
"""

from wakeonlan import send_magic_packet
from ..device import Device


class WakeOnLanSender:
    """Handles sending Wake-on-LAN packets to devices."""
    
    @staticmethod
    def wake_device(device: Device) -> None:
        """
        Send a Wake-on-LAN packet to a device.
        
        Args:
            device: Device to wake up
            
        Raises:
            Exception: If sending the packet fails
        """
        try:
            if device.ip_address:
                send_magic_packet(device.mac_address, ip_address=device.ip_address, port=device.port)
            else:
                send_magic_packet(device.mac_address, port=device.port)
        except Exception as e:
            raise Exception(f"Failed to send Wake-on-LAN packet: {str(e)}")
    
    @staticmethod
    def wake_by_mac(mac_address: str, ip_address: str = None, port: int = 9) -> None:
        """
        Send a Wake-on-LAN packet by MAC address.
        
        Args:
            mac_address: MAC address of the device
            ip_address: Optional IP address (uses broadcast if None)
            port: UDP port (default: 9)
            
        Raises:
            Exception: If sending the packet fails
        """
        try:
            if ip_address:
                send_magic_packet(mac_address, ip_address=ip_address, port=port)
            else:
                send_magic_packet(mac_address, port=port)
        except Exception as e:
            raise Exception(f"Failed to send Wake-on-LAN packet: {str(e)}")
    
    @staticmethod
    def validate_mac_address(mac_address: str) -> bool:
        """
        Validate MAC address format.
        
        Args:
            mac_address: MAC address to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(mac_pattern, mac_address))
    
    @staticmethod
    def validate_ip_address(ip_address: str) -> bool:
        """
        Validate IP address format.
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            True if valid, False otherwise
        """
        import socket
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
