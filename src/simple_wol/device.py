"""
Device class for representing network devices that can be woken up.
"""

from typing import Dict


class Device:
    """Represents a network device that can be woken up."""
    
    def __init__(self, name: str, mac_address: str, ip_address: str = "", port: int = 9):
        """
        Initialize a Device.
        
        Args:
            name: Friendly name for the device
            mac_address: MAC address of the device
            ip_address: IP address (optional, uses broadcast if empty)
            port: UDP port for Wake-on-LAN (default: 9)
        """
        self.name = name
        self.mac_address = mac_address.upper()
        self.ip_address = ip_address
        self.port = port
    
    def to_dict(self) -> Dict:
        """Convert device to dictionary for serialization."""
        return {
            'name': self.name,
            'mac_address': self.mac_address,
            'ip_address': self.ip_address,
            'port': self.port
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Device':
        """Create device from dictionary."""
        return cls(
            name=data['name'],
            mac_address=data['mac_address'],
            ip_address=data.get('ip_address', ''),
            port=data.get('port', 9)
        )
    
    def __str__(self) -> str:
        """String representation of the device."""
        return f"Device(name='{self.name}', mac='{self.mac_address}', ip='{self.ip_address}', port={self.port})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the device."""
        return self.__str__()
