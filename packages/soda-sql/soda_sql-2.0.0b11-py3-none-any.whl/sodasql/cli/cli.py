#  Copyright 2020 Soda
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import datetime
import logging
import sys
from typing import Optional

import click
import yaml

from sodasql.cli.scan_initializer import ScanInitializer
from sodasql.common.logging_helper import LoggingHelper
from sodasql.scan.file_system import FileSystemSingleton
from sodasql.scan.scan_builder import ScanBuilder
from sodasql.scan.warehouse import Warehouse
from sodasql.scan.warehouse_yml_parser import (WarehouseYmlParser,
                                               read_warehouse_yml_file)
from sodasql.version import SODA_SQL_VERSION

LoggingHelper.configure_for_cli()


@click.group(help=f"Soda CLI version {SODA_SQL_VERSION}")
def main():
    pass


@main.command()
@click.argument('warehouse_type')
@click.option('-f', '--file',
              required=False,
              default='warehouse.yml',
              help='The destination filename for the warehouse configuration details. This can be a relative path.')
@click.option('-d', '--database',  required=False, default=None, help='The database name to use for the connection')
@click.option('-u', '--username',  required=False, default=None, help='The username to use for the connection, through env_var(...)')
@click.option('-p', '--password',  required=False, default=None, help='The password to use for the connection, through env_var(...)')
@click.option('-w', '--warehouse', required=False, default=None, help='The warehouse name')
def create(warehouse_type: str,
           file: Optional[str],
           warehouse: Optional[str],
           database: Optional[str],
           username: Optional[str],
           password: Optional[str]):
    """
    Creates a new warehouse.yml file and prepares credentials in your ~/.soda/env_vars.yml
    Nothing will be overwritten or removed, only added if it does not exist yet.

    WAREHOUSE_TYPE is one of {postgres, snowflake, redshift, bigquery, athena}
    """
    try:
        """
        Creates a warehouse.yml file
        """
        logging.info(f"Soda CLI version {SODA_SQL_VERSION}")
        file_system = FileSystemSingleton.INSTANCE

        # if not warehouse:
        #     warehouse_dir_parent, warehouse_dir_name = file_system.split(warehouse_dir)
        #     warehouse = warehouse_dir_name if warehouse_dir_name != '.' else warehouse_type

        from sodasql.scan.dialect import ALL_WAREHOUSE_TYPES, Dialect
        dialect = Dialect.create_for_warehouse_type(warehouse_type)
        if not dialect:
            logging.info(
                f"Invalid warehouse type {warehouse_type}, use one of {str(ALL_WAREHOUSE_TYPES)}")
            return 1

        configuration_params = {}
        if isinstance(database, str):
            configuration_params['database'] = database
        if isinstance(username, str):
            configuration_params['username'] = username
        if isinstance(password, str):
            configuration_params['password'] = password
        connection_properties = dialect.default_connection_properties(configuration_params)
        warehouse_env_vars_dict = dialect.default_env_vars(configuration_params)

        if file_system.file_exists(file):
            logging.info(f"Warehouse file {file} already exists")
        else:
            logging.info(f"Creating warehouse YAML file {file} ...")
            file_system.mkdirs(file_system.dirname(file))

            if not warehouse:
                warehouse = warehouse_type

            warehouse_dict = {
                'name': warehouse,
                'connection': connection_properties
            }
            warehouse_yml_str = yaml.dump(warehouse_dict, default_flow_style=False, sort_keys=False)
            file_system.file_write_from_str(file, warehouse_yml_str)

        dot_soda_dir = file_system.join(file_system.user_home_dir(), '.soda')
        if not file_system.file_exists(dot_soda_dir):
            file_system.mkdirs(dot_soda_dir)

        env_vars_file = file_system.join(dot_soda_dir, 'env_vars.yml')
        env_vars_yml_str = ''
        env_vars_file_exists = file_system.file_exists(env_vars_file)
        if env_vars_file_exists:
            env_vars_yml_str = file_system.file_read_as_str(env_vars_file)
            existing_env_vars_yml_dict = yaml.load(env_vars_yml_str, Loader=yaml.FullLoader)
            if isinstance(existing_env_vars_yml_dict, dict) and warehouse in existing_env_vars_yml_dict:
                logging.info(f"Warehouse section {warehouse} already exists in {env_vars_file}.  Skipping...")
                warehouse_env_vars_dict = None

        if warehouse_env_vars_dict:
            warehouse_env_vars_dict = {
                warehouse: warehouse_env_vars_dict
            }

            if len(env_vars_yml_str) > 0:
                env_vars_yml_str += '\n'

            env_vars_yml_str += yaml.dump(warehouse_env_vars_dict,
                                          default_flow_style=False,
                                          sort_keys=False)

            if env_vars_file_exists:
                logging.info(
                    f"Adding env vars for {warehouse} to {env_vars_file}")
            else:
                logging.info(
                    f"Creating {env_vars_file} with example env vars in section {warehouse}")

            file_system.file_write_from_str(env_vars_file, env_vars_yml_str)

        logging.info(f"Review warehouse.yml by running command")
        logging.info(f"  cat {file}")
        if warehouse_env_vars_dict:
            logging.info(
                f"Review section {warehouse} in ~/.soda/env_vars.yml by running command")
            logging.info(f"  cat ~/.soda/env_vars.yml")
        logging.info(f"Then run the soda init command")
    except Exception as e:
        logging.exception(f'Exception: {str(e)}')
        return 1


@main.command()
@click.argument('warehouse_file', required=False, default='warehouse.yml')
def init(warehouse_file: str):
    """
    Finds tables in the warehouse and creates scan YAML files based on the data in the table. By default it creates
    files in a subdirectory called "tables" on the same level as the warehouse file.

    WAREHOUSE_FILE contains the connection details to the warehouse. This file can be created using the `soda create` command.
    The warehouse file argument is optional and defaults to 'warehouse.yml'.
    """
    logging.info(SODA_SQL_VERSION)
    file_system = FileSystemSingleton.INSTANCE
    warehouse = None

    try:
        logging.info(f'Initializing {warehouse_file} ...')

        warehouse_yml_dict = read_warehouse_yml_file(warehouse_file)
        warehouse_yml_parser = WarehouseYmlParser(warehouse_yml_dict, warehouse_file)
        warehouse = Warehouse(warehouse_yml_parser.warehouse_yml)

        logging.info('Querying warehouse for tables')
        warehouse_dir = file_system.dirname(warehouse_file)
        scan_initializer = ScanInitializer(warehouse, warehouse_dir)
        scan_initializer.initialize_scan_ymls()

        logging.info(
            f"Next run 'soda scan {warehouse_file} {scan_initializer.first_table_scan_yml_file}' to calculate measurements and run tests")

    except Exception as e:
        logging.exception(f'Exception: {str(e)}')
        return 1

    finally:
        if warehouse and warehouse.connection:
            try:
                warehouse.connection.close()
            except Exception as e:
                logging.debug(f'Closing connection failed: {str(e)}')


@main.command()
@click.argument('warehouse_yml_file')
@click.argument('scan_yml_file')
@click.option('-v', '--variables',
              required=False,
              default=None,
              multiple=True,
              help='Variables like -v start=2020-04-12.  Put values with spaces in single or double quotes.')
@click.option('-t', '--time',
              required=False,
              default=datetime.datetime.now().isoformat(timespec='seconds'),
              help='The scan time in ISO8601 format like eg 2020-12-31T16:48:30Z')
def scan(scan_yml_file: str, warehouse_yml_file: str, variables: tuple = None, time: str = None):
    """
    Computes all measurements and runs all tests on one table.  Exit code 0 means all tests passed.
    Non zero exit code means tests have failed or an exception occurred.
    If the warehouse YAML file has a Soda cloud account configured, measurements and test results will be uploaded.

    WAREHOUSE_YML_FILE is the warehouse YAML file containing connection details.

    SCAN_YML_FILE is the scan YAML file that contains the metrics and tests for a table to run.
    """
    logging.info(SODA_SQL_VERSION)

    try:
        variables_dict = {}
        if variables:
            for variable in variables:
                assign_index = variable.find('=')
                if 0 < assign_index < len(variable) - 1:
                    variable_name = variable[0:assign_index]
                    variable_value = variable[assign_index + 1:]
                    variables_dict[variable_name] = variable_value
            logging.debug(f'Variables {variables_dict}')

        scan_builder = ScanBuilder()
        scan_builder.warehouse_yml_file = warehouse_yml_file
        scan_builder.scan_yml_file = scan_yml_file
        scan_builder.time = time

        logging.info(f'Scanning {scan_yml_file} ...')

        scan_builder.variables = variables_dict
        scan = scan_builder.build()
        if not scan:
            logging.error(f'Could not read scan configurations. Aborting before scan started.')
            sys.exit(1)

        from sodasql.scan.scan_result import ScanResult
        scan_result: ScanResult = scan.execute()

        for measurement in scan_result.measurements:
            logging.info(measurement)

        logging.info(f'{len(scan_result.measurements)} measurements computed')
        logging.info(f'{len(scan_result.test_results)} tests executed')
        if scan_result.has_failures():
            logging.info(f'{scan_result.failures_count()} of {len(scan_result.test_results)} tests failed:')
            for test_result in scan_result.test_results:
                if not test_result.passed:
                    logging.info(f'  {test_result.test.description} cause {test_result.test.first_metric}={test_result.value}')
        else:
            logging.info(f'All is good. No tests failed.')
        sys.exit(scan_result.failures_count())

    except Exception as e:
        logging.exception(f'Scan failed: {str(e)}')
        sys.exit(1)

