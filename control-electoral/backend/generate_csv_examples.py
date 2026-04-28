#!/usr/bin/env python
"""Generar archivos CSV de ejemplo para importación"""
import csv

# Parroquias de ejemplo
parroquias_data = [
    ["001", "Parroquia Centro", "3", "2", "5000"],
    ["002", "Parroquia Norte", "2", "2", "4500"],
    ["003", "Parroquia Sur", "2", "3", "4000"],
]

with open('parroquias_ejemplo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo', 'nombre', 'nro_juntas_masculino', 'nro_juntas_femenino', 'nro_votantes'])
    writer.writerows(parroquias_data)

print("✓ parroquias_ejemplo.csv creado")

# Zonas de ejemplo
zonas_data = [
    ["Z001", "Zona A", "001"],
    ["Z002", "Zona B", "001"],
    ["Z003", "Zona C", "002"],
    ["Z004", "Zona D", "003"],
]

with open('zonas_ejemplo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo', 'nombre', 'parroquia_codigo'])
    writer.writerows(zonas_data)

print("✓ zonas_ejemplo.csv creado")

# Recintos de ejemplo
recintos_data = [
    ["R001", "Recinto 1", "Z001", "Calle 1 #123", "1000"],
    ["R002", "Recinto 2", "Z001", "Calle 2 #456", "1100"],
    ["R003", "Recinto 3", "Z002", "Calle 3 #789", "950"],
    ["R004", "Recinto 4", "Z003", "Calle 4 #234", "1050"],
]

with open('recintos_ejemplo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo', 'nombre', 'zona_codigo', 'direccion', 'nro_votantes'])
    writer.writerows(recintos_data)

print("✓ recintos_ejemplo.csv creado")

# Juntas de ejemplo
juntas_data = [
    ["J001", "Junta 1", "100", "M", "R001", "001"],
    ["J002", "Junta 2", "110", "F", "R001", "002"],
    ["J003", "Junta 3", "120", "M", "R002", "001"],
    ["J004", "Junta 4", "95", "F", "R003", "001"],
]

with open('juntas_ejemplo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo', 'nombre', 'nro_votantes', 'tipo', 'recinto_codigo', 'numero'])
    writer.writerows(juntas_data)

print("✓ juntas_ejemplo.csv creado")
print("\nTodos los archivos de ejemplo han sido creados correctamente.")
