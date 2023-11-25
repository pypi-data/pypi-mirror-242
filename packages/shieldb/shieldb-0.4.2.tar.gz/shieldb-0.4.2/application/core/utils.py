import argparse
import os

from InquirerPy.validator import NumberValidator
from application.core.enums import Actions
from InquirerPy import inquirer
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


class Utils:
    @staticmethod
    def connect_db():
        try:
            db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
            engine = create_engine(db_uri)
            conn = engine.connect()
            return conn
        except SQLAlchemyError as e:
            return None

    @staticmethod
    def read_user_args():

        action = inquirer.select(
            message="Select your action",
            choices=['delete', 'mask']
        ).execute()

        table = inquirer.text(message="What's your table name?").execute()

        user_args = {
            'action': action,
            'table': table,
            'percentage': 0,
            'columns': [],
            'place_to_mask': None,
            'mask_type': 'regex'
        }

        if action == Actions.DELETE.value:
            percentage = inquirer.text(
                message="Enter the percentage of data to be deleted (0-100):",
                validate=NumberValidator(float_allowed=True, message="Please enter a valid number between 0 and 100."),
                filter=lambda value: float(value) if 0 <= float(value) <= 100 else 0,
                validate_while_typing=True,
                default="0"
            ).execute()
            user_args['percentage'] = percentage
        elif action == Actions.MASK.value:
            columns = inquirer.text(
                message="Enter the columns to be masked, separated by spaces:",
                default="",
                filter=lambda value: value.split() if value else []
            ).execute()
            mask_type = inquirer.select(
                message="Select your mask type",
                choices=['shuffle (Shieldb --> hieldSb)', 'regex', 'reverse (Shieldb --> bdleihS)', 'middle (Shieldb '
                                                                                                    '--> Sh***db)',
                         'start (Shieldb --> ***eldb)', 'end ( Shie***)', 'random_char (Shieldb --> S*ei*d*)', 'nltk ('
                                                                                                              'Shieldb --> Apple)', 'random_character (Shieldb --> Shabcdb)']
            ).execute()

            user_args['mask_type'] = mask_type
            user_args['columns'] = columns

        parser = argparse.ArgumentParser(prog='shieldb', description='Script for deleting or masking data from '
                                                                     'a database\n '
                                                                     'Before running the src, make sure to '
                                                                     'set the database '
                                                                     'to work with. '
                                                                     'You can set the database by defining the '
                                                                     'SQLALCHEMY_DATABASE_URI variable.\n '
                                                                     'Usage examples:\n'
                                                                     'SQLALCHEMY_DATABASE_URI=""'
                                                                     '%(prog)  --action delete --table my_table '
                                                                     '--percentage 20\n '
                                                                     '%(prog)  --action mask --table my_table '
                                                                     '--columns column1 '
                                                                     'column2')
        parser.add_argument('--action', default=user_args['action'], help='Operation to be performed')
        parser.add_argument('--table', default=user_args['table'], help='Name of the table from which data will be deleted or masked')
        parser.add_argument('--percentage', type=float, default=user_args['percentage'],
                            help='Percentage of data to be deleted (default: 0), PERCENTAGE SHOULD BE BETWEEN 0 AND 100.')
        parser.add_argument('--columns', nargs='+', default=user_args['columns'],
                            help='The columns to be masked will be entered with spaces. If columns are not entered, '
                                 'the entire table is masked.')
        parser.add_argument('--place_to_mask', help='Name of the table from which data will be deleted or masked')
        parser.add_argument('--mask_type', choices=['shuffle', 'regex', 'reverse', 'middle', 'start', 'end', 'random', 'nltk', 'random_character'],
                            default=user_args['mask_type'], help='determines the type of masking')

        command_line_args = parser.parse_args()
        return command_line_args


