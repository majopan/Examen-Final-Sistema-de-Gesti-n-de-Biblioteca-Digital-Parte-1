import re 
# ============================================
# EXAMEN — Programación 2
# Diccionarios y Arreglos (Python)
# Tema: Sistema de Gestión de Biblioteca Digital
# ============================================
# Reglas de libros (simplificadas para este examen):
# - ISBN: formato ISBN-### (ISBN + 3 dígitos), ej: "ISBN-001", "ISBN-042"
# - Géneros: "FICCION", "CIENCIA", "HISTORIA", "ARTE"
# - Cada libro tiene un número de ejemplares disponibles
#
# Préstamos:
# - Duración estándar: 14 días
# - Multa por día de retraso: $2000
# - Un usuario no puede pedir el mismo libro si ya tiene uno prestado
#
# Recomendación: separar funciones de "consulta" (no mutan)
# y "registro" (sí mutan agregando a las listas).
#
# NO usar librerías externas. Usar solo listas y diccionarios.
# ============================================

GENEROS_VALIDOS = ["FICCION", "CIENCIA", "HISTORIA", "ARTE"]
COSTO_MULTA_DIARIA = 2000

# ----------------------------------------------------
# FUNCIONES AUXILIARES Y DE VALIDACIÓN
# ----------------------------------------------------

def validar_isbn(isbn):
    """
    Valida el formato del ISBN. (ISBN-###)
    """
    if not isinstance(isbn, str):
        return False
        
    isbn_limpio = isbn.strip().upper()
    patron = r"^ISBN-\d{3}$" 
    
    return bool(re.fullmatch(patron, isbn_limpio))
# Requisito 3: OK

def calcular_multa(dias_retraso):
    """
    Calcula la multa por días de retraso.
    """
    if dias_retraso > 0:
        return dias_retraso * COSTO_MULTA_DIARIA
    else:
        return 0
# Requisito 5: OK

# ----------------------------------------------------
# FUNCIONES DE REGISTRO (SÍ MUTAN LAS LISTAS)
# ----------------------------------------------------

def agregar_libro(libros, isbn, titulo, autor, genero, ejemplares):
    """
    Agrega un libro si el ISBN es válido y no está repetido.
    """
    
    # 1) Validar ISBN
    if not validar_isbn(isbn):
        return -1
        
    isbn_normalizado = isbn.strip().upper()
    genero_normalizado = genero.strip().upper()
    
    # 2) El ISBN NO existe ya en 'libros'
    for libro in libros:
        if libro.get("isbn") == isbn_normalizado:
            return -1 
            
    # 3) ejemplares debe ser > 0
    if not isinstance(ejemplares, int) or ejemplares <= 0:
        return -1
        
    # 4) genero debe ser válido
    if genero_normalizado not in GENEROS_VALIDOS:
        return -1
        
    # Mutación de 'libros'
    nuevo_libro = {
        "isbn": isbn_normalizado,
        "titulo": titulo,
        "autor": autor,
        "genero": genero_normalizado,
        "ejemplares_totales": ejemplares,
        "ejemplares_disponibles": ejemplares
    }
    libros.append(nuevo_libro)
    return len(libros)
# Requisito 4: OK

def registrar_prestamo(libros, prestamos, isbn, codigo_usuario, dias_prestamo):
    """
    Registra un préstamo solo si hay ejemplares disponibles y el usuario
    no tiene ese libro prestado.
    """
    
    isbn_normalizado = isbn.strip().upper()
    libro_encontrado = None
    indice_libro = -1
    
    # 1) Buscar el libro 
    for i, libro in enumerate(libros):
        if libro.get("isbn") == isbn_normalizado:
            libro_encontrado = libro
            indice_libro = i
            break
            
    if libro_encontrado is None:
        return -1 
        
    # 2) ejemplares_disponibles > 0
    if libro_encontrado.get("ejemplares_disponibles", 0) <= 0:
        return -1 
        
    # 3) El usuario NO tiene un préstamo activo del mismo libro
    for prestamo in prestamos:
        if (prestamo.get("codigo_usuario") == codigo_usuario and
            prestamo.get("isbn") == isbn_normalizado and
            prestamo.get("devuelto") == False):
            return -1 

    # Efecto 1: Reduce ejemplares disponibles (Mutación de 'libros')
    libros[indice_libro]["ejemplares_disponibles"] -= 1
    
    # Efecto 2: Añade a prestamos (Mutación de 'prestamos')
    nuevo_prestamo = {
        "isbn": isbn_normalizado,
        "codigo_usuario": codigo_usuario,
        "dias_prestamo": dias_prestamo,
        "dias_retraso": 0,
        "devuelto": False
    }
    prestamos.append(nuevo_prestamo)
    return len(prestamos)
# Requisito 6: OK

def registrar_devolucion(libros, prestamos, isbn, codigo_usuario, dias_retraso):
    """
    Registra la devolución de un libro.
    """
    
    isbn_normalizado = isbn.strip().upper()
    prestamo_activo_encontrado = None
    
    # 1) Buscar el préstamo ACTIVO
    for prestamo in prestamos:
        if (prestamo.get("codigo_usuario") == codigo_usuario and
            prestamo.get("isbn") == isbn_normalizado and
            prestamo.get("devuelto") == False):
            prestamo_activo_encontrado = prestamo
            break
            
    if prestamo_activo_encontrado is None:
        return -1 
        
    # Buscar el libro (necesario para mutar ejemplares)
    libro_encontrado = None
    for libro in libros:
        if libro.get("isbn") == isbn_normalizado:
            libro_encontrado = libro
            break

    # Efecto 1: Calcular multa
    multa_generada = calcular_multa(dias_retraso)
    
    # Efecto 2 & 3: Marcar devuelto=True y actualizar dias_retraso (Mutación de 'prestamos')
    prestamo_activo_encontrado["devuelto"] = True
    prestamo_activo_encontrado["dias_retraso"] = dias_retraso
    
    # Efecto 4: Incrementar ejemplares disponibles (Mutación de 'libros')
    if libro_encontrado:
        libro_encontrado["ejemplares_disponibles"] += 1
        
    # Retorna la multa calculada.
    return multa_generada
# Requisito 7: OK

# ----------------------------------------------------
# FUNCIONES DE CONSULTA (NO MUTAN LAS LISTAS)
# ----------------------------------------------------

def contar_libros_por_genero(libros):
    """
    Cuenta cuántos libros hay de cada género.
    """
    conteo = {genero: 0 for genero in GENEROS_VALIDOS}
    
    for libro in libros:
        genero = libro.get("genero", "").upper()
        if genero in conteo:
            conteo[genero] += 1
            
    return conteo
# Requisito 1: OK

def usuarios_con_estado(usuarios, estado_activo):
    """
    Devuelve los códigos (sin repetidos y en orden de aparición) de usuarios
    con un estado dado.
    """
    codigos_filtrados = []
    
    for usuario in usuarios:
        if usuario.get("activo") == estado_activo:
            codigo = usuario.get("codigo")
            if codigo is not None and codigo not in codigos_filtrados:
                codigos_filtrados.append(codigo)
                
    return codigos_filtrados
# Requisito 2: OK

def total_multas_por_usuario(prestamos, codigo_usuario):
    """
    Suma el total de multas acumuladas por un usuario.
    """
    total_multa = 0
    for prestamo in prestamos:
        if prestamo.get("codigo_usuario") == codigo_usuario:
            dias_retraso = prestamo.get("dias_retraso", 0)
            total_multa += calcular_multa(dias_retraso) 
            
    return total_multa
# Requisito 8: OK

def libros_mas_prestados(libros, prestamos, top_n):
    """
    Retorna los N libros más prestados (ordenados de mayor a menor).
    """
    conteo_prestamos = {}
    for prestamo in prestamos:
        isbn = prestamo.get("isbn")
        if isbn:
            conteo_prestamos[isbn] = conteo_prestamos.get(isbn, 0) + 1
            
    mapa_libros = {libro["isbn"]: libro["titulo"] for libro in libros}
    
    ranking = []
    for isbn, total in conteo_prestamos.items():
        titulo = mapa_libros.get(isbn, "Título Desconocido")
        ranking.append((isbn, titulo, total))
        
    ranking_ordenado = sorted(ranking, key=lambda x: x[2], reverse=True)
    
    return ranking_ordenado[:top_n]
# Requisito 9: OK

def usuarios_con_multas_pendientes(usuarios, prestamos):
    """
    Retorna lista de usuarios que tienen préstamos con multas sin pagar.
    """
    lista_resultado = []
    
    for usuario in usuarios:
        codigo = usuario.get("codigo")
        nombre = usuario.get("nombre")
        total_multas = total_multas_por_usuario(prestamos, codigo)
        
        if total_multas > 0:
            lista_resultado.append((codigo, nombre, total_multas))
            
    lista_resultado_ordenada = sorted(lista_resultado, key=lambda x: x[2], reverse=True)
    
    return lista_resultado_ordenada
# Requisito 10: OK

def disponibilidad_por_genero(libros):
    """
    Calcula el total de ejemplares disponibles por género.
    """
    disponibilidad = {genero: 0 for genero in GENEROS_VALIDOS}
    
    for libro in libros:
        genero = libro.get("genero", "").upper()
        ejemplares_disponibles = libro.get("ejemplares_disponibles", 0)
        
        if genero in disponibilidad:
            disponibilidad[genero] += ejemplares_disponibles
            
    return disponibilidad
# Requisito 11: OK

def prestamos_activos_por_usuario(prestamos, codigo_usuario):
    """
    (Bonus) Retorna lista de ISBNs de libros que el usuario tiene prestados actualmente.
    """
    isbns_activos = []
    for prestamo in prestamos:
        if (prestamo.get("codigo_usuario") == codigo_usuario and 
            prestamo.get("devuelto") == False):
            isbns_activos.append(prestamo.get("isbn"))
            
    return isbns_activos
# Requisito 12: OK (Bonus)


# =========================
# Zona de pruebas automáticas
# =========================
if __name__ == "__main__":
    libros = []
    usuarios = []
    prestamos = []

    print("Plantilla cargada. Iniciando casos de prueba... 🚀")
    print("--------------------------------------------------")
    
    # =========================
    # CASO 1: Validación de ISBN y alta de libros
    # =========================
    print("## Caso 1: Validación de ISBN y alta de libros")
    
    # Requisito 3: validar_isbn(isbn)
    assert validar_isbn("ISBN-001") == True
    assert validar_isbn("ISBN-999") == True
    assert validar_isbn(" isbn-042 ") == True
    assert validar_isbn("ISBN001") == False
    assert validar_isbn("ISBN-1") == False
    assert validar_isbn("ISB-123") == False
    print("Requisito 3 (validar_isbn): OK ✅")

    # Requisito 4: agregar_libro(libros, ...)
    assert agregar_libro(libros, "ISBN-001", "1984", "George Orwell", "FICCION", 3) == 1
    assert agregar_libro(libros, "ISBN-002", "Sapiens", "Yuval Harari", "HISTORIA", 2) == 2
    assert agregar_libro(libros, "ISBN-003", "Cosmos", "Carl Sagan", "CIENCIA", 4) == 3
    # Rechazos
    assert agregar_libro(libros, "ISBN-001", "Otro libro", "Otro autor", "FICCION", 2) == -1  # repetido
    assert agregar_libro(libros, "ISBN004", "Libro", "Autor", "FICCION", 1) == -1  # ISBN inválido
    assert agregar_libro(libros, "ISBN-005", "Libro", "Autor", "FICCION", 0) == -1  # ejemplares = 0
    assert agregar_libro(libros, "ISBN-006", "Libro", "Autor", "TERROR", 1) == -1  # género inválido
    
    print("Requisito 4 (agregar_libro): OK ✅")
    print("Libros registrados:", len(libros))
    print("✅ Caso 1 superado")
    
    # =========================
    # CASO 2: Préstamos y multas
    # =========================
    print("\n## Caso 2: Préstamos y multas")
    
    # Requisito 5: calcular_multa(dias_retraso)
    assert calcular_multa(0) == 0
    assert calcular_multa(-5) == 0
    assert calcular_multa(3) == 6000
    assert calcular_multa(10) == 20000
    print("Requisito 5 (calcular_multa): OK ✅")

    # Requisito 6: registrar_prestamo(...)
    t0 = len(prestamos)
    assert registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) == t0 + 1
    assert libros[0]["ejemplares_disponibles"] == 2  
    t1 = len(prestamos)
    assert registrar_prestamo(libros, prestamos, "ISBN-002", 202, 14) == t1 + 1
    t2 = len(prestamos)
    assert registrar_prestamo(libros, prestamos, "ISBN-003", 201, 14) == t2 + 1
    # Rechazos
    assert registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) == -1  # ya tiene ese libro
    assert registrar_prestamo(libros, prestamos, "ISBN-999", 203, 14) == -1  # libro inexistente
    # Agotar ejemplares
    registrar_prestamo(libros, prestamos, "ISBN-001", 202, 14)
    registrar_prestamo(libros, prestamos, "ISBN-001", 203, 14)
    assert libros[0]["ejemplares_disponibles"] == 0
    assert registrar_prestamo(libros, prestamos, "ISBN-001", 204, 14) == -1  # sin ejemplares
    
    print("Requisito 6 (registrar_prestamo): OK ✅")
    print("Préstamos registrados:", len(prestamos))
    print("✅ Caso 2 superado")
    
    # =========================
    # CASO 3: Devoluciones
    # =========================
    print("\n## Caso 3: Devoluciones")
    
    # Requisito 7: registrar_devolucion(...)
    multa1 = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0)
    assert multa1 == 0
    assert libros[0]["ejemplares_disponibles"] == 1 
    
    multa2 = registrar_devolucion(libros, prestamos, "ISBN-002", 202, 5)
    assert multa2 == 10000 
    
    # Rechazo: préstamo inexistente o ya devuelto
    assert registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0) == -1  # ya devuelto
    assert registrar_devolucion(libros, prestamos, "ISBN-999", 201, 0) == -1  # libro inexistente
    
    print("Requisito 7 (registrar_devolucion): OK ✅")
    print(f'Ejemplares disponibles de "ISBN-001" después de devolución: {libros[0]["ejemplares_disponibles"]}')
    print("✅ Caso 3 superado")
    
    # =========================
    # CASO 4: Consultas y totales
    # =========================
    print("\n## Caso 4: Consultas y totales")
    usuarios = [
        {"codigo": 201, "nombre": "Ana López", "activo": True},
        {"codigo": 202, "nombre": "Luis Gómez", "activo": True},
        {"codigo": 203, "nombre": "María Torres", "activo": False},
    ]
    
    registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14)
    registrar_devolucion(libros, prestamos, "ISBN-001", 201, 7)
    
    # Requisito 8: total_multas_por_usuario(...)
    assert total_multas_por_usuario(prestamos, 201) == 14000
    assert total_multas_por_usuario(prestamos, 202) == 10000
    assert total_multas_por_usuario(prestamos, 203) == 0
    print("Requisito 8 (total_multas_por_usuario): OK ✅")
    print(f"Total multas 201: {total_multas_por_usuario(prestamos, 201)}, Total multas 202: {total_multas_por_usuario(prestamos, 202)}")
    
    # Requisito 10: usuarios_con_multas_pendientes(...)
    multas_pend = usuarios_con_multas_pendientes(usuarios, prestamos)
    assert len(multas_pend) == 2
    assert multas_pend[0][0] == 201
    assert multas_pend[0][2] == 14000
    print("Requisito 10 (usuarios_con_multas_pendientes): OK ✅")
    print(f"Usuarios con multas pendientes: {multas_pend}")
    
    # Requisito 9: libros_mas_prestados(...)
    top = libros_mas_prestados(libros, prestamos, 2)
    assert top[0][0] == "ISBN-001"
    assert top[0][2] == 4
    print("Requisito 9 (libros_mas_prestados): OK ✅")
    print(f"Top 2 libros más prestados: {top}")
    
    # Requisito 1: contar_libros_por_genero(...)
    conteo = contar_libros_por_genero(libros)
    assert conteo["FICCION"] == 1
    assert conteo["CIENCIA"] == 1
    assert conteo["HISTORIA"] == 1
    assert conteo["ARTE"] == 0
    print("Requisito 1 (contar_libros_por_genero): OK ✅")
    print(f"Conteo por género: {conteo}")
    
    # Requisito 2: usuarios_con_estado(...)
    activos = usuarios_con_estado(usuarios, True)
    assert 201 in activos and 202 in activos
    assert 203 not in activos
    print("Requisito 2 (usuarios_con_estado): OK ✅")
    print(f"Usuarios activos: {activos}")
    
    # Requisito 11: disponibilidad_por_genero(...)
    disp = disponibilidad_por_genero(libros)
    assert disp["FICCION"] == 1 
    assert disp["HISTORIA"] == 2   # VALOR CORREGIDO
    assert disp["CIENCIA"] == 3   
    assert disp["ARTE"] == 0
    print("Requisito 11 (disponibilidad_por_genero): OK ✅")
    print(f"Disponibilidad por género: {disp}")
    print("✅ Caso 4 superado")
    
    # =========================
    # CASO 5 (bonus): Préstamos activos
    # =========================
    print("\n## Caso 5 (bonus): Préstamos activos")
    
    # Requisito 12 (Bonus): prestamos_activos_por_usuario(...)
    activos_203 = prestamos_activos_por_usuario(prestamos, 203)
    assert "ISBN-001" in activos_203
    assert len(activos_203) == 1
    
    activos_201 = prestamos_activos_por_usuario(prestamos, 201)
    assert len(activos_201) == 1  
    assert "ISBN-003" in activos_201
    
    print("Requisito 12 (prestamos_activos_por_usuario): OK ✅")
    print(f"Préstamos activos 203: {activos_203}")
    print(f"Préstamos activos 201: {activos_201}")
    
    print("✅ Caso 5 (bonus) superado")
    print("--------------------------------------------------")
    print("✅ Todos los casos de prueba pasaron correctamente")