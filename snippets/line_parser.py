import re

# Function to parse the configuration file
def parse_configuration(config_data):
    # Regular expression to identify the start of each interface configuration
    interface_start_regex = r"^interface\s+(\S+)"
    interface_starts = [match for match in re.finditer(interface_start_regex, config_data, re.MULTILINE)]

    # Parsing each interface configuration
    parsed_interfaces = []
    for i in range(len(interface_starts)):
        start = interface_starts[i].start()
        end = interface_starts[i + 1].start() if i + 1 < len(interface_starts) else len(config_data)
        interface_config = config_data[start:end]

        # Extracting interface name
        interface_name = re.search(r"^interface\s+(\S+)", interface_config, re.MULTILINE).group(1)

        # Extracting description if available
        description_match = re.search(r"\n\s+description\s+(.+)", interface_config, re.MULTILINE)
        description = description_match.group(1) if description_match else "No description"

        # Extracting switchport mode if available
        switchport_mode_match = re.search(r"\n\s+switchport mode (access|trunk)", interface_config, re.MULTILINE)
        switchport_mode = switchport_mode_match.group(1) if switchport_mode_match else "No switchport mode"

        parsed_interfaces.append((interface_name, description, switchport_mode))

    return parsed_interfaces

# Parsing the actual configuration data
#parsed_data = parse_configuration(config_data)


