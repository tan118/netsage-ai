import ipaddress

def check_duplicate_ips(devices):
    """
    Check whether multiple devices use the same IP address.
    """
    seen = {}
    problems = []

    for device, info in devices.items():
        ip = info["ip"]

        if ip in seen:
            problems.append(
                f"Duplicate IP {ip}: {device} and {seen[ip]}"
            )
        else:
            seen[ip] = device

    return problems


def check_subnet_masks(devices):
    """
    Check whether IP addresses and subnet masks form valid networks.
    """
    problems = []

    for device, info in devices.items():
        ip = info["ip"]
        mask = info["mask"]

        try:
            ipaddress.IPv4Network(
                f"{ip}/{mask}",
                strict=False
            )
        except ValueError:
            problems.append(
                f"Invalid IP/mask combination on {device}: "
                f"{ip} / {mask}"
            )

    return problems


def check_gateways(devices):
    """
    Check whether a device's gateway belongs to the same subnet.
    """
    problems = []

    for device, info in devices.items():
        ip = info["ip"]
        mask = info["mask"]
        gateway = info["gateway"]

        try:
            network = ipaddress.IPv4Network(
                f"{ip}/{mask}",
                strict=False
            )

            if gateway and ipaddress.IPv4Address(gateway) not in network:
                problems.append(
                    f"Gateway mismatch on {device}: "
                    f"{gateway} is outside {network}"
                )

        except ValueError:
            problems.append(
                f"Unable to validate gateway for {device}"
            )

    return problems


def check_interfaces(interfaces):
    """
    Detect interfaces that are administratively or operationally down.
    """
    problems = []

    for interface, status in interfaces.items():
        if status.lower() in ["down", "administratively down"]:
            problems.append(
                f"Interface {interface} is {status}"
            )

    return problems


def check_vlans(required_vlans, existing_vlans):
    """
    Detect VLANs that are required but do not exist.
    """
    problems = []

    for vlan in required_vlans:
        if vlan not in existing_vlans:
            problems.append(
                f"Missing VLAN: {vlan}"
            )

    return problems


def check_routes(required_routes, routing_table):
    """
    Detect required networks that are missing from the routing table.
    """
    problems = []

    for route in required_routes:
        if route not in routing_table:
            problems.append(
                f"Missing route: {route}"
            )

    return problems


def run_all_checks(test_case):
    """
    Run all deterministic checks for a troubleshooting case.
    """

    results = {}

    results["duplicate_ips"] = check_duplicate_ips(
        test_case.get("devices", {})
    )

    results["subnet_masks"] = check_subnet_masks(
        test_case.get("devices", {})
    )

    results["gateways"] = check_gateways(
        test_case.get("devices", {})
    )

    results["interfaces"] = check_interfaces(
        test_case.get("interfaces", {})
    )

    results["vlans"] = check_vlans(
        test_case.get("required_vlans", []),
        test_case.get("existing_vlans", [])
    )

    results["routes"] = check_routes(
        test_case.get("required_routes", []),
        test_case.get("routing_table", [])
    )

    return results


if __name__ == "__main__":

    # Sample troubleshooting case
    sample_case = {

        "devices": {
            "PC-A": {
                "ip": "192.168.10.10",
                "mask": "255.255.255.0",
                "gateway": "192.168.20.1"
            },

            "PC-B": {
                "ip": "192.168.10.10",
                "mask": "255.255.255.0",
                "gateway": "192.168.10.1"
            }
        },

        "interfaces": {
            "Fa0/1": "up",
            "Fa0/2": "administratively down"
        },

        "required_vlans": [10, 20, 30],
        "existing_vlans": [10, 20],

        "required_routes": [
            "192.168.30.0/24",
            "192.168.40.0/24"
        ],

        "routing_table": [
            "192.168.30.0/24"
        ]
    }

    results = run_all_checks(sample_case)

    print("\n===== NETSAGE AI RULE CHECKER =====\n")

    for check, problems in results.items():

        print(f"{check.upper()}:")

        if problems:
            for problem in problems:
                print(f"  [!] {problem}")
        else:
            print("  [OK] No problems detected.")

        print()