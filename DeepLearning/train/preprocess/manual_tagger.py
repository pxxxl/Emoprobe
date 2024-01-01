import csv
import random


class ManualTagger:
    """
    Read txt from txt_file, and allow user to tag them manually
    """
    def __init__(self, txt_file, csv_file):
        self.txt_file = txt_file
        self.csv_file = csv_file
        self.data = None

    def append_to_csv(self, data):
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def delete_line_from_txt_file(self):
        with open(self.txt_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if lines:
            # 移除第一行
            lines.pop(0)

        with open(self.txt_file, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def tag(self):

        # 打开并读取txt文件的内容
        with open(self.txt_file, 'r', encoding='utf-8', errors='replace') as txtfile:
            for line in txtfile:
                line = line.strip()
                print(f'Original Line: {line}')

                # 获取用户输入
                user_input = input("Enter a number or press Enter to skip: ")

                if user_input.strip().isdigit():
                    line_to_write = [user_input, line]
                    self.append_to_csv(line_to_write)
                # 删除已处理的行
                self.delete_line_from_txt_file()

        print(f'Data has been processed and saved to {self.csv_file}')

    def shuffle_csv(self):
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        # 随机重排数据行
        random.shuffle(data)

        # 将重排后的数据写入新的CSV文件
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        print(self.csv_file + 'has been shuffled')


tagger = ManualTagger('2K.txt', '2K.csv')
tagger.tag()
