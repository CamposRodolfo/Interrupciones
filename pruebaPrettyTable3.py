from prettytable import PrettyTable

table = PrettyTable(["Column 1", "Column 2", "Column 3"])
table.add_row(["A", "B", "C"])
table.add_row(["F", "O", "O"])
table.add_row(["B", "A", "R"])

for fila in table:
    fila.border = False
    fila.header = False
    print(fila.get_string(fields=["Column 1"]).strip()) # Column 1