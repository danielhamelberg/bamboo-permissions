"""
# Bamboo Access


Python class to collect user and group access information for Atlassian Bamboo Global permissions, Build plan permissions, Project permissions, Deployment permissions, Deployment project permissions, Deployment environment permissions.


1. At the Global level, the permission keys are: Access, Create, Create repository, Restricted admin, Admin.
2. At the Build Plan level, the permission keys are: View, Edit, View configuration,Build, Clone, Admin.
3. At the Projects level, the permission keys are: Create plan, Admin.
4. At the Deployment projects level, the permission keys are: Create plan, Admin.
5. At the Deployment environments level, the permission keys are: View, Edit, Deploy.

Prerequisites
What things you need to install the software and how to install them
- Python 3.6.5
- Bamboo
- Pandas
- PyYaml
"""

import pandas as pd
import yaml
import os
import sys
import logging
import argparse
import time
import datetime
import re

from atlassian import Bamboo as bamboo

class BambooAccess:
    """
    Class to collect user and group access information for Atlassian Bamboo (version 6.8) Global permissions, Build plan permissions, Project permissions, Deployment permissions, Deployment project permissions, Deployment environment permissions.
    """
    def __init__(self, bamboo_url, bamboo_user, bamboo_password, bamboo_log_file, bamboo_log_level):
        """
        Initialize the class with the Bamboo URL, user, password, log file and log level.
        :param bamboo_url: Bamboo URL
        :param bamboo_user: Bamboo user
        :param bamboo_password: Bamboo password
        :param bamboo_log_file: Bamboo log file
        :param bamboo_log_level: Bamboo log level
        """
        self.bamboo_url = bamboo_url
        self.bamboo_user = bamboo_user
        self.bamboo_password = bamboo_password
        self.bamboo_log_file = bamboo_log_file
        self.bamboo_log_level = bamboo_log_level
        self.bamboo_client = bamboo.Bamboo(self.bamboo_url, self.bamboo_user, self.bamboo_password)
        self.bamboo_client.logger.setLevel(self.bamboo_log_level)
        self.bamboo_client.logger.addHandler(logging.FileHandler(self.bamboo_log_file))
        self.bamboo_client.logger.info("Bamboo client initialized")

    def get_global_permissions(self):
        """
        Get the global permissions for all users and groups.
        :return: Global permissions for all users and groups
        """
        global_permissions = self.bamboo_client.get_global_permissions()
        return global_permissions

    def get_build_plan_permissions(self):
        """
        Get the build plan permissions for all users and groups.
        :return: Build plan permissions for all users and groups
        """
        build_plan_permissions = self.bamboo_client.get_build_plan_permissions()
        return build_plan_permissions

    def get_project_permissions(self):
        """
        Get the project permissions for all users and groups.
        :return: Project permissions for all users and groups
        """
        project_permissions = self.bamboo_client.get_project_permissions()
        return project_permissions

    def get_deployment_permissions(self):
        """
        Get the deployment permissions for all users and groups.
        :return: Deployment permissions for all users and groups
        """
        deployment_permissions = self.bamboo_client.get_deployment_permissions()
        return deployment_permissions

    def get_deployment_project_permissions(self):
        """
        Get the deployment project permissions for all users and groups.
        :return: Deployment project permissions for all users and groups
        """
        deployment_project_permissions = self.bamboo_client.get_deployment_project_permissions()
        return deployment_project_permissions

    def get_deployment_environment_permissions(self):
        """
        Get the deployment environment permissions for all users and groups.
        :return: Deployment environment permissions for all users and groups
        """
        deployment_environment_permissions = self.bamboo_client.get_deployment_environment_permissions()
        return deployment_environment_permissions

    def get_all_permissions(self):
        """
        Get all permissions for all users and groups.
        :return: All permissions for all users and groups
        """
        global_permissions = self.get_global_permissions()
        build_plan_permissions = self.get_build_plan_permissions()
        project_permissions = self.get_project_permissions()
        deployment_permissions = self.get_deployment_permissions()
        deployment_project_permissions = self.get_deployment_project_permissions()
        deployment_environment_permissions = self.get_deployment_environment_permissions()
        return global_permissions, build_plan_permissions, project_permissions, deployment_permissions, deployment_project_permissions, deployment_environment_permissions

    def get_all_permissions_df(self):
        """
        Get all permissions for all users and groups in a dataframe.
        :return: All permissions for all users and groups in a dataframe
        """
        global_permissions, build_plan_permissions, project_permissions, deployment_permissions, deployment_project_permissions, deployment_environment_permissions = self.get_all_permissions()
        global_permissions_df = pd.DataFrame(global_permissions)
        build_plan_permissions_df = pd.DataFrame(build_plan_permissions)
        project_permissions_df = pd.DataFrame(project_permissions)
        deployment_permissions_df = pd.DataFrame(deployment_permissions)
        deployment_project_permissions_df = pd.DataFrame(deployment_project_permissions)
        deployment_environment_permissions_df = pd.DataFrame(deployment_environment_permissions)
        return global_permissions_df, build_plan_permissions_df, project_permissions_df, deployment_permissions_df, deployment_project_permissions_df, deployment_environment_permissions_df

    def get_all_permissions_df_yaml(self):
        """
        Get all permissions for all users and groups in a dataframe and write to a YAML file.
        :return: All permissions for all users and groups in a dataframe and write to a YAML file
        """
        global_permissions_df, build_plan_permissions_df, project_permissions_df, deployment_permissions_df, deployment_project_permissions_df, deployment_environment_permissions_df = self.get_all_permissions_df()
        global_permissions_df_yaml = global_permissions_df.to_dict(orient='records')
        build_plan_permissions_df_yaml = build_plan_permissions_df.to_dict(orient='records')
        project_permissions_df_yaml = project_permissions_df.to_dict(orient='records')
        deployment_permissions_df_yaml = deployment_permissions_df.to_dict(orient='records')
        deployment_project_permissions_df_yaml = deployment_project_permissions_df.to_dict(orient='records')
        deployment_environment_permissions_df_yaml = deployment_environment_permissions_df.to_dict(orient='records')
        return global_permissions_df_yaml, build_plan_permissions_df_yaml, project_permissions_df_yaml, deployment_permissions_df_yaml, deployment_project_permissions_df_yaml, deployment_environment_permissions_df_yaml

    def write_all_permissions_df_yaml(self, output_file):
        """
        Write all permissions for all users and groups in a dataframe to a YAML file.
        :param output_file: Output file
        :return: All permissions for all users and groups in a dataframe and write to a YAML file
        """
        global_permissions_df_yaml, build_plan_permissions_df_yaml, project_permissions_df_yaml, deployment_permissions_df_yaml, deployment_project_permissions_df_yaml, deployment_environment_permissions_df_yaml = self.get_all_permissions_df_yaml()
        with open(output_file, 'w') as outfile:
            yaml.dump({'global_permissions': global_permissions_df_yaml, 'build_plan_permissions': build_plan_permissions_df_yaml, 'project_permissions': project_permissions_df_yaml, 'deployment_permissions': deployment_permissions_df_yaml, 'deployment_project_permissions': deployment_project_permissions_df_yaml, 'deployment_environment_permissions': deployment_environment_permissions_df_yaml}, outfile, default_flow_style=False)
        return global_permissions_df_yaml, build_plan_permissions_df_yaml, project_permissions_df_yaml, deployment_permissions_df_yaml, deployment_project_permissions_df_yaml, deployment_environment_permissions_df_yaml

if __name__ == '__main__':
    bamboo = BambooAccess()
    bamboo.write_all_permissions_df_yaml('permissions.yaml')
