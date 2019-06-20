import time
import os
from terminaltables import SingleTable
from copy import deepcopy
from colorclass import Color

class BHTable:

    def __init__(self):
        self.blank = ' ' * 19
        self.latest_data = None
        self.previous = {'bh-address': None, 'bh-system': None, 'bh-region': None, 'bh-econ': None, 'bh-life': None,
                         'exit-address': None, 'exit-system': None, 'exit-region': None, 'exit-econ': None, 'exit-life': None}
        self.current = {'bh-address': None, 'bh-system': None, 'bh-region': None, 'bh-econ': None, 'bh-life': None,
                        'exit-address': None, 'exit-system': None, 'exit-region': None, 'exit-econ': None, 'exit-life': None}

    def output_address(self, address):
        if address[-2:] == '79' and not self.current['bh-address']:
            self.current['bh-address'] = address
            self.latest_data = 'bh-address'
        elif address[-2:] != '79' and not self.current['exit-address']:
            self.current['exit-address'] = address
            self.latest_data = 'exit-address'

        self.display_tables()

    def output_ocr_info(self, ocr_data):
        if not self.current['bh-system'] and not self.current['bh-region']:
            for key in list(ocr_data):
                self.current['bh-' + key] = ocr_data.pop(key)
            self.latest_data = 'bh-ocr'
        elif not self.current['exit-system'] and not self.current['exit-region'] and self.current['bh-address'] and self.current['bh-system']:
            for key in list(ocr_data):
                self.current['exit-' + key] = ocr_data.pop(key)
            self.latest_data = 'exit-ocr'
        elif self.current['bh-system'] and self.current['bh-region'] and not self.current['bh-address']:
            # User takes a second screenshot of black hole system, it should overwrite old data
            for key in list(ocr_data):
                self.current['bh-' + key] = ocr_data.pop(key)
            self.latest_data = 'bh-ocr'
        elif self.current['exit-system'] and self.current['exit-region'] and self.current['bh-address'] and self.current['bh-system'] and not self.current['exit-address']:
            # User takes a second screenshot of exit system, it should overwrite old data
            for key in list(ocr_data):
                self.current['exit-' + key] = ocr_data.pop(key)
            self.latest_data = 'exit-ocr'

        self.display_tables()

    def next_blackhole(self):
        self.previous = deepcopy(self.current)
        self.current = {'bh-address': None, 'bh-system': None, 'bh-region': None, 'bh-econ': None, 'bh-life': None,
                        'exit-address': None, 'exit-system': None, 'exit-region': None, 'exit-econ': None, 'exit-life': None}

    def convert_dict_to_table(self, bh_data, draw_color=False):

        temp_data = {}
        for key, value in bh_data.items():
            if not value:
                temp_data[key] = self.blank
            else:
                temp_data[key] = value

        if draw_color is True:
            if self.latest_data == 'bh-address':
                table_data = [
                    ['', 'Entrance', 'Exit'],
                    ['Address', Color(self.add_green_tag(temp_data['bh-address'])), temp_data['exit-address']],
                    ['System ', temp_data['bh-system'], temp_data['exit-system']],
                    ['Region ', temp_data['bh-region'], temp_data['exit-region']],
                    ['Economy ', temp_data['bh-econ'], temp_data['exit-econ']],
                    ['Life ', temp_data['bh-life'], temp_data['exit-life']]
                ]
            elif self.latest_data == 'exit-address':
                table_data = [
                    ['', 'Entrance', 'Exit'],
                    ['Address', temp_data['bh-address'], Color(self.add_green_tag(temp_data['exit-address']))],
                    ['System ', temp_data['bh-system'], temp_data['exit-system']],
                    ['Region ', temp_data['bh-region'], temp_data['exit-region']],
                    ['Economy ', temp_data['bh-econ'], temp_data['exit-econ']],
                    ['Life ', temp_data['bh-life'], temp_data['exit-life']]
                ]
            elif self.latest_data == 'bh-ocr':
                table_data = [
                    ['', 'Entrance', 'Exit'],
                    ['Address', temp_data['bh-address'], temp_data['exit-address']],
                    ['System ', Color(self.add_green_tag(temp_data['bh-system'])), temp_data['exit-system']],
                    ['Region ', Color(self.add_green_tag(temp_data['bh-region'])), temp_data['exit-region']],
                    ['Economy ', Color(self.add_green_tag(temp_data['bh-econ'])), temp_data['exit-econ']],
                    ['Life ', Color(self.add_green_tag(temp_data['bh-life'])), temp_data['exit-life']]
                ]
            elif self.latest_data == 'exit-ocr':
                table_data = [
                    ['', 'Entrance', 'Exit'],
                    ['Address', temp_data['bh-address'], temp_data['exit-address']],
                    ['System ', temp_data['bh-system'], Color(self.add_green_tag(temp_data['exit-system']))],
                    ['Region ', temp_data['bh-region'], Color(self.add_green_tag(temp_data['exit-region']))],
                    ['Economy ', temp_data['bh-econ'], Color(self.add_green_tag(temp_data['exit-econ']))],
                    ['Life ', temp_data['bh-life'], Color(self.add_green_tag(temp_data['exit-life']))]
                ]
            else:
                table_data = [
                    ['', 'Entrance', 'Exit'],
                    ['Address', temp_data['bh-address'], temp_data['exit-address']],
                    ['System ', temp_data['bh-system'], temp_data['exit-system']],
                    ['Region ', temp_data['bh-region'], temp_data['exit-region']],
                    ['Economy ', temp_data['bh-econ'], temp_data['exit-econ']],
                    ['Life ', temp_data['bh-life'], temp_data['exit-life']]
                ]

            self.latest_data = None

        else:
            table_data = [
                ['', 'Entrance', 'Exit'],
                ['Address', temp_data['bh-address'], temp_data['exit-address']],
                ['System ', temp_data['bh-system'], temp_data['exit-system']],
                ['Region ', temp_data['bh-region'], temp_data['exit-region']],
                ['Economy ', temp_data['bh-econ'], temp_data['exit-econ']],
                ['Life ', temp_data['bh-life'], temp_data['exit-life']]
            ]

        return table_data

    def add_green_tag(self, data):
        return '{autogreen}'+data+'{/autogreen}'

    def display_tables(self):
        os.system('cls')
        if self.previous['bh-address']:
            previous_table = SingleTable(self.convert_dict_to_table(self.previous), title='Previous Black Hole')
            print(previous_table.table)
            print('\n')

        current_table = SingleTable(self.convert_dict_to_table(self.current, draw_color=True), title='Current Black Hole')
        print(current_table.table)

