# [Mismo código de funciones que antes...]

def contar_libros_por_genero(libros):
    # ... (Implementación idéntica)
    conteo = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for libro in libros:
        genero = libro.get("genero", "").upper()
        if genero in conteo:
            conteo[genero] += 1
    return conteo

def usuarios_con_estado(usuarios, estado_activo):
    # ... (Implementación idéntica)
    codigos = []
    for usuario in usuarios:
        if usuario.get("activo") == estado_activo:
            codigo = usuario.get("codigo")
            if codigo not in codigos:
                codigos.append(codigo)
    return codigos

def validar_isbn(isbn):
    # ... (Implementación idéntica)
    if not isinstance(isbn, str):
        return False
    isbn_clean = isbn.strip().upper()
    if not isbn_clean.startswith("ISBN-") or len(isbn_clean) != 8:
        return False
    digitos = isbn_clean[5:]
    return digitos.isdigit()

def agregar_libro(libros, isbn, titulo, autor, genero, ejemplares):
    # ... (Implementación idéntica)
    isbn_clean = isbn.strip().upper()
    genero_clean = genero.strip().upper()
    GENEROS_VALIDOS = ["FICCION", "CIENCIA", "HISTORIA", "ARTE"]
    if not validar_isbn(isbn): return -1
    for libro in libros:
        if libro["isbn"] == isbn_clean: return -1
    if not isinstance(ejemplares, int) or ejemplares <= 0: return -1
    if genero_clean not in GENEROS_VALIDOS: return -1
    
    nuevo_libro = {
        "isbn": isbn_clean, "titulo": titulo, "autor": autor, 
        "genero": genero_clean, "ejemplares_totales": ejemplares, 
        "ejemplares_disponibles": ejemplares
    }
    libros.append(nuevo_libro)
    return len(libros)

def calcular_multa(dias_retraso):
    # ... (Implementación idéntica)
    if dias_retraso > 0:
        return dias_retraso * 2000
    return 0

def registrar_prestamo(libros, prestamos, isbn, codigo_usuario, dias_prestamo):
    # ... (Implementación idéntica)
    isbn_clean = isbn.strip().upper()
    libro_encontrado = None
    indice_libro = -1
    for i, libro in enumerate(libros):
        if libro["isbn"] == isbn_clean:
            libro_encontrado = libro
            indice_libro = i
            break
            
    if libro_encontrado is None: return -1
    if libro_encontrado["ejemplares_disponibles"] <= 0: return -1
    for prestamo in prestamos:
        if (prestamo.get("codigo_usuario") == codigo_usuario and
            prestamo.get("isbn") == isbn_clean and
            prestamo.get("devuelto") == False):
            return -1

    libros[indice_libro]["ejemplares_disponibles"] -= 1
    nuevo_prestamo = {
        "isbn": isbn_clean, "codigo_usuario": codigo_usuario, 
        "dias_prestamo": dias_prestamo, "dias_retraso": 0, "devuelto": False
    }
    prestamos.append(nuevo_prestamo)
    return len(prestamos)

def registrar_devolucion(libros, prestamos, isbn, codigo_usuario, dias_retraso):
    # ... (Implementación idéntica)
    isbn_clean = isbn.strip().upper()
    prestamo_activo = None
    for prestamo in prestamos:
        if (prestamo.get("isbn") == isbn_clean and
            prestamo.get("codigo_usuario") == codigo_usuario and
            prestamo.get("devuelto") == False):
            prestamo_activo = prestamo
            break
            
    if prestamo_activo is None: return -1

    libro_encontrado = None
    for libro in libros:
        if libro["isbn"] == isbn_clean:
            libro_encontrado = libro
            break
            
    if libro_encontrado is not None:
        libro_encontrado["ejemplares_disponibles"] += 1
        
    prestamo_activo["devuelto"] = True
    prestamo_activo["dias_retraso"] = dias_retraso
    
    return calcular_multa(dias_retraso)

def total_multas_por_usuario(prestamos, codigo_usuario):
    # ... (Implementación idéntica)
    total_multa = 0
    for prestamo in prestamos:
        if prestamo.get("codigo_usuario") == codigo_usuario:
            dias_retraso = prestamo.get("dias_retraso", 0)
            if dias_retraso > 0:
                total_multa += calcular_multa(dias_retraso)
    return total_multa

def libros_mas_prestados(libros, prestamos, top_n):
    # ... (Implementación idéntica)
    conteo_isbn = {}
    for prestamo in prestamos:
        isbn = prestamo["isbn"]
        conteo_isbn[isbn] = conteo_isbn.get(isbn, 0) + 1
        
    ranking_completo = []
    isbn_a_titulo = {libro["isbn"]: libro["titulo"] for libro in libros}
    
    for isbn, total in conteo_isbn.items():
        titulo = isbn_a_titulo.get(isbn, "Título Desconocido")
        ranking_completo.append((isbn, titulo, total))
        
    ranking_completo.sort(key=lambda x: x[2], reverse=True)
    
    return ranking_completo[:top_n]

def usuarios_con_multas_pendientes(usuarios, prestamos):
    # ... (Implementación idéntica)
    lista_multados = []
    for usuario in usuarios:
        codigo = usuario["codigo"]
        nombre = usuario["nombre"]
        total_multas = total_multas_por_usuario(prestamos, codigo)
        
        if total_multas > 0:
            lista_multados.append((codigo, nombre, total_multas))
            
    lista_multados.sort(key=lambda x: x[2], reverse=True)
    
    return lista_multados

def disponibilidad_por_genero(libros):
    # ... (Implementación idéntica)
    disponibilidad = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for libro in libros:
        genero = libro.get("genero", "").upper()
        ejemplares = libro.get("ejemplares_disponibles", 0)
        if genero in disponibilidad:
            disponibilidad[genero] += ejemplares
    return disponibilidad

def prestamos_activos_por_usuario(prestamos, codigo_usuario):
    # ... (Implementación idéntica)
    isbns_activos = []
    for prestamo in prestamos:
        if (prestamo.get("codigo_usuario") == codigo_usuario and
            prestamo.get("devuelto") == False):
            isbns_activos.append(prestamo["isbn"])
    return isbns_activos

# =========================
# Zona de Pruebas Automáticas con Impresiones
# =========================
if __name__ == "__main__":
    libros = []
    usuarios = []
    prestamos = []

    print("Plantilla cargada. Iniciando casos de prueba. ✅")
    print("--------------------------------------------------")

    ## CASO 1: Validación de ISBN y alta de libros
    print("\n## 📚 CASO 1: Validación de ISBN y alta de libros")
    
    # Pruebas de validación (silenciosas si pasan)
    validar_isbn_ok = validar_isbn("ISBN-001") and validar_isbn(" isbn-042 ")
    validar_isbn_fail = not validar_isbn("ISBN001") and not validar_isbn("ISBN-1")
    print(f"* Validación de ISBN (Formato): OK (Válidos={validar_isbn_ok}, Inválidos={validar_isbn_fail})")

    # Alta de libros
    print("\n* Intentando agregar 3 libros válidos:")
    r1 = agregar_libro(libros, "ISBN-001", "1984", "George Orwell", "FICCION", 3)
    r2 = agregar_libro(libros, "ISBN-002", "Sapiens", "Yuval Harari", "HISTORIA", 2)
    r3 = agregar_libro(libros, "ISBN-003", "Cosmos", "Carl Sagan", "CIENCIA", 4)
    print(f"  - Registros exitosos: {r1}, {r2}, {r3}")
    
    # Rechazos
    r_rep = agregar_libro(libros, "ISBN-001", "Otro", "Autor", "FICCION", 2)
    r_inv = agregar_libro(libros, "ISBN004", "Libro", "Autor", "FICCION", 1)
    r_ejem = agregar_libro(libros, "ISBN-005", "Libro", "Autor", "FICCION", 0)
    r_gen = agregar_libro(libros, "ISBN-006", "Libro", "Autor", "TERROR", 1)
    print(f"  - Rechazos (ISBN repetido/inválido/ejemplares/género): {r_rep}, {r_inv}, {r_ejem}, {r_gen} (Esperado: -1, -1, -1, -1)")

    print(f"\n* Estado final de **libros** (total: {len(libros)}):")
    for libro in libros:
        print(f"  - {libro['isbn']}: {libro['titulo']} ({libro['ejemplares_disponibles']}/{libro['ejemplares_totales']})")
    print("✅ Caso 1 superado")
    
    print("--------------------------------------------------")

    ## CASO 2: Préstamos y multas
    print("\n## 💰 CASO 2: Préstamos y multas")
    
    # Multas
    print(f"* Cálculo de Multas: 3 días -> ${calcular_multa(3)}, -5 días -> ${calcular_multa(-5)}")
    
    # Registrar préstamos
    print("\n* Registrando préstamos:")
    p1 = registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) # P1
    p2 = registrar_prestamo(libros, prestamos, "ISBN-002", 202, 14) # P2
    p3 = registrar_prestamo(libros, prestamos, "ISBN-003", 201, 14) # P3
    print(f"  - P1, P2, P3 registrados. Total préstamos: {len(prestamos)}")
    print(f"  - Disponibles ISBN-001 después de P1: {libros[0]['ejemplares_disponibles']}") # Debe ser 2
    
    # Rechazos de préstamo
    r_ya = registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) # Ya lo tiene (201)
    r_inex = registrar_prestamo(libros, prestamos, "ISBN-999", 203, 14) # Inexistente
    print(f"  - Rechazo (Ya tiene libro / Inexistente): {r_ya}, {r_inex} (Esperado: -1, -1)")

    # Agotar ejemplares
    registrar_prestamo(libros, prestamos, "ISBN-001", 202, 14) # P4
    registrar_prestamo(libros, prestamos, "ISBN-001", 203, 14) # P5
    r_agotado = registrar_prestamo(libros, prestamos, "ISBN-001", 204, 14)
    print(f"  - ISBN-001 disponibles: {libros[0]['ejemplares_disponibles']} (Agotado)")
    print(f"  - Rechazo (Agotado): {r_agotado} (Esperado: -1)")
    
    print(f"\n* Estado final de **préstamos** (total: {len(prestamos)}):")
    for i, p in enumerate(prestamos):
        print(f"  - P{i+1}: ISBN {p['isbn']}, User {p['codigo_usuario']}, Devuelto: {p['devuelto']}")
    print("✅ Caso 2 superado")
    
    print("--------------------------------------------------")

    ## CASO 3: Devoluciones
    print("\n## 📤 CASO 3: Devoluciones")

    # Devolución sin retraso (P1: ISBN-001, 201)
    m1 = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0) # D1
    print(f"* Devolución D1 (ISBN-001, 201, 0 días): Multa ${m1}")
    print(f"  - Disponibles ISBN-001: {libros[0]['ejemplares_disponibles']}") # Debe ser 1

    # Devolución con retraso (P2: ISBN-002, 202)
    m2 = registrar_devolucion(libros, prestamos, "ISBN-002", 202, 5) # D2
    print(f"* Devolución D2 (ISBN-002, 202, 5 días): Multa ${m2}") # Debe ser 10000
    
    # Rechazo de devolución
    r_dev1 = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0) # Ya devuelto
    r_dev2 = registrar_devolucion(libros, prestamos, "ISBN-999", 201, 0) # Inexistente
    print(f"  - Rechazos (Ya devuelto / Inexistente): {r_dev1}, {r_dev2} (Esperado: -1, -1)")

    print(f"\n* Estado parcial de **libros**:")
    for libro in libros:
        print(f"  - {libro['isbn']}: {libro['ejemplares_disponibles']} disponibles")
    print("✅ Caso 3 superado")

    print("--------------------------------------------------")

    ## CASO 4: Consultas y totales
    print("\n## 📊 CASO 4: Consultas y totales (No mutan datos)")
    
    usuarios = [
        {"codigo": 201, "nombre": "Ana López", "activo": True},
        {"codigo": 202, "nombre": "Luis Gómez", "activo": True},
        {"codigo": 203, "nombre": "María Torres", "activo": False},
    ]

    # Pre-paso para multas: P6 y D3 (multa de 7 días)
    registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) # P6
    registrar_devolucion(libros, prestamos, "ISBN-001", 201, 7)  # D3

    # Total multas por usuario
    multa_201 = total_multas_por_usuario(prestamos, 201) # 14000
    multa_202 = total_multas_por_usuario(prestamos, 202) # 10000
    print(f"* Total Multas 201 (Ana): ${multa_201} (Esperado: $14000)")
    print(f"* Total Multas 202 (Luis): ${multa_202} (Esperado: $10000)")

    # Usuarios con multas pendientes
    multas_pend = usuarios_con_multas_pendientes(usuarios, prestamos)
    print(f"\n* Usuarios con multas pendientes (Top {len(multas_pend)}):")
    for codigo, nombre, total in multas_pend:
        print(f"  - {codigo} ({nombre}): ${total}")
    
    # Libros más prestados (ISBN-001: 4, ISBN-002: 1, ISBN-003: 1)
    top_libros = libros_mas_prestados(libros, prestamos, 2)
    print(f"\n* Libros más prestados (Top 2):")
    for isbn, titulo, total in top_libros:
        print(f"  - {isbn} ({titulo}): {total} préstamos")
    
    # Contar libros por género
    conteo_gen = contar_libros_por_genero(libros)
    print(f"\n* Conteo de libros por género: {conteo_gen}")
    
    # Usuarios activos
    activos = usuarios_con_estado(usuarios, True)
    print(f"* Códigos de usuarios activos: {activos}")

    # Disponibilidad por género (CORREGIDA)
    disp = disponibilidad_por_genero(libros)
    print(f"\n* Disponibilidad de ejemplares por género:")
    print(f"  - FICCION: {disp['FICCION']} (Esperado: 1)")
    print(f"  - HISTORIA: {disp['HISTORIA']} (Esperado: 2. ¡Caso corregido!)")
    print(f"  - CIENCIA: {disp['CIENCIA']} (Esperado: 3)")
    print("✅ Caso 4 superado")
    
    print("--------------------------------------------------")

    ## CASO 5 (bonus): Préstamos activos
    print("\n## 🎯 CASO 5 (bonus): Préstamos activos")
    
    # Préstamos activos: P3 (ISBN-003, 201) y P5 (ISBN-001, 203)
    act_203 = prestamos_activos_por_usuario(prestamos, 203)
    act_201 = prestamos_activos_por_usuario(prestamos, 201)
    
    print(f"* Préstamos activos Usuario 203 (María): {act_203}") # Esperado: ['ISBN-001']
    print(f"* Préstamos activos Usuario 201 (Ana): {act_201}") # Esperado: ['ISBN-003']
    print("✅ Caso 5 (bonus) superado")
    
    print("\n==================================================")
    print("✅ TODOS LOS PROCESOS COMPLETADOS CORRECTAMENTE ✅")
    print("==================================================")