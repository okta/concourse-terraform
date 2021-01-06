#!/usr/bin/env python3

import os
import shutil
import stat
import sys

GIT_CREDENTIAL_DIR = "~/"
GIT_CREDENTIAL_FILE_VAR = 'CT_GIT_CREDENTIAL_FILE'
GIT_CREDENTIAL_VALUE_VAR = 'CT_GIT_CREDENTIAL_VALUE'
GIT_CREDENTIAL_FILE_NAME = '.git-credentials'

GIT_CONFIG_DIR = "~/"
GIT_CONFIG_FILE_VAR = 'CT_GIT_CONFIG_FILE'
GIT_CONFIG_VALUE_VAR = 'CT_GIT_CONFIG_VALUE'
GIT_CONFIG_FILE_NAME = '.gitconfig'


def log(message: str) -> None:
    print(f"[install-git-credential] {message}", file=sys.stderr)


# def create_git_config(
#         git_credential_file_path: str,
#         git_credential_dir: str) -> None:
#     git_config_file_path = \
#         os.path.join(
#             GIT_CREDENTIAL_DIR,
#             GIT_CREDENTIAL_FILE_VAR)
#     git_config = 'StrictHostKeyChecking no\nLogLevel quiet\n'
#     if os.path.exists(git_config_file_path):
#         ssh_config += f'Host *\n    IdentityFile {ssh_key_file_path}\n'
#     with open(git_config_file_path, 'w') as ssh_config_file:
#         ssh_config_file.write(ssh_config)
#     log(f"wrote git config to: {git_config_file_path}")


def main(environment: dict, ssh_keys_dir: str = None) -> None:
    # get vars from environment
    git_config_file_from_var = environment.get(GIT_CONFIG_FILE_VAR)
    git_config_value_from_var = environment.get(GIT_CONFIG_VALUE_VAR)

    git_credential_file_from_var = environment.get(GIT_CREDENTIAL_FILE_VAR)
    git_credential_value_from_var = environment.get(GIT_CREDENTIAL_VALUE_VAR)

    # check if both are set
    if git_config_file_from_var and git_config_value_from_var:
        raise RuntimeError('cannot specify both git config file path and value')

    # check if both are set
    if git_credential_file_from_var and git_credential_value_from_var:
        raise RuntimeError('cannot specify both git credentials file path and value')

    # prep ssh key file path
    git_config_file_path = os.path.join(GIT_CONFIG_DIR, GIT_CONFIG_FILE_NAME)
    git_credential_file_path = os.path.join(GIT_CREDENTIAL_DIR, GIT_CREDENTIAL_FILE_NAME)

    if git_config_value_from_var:
        # write value to file
        with open(git_config_file_path, 'w') as git_config_file:
            git_config_file.write(git_config_value_from_var)
    elif git_config_file_from_var:
        shutil.copyfile(git_config_file_from_var, git_config_file_path)

    if git_credential_file_from_var:
        # write value to file
        with open(git_credential_file_path, 'w') as git_credential_file:
            git_credential_file.write(git_credential_file_from_var)
    elif git_credential_file_from_var:
        shutil.copyfile(git_credential_file_from_var, git_credential_file_path)


if __name__ == '__main__':
    main(os.environ)
