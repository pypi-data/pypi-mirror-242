from paquete_ibero_al_SRR_EIGO import ibero_al as AL

filas = int(input("Ingrese el número de filas de las matrices: "))
columnas = int(input("Ingrese el número de columnas de las matrices: "))
escalar = float(input("Ingrese el escalar: "))

print("Ingrese la primera matriz:")
matriz_A = AL.pedir_matriz(filas, columnas)

print("Ingrese la segunda matriz:")
matriz_B = AL.pedir_matriz(filas, columnas)

resultado_suma = AL.suma_matrices(matriz_A, matriz_B)
resultado_resta = AL.resta_matrices(matriz_A, matriz_B)
resultado_determinante = AL.determinante(matriz_A, filas, columnas)
resultado_escalar = AL.producto_escalar(escalar, matriz_A)

print(resultado_suma)
print("\n", resultado_resta)
print("\n", resultado_determinante)
print("\n", resultado_escalar)
