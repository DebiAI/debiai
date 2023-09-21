from configparser import ConfigParser
from termcolor import colored

import os, json

config_path = "config/config.ini"
config_parser = ConfigParser()

config = {}


def set_config_value(section, key, value):
    global config

    if section in config and key in config[section]:
        if config[section][key] != value:
            # The default value is different from the one in the config file
            config[section][key] = value

            print(
                "Overriding "
                + colored(section + " / " + key, "yellow")
                + " with value "
                + colored(value, "yellow")
            )


def init_config():
    global config

    print("===================== CONFIG =======================")

    # Default config
    config = {
        "DATA_PROVIDERS_CONFIG": {
            "creation": True,
            "deletion": True,
            "web_data_provider_cache": True,
            "web_data_provider_cache_duration": 120,
        },
        "PYTHON_MODULE_DATA_PROVIDER": {
            "enabled": True,
            "allow_create_projects": True,
            "allow_delete_projects": True,
            "allow_create_selections": True,
            "allow_delete_selections": True,
            "allow_create_models": True,
            "allow_delete_models": True,
            "allow_insert_results": True,
        },
        "WEB_DATA_PROVIDERS": {
            # "name": "url"
        },
        "ALGO_PROVIDERS_CONFIG": {
            "enable_integrated": True,
            "creation": True,
            "deletion": True,
        },
        "ALGO_PROVIDERS": {
            # "name": "url"
        },
        "EXPORT_METHODS_CONFIG": {
            "creation": True,
            "deletion": True,
        },
        "EXPORT_METHODS": {
            # "name": "type, param1, param2, ..."
        },
    }

    # First, read the config file
    config_parser.read(config_path)

    for section in config.keys():
        if section not in config_parser.sections():
            print("Section '" + section + "' not found, using default values")
            continue

        for key in config[section].keys():
            if key not in config_parser[section]:
                print(
                    "Key "
                    + colored(key, "yellow")
                    + " not found in section "
                    + colored(section, "yellow")
                    + ", using default value"
                )
                continue

            # Deal with booleans
            if type(config[section][key]) == bool:
                if str.lower(config_parser[section][key]) == "false":
                    set_config_value(section, key, False)
                elif str.lower(config_parser[section][key]) == "true":
                    set_config_value(section, key, True)
                else:
                    print(
                        "Invalid boolean value for "
                        + colored(key, "yellow")
                        + ", using default value"
                    )
                    continue

            # Deal with integers
            elif type(config[section][key]) == int:
                try:
                    set_config_value(section, key, int(config_parser[section][key]))
                except ValueError:
                    print(
                        "Invalid integer value for "
                        + colored(key, "yellow")
                        + ", using default value"
                    )
                    continue

            # Deal with strings
            elif type(config[section][key]) == str:
                set_config_value(section, key, str(config_parser[section][key]))

        # Deal with specific cases
        # Web data-providers
        if section == "WEB_DATA_PROVIDERS":
            for data_provider in config_parser[section]:
                url = config_parser[section][data_provider]
                print(
                    "Adding Web data-provider "
                    + colored(data_provider, "yellow")
                    + " with url "
                    + colored(url, "yellow")
                )

                config["WEB_DATA_PROVIDERS"][data_provider] = url

        # Algo-providers
        if section == "ALGO_PROVIDERS":
            for algo_provider in config_parser[section]:
                url = config_parser[section][algo_provider]
                print(
                    "Adding AlgoProvider "
                    + colored(algo_provider, "yellow")
                    + " with url "
                    + colored(url, "yellow")
                )

                config["ALGO_PROVIDERS"][algo_provider] = url

        # Export methods
        if section == "EXPORT_METHODS":
            for export_method in config_parser[section]:
                type_and_parameters = config_parser[section][export_method]
                print(
                    "Adding export method "
                    + colored(export_method, "yellow")
                    + " with type and parameters "
                    + colored(type_and_parameters, "yellow")
                )

                config["EXPORT_METHODS"][export_method] = type_and_parameters

    print("done")
    exit()

    for section in config_parser.sections():
        # Data providers config
        if section == "DATA_PROVIDERS_CONFIG":
            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: Data Providers creation disabled")
                    config["DATA_PROVIDERS_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: Data Providers deletion disabled")
                    config["DATA_PROVIDERS_CONFIG"]["deletion"] = False

            if "web_data_provider_cache" in config_parser[section]:
                if (
                    str.lower(config_parser[section]["web_data_provider_cache"])
                    == "false"
                ):
                    print("Config file: Web Data Provider cache disabled")
                    config["DATA_PROVIDERS_CONFIG"]["web_data_provider_cache"] = False

            if "web_data_provider_cache_duration" in config_parser[section]:
                try:
                    config["DATA_PROVIDERS_CONFIG"][
                        "web_data_provider_cache_duration"
                    ] = int(config_parser[section]["web_data_provider_cache_duration"])
                except ValueError:
                    print(
                        "Config file: Invalid Web Data Provider cache duration,",
                        "defaulting to 120 seconds",
                    )

            continue

        if section == "PYTHON_MODULE_DATA_PROVIDER":
            if "enabled" in config_parser[section]:
                if str.lower(config_parser[section]["enabled"]) == "false":
                    print("Config file: Python Module Data Provider disabled")
                    config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = False
                elif str.lower(config_parser[section]["enabled"]) == "true":
                    print("Config file: Python Module Data Provider enabled")
                    config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = True
            continue

        if section == "WEB_DATA_PROVIDERS":
            for data_provider in config_parser[section]:
                print(
                    "Config file: detected data provider '"
                    + data_provider
                    + "' from config file"
                )
                config["WEB_DATA_PROVIDERS"][data_provider] = config_parser[section][
                    data_provider
                ]
            continue

        # AlgoProvider
        if section == "ALGO_PROVIDERS_CONFIG":
            if "enable_integrated" in config_parser[section]:
                if str.lower(config_parser[section]["enable_integrated"]) == "false":
                    print("Config file: Integrated AlgoProvider disabled")
                    config["ALGO_PROVIDERS_CONFIG"]["enable_integrated"] = False

            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: AlgoProvider creation disabled")
                    config["ALGO_PROVIDERS_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: AlgoProvider deletion disabled")
                    config["ALGO_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        if section == "ALGO_PROVIDERS":
            for algo_provider in config_parser[section]:
                print(
                    "Config file: detected AlgoProvider '"
                    + algo_provider
                    + "' from config file"
                )
                config["ALGO_PROVIDERS"][algo_provider] = config_parser[section][
                    algo_provider
                ]
            continue

        # Export methods
        if section == "EXPORT_METHODS_CONFIG":
            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: Export method creation disabled")
                    config["EXPORT_METHODS_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: Export method deletion disabled")
                    config["EXPORT_METHODS_CONFIG"]["deletion"] = False
            continue

        if section == "EXPORT_METHODS":
            for export_method in config_parser[section]:
                print(
                    "Config file: detected export method '"
                    + export_method
                    + "' from config file"
                )
                config["EXPORT_METHODS"][export_method] = config_parser[section][
                    export_method
                ]
            continue

        print("Config section '" + section + "' not recognized, skipping")

    # Then deal with environment variables
    for env_var in os.environ:
        # Deal with DATA_PROVIDERS in env variables
        if env_var == "DEBIAI_DATA_PROVIDERS_CREATION_ENABLED":
            # Env var format: DEBIAI_DATA_PROVIDERS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Data Providers creation disabled")
                config["DATA_PROVIDERS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_DATA_PROVIDERS_DELETION_ENABLED":
            # Env var format: DEBIAI_DATA_PROVIDERS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Data Providers deletion disabled")
                config["DATA_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        # Deal with PYTHON_MODULE_DATA_PROVIDER in env variables
        if env_var == "DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED":
            # Env var format: DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Python Module Data Provider disabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = False
            elif str.lower(os.environ[env_var]) == "true":
                print("Environment variables: Python Module Data Provider enabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = True
            continue

        # Deal with Data Providers in env variables
        if env_var == "DEBIAI_WEB_DATA_PROVIDERS_CACHE_ENABLED":
            # Env var format: DEBIAI_WEB_DATA_PROVIDERS_CACHE_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Web Data Provider cache disabled")
                config["DATA_PROVIDERS_CONFIG"]["web_data_provider_cache"] = False
            continue

        if env_var == "DEBIAI_WEB_DATA_PROVIDERS_CACHE_DURATION":
            # Env var format: DEBIAI_WEB_DATA_PROVIDERS_CACHE_DURATION=<duration>
            try:
                config["DATA_PROVIDERS_CONFIG"][
                    "web_data_provider_cache_duration"
                ] = int(os.environ[env_var])
            except ValueError:
                print(
                    "Environment variables: Invalid Web Data Provider cache duration,",
                    "defaulting to 120 seconds",
                )
            continue

        if "DEBIAI_WEB_DATA_PROVIDER" in env_var:
            # Env var format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 5:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>")
                continue

            data_provider_name = env_var.split("_")[4]
            data_provider_url = os.environ[env_var]

            if len(data_provider_name) == 0:
                print(
                    "Environment variables: invalid data provider name '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>")
                continue

            print(
                "Environment variables: detected Web data provider '"
                + data_provider_name
                + "' from environment variables"
            )

            config["WEB_DATA_PROVIDERS"][data_provider_name] = data_provider_url

        # Deal with AlgoProvider in env variables
        if env_var == "DEBIAI_ALGO_PROVIDERS_ENABLE_INTEGRATED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_ENABLE_INTEGRATED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Integrated Data Providers disabled")
                config["DATA_PROVIDERS_CONFIG"]["enable_integrated"] = False
            continue

        if env_var == "DEBIAI_ALGO_PROVIDERS_CREATION_ENABLED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoProvider creation disabled")
                config["ALGO_PROVIDERS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_ALGO_PROVIDERS_DELETION_ENABLED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoProvider deletion disabled")
                config["ALGO_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        # Deal with AlgoProvider list in env variables
        if "DEBIAI_ALGO_PROVIDER" in env_var:
            # Env var format: DEBIAI_ALGO_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 4:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_PROVIDER_<name>=<url>")
                continue

            algo_provider_name = env_var.split("_")[3]
            algo_provider_url = os.environ[env_var]

            if len(algo_provider_name) == 0:
                print(
                    "Environment variables: invalid AlgoProvider name '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_PROVIDER_<name>=<url>")
                continue

            print(
                "Environment variables: detected AlgoProvider '"
                + algo_provider_name
                + "' from environment variables"
            )

            config["ALGO_PROVIDERS"][algo_provider_name] = algo_provider_url

        # Deal with Export Methods in env variables
        if env_var == "DEBIAI_EXPORT_METHODS_CREATION_ENABLED":
            # Env var format: DEBIAI_EXPORT_METHODS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Export method creation disabled")
                config["EXPORT_METHODS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_EXPORT_METHODS_DELETION_ENABLED":
            # Env var format: DEBIAI_EXPORT_METHODS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Export method deletion disabled")
                config["EXPORT_METHODS_CONFIG"]["deletion"] = False
            continue

        # Deal with Export Methods list in env variables
        if "DEBIAI_EXPORT_METHOD_" in env_var:
            # Env var format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
            if len(env_var.split("_")) != 4:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            export_method_name = env_var.split("_")[3]
            export_method_type_and_parameters = os.environ[env_var]

            if len(export_method_name) == 0:
                print(
                    "Environment variables: Invalid export method name "
                    + env_var
                    + ", skipping"
                )
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            print(
                "Environment variables: Detected export method '"
                + export_method_name
                + "' from environment variables"
            )

            config["EXPORT_METHODS"][
                export_method_name
            ] = export_method_type_and_parameters

    print("Config loaded")
    print(json.dumps(config, sort_keys=True, indent=4))


def get_config():
    return config
