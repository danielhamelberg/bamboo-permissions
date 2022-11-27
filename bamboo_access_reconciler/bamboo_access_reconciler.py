import pandas as pd
import yaml
import os
import sys
import logging
import argparse
import time
import datetime
import re

from bamboo_access import BambooAccess

from atlassian import Bamboo as bamboo

class BambooAccessReconciler:
    """
    Class to reconcile user and group access information for Atlassian Bamboo (version 6.8) Global permissions, Build plan permissions, Project permissions, Deployment permissions, Deployment project permissions, Deployment environment permissions.
    How it works:
    1. Read the current permissions from Bamboo.
    2. Read the desired permissions from a YAML file.
    3. Compare the current permissions with the desired permissions.
    4. If there are any differences, then update the permissions in Bamboo.
    """
    def __init__(self, bamboo_url, bamboo_user, bamboo_password, bamboo_log_file, bamboo_log_level, desired_permissions_file):
        """
        Initialize the class with the Bamboo URL, user, password, log file, log level and desired permissions file.
        :param bamboo_url: Bamboo URL
        :param bamboo_user: Bamboo user
        :param bamboo_password: Bamboo password
        :param bamboo_log_file: Bamboo log file
        :param bamboo_log_level: Bamboo log level
        :param desired_permissions_file: Desired permissions file
        """
        self.bamboo_url = bamboo_url
        self.bamboo_user = bamboo_user
        self.bamboo_password = bamboo_password
        self.bamboo_log_file = bamboo_log_file
        self.bamboo_log_level = bamboo_log_level
        self.desired_permissions_file = desired_permissions_file
        self.bamboo_client = bamboo.Bamboo(self.bamboo_url, self.bamboo_user, self.bamboo_password)
        self.bamboo_client.logger.setLevel(self.bamboo_log_level)
        self.bamboo_client.logger.addHandler(logging.FileHandler(self.bamboo_log_file))
        self.bamboo_client.logger.info("Bamboo client initialized")

    def get_current_permissions(self):
        """
        Get the current permissions for all users and groups.
        :return: Current permissions for all users and groups
        """
        current_permissions = BambooAccess(self.bamboo_url, self.bamboo_user, self.bamboo_password, self.bamboo_log_file, self.bamboo_log_level)
        current_permissions_df_yaml = current_permissions.write_all_permissions_df_yaml('current_permissions.yaml')
        return current_permissions_df_yaml

    def get_desired_permissions(self):
        """
        Get the desired permissions for all users and groups.
        :return: Desired permissions for all users and groups
        """
        with open(self.desired_permissions_file, 'r') as stream:
            try:
                desired_permissions_df_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return desired_permissions_df_yaml

    def get_current_permissions_df(self):
        """
        Get the current permissions for all users and groups in a dataframe.
        :return: Current permissions for all users and groups in a dataframe
        """
        current_permissions_df_yaml = self.get_current_permissions()
        global_permissions_df_yaml = current_permissions_df_yaml[0]
        build_plan_permissions_df_yaml = current_permissions_df_yaml[1]
        project_permissions_df_yaml = current_permissions_df_yaml[2]
        deployment_permissions_df_yaml = current_permissions_df_yaml[3]
        deployment_project_permissions_df_yaml = current_permissions_df_yaml[4]
        deployment_environment_permissions_df_yaml = current_permissions_df_yaml[5]
        global_permissions_df = pd.DataFrame(global_permissions_df_yaml)
        build_plan_permissions_df = pd.DataFrame(build_plan_permissions_df_yaml)
        project_permissions_df = pd.DataFrame(project_permissions_df_yaml)
        deployment_permissions_df = pd.DataFrame(deployment_permissions_df_yaml)
        deployment_project_permissions_df = pd.DataFrame(deployment_project_permissions_df_yaml)
        deployment_environment_permissions_df = pd.DataFrame(deployment_environment_permissions_df_yaml)
        return global_permissions_df, build_plan_permissions_df, project_permissions_df, deployment_permissions_df, deployment_project_permissions_df, deployment_environment_permissions_df

    def get_desired_permissions_df(self):
        """
        Get the desired permissions for all users and groups in a dataframe.
        :return: Desired permissions for all users and groups in a dataframe
        """
        desired_permissions_df_yaml = self.get_desired_permissions()
        global_permissions_df_yaml = desired_permissions_df_yaml['global_permissions']
        build_plan_permissions_df_yaml = desired_permissions_df_yaml['build_plan_permissions']
        project_permissions_df_yaml = desired_permissions_df_yaml['project_permissions']
        deployment_permissions_df_yaml = desired_permissions_df_yaml['deployment_permissions']
        deployment_project_permissions_df_yaml = desired_permissions_df_yaml['deployment_project_permissions']
        deployment_environment_permissions_df_yaml = desired_permissions_df_yaml['deployment_environment_permissions']
        global_permissions_df = pd.DataFrame(global_permissions_df_yaml)
        build_plan_permissions_df = pd.DataFrame(build_plan_permissions_df_yaml)
        project_permissions_df = pd.DataFrame(project_permissions_df_yaml)
        deployment_permissions_df = pd.DataFrame(deployment_permissions_df_yaml)
        deployment_project_permissions_df = pd.DataFrame(deployment_project_permissions_df_yaml)
        deployment_environment_permissions_df = pd.DataFrame(deployment_environment_permissions_df_yaml)
        return global_permissions_df, build_plan_permissions_df, project_permissions_df, deployment_permissions_df, deployment_project_permissions_df, deployment_environment_permissions_df

    def get_permissions_diff(self):
        """
        Get the difference between the current permissions and the desired permissions.
        :return: Difference between the current permissions and the desired permissions
        """
        current_permissions_df = self.get_current_permissions_df()
        desired_permissions_df = self.get_desired_permissions_df()
        global_permissions_diff = current_permissions_df[0].merge(desired_permissions_df[0], indicator=True, how='outer')
        build_plan_permissions_diff = current_permissions_df[1].merge(desired_permissions_df[1], indicator=True, how='outer')
        project_permissions_diff = current_permissions_df[2].merge(desired_permissions_df[2], indicator=True, how='outer')
        deployment_permissions_diff = current_permissions_df[3].merge(desired_permissions_df[3], indicator=True, how='outer')
        deployment_project_permissions_diff = current_permissions_df[4].merge(desired_permissions_df[4], indicator=True, how='outer')
        deployment_environment_permissions_diff = current_permissions_df[5].merge(desired_permissions_df[5], indicator=True, how='outer')
        return global_permissions_diff, build_plan_permissions_diff, project_permissions_diff, deployment_permissions_diff, deployment_project_permissions_diff, deployment_environment_permissions_diff

    def get_permissions_diff_df(self):
        """
        Get the difference between the current permissions and the desired permissions in a dataframe.
        :return: Difference between the current permissions and the desired permissions in a dataframe
        """
        permissions_diff = self.get_permissions_diff()
        global_permissions_diff = permissions_diff[0]
        build_plan_permissions_diff = permissions_diff[1]
        project_permissions_diff = permissions_diff[2]
        deployment_permissions_diff = permissions_diff[3]
        deployment_project_permissions_diff = permissions_diff[4]
        deployment_environment_permissions_diff = permissions_diff[5]
        return global_permissions_diff, build_plan_permissions_diff, project_permissions_diff, deployment_permissions_diff, deployment_project_permissions_diff, deployment_environment_permissions_diff

    def get_permissions_diff_df_yaml(self):
        """
        Get the difference between the current permissions and the desired permissions in a dataframe and write to a YAML file.
        :return: Difference between the current permissions and the desired permissions in a dataframe and write to a YAML file
        """
        permissions_diff_df = self.get_permissions_diff_df()
        global_permissions_diff_df = permissions_diff_df[0]
        build_plan_permissions_diff_df = permissions_diff_df[1]
        project_permissions_diff_df = permissions_diff_df[2]
        deployment_permissions_diff_df = permissions_diff_df[3]
        deployment_project_permissions_diff_df = permissions_diff_df[4]
        deployment_environment_permissions_diff_df = permissions_diff_df[5]
        global_permissions_diff_df_yaml = global_permissions_diff_df.to_dict(orient='records')
        build_plan_permissions_diff_df_yaml = build_plan_permissions_diff_df.to_dict(orient='records')
        project_permissions_diff_df_yaml = project_permissions_diff_df.to_dict(orient='records')
        deployment_permissions_diff_df_yaml = deployment_permissions_diff_df.to_dict(orient='records')
        deployment_project_permissions_diff_df_yaml = deployment_project_permissions_diff_df.to_dict(orient='records')
        deployment_environment_permissions_diff_df_yaml = deployment_environment_permissions_diff_df.to_dict(orient='records')
        return global_permissions_diff_df_yaml, build_plan_permissions_diff_df_yaml, project_permissions_diff_df_yaml, deployment_permissions_diff_df_yaml, deployment_project_permissions_diff_df_yaml, deployment_environment_permissions_diff_df_yaml

    def write_permissions_diff_df_yaml(self, output_file):
        """
        Write the difference between the current permissions and the desired permissions in a dataframe to a YAML file.
        :param output_file: Output file
        :return: Difference between the current permissions and the desired permissions in a dataframe and write to a YAML file
        """
        permissions_diff_df_yaml = self.get_permissions_diff_df_yaml()
        global_permissions_diff_df_yaml = permissions_diff_df_yaml[0]
        build_plan_permissions_diff_df_yaml = permissions_diff_df_yaml[1]
        project_permissions_diff_df_yaml = permissions_diff_df_yaml[2]
        deployment_permissions_diff_df_yaml = permissions_diff_df_yaml[3]
        deployment_project_permissions_diff_df_yaml = permissions_diff_df_yaml[4]
        deployment_environment_permissions_diff_df_yaml = permissions_diff_df_yaml[5]
        with open(output_file, 'w') as outfile:
            yaml.dump({'global_permissions_diff': global_permissions_diff_df_yaml, 'build_plan_permissions_diff': build_plan_permissions_diff_df_yaml, 'project_permissions_diff': project_permissions_diff_df_yaml, 'deployment_permissions_diff': deployment_permissions_diff_df_yaml, 'deployment_project_permissions_diff': deployment_project_permissions_diff_df_yaml, 'deployment_environment_permissions_diff': deployment_environment_permissions_diff_df_yaml}, outfile, default_flow_style=False)
        return global_permissions_diff_df_yaml, build_plan_permissions_diff_df_yaml, project_permissions_diff_df_yaml, deployment_permissions_diff_df_yaml, deployment_project_permissions_diff_df_yaml, deployment_environment_permissions_diff_df_yaml

    def update_permissions(self):
        """
        Update the permissions in Bamboo.
        :return: Updated permissions in Bamboo
        """
        permissions_diff_df = self.get_permissions_diff_df()
        global_permissions_diff_df = permissions_diff_df[0]
        build_plan_permissions_diff_df = permissions_diff_df[1]
        project_permissions_diff_df = permissions_diff_df[2]
        deployment_permissions_diff_df = permissions_diff_df[3]
        deployment_project_permissions_diff_df = permissions_diff_df[4]
        deployment_environment_permissions_diff_df = permissions_diff_df[5]
        global_permissions_diff_df_added = global_permissions_diff_df[global_permissions_diff_df['_merge'] == 'right_only']
        build_plan_permissions_diff_df_added = build_plan_permissions_diff_df[build_plan_permissions_diff_df['_merge'] == 'right_only']
        project_permissions_diff_df_added = project_permissions_diff_df[project_permissions_diff_df['_merge'] == 'right_only']
        deployment_permissions_diff_df_added = deployment_permissions_diff_df[deployment_permissions_diff_df['_merge'] == 'right_only']
        deployment_project_permissions_diff_df_added = deployment_project_permissions_diff_df[deployment_project_permissions_diff_df['_merge'] == 'right_only']
        deployment_environment_permissions_diff_df_added = deployment_environment_permissions_diff_df[deployment_environment_permissions_diff_df['_merge'] == 'right_only']
        global_permissions_diff_df_removed = global_permissions_diff_df[global_permissions_diff_df['_merge'] == 'left_only']
        build_plan_permissions_diff_df_removed = build_plan_permissions_diff_df[build_plan_permissions_diff_df['_merge'] == 'left_only']
        project_permissions_diff_df_removed = project_permissions_diff_df[project_permissions_diff_df['_merge'] == 'left_only']
        deployment_permissions_diff_df_removed = deployment_permissions_diff_df[deployment_permissions_diff_df['_merge'] == 'left_only']
        deployment_project_permissions_diff_df_removed = deployment_project_permissions_diff_df[deployment_project_permissions_diff_df['_merge'] == 'left_only']
        deployment_environment_permissions_diff_df_removed = deployment_environment_permissions_diff_df[deployment_environment_permissions_diff_df['_merge'] == 'left_only']
        global_permissions_diff_df_added_yaml = global_permissions_diff_df_added.to_dict(orient='records')
        build_plan_permissions_diff_df_added_yaml = build_plan_permissions_diff_df_added.to_dict(orient='records')
        project_permissions_diff_df_added_yaml = project_permissions_diff_df_added.to_dict(orient='records')
        deployment_permissions_diff_df_added_yaml = deployment_permissions_diff_df_added.to_dict(orient='records')
        deployment_project_permissions_diff_df_added_yaml = deployment_project_permissions_diff_df_added.to_dict(orient='records')
        deployment_environment_permissions_diff_df_added_yaml = deployment_environment_permissions_diff_df_added.to_dict(orient='records')
        global_permissions_diff_df_removed_yaml = global_permissions_diff_df_removed.to_dict(orient='records')
        build_plan_permissions_diff_df_removed_yaml = build_plan_permissions_diff_df_removed.to_dict(orient='records')
        project_permissions_diff_df_removed_yaml = project_permissions_diff_df_removed.to_dict(orient='records')
        deployment_permissions_diff_df_removed_yaml = deployment_permissions_diff_df_removed.to_dict(orient='records')
        deployment_project_permissions_diff_df_removed_yaml = deployment_project_permissions_diff_df_removed.to_dict(orient='records')
        deployment_environment_permissions_diff_df_removed_yaml = deployment_environment_permissions_diff_df_removed.to_dict(orient='records')
        for global_permission_diff_df_added_yaml in global_permissions_diff_df_added_yaml:
            self.bamboo_client.add_global_permission(global_permission_diff_df_added_yaml['permission'], global_permission_diff_df_added_yaml['type'], global_permission_diff_df_added_yaml['name'])
        for build_plan_permission_diff_df_added_yaml in build_plan_permissions_diff_df_added_yaml:
            self.bamboo_client.add_build_plan_permission(build_plan_permission_diff_df_added_yaml['permission'], build_plan_permission_diff_df_added_yaml['type'], build_plan_permission_diff_df_added_yaml['name'], build_plan_permission_diff_df_added_yaml['projectKey'], build_plan_permission_diff_df_added_yaml['planKey'])
        for project_permission_diff_df_added_yaml in project_permissions_diff_df_added_yaml:
            self.bamboo_client.add_project_permission(project_permission_diff_df_added_yaml['permission'], project_permission_diff_df_added_yaml['type'], project_permission_diff_df_added_yaml['name'], project_permission_diff_df_added_yaml['projectKey'])
        for deployment_permission_diff_df_added_yaml in deployment_permissions_diff_df_added_yaml:
            self.bamboo_client.add_deployment_permission(deployment_permission_diff_df_added_yaml['permission'], deployment_permission_diff_df_added_yaml['type'], deployment_permission_diff_df_added_yaml['name'])
        for deployment_project_permission_diff_df_added_yaml in deployment_project_permissions_diff_df_added_yaml:
            self.bamboo_client.add_deployment_project_permission(deployment_project_permission_diff_df_added_yaml['permission'], deployment_project_permission_diff_df_added_yaml['type'], deployment_project_permission_diff_df_added_yaml['name'], deployment_project_permission_diff_df_added_yaml['projectKey'])
        for deployment_environment_permission_diff_df_added_yaml in deployment_environment_permissions_diff_df_added_yaml:
            self.bamboo_client.add_deployment_environment_permission(deployment_environment_permission_diff_df_added_yaml['permission'], deployment_environment_permission_diff_df_added_yaml['type'], deployment_environment_permission_diff_df_added_yaml['name'], deployment_environment_permission_diff_df_added_yaml['projectKey'], deployment_environment_permission_diff_df_added_yaml['environmentId'])
        for global_permission_diff_df_removed_yaml in global_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_global_permission(global_permission_diff_df_removed_yaml['permission'], global_permission_diff_df_removed_yaml['type'], global_permission_diff_df_removed_yaml['name'])
        for build_plan_permission_diff_df_removed_yaml in build_plan_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_build_plan_permission(build_plan_permission_diff_df_removed_yaml['permission'], build_plan_permission_diff_df_removed_yaml['type'], build_plan_permission_diff_df_removed_yaml['name'], build_plan_permission_diff_df_removed_yaml['projectKey'], build_plan_permission_diff_df_removed_yaml['planKey'])
        for project_permission_diff_df_removed_yaml in project_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_project_permission(project_permission_diff_df_removed_yaml['permission'], project_permission_diff_df_removed_yaml['type'], project_permission_diff_df_removed_yaml['name'], project_permission_diff_df_removed_yaml['projectKey'])
        for deployment_permission_diff_df_removed_yaml in deployment_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_deployment_permission(deployment_permission_diff_df_removed_yaml['permission'], deployment_permission_diff_df_removed_yaml['type'], deployment_permission_diff_df_removed_yaml['name'])
        for deployment_project_permission_diff_df_removed_yaml in deployment_project_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_deployment_project_permission(deployment_project_permission_diff_df_removed_yaml['permission'], deployment_project_permission_diff_df_removed_yaml['type'], deployment_project_permission_diff_df_removed_yaml['name'], deployment_project_permission_diff_df_removed_yaml['projectKey'])
        for deployment_environment_permission_diff_df_removed_yaml in deployment_environment_permissions_diff_df_removed_yaml:
            self.bamboo_client.remove_deployment_environment_permission(deployment_environment_permission_diff_df_removed_yaml['permission'], deployment_environment_permission_diff_df_removed_yaml['type'], deployment_environment_permission_diff_df_removed_yaml['name'], deployment_environment_permission_diff_df_removed_yaml['projectKey'], deployment_environment_permission_diff_df_removed_yaml['environmentId'])
        return global_permissions_diff_df_added_yaml, build_plan_permissions_diff_df_added_yaml, project_permissions_diff_df_added_yaml, deployment_permissions_diff_df_added_yaml, deployment_project_permissions_diff_df_added_yaml, deployment_environment_permissions_diff_df_added_yaml, global_permissions_diff_df_removed_yaml, build_plan_permissions_diff_df_removed_yaml, project_permissions_diff_df_removed_yaml, deployment_permissions_diff_df_removed_yaml, deployment_project_permissions_diff_df_removed_yaml, deployment_environment_permissions_diff_df_removed_yaml

    def write_permissions_diff_df_yaml_added(self, output_file):
        """
        Write the permissions that need to be added to a YAML file.
        :param output_file: Output file
        :return: Permissions that need to be added to a YAML file
        """
        permissions_diff_df_yaml_added = self.update_permissions()
        global_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[0]
        build_plan_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[1]
        project_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[2]
        deployment_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[3]
        deployment_project_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[4]
        deployment_environment_permissions_diff_df_yaml_added = permissions_diff_df_yaml_added[5]
        with open(output_file, 'w') as outfile:
            yaml.dump({'global_permissions_diff_added': global_permissions_diff_df_yaml_added, 'build_plan_permissions_diff_added': build_plan_permissions_diff_df_yaml_added, 'project_permissions_diff_added': project_permissions_diff_df_yaml_added, 'deployment_permissions_diff_added': deployment_permissions_diff_df_yaml_added, 'deployment_project_permissions_diff_added': deployment_project_permissions_diff_df_yaml_added, 'deployment_environment_permissions_diff_added': deployment_environment_permissions_diff_df_yaml_added}, outfile, default_flow_style=False)
        return global_permissions_diff_df_yaml_added, build_plan_permissions_diff_df_yaml_added, project_permissions_diff_df_yaml_added, deployment_permissions_diff_df_yaml_added, deployment_project_permissions_diff_df_yaml_added, deployment_environment_permissions_diff_df_yaml_added

    def write_permissions_diff_df_yaml_removed(self, output_file):
        """
        Write the permissions that need to be removed to a YAML file.
        :param output_file: Output file
        :return: Permissions that need to be removed to a YAML file
        """
        permissions_diff_df_yaml_removed = self.update_permissions()
        global_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[6]
        build_plan_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[7]
        project_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[8]
        deployment_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[9]
        deployment_project_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[10]
        deployment_environment_permissions_diff_df_yaml_removed = permissions_diff_df_yaml_removed[11]
        with open(output_file, 'w') as outfile:
            yaml.dump({'global_permissions_diff_removed': global_permissions_diff_df_yaml_removed, 'build_plan_permissions_diff_removed': build_plan_permissions_diff_df_yaml_removed, 'project_permissions_diff_removed': project_permissions_diff_df_yaml_removed, 'deployment_permissions_diff_removed': deployment_permissions_diff_df_yaml_removed, 'deployment_project_permissions_diff_removed': deployment_project_permissions_diff_df_yaml_removed, 'deployment_environment_permissions_diff_removed': deployment_environment_permissions_diff_df_yaml_removed}, outfile, default_flow_style=False)
        return global_permissions_diff_df_yaml_removed, build_plan_permissions_diff_df_yaml_removed, project_permissions_diff_df_yaml_removed, deployment_permissions_diff_df_yaml_removed, deployment_project_permissions_diff_df_yaml_removed, deployment_environment_permissions_diff_df_yaml_removed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reconcile user and group access information for Atlassian Bamboo (version 6.8) Global permissions, Build plan permissions, Project permissions, Deployment permissions, Deployment project permissions, Deployment environment permissions.')
    parser.add_argument('--bamboo_url', help='Bamboo URL', required=True)
    parser.add_argument('--bamboo_user', help='Bamboo user', required=True)
    parser.add_argument('--bamboo_password', help='Bamboo password', required=True)
    parser.add_argument('--bamboo_log_file', help='Bamboo log file', required=True)
    parser.add_argument('--bamboo_log_level', help='Bamboo log level', required=True)
    parser.add_argument('--desired_permissions_file', help='Desired permissions file', required=True)
    args = parser.parse_args()
    bamboo_access_reconciler = BambooAccessReconciler(args.bamboo_url, args.bamboo_user, args.bamboo_password, args.bamboo_log_file, args.bamboo_log_level, args.desired_permissions_file)
    bamboo_access_reconciler.write_permissions_diff_df_yaml('permissions_diff.yaml')
    bamboo_access_reconciler.write_permissions_diff_df_yaml_added('permissions_diff_added.yaml')
    bamboo_access_reconciler.write_permissions_diff_df_yaml_removed('permissions_diff_removed.yaml')

"""
The desired permissions file is a YAML file that contains the desired permissions for the Bamboo instance. The desired permissions file is structured as follows:

global_permissions:
  - name: <user or group name>
    permissions:
      - <permission name>
  - name: <user or group name>
    permissions:
      - <permission name>
build_plan_permissions:
  - name: <build plan name>
    permissions:
      - name: <user or group name>
        permissions:
          - <permission name>
      - name: <user or group name>
        permissions:
          - <permission name>
project_permissions:
  - name: <project name>
    permissions:
      - name: <user or group name>
        permissions:
          - <permission name>
      - name: <user or group name>
        permissions:
          - <permission name>
deployment_permissions:
  - name: <deployment name>
    permissions:
      - name: <user or group name>
        permissions:
          - <permission name>
      - name: <user or group name>
        permissions:
          - <permission name>
deployment_project_permissions:
  - name: <deployment project name>
    permissions:
      - name: <user or group name>
        permissions:
          - <permission name>
      - name: <user or group name>
        permissions:
          - <permission name>
deployment_environment_permissions:
  - name: <deployment environment name>
    permissions:
      - name: <user or group name>
        permissions:
          - <permission name>
      - name: <user or group name>
        permissions:
          - <permission name>

The following is an example of a desired permissions file:

global_permissions:
  - name: admin
    permissions:
      - ADMINISTER
      - BUILD
      - CLONE
      - EDIT
      - VIEW
  - name: jdoe
    permissions:
      - BUILD
      - CLONE
      - EDIT
      - VIEW
build_plan_permissions:
  - name: BUILD-PLAN-1
    permissions:
      - name: admin
        permissions:
          - ADMINISTER
          - BUILD
          - CLONE
          - EDIT
          - VIEW
      - name: jdoe
        permissions:
          - BUILD
          - CLONE
          - EDIT
          - VIEW
project_permissions:
  - name: PROJECT-1
    permissions:
      - name: admin
        permissions:
          - ADMINISTER
          - BUILD
          - CLONE
          - EDIT
          - VIEW
      - name: jdoe
        permissions:
          - BUILD
          - CLONE
          - EDIT
          - VIEW
deployment_permissions:
  - name: DEPLOYMENT-1
    permissions:
      - name: admin
        permissions:
          - ADMINISTER
          - BUILD
          - CLONE
          - EDIT
          - VIEW
      - name: jdoe
        permissions:
          - BUILD
          - CLONE
          - EDIT
          - VIEW
deployment_project_permissions:
  - name: DEPLOYMENT-PROJECT-1
    permissions:
      - name: admin
        permissions:
          - ADMINISTER
          - BUILD
          - CLONE
          - EDIT
          - VIEW
      - name: jdoe
        permissions:
          - BUILD
          - CLONE
          - EDIT
          - VIEW
deployment_environment_permissions:
  - name: DEPLOYMENT-ENVIRONMENT-1
    permissions:
      - name: admin
        permissions:
          - ADMINISTER
          - BUILD
          - CLONE
          - EDIT
          - VIEW
      - name: jdoe
        permissions:
          - BUILD
          - CLONE
          - EDIT
          - VIEW

"""