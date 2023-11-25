import json
import random
import re
import signal
import string
import nltk
from nltk.corpus import words
from sqlalchemy import text
from application.core.replace_utils import ReplaceUtils
from application.core.enums import Actions

patterns = {
            'tc': re.compile(r'\b(\d{4})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'credit_card': re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b'),
            'email': re.compile(r'\b[A-Za-z0-9._*%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'password': re.compile(r'(\b[A-Za-z0-9_-]+:)\s*\b([A-Za-z0-9_-]+)\b'),
        }

replace_functions = {
                'email': ReplaceUtils.replace_email,
                'phone': ReplaceUtils.replace_phone_number,
                'tc': ReplaceUtils.replace_phone_number,
                'credit_card': ReplaceUtils.replace_credit_card_number,
                'password': ReplaceUtils.replace_password,
            }

nltk.download('words')


class MaskUtils:
    def __init__(self, connection, args, chunk_size=500):
        self.connection = connection
        self.args = args
        self.chunk_size = chunk_size

    @staticmethod
    def handler(signum, frame):
        print("User interrupted the process. Custom message here.")
        raise SystemExit

    @staticmethod
    def mask_shuffle_text(text_data):
        if isinstance(text_data, str):
            char_list = list(text_data)
            indexes = list(range(len(char_list)))
            random.shuffle(indexes)

            text_data = ''.join(char_list[i] for i in indexes)
        return text_data

    @staticmethod
    def mask_start_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            mask_length = int(length * (40 / 100.0))

            masked_part = Actions.MASK_CHAR.value * mask_length
            text_data = masked_part + text_data[mask_length:]

        return text_data

    @staticmethod
    def mask_regex_text(text_data):
        if isinstance(text_data, str):
            for pattern_name, pattern in patterns.items():
                replace_function = replace_functions.get(pattern_name, lambda x: x)
                text_data = pattern.sub(replace_function, text_data)

        return text_data

    @staticmethod
    def mask_reverse_text(text_data):
        text_data = text_data[::-1]
        return text_data

    @staticmethod
    def mask_random_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            num_to_replace = int(length * (40 / 100.0))
            indices_to_replace = random.sample(range(length), num_to_replace)
            modified_list = list(text_data)
            for index in indices_to_replace:
                modified_list[index] = Actions.MASK_CHAR.value

            text_data = ''.join(modified_list)
        return text_data

    @staticmethod
    def mask_middle_text(text_data):
        length = len(text_data)
        start_length = int(length * (25 / 100.0))
        end_length = int(length * (25 / 100.0))
        middle_length = length - start_length - end_length

        if middle_length <= 0:
            text_data = text_data

        text_data = text_data[:start_length] + (Actions.MASK_CHAR.value * middle_length) + text_data[-end_length:]
        return text_data

    @staticmethod
    def mask_end_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            mask_length = int(length * (60 / 100.0))
            masked_part = Actions.MASK_CHAR.value * mask_length
            text_data = text_data[:-mask_length] + masked_part

        return text_data

    @staticmethod
    def mask_middle_with_random_chars(text_data):
        length = len(text_data)
        start_length = int(length * 0.25)
        end_length = int(length * 0.25)
        middle_length = length - start_length - end_length

        if middle_length <= 0:
            return text_data

        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=middle_length))
        text_data = text_data[:start_length] + random_chars + text_data[-end_length:]
        return text_data

    @staticmethod
    def mask_nltk_text(text_data):
        word_list = words.words()
        new_text = ''
        text_length = len(text_data)

        while len(new_text) < text_length:
            random_word = random.choice(word_list)
            if len(new_text) + len(random_word) + 1 > text_length:
                if len(new_text) < text_length:
                    new_text += random_word[:text_length - len(new_text)]
                break
            new_text += random_word + ' '

        return new_text.strip()

    def mask_json_data(self, json_data):
        masked_data = json_data.copy()
        for key, value in masked_data.items():
            if isinstance(value, str) and value.startswith('{'):
                masked_data[key] = MaskUtils.mask_json_data(self, json.loads(value))
            elif isinstance(value, list):
                masked_list = []
                for item in value:
                    if isinstance(item, list):
                        masked_list.append(MaskUtils.mask_array_data(self, item))
                    elif isinstance(item, str) and item.startswith('{'):
                        masked_list.append(MaskUtils.mask_json_data(self, json.loads(item)))
                    elif isinstance(item, dict):
                        masked_list.append(MaskUtils.mask_json_data(self, item))
                    else:
                        if Actions.REGEX_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_regex_text(item))
                        elif Actions.SHUFFLE_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_shuffle_text(item))
                        elif Actions.REVERSE_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_reverse_text(item))
                        elif Actions.RANDOM_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_random_text(item))
                        elif Actions.MIDDLE_MASK_CHAR_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_middle_text(item))
                        elif Actions.START_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_start_text(item))
                        elif Actions.END_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_end_text(item))
                        elif Actions.NLTK_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_nltk_text(item))
                        elif Actions.MIDDLE_RANDOM_CHARACTER_METHOD.value == self.args.mask_type:
                            masked_list.append(MaskUtils.mask_middle_with_random_chars(item))
                masked_data[key] = masked_list
            elif isinstance(value, dict) or (isinstance(value, str) and value.startswith('{')):
                if isinstance(value, str):
                    value = json.loads(value)
                masked_data[key] = MaskUtils.mask_json_data(value)
            elif isinstance(value, str):
                if Actions.RANDOM_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_random_text(value)
                elif Actions.REGEX_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_regex_text(value)
                elif Actions.MIDDLE_MASK_CHAR_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_random_text(value)
                elif Actions.SHUFFLE_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_shuffle_text(value)
                elif Actions.REVERSE_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_reverse_text(value)
                elif Actions.END_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_end_text(value)
                elif Actions.START_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_start_text(value)
                elif Actions.NLTK_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_nltk_text(value)
                elif Actions.MIDDLE_RANDOM_CHARACTER_METHOD.value == self.args.mask_type:
                    masked_data[key] = MaskUtils.mask_middle_with_random_chars(value)

        masked_json_data = json.dumps(masked_data)

        return masked_json_data

    def mask_array_data(self, char_var_data):
        if isinstance(char_var_data, list):
            masked_list = []
            for item in char_var_data:
                if isinstance(item, list):
                    masked_list.append(MaskUtils.mask_array_data(self, item))
                elif isinstance(item, dict) or (isinstance(item, str) and item.startswith('{')):
                    masked_list.append(MaskUtils.mask_json_data(self, item))
                else:
                    if Actions.REGEX_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_regex_text(item))
                    elif Actions.SHUFFLE_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_shuffle_text(item))
                    elif Actions.REVERSE_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_reverse_text(item))
                    elif Actions.RANDOM_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_random_text(item))
                    elif Actions.MIDDLE_MASK_CHAR_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_middle_text(item))
                    elif Actions.START_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_start_text(item))
                    elif Actions.END_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_end_text(item))
                    elif Actions.NLTK_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_nltk_text(item))
                    elif Actions.MIDDLE_RANDOM_CHARACTER_METHOD.value == self.args.mask_type:
                        masked_list.append(MaskUtils.mask_middle_with_random_chars(item))
            char_var_data = masked_list
        return char_var_data

    def get_table_columns(self):
        result = self.connection.execute(text(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.args.table}' AND column_name <> 'id'"
        ).params(table=self.args.table))

        return [row[0] for row in result]

    def delete_rows_in_chunks(self):

        signal.signal(signal.SIGINT, MaskUtils.handler)

        try:
            if not 0 <= self.args.percentage <= 100:
                print("Error: Percentage should be between 0 and 100.")
                return

            with self.connection.begin():
                total_rows = self.connection.execute(text(f'SELECT COUNT(*) FROM {self.args.table}')).scalar()
                rows_to_delete = int(total_rows * (self.args.percentage / 100))

                if rows_to_delete > 0:
                    chunks = (rows_to_delete + self.chunk_size - 1) // self.chunk_size

                    for chunk in range(chunks):
                        offset = chunk * self.chunk_size
                        limit = min(self.chunk_size, rows_to_delete - offset)

                        delete_query = text(
                            f'DELETE FROM {self.args.table} WHERE ctid IN (SELECT ctid FROM {self.args.table} ORDER BY RANDOM() OFFSET :offset LIMIT :limit)'
                        ).bindparams(offset=offset, limit=limit)
                        self.connection.execute(delete_query)
                        print(f"{chunk + 1} chunks processed.")

                    print(f"{self.args.percentage}% of data deleted from the {self.args.table} table.")
                else:
                    print(f"No rows to delete from the {self.args.table} table.")
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def is_column_maskable(self, column_name):
        query = text(f'SELECT data_type FROM information_schema.columns WHERE table_name = :table_name AND column_name = :column_name')\
            .bindparams(table_name=self.args.table, column_name=column_name)
        result = self.connection.execute(query, {"table_name": self.args.table, "column_name": column_name}).scalar()

        if not result:
            return False, None

        data_type = result.lower()
        maskable_types = ['array', 'text', 'jsonb', 'character varying']
        is_maskable = data_type in maskable_types

        return is_maskable, data_type if is_maskable else None

    def masking(self):
        columns = self.args.columns if self.args.columns else self.get_table_columns()

        try:

            total_rows = self.connection.execute(text(f"SELECT COUNT(*) FROM {self.args.table}")).scalar()

            signal.signal(signal.SIGINT, MaskUtils.handler)

            for column in columns:
                maskable, data_type = self.is_column_maskable(column)
                if not maskable:
                    print(f"Skipping column '{column}' because its type is not maskable.")
                    continue

                for offset in range(0, total_rows, self.chunk_size):
                    query = text(
                        f"SELECT id, {column} FROM {self.args.table} ORDER BY id LIMIT {self.chunk_size} OFFSET {offset};"
                    )
                    id_and_column_data = self.connection.execute(query).fetchall()

                    for tuple_data in id_and_column_data:
                        row_id, old_value = tuple_data
                        if old_value is not None:
                            if data_type == 'character varying' or data_type == 'text':
                                if Actions.REGEX_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_regex_text(old_value)
                                elif Actions.SHUFFLE_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_shuffle_text(old_value)
                                elif Actions.REVERSE_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_reverse_text(old_value)
                                elif Actions.RANDOM_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_random_text(old_value)
                                elif Actions.MIDDLE_MASK_CHAR_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_middle_text(old_value)
                                elif Actions.START_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_start_text(old_value)
                                elif Actions.END_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_end_text(old_value)
                                elif Actions.NLTK_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_nltk_text(old_value)
                                elif Actions.MIDDLE_RANDOM_CHARACTER_METHOD.value == self.args.mask_type:
                                    old_value = MaskUtils.mask_middle_with_random_chars(old_value)
                            elif data_type == 'jsonb':
                                old_value = MaskUtils.mask_json_data(self, old_value)
                            elif data_type == 'array':
                                old_value = MaskUtils.mask_array_data(old_value)

                            update_query = text(
                                f"UPDATE {self.args.table} SET {column} = :regenerated_value WHERE id = :row_id"
                            )
                            self.connection.execute(update_query, {"regenerated_value": old_value, "row_id": row_id})
                            self.connection.commit()
                    print(f"Updated {self.chunk_size} rows in {self.args.table} for {column}, offset: {offset}")

            self.connection.close()
        except Exception as e:
            print("error : ", e)

