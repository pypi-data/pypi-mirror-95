import os
import boto3

from typing import Optional, Union
from flask import Flask, config
from beautifultable import BeautifulTable
from flask_environment_manager.whitelist_parser import WhitelistParser


class SsmEnvironmentManager:
    def __init__(
        self,
        app: Flask,
        paths: list = [],
        region_name: Optional[str] = None,
        decrypt: bool = False,
        config_pyfile: Optional[str] = None,
    ):
        """
        Will read the AWS SSM access details from the app.config
        :param app: The Flask app instance
        :param paths: A list of paths of the parameters in the SSM instance to read.
        :param region_name: The region of the SSM instance. This will override the app.config value if provided.
        :param decrypt: If True, SecureString parameters are automatically decrypted.
        :param config_pyfile:
        """
        self._app = app
        self._paths = paths
        self._decrypt = decrypt

        if self._app is not None:
            self._aws_access_key = self._app.config.get("AWS_SSM_ACCESS_KEY")
            self._aws_access_secret = self._app.config.get("AWS_SSM_ACCESS_SECRET")
            self._region_name = self._app.config.get("AWS_SSM_REGION")

        if region_name:
            self._region_name = region_name

        self._config_pyfile = config_pyfile

    def compare_env_and_ssm(self) -> dict:
        """
        Compare the environment to the SSM parameters.
        Prints a report in the form of a table to the console.
        Intended to be used during development.
        :returns: dict containing a list of missing parameters and a list of mismatched values
        """
        table = BeautifulTable()
        table.columns.header = [
            "OS Parameter",
            "os.environ Value",
            "SSM Value",
            "Present in both os.environ and SSM",
            "Values Match",
        ]

        missing_params = []
        mismatched_params = []
        ssm_parameters = self._get_parameters_from_paths()
        for key in os.environ.keys():
            stored_in_ssm = "YES"
            mismatch = "YES"
            if key not in ssm_parameters.keys():
                missing_params.append(key)
                stored_in_ssm = "NO"

            if ssm_parameters.get(key) != os.environ.get(key):
                mismatched_params.append(key)
                mismatch = "NO"

            table.rows.append(
                [
                    key,
                    str(os.environ.get(key)),
                    str(ssm_parameters.get(key)),
                    stored_in_ssm,
                    mismatch,
                ]
            )

        table.rows.append(
            [
                "",
                "",
                "Total NO's",
                str(len(missing_params)),
                str(len(mismatched_params)),
            ]
        )

        self._app.logger.debug(f"SSM Parameter/Current Environment Comparison\n{table}")

        return {
            "missing": missing_params,
            "mismatched": mismatched_params,
        }

    def load_into_config(self) -> None:
        """
        Load the SSM parameters into the Flask app config.
        """
        parameters = self._get_parameters_to_parse()
        WhitelistParser(self._app, parameters).parse()

    def _get_parameters_to_parse(self) -> dict:
        """
        Get parameters from SSM or from a local config file.
        :returns: A dict of parameter names and values
        """
        if self._config_pyfile:
            self._app.logger.debug(f"Reading parameters from {self._config_pyfile}")
            self._app.config.from_pyfile(self._config_pyfile, silent=False)
            parameters = dict(self._app.config)
        else:
            self._app.logger.debug(f"Reading parameters from SSM")
            parameters = self._get_parameters_from_paths()
        return parameters

    def _get_parameters_from_paths(self) -> dict:
        """
        Iterate over the paths to build a dictionary of
        parameter/value pairings.
        :returns: A dict of parameter names and values
        """
        ssm_parameters: dict = {}
        for path in self._paths:
            values = self._get_ssm_parameters(str(path))
            ssm_parameters = {**ssm_parameters, **values}
        return ssm_parameters

    def _get_ssm_parameters(self, path: str) -> dict:
        """
        Get all parameters in a given path from SSM.
        The name of the keys in the return dict is the final
        part of the parameter path, e.g '/a/param/path' will
        be stored in the dict as 'path'
        :param path: The path in SSM to read variables from
        :returns: A dict of parameter names and values.
        """
        client = boto3.client(
            "ssm",
            region_name=self._region_name,
            aws_access_key_id=self._aws_access_key,
            aws_secret_access_key=self._aws_access_secret,
        )
        more_parameters = True
        ssm_values: dict = {}
        ssm_repsonse: dict = {}
        while more_parameters:
            if ssm_repsonse.get("NextToken"):
                ssm_repsonse = client.get_parameters_by_path(
                    Path=path,
                    Recursive=True,
                    NextToken=ssm_repsonse.get("NextToken"),
                    WithDecryption=self._decrypt,
                )
            else:
                ssm_repsonse = client.get_parameters_by_path(
                    Path=path,
                    Recursive=True,
                    WithDecryption=self._decrypt,
                )

            parameters = ssm_repsonse.get("Parameters", [])
            for param in parameters:
                name = param.get("Name")
                if name:
                    path_parts = param["Name"].split("/")
                    if len(path_parts) > 0:
                        name = path_parts[-1]

                value = param.get("Value")
                ssm_values[name] = value

            if not ssm_repsonse.get("NextToken"):
                more_parameters = False

        return ssm_values
