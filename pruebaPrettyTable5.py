from prettytable import PrettyTable

# Inicializar la tabla con columnas y filas
table = PrettyTable(["Column 1", "Column 2", "Column 3", "Columna 4"])
table.add_row(["A", "B", "C",0])
table.add_row(["F", "-", "O", "A"])
table.add_row(["B", "A", "R",0])

# Imprimir la tabla original
print("Tabla original:")
print(table)

# Valor a buscar y nuevo valor a insertar
valor_buscar = "F"
nuevo_valor = "nuevo"

# Buscar la fila donde el primer valor coincide con valor_buscar
for fila in table._rows:
    if fila[0] == valor_buscar:
        # Recorrer las columnas de la fila para encontrar una celda vacía
        for i in range(1, len(fila)):
            if fila[i] is None or fila[i] == "" or fila[i] == "-":
                fila[i] = nuevo_valor
                break
        else:
            # Si no se encuentra una celda vacía, agregar una nueva columna
            nueva_columna = f"TP{len(table.field_names)}"
            table.field_names.append(nueva_columna)
            table._align[nueva_columna] = 'c'  # Establecer alineación horizontal para la nueva columna
            table._valign[nueva_columna] = 't'  # Establecer alineación vertical para la nueva columna
            for f in table._rows:
                f.append("-")
            fila[-1] = nuevo_valor
            break

# Imprimir la tabla modificada
print("\nTabla modificada:")
print(table)
