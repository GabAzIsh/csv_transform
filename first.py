# IMPORT LIBRARIES SECTION
import csv
from datetime import datetime

# DETERMINE CONSTANTS
column_dict = {
    'номер договора': 'ACCOUNT_RK',
    'номер точки продажи (POS)': 'INTERNAL_ORG_ORIGINAL_RK',
    'сумма кредита': 'LOAN_AMOUNT',
    'дата': 'APPLICATION_DT'
}


# DETERMINE CLASSES AND FUNCTIONS
def typing(data):
    data['ACCOUNT_RK'] = [int(item) for item in data['ACCOUNT_RK']]  # assign integer type
    data['INTERNAL_ORG_ORIGINAL_RK'] = [int(item) for item in data['INTERNAL_ORG_ORIGINAL_RK']]  # assign integer type
    data['LOAN_AMOUNT'] = [int(float(item) * 100) for item in
                           data['LOAN_AMOUNT']]  # assign integer type by converting rubles into kopecks
    data['APPLICATION_DT'] = [datetime.fromisoformat(item) for item in data[
        'APPLICATION_DT']]  # assign datetime format by using standard iso format  of date's string


# class TableCreator:
#     def _get(self, data):
#         if isinstance(data, csv.DictReader):
#             return self.from_csv(data)
#         elif isinstance(data, list):
#             return self.from_list()
#
#     @classmethod
#     def from_csv(cls, data):
#         i_table = [[] for i in range(len(data.fieldnames))]
#         for row in reader.reader:
#             for i in range(len(row)):
#                 i_table[i].append(row[i])
#         csv_table =
#         return
#
#     @classmethod
#     def from_list(cls, data):
#         return TableForCreditSum(i_table)

class TableForCreditSum:
    def __init__(self, data, fieldnames):
        assert 'LOAN_AMOUNT' in fieldnames, 'Table must consist "LOAN_AMOUNT" field'
        self.col_names_dict = self.col_names_dict_from_list(fieldnames)
        if isinstance(data, csv.DictReader):
            self.data = self.from_csv(data)
        elif isinstance(data, list):
            if len(data) != len(fieldnames):
                raise 'Invalid list shape'
            else:
                self.data = data

    def __add__(self, other):
        self.data += other

    def __iadd__(self, other):
        self.__add__(other)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, column_index):
        if column_index is int:
            return self.data[column_index]
        elif type(column_index) is str:
            if column_index in self.col_names_dict.keys():
                return self.data[self.col_names_dict[column_index]]
        else:
            raise f"Invalid column name {column_index} "

    def __setitem__(self, column_index, value):
        if column_index is int:
            self.data[column_index] = value
        elif type(column_index) is str:
            if column_index in self.col_names_dict.keys():
                self.data[self.col_names_dict[column_index]] = value
        else:
            pass

    @classmethod
    def col_names_dict_from_list(cls, fieldnames):
        col_names_set = [(fieldnames[i], i) for i in range(len(fieldnames))]
        return dict(col_names_set)

    def from_csv(self, data):
        i_table = [[] for i in range(len(self.col_names_dict))]
        for row in reader.reader:
            for i in range(len(row)):
                i_table[i].append(row[i])
        return i_table

    def loc(self, row, column):
        if column is int:
            return self.data[row][column]
        elif column is str:
            if column in self.col_names_dict.keys():
                return self.data[row][self.col_names_dict[column]]
        else:
            raise 'Invalid column name'

    @property
    def row_count(self):
        return len(self.data[0])

    def sort_by(self, column_name):
        table_raw = list(zip(*self.data))
        column_number = self.col_names_dict[column_name]
        table_raw.sort(key=lambda row: row[column_number])
        self.data = [list(col) for col in list(zip(*table_raw))]


class Rearrange:

    def __init__(self, table_for_rearrange):
        self.table = table_for_rearrange

    @classmethod
    def render_table(cls, data_list, fieldnames):
        data_table = []
        for date_cells in data_list:
            date_row = [0 for i in range(len(fieldnames))]
            point_amount_cells = date_cells[1]
            for point_row in point_amount_cells:
                date_row[fieldnames.index(str(point_row[0]))] = point_row[1]
                print(point_row[0])
            data_table.append([date_cells[0], date_row])
        return data_table

    def prepare_fieldnames(self, y_axe, x_axe):
        x_set = sorted(list(set(self.table[x_axe])))
        # create fieldnames
        x_set = [str(item) for item in x_set]
        fieldnames = ' % '.join(x_set).split(' ')
        fieldnames.insert(0, f'{y_axe}\\{x_axe}')
        return fieldnames

    def two_axe_table(self, y_axe, x_axe):
        fieldnames = self.prepare_fieldnames(y_axe, x_axe)
        # create table values
        self.table.sort_by(x_axe)
        self.table.sort_by(y_axe)
        # create temporary variables
        i_y_set = 0
        i_x_set = 0
        x_y_list = []
        point_amount_cells = []
        amount_chunk = 0
        sum_for_date = 0
        # Create 2 axe list with required axes in 1 cycle
        for i in range(self.table.row_count):
            amount_for_i = self.table[column_dict['сумма кредита']][i]
            if self.table[y_axe][i] == i_y_set:
                if self.table[x_axe][i] == i_x_set:
                    amount_chunk += amount_for_i
                else:
                    point_amount_cells.append([i_x_set, amount_chunk])
                    amount_chunk = amount_for_i
                    i_x_set = self.table[x_axe][i]
            else:
                if point_amount_cells:
                    point_amount_cells.append([i_x_set, amount_chunk])
                    x_y_list.append([i_y_set, point_amount_cells, sum_for_date])
                i_x_set = self.table[x_axe][i]
                i_y_set = self.table[y_axe][i]
                amount_chunk = amount_for_i
                sum_for_date = amount_chunk
                point_amount_cells = []
            if i == len(table[0]) - 1:
                point_amount_cells.append([i_x_set, amount_chunk])
                x_y_list.append([i_y_set, point_amount_cells, sum_for_date])
        # Rendering from the list the table
        self.t_axe_table = self.render_table(x_y_list, fieldnames)




if __name__ == '__main__':
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        # raw_data = [row for row in reader]
        table = TableForCreditSum(reader, reader.fieldnames)
    # group table by dates and points
    typing(table)
    table.sort_by(column_dict['дата'])

    new_table = Rearrange(table).two_axe_table(column_dict['дата'], column_dict['номер точки продажи (POS)'])
    new_table.sum()

    main_dict = {
        'ACCOUNT_RK': 'номер договора',
        'INTERNAL_ORG_ORIGINAL_RK': 'номер точки продажи (POS)',
        'LOAN_AMOUNT': 'сумма кредита',
        'APPLICATION_DT': 'дата'
    }
