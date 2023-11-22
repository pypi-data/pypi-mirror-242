# Entrypoint

# TODO: make project.toml file
# just install with pip
# call it: noetic --help

# TODO: the config file will be a yaml file in the format:

    # settings:
    #     path_connector_development: ''
    #     # TODO: within the .noetic-sdk dir there will be a mocksever dir and in there the files needed for mockserver
    #     path_config_dir: '~/.noetic-sdk'
    #
    # noetic_connections:
    #   <nickname>:
    #       url: 'https://localhost'
    #       tenant: 'noetic'
    #       username: 'noetic'
    #       password: '___{{name_of_property_in_keychain}}___'
    #       api_key: 'some string'
    #       default: true


from argparse import ArgumentParser

root_parser = ArgumentParser(
    prog="noetic",
    description="""Python SDK for developing with Noetic""",
    epilog="For support, please visit https://noeticcyber.com")

# root_parser.usage = """
#     $ noetic <command> ...
#     $ noetic -v <subcommand> ...
#     """

# main_parser = root_parser.add_subparsers(
#     title="Commands",
#     metavar="",
#     dest="main"
# )

# apps_args_parser = ArgumentParser(add_help=False)

# app_cmds_parser = apps_args_parser.add_subparsers(
#     title="Commands",
#     metavar="",
#     dest="apps"
# )

# apps_init_args = ArgumentParser(add_help=False)
# apps_init_args.add_argument("-p", "--path")

# app_cmds_parser.add_parser(name="init",
#                            help="Initialise development of a Connector",
#                            parents=[apps_init_args])

# app_cmds_parser.add_parser(name="validate",
#                            help="Validate a Connector meets minimum requirements",
#                            parents=[])

# apps_install_args = ArgumentParser(add_help=False)
# apps_install_args.add_argument("-p", "--path")
# apps_install_args.add_argument("-c", "--connection", help="The nickname of the connection to use. If not specified uses the default connection. If no default, prompts the user")

# app_cmds_parser.add_parser(name="install",
#                            help="Install a Connector on Noetic from a file path or .zip file",
#                            parents=[apps_install_args])

# app_cmds_parser.add_parser(name="list",
#                            help="List all the Connectors installed in Noetic",
#                            parents=[])

# main_parser.add_parser(name="apps",
#                        help="Develop Connectors with Noetic",
#                        parents=[apps_args_parser])



# types_args_parser = ArgumentParser(add_help=False)

# types_cmds_parser = types_args_parser.add_subparsers(
#     title="Commands",
#     metavar="",
#     dest="types"
# )

# types_cmds_parser.add_parser(name="new",
#                            help="Add a new Type to Noetic",
#                            parents=[])

# main_parser.add_parser(name="types",
#                        help="Manage Types in Noetic",
#                        parents=[types_args_parser])


# config_args_parser = ArgumentParser(add_help=False)

# config_cmds_parser = config_args_parser.add_subparsers(
#     title="Commands",
#     metavar="",
#     dest="config"
# )

# config_usage = """
#     noetic config -h
#     noetic config init -t <tenant name> -u TODO
#     noetic config add
#     noetic config delete
#     noetic config default -n <connection_nickname>
# """

# config_cmds_parser.add_parser(name="init",
#                               help="Create a new '~/.noetic/.noetic_sdk_config.yaml' file",
#                               parents=[])

# # TODO: this needs the arguments:
# #   -t: tenant
# #   -u: username
# #   -url: url to noetic
# config_cmds_parser.add_parser(name="add",
#                               help="Add a new connection to the configuration file",
#                               parents=[])

# config_cmds_parser.add_parser(name="delete",
#                               help="Delete a connection from the configuration file",
#                               parents=[])

# config_cmds_parser.add_parser(name="default",
#                               help="Pick a connection that is used by default",
#                               parents=[])

# main_parser.add_parser(name="config",
#                         help="Configure your SDK with Noetic",
#                         usage=config_usage,
#                         parents=[config_args_parser])


def main():
    # print("Calling Noetic main")
    args = root_parser.parse_args()


if __name__ == "__main__":
    main()
