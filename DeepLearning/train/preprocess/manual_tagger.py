"""
This is a manual tagger for user to tag txt comments by their standards.

File Name: manual_tagger.py
Author: Lin Ziyao (GitHub: Sen-Yao)
Date Created: 2024-01-01
Purpose: Tag comments' emotions

"""

import csv
import random
import os


class ManualTagger:
    """
    This class reads text from a text file and allows users to tag them manually.
    """

    def __init__(self, txt_file, csv_file):
        self.txt_file = txt_file
        self.csv_file = csv_file
        self.data = None

    def append_to_csv(self, data):
        """
        Appends data to the specified CSV file.

        Args:
            data (list): The data to be appended.
        """
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def delete_line_from_txt_file(self):
        """
        Deletes the first line from the specified text file.
        """
        with open(self.txt_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if lines:
            # Remove first line
            lines.pop(0)

        with open(self.txt_file, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def tag(self):
        """
        Tags comments manually based on user input.
        """
        with open(self.txt_file, 'r', encoding='utf-8', errors='replace') as txtfile:
            for line in txtfile:
                line = line.strip()
                print(f'\nOriginal comments: {line}')

                user_input = input("Enter a number or press Enter to skip: ")

                if user_input.strip().isdigit():
                    line_to_write = [user_input, line]
                    self.append_to_csv(line_to_write)
                self.delete_line_from_txt_file()

        print(f'Data has been processed and saved to {self.csv_file}')

    def shuffle_csv(self):
        """
        Shuffles the rows of the CSV file.
        """
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        random.shuffle(data)
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        print(self.csv_file + 'has been shuffled')


if __name__ == "__main__":
    current_script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'raw_data')
    tagger = ManualTagger(os.path.join(current_script_path, 'untagged_sentences.txt'), 'tagged_sentences.csv')
    tagger.tag()
    tagger.shuffle_csv()
