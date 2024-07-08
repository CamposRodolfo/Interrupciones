from prettytable import PrettyTable

table = PrettyTable(["Column 1", "Column 2", "Column 3"])
table.add_row(["A", "B", "C"])
table.add_row(["F", "O", "O"])
table.add_row(["B", "A", "R"])

print("\n")
print("\n")

print(table)

print("\n")
print("\n")
print("\n")

for row in table:
    print(row)