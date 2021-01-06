#!/usr/bin/env python3

import os
import shutil
import sys

GIT_CREDENTIAL_DIR = "/root/"
GIT_CREDENTIAL_FILE_VAR = 'CT_GIT_CREDENTIAL_FILE'
GIT_CREDENTIAL_VALUE_VAR = 'CT_GIT_CREDENTIAL_VALUE'
GIT_CREDENTIAL_FILE_NAME = '.git-credentials'

GIT_CONFIG_DIR = "/root/"
GIT_CONFIG_FILE_VAR = 'CT_GIT_CONFIG_FILE'
GIT_CONFIG_VALUE_VAR = 'CT_GIT_CONFIG_VALUE'
GIT_CONFIG_FILE_NAME = '.gitconfig'


def log(message: str) -> None:
    print(f"[install-git-credential] {message}", file=sys.stderr)


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

    if git_credential_value_from_var:
        # write value to file
        with open(git_credential_file_path, 'w') as git_credential_file:
            git_credential_file.write(git_credential_file_from_var)
    elif git_credential_file_from_var:
        shutil.copyfile(git_credential_file_from_var, git_credential_file_path)


if __name__ == '__main__':
    main(os.environ)
