import json
import pynetbox
from pprint import pprint

NETBOX_API_URL = "http://netbox.example.com"
NETBOX_API_TOKEN = "f1801f2f519ed714f24fd89b5cc63c598da711f6"
# Инициализация соединения с NetBox
nb = pynetbox.api(NETBOX_API_URL, token=NETBOX_API_TOKEN)

def get_device_info(device_name):
    # Получение устройства по имени
    device = nb.dcim.devices.get(name=device_name)

    if not device:
        print(f"Device {device_name} not found.")
        return

    # Основная информация об устройстве
    device_info = {
        "name": device.name,
        "device_type": device.device_type,
        #"device_role": device.device_role,
        "site": device.site.name,
        "status": device.status,
        "serial": device.serial,
        "asset_tag": device.asset_tag,
        "primary_ip": device.primary_ip4.address if device.primary_ip4 else None,
        "interfaces": [],
        "custom_fields": device.custom_fields,
        "oob_ip": device.oob_ip.address.split('/')[0]
    }

    # Получение интерфейсов устройства
    interfaces = nb.dcim.interfaces.filter(device_id=device.id)
    for interface in interfaces:
        interface_info = {
            "name": interface.name,
            "type": interface.type,
            "enabled": interface.enabled,
            "mac_address": interface.mac_address,
            "mtu": interface.mtu,
            "description": interface.description,
            "mode": interface.mode,
            "untagged_vlan": interface.untagged_vlan.name if interface.untagged_vlan else None,
            "tagged_vlans": [vlan.name for vlan in interface.tagged_vlans] if interface.tagged_vlans else [],
            #"ip_addresses": [ip.address for ip in interface.ip_addresses]
        }
        device_info["interfaces"].append(interface_info)

    # Печать полной информации об устройстве
    pprint(device_info)

if __name__ == "__main__":
    device_name = input("Enter the device name: ")
    get_device_info(device_name)

