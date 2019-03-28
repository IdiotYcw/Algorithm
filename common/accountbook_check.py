import docx
import csv
from datetime import datetime

fee_list = []
book_list = []

# with open('../materials/books/台账.csv', 'r') as f:
#     reader = csv.reader(f, dialect='excel', delimiter=',')
#     for line in reader:
#         name = line[0].strip()
#         scale = float(line[4].strip().replace(',', ''))
#         end_date = datetime.strptime(line[7].strip(), '%m/%d/%Y')
#         book_list.append([name, scale, end_date])
#
# print(book_list)
#
# with open('../materials/books/金额费用.csv', 'r') as f:
#     reader = csv.reader(f, dialect='excel', delimiter=',')
#     for line in reader:
#         code = line[0].strip()
#         name = line[1].strip()
#         manager_fee = float(line[2].strip().replace(',', ''))
#         sale_fee = float(line[5].strip().replace(',', ''))
#         client_fee = float(line[6].strip().replace(',', ''))
#         fee_list.append([code, name, manager_fee, sale_fee, client_fee])
#
# print(fee_list)

doc = docx.Document('/home/ycw/PycharmProjects/algorithm/materials/books/CN_SCE265_PB0002_2018-12-31_马上模板.docx')
print(doc.paragrahs)
print(doc.tables)
print(doc.sections)
print(doc.styles)
