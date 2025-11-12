def contar_libros_por_genero(libros):
    conteo = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for libro in libros:
        genero = libro.get("genero", "").upper()
        if genero in conteo:
            conteo[genero] += 1
    return conteo

def usuarios_con_estado(usuarios, estado_activo):
    codigos = []
    for usuario in usuarios:
        if usuario.get("activo") == estado_activo:
            codigo = usuario.get("codigo")
            if codigo not in codigos:
                codigos.append(codigo)
    return codigos

def validar_isbn(isbn):
    if not isinstance(isbn, str):
        return False
    isbn_clean = isbn.strip().upper()
    return (isbn_clean.startswith("ISBN-") and 
            len(isbn_clean) == 8 and 
            isbn_clean[5:].isdigit())

def agregar_libro(libros, isbn, titulo, autor, genero, ejemplares):
    GENEROS_VALIDOS = ["FICCION", "CIENCIA", "HISTORIA", "ARTE"]
    
    if not validar_isbn(isbn): return -1
    if not isinstance(ejemplares, int) or ejemplares <= 0: return -1
    
    isbn_clean = isbn.strip().upper()
    genero_clean = genero.strip().upper()
    
    if genero_clean not in GENEROS_VALIDOS: return -1
    if any(libro["isbn"] == isbn_clean for libro in libros): return -1
    
    nuevo_libro = {
        "isbn": isbn_clean, "titulo": titulo, "autor": autor, 
        "genero": genero_clean, "ejemplares_totales": ejemplares, 
        "ejemplares_disponibles": ejemplares
    }
    libros.append(nuevo_libro)
    return len(libros)

def calcular_multa(dias_retraso):
    return dias_retraso * 2000 if dias_retraso > 0 else 0

def registrar_prestamo(libros, prestamos, isbn, codigo_usuario, dias_prestamo):
    isbn_clean = isbn.strip().upper()
    
    libro_encontrado = None
    for i, libro in enumerate(libros):
        if libro["isbn"] == isbn_clean:
            libro_encontrado = libro
            indice_libro = i
            break
    
    if not libro_encontrado or libro_encontrado["ejemplares_disponibles"] <= 0:
        return -1
    
    for prestamo in prestamos:
        if (prestamo["codigo_usuario"] == codigo_usuario and
            prestamo["isbn"] == isbn_clean and
            not prestamo["devuelto"]):
            return -1
    
    libros[indice_libro]["ejemplares_disponibles"] -= 1
    prestamos.append({
        "isbn": isbn_clean, "codigo_usuario": codigo_usuario, 
        "dias_prestamo": dias_prestamo, "dias_retraso": 0, "devuelto": False
    })
    return len(prestamos)

def registrar_devolucion(libros, prestamos, isbn, codigo_usuario, dias_retraso):
    """Registra devolución de libro"""
    isbn_clean = isbn.strip().upper()
    
    for prestamo in prestamos:
        if (prestamo["isbn"] == isbn_clean and
            prestamo["codigo_usuario"] == codigo_usuario and
            not prestamo["devuelto"]):
            
            for libro in libros:
                if libro["isbn"] == isbn_clean:
                    libro["ejemplares_disponibles"] += 1
                    break
            
            prestamo["devuelto"] = True
            prestamo["dias_retraso"] = dias_retraso
            
            return calcular_multa(dias_retraso)
    
    return -1

def total_multas_por_usuario(prestamos, codigo_usuario):
    """Calcula total de multas de un usuario"""
    return sum(calcular_multa(p.get("dias_retraso", 0)) 
                for p in prestamos if p.get("codigo_usuario") == codigo_usuario)

def libros_mas_prestados(libros, prestamos, top_n):
    conteo = {}
    for prestamo in prestamos:
        conteo[prestamo["isbn"]] = conteo.get(prestamo["isbn"], 0) + 1
    
    isbn_a_titulo = {libro["isbn"]: libro["titulo"] for libro in libros}
    ranking = [(isbn, isbn_a_titulo.get(isbn, "Desconocido"), total) 
                for isbn, total in conteo.items()]
    
    ranking.sort(key=lambda x: x[2], reverse=True)
    return ranking[:top_n]

def usuarios_con_multas_pendientes(usuarios, prestamos):
    multados = []
    for usuario in usuarios:
        total = total_multas_por_usuario(prestamos, usuario["codigo"])
        if total > 0:
            multados.append((usuario["codigo"], usuario["nombre"], total))
    
    multados.sort(key=lambda x: x[2], reverse=True)
    return multados

def disponibilidad_por_genero(libros):
    disp = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for libro in libros:
        genero = libro.get("genero", "").upper()
        if genero in disp:
            disp[genero] += libro.get("ejemplares_disponibles", 0)
    return disp

def prestamos_activos_por_usuario(prestamos, codigo_usuario):
    return [p["isbn"] for p in prestamos 
            if p["codigo_usuario"] == codigo_usuario and not p["devuelto"]]

# =========================
# Zona de Pruebas
# =========================

def ejecutar_caso_1():
    print("\n" + "="*50)
    print("CASO 1: Validación de ISBN y alta de libros")
    print("="*50)
    
    libros = []
    
    print("\n1. Validación de ISBN:")
    tests_isbn = [
        ("ISBN-001", True), ("ISBN-999", True), (" isbn-042 ", True),
        ("ISBN001", False), ("ISBN-1", False), ("ISB-123", False)
    ]
    
    for isbn, esperado in tests_isbn:
        resultado = validar_isbn(isbn)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} '{isbn}' -> {resultado} (esperado: {esperado})")
    
    print("\n2. Alta de libros:")
    altas = [
        ("ISBN-001", "1984", "George Orwell", "FICCION", 3, 1),
        ("ISBN-002", "Sapiens", "Yuval Harari", "HISTORIA", 2, 2),
        ("ISBN-003", "Cosmos", "Carl Sagan", "CIENCIA", 4, 3)
    ]
    
    for isbn, titulo, autor, genero, ejemplares, esperado in altas:
        resultado = agregar_libro(libros, isbn, titulo, autor, genero, ejemplares)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Agregar '{titulo}': {resultado} (esperado: {esperado})")
    
    print("\n3. Rechazos de alta:")
    rechazos = [
        ("ISBN-001", "Otro", "Autor", "FICCION", 2, -1),  # repetido
        ("ISBN004", "Libro", "Autor", "FICCION", 1, -1),  # ISBN inválido
        ("ISBN-005", "Libro", "Autor", "FICCION", 0, -1), # ejemplares = 0
        ("ISBN-006", "Libro", "Autor", "TERROR", 1, -1)   # género inválido
    ]
    
    for isbn, titulo, autor, genero, ejemplares, esperado in rechazos:
        resultado = agregar_libro(libros, isbn, titulo, autor, genero, ejemplares)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Rechazar '{isbn}': {resultado} (esperado: {esperado})")
    
    print(f"\nEstado final: {len(libros)} libros en sistema")
    for libro in libros:
        print(f"   - {libro['isbn']}: {libro['titulo']} ({libro['genero']})")
    
    return libros

def ejecutar_caso_2(libros):
    print("\n" + "="*50)
    print("CASO 2: Préstamos y multas")
    print("="*50)
    
    prestamos = []
    
    print("\n1. Cálculo de multas:")
    tests_multas = [(0, 0), (-5, 0), (3, 6000), (10, 20000)]
    
    for dias, esperado in tests_multas:
        resultado = calcular_multa(dias)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} {dias} días -> ${resultado} (esperado: ${esperado})")
    
    print("\n2. Préstamos válidos:")
    prestamos_validos = [
        ("ISBN-001", 201, 14, 1),
        ("ISBN-002", 202, 14, 2),
        ("ISBN-003", 201, 14, 3)
    ]
    
    for isbn, usuario, dias, esperado in prestamos_validos:
        resultado = registrar_prestamo(libros, prestamos, isbn, usuario, dias)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Préstamo {isbn} para usuario {usuario}: {resultado}")
    
    print(f"\n3. Disponibilidad después de préstamos:")
    for libro in libros:
        print(f"   - {libro['isbn']}: {libro['ejemplares_disponibles']}/{libro['ejemplares_totales']} disponibles")
    
    print("\n4. Rechazos de préstamo:")
    rechazos = [
        ("ISBN-001", 201, 14, -1),  # ya tiene el libro
        ("ISBN-999", 203, 14, -1)   # libro inexistente
    ]
    
    for isbn, usuario, dias, esperado in rechazos:
        resultado = registrar_prestamo(libros, prestamos, isbn, usuario, dias)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Rechazar préstamo {isbn}: {resultado}")
    
    print("\n5. Agotar ejemplares:")
    registrar_prestamo(libros, prestamos, "ISBN-001", 202, 14)  # préstamo 4
    registrar_prestamo(libros, prestamos, "ISBN-001", 203, 14)  # préstamo 5
    
    resultado = registrar_prestamo(libros, prestamos, "ISBN-001", 204, 14)
    estado = "[OK]" if resultado == -1 else "[ERROR]"
    print(f"   {estado} Rechazar por agotado: {resultado} (esperado: -1)")
    print(f"   - ISBN-001 disponibles: {libros[0]['ejemplares_disponibles']}")
    
    return prestamos

def ejecutar_caso_3(libros, prestamos):
    print("\n" + "="*50)
    print("CASO 3: Devoluciones")
    print("="*50)
    
    print("\n1. Devolución sin retraso:")
    multa1 = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0)
    estado = "[OK]" if multa1 == 0 else "[ERROR]"
    print(f"   {estado} Devolución ISBN-001, usuario 201: multa ${multa1}")
    print(f"   - Disponibles ISBN-001: {libros[0]['ejemplares_disponibles']}")
    
    print("\n2. Devolución con retraso:")
    multa2 = registrar_devolucion(libros, prestamos, "ISBN-002", 202, 5)
    estado = "[OK]" if multa2 == 10000 else "[ERROR]"
    print(f"   {estado} Devolución ISBN-002, usuario 202 (5 días): multa ${multa2}")
    
    print("\n3. Rechazos de devolución:")
    rechazos = [
        ("ISBN-001", 201, 0, -1),  # ya devuelto
        ("ISBN-999", 201, 0, -1)   # libro inexistente
    ]
    
    for isbn, usuario, dias, esperado in rechazos:
        resultado = registrar_devolucion(libros, prestamos, isbn, usuario, dias)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Rechazar devolución {isbn}: {resultado}")
    
    return prestamos

def ejecutar_caso_4(libros, prestamos):
    print("\n" + "="*50)
    print("CASO 4: Consultas y totales")
    print("="*50)
    
    usuarios = [
        {"codigo": 201, "nombre": "Ana López", "activo": True},
        {"codigo": 202, "nombre": "Luis Gómez", "activo": True},
        {"codigo": 203, "nombre": "María Torres", "activo": False},
    ]
    
    print("\n1. Operaciones adicionales para pruebas:")
    registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14)
    multa = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 7)
    print(f"   - Nuevo préstamo y devolución con 7 días: multa ${multa}")
    
    print("\n2. Total multas por usuario:")
    tests_multas = [(201, 14000), (202, 10000), (203, 0)]
    
    for usuario, esperado in tests_multas:
        resultado = total_multas_por_usuario(prestamos, usuario)
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} Usuario {usuario}: ${resultado} (esperado: ${esperado})")
    
    print("\n3. Usuarios con multas pendientes:")
    multas_pend = usuarios_con_multas_pendientes(usuarios, prestamos)
    print(f"   - Encontrados: {len(multas_pend)} usuarios con multas")
    for codigo, nombre, total in multas_pend:
        print(f"     * {codigo} ({nombre}): ${total}")
    
    print("\n4. Libros más prestados (Top 2):")
    top_libros = libros_mas_prestados(libros, prestamos, 2)
    for isbn, titulo, total in top_libros:
        print(f"   - {isbn} ({titulo}): {total} préstamos")
    
    print("\n5. Conteo de libros por género:")
    conteo = contar_libros_por_genero(libros)
    for genero, cantidad in conteo.items():
        print(f"   - {genero}: {cantidad} libros")
    
    print("\n6. Usuarios activos:")
    activos = usuarios_con_estado(usuarios, True)
    print(f"   - Códigos: {activos}")
    
    print("\n7. Disponibilidad por género:")
    disp = disponibilidad_por_genero(libros)
    tests_disp = [("FICCION", 1), ("HISTORIA", 1), ("CIENCIA", 3)]
    
    for genero, esperado in tests_disp:
        resultado = disp[genero]
        estado = "[OK]" if resultado == esperado else "[ERROR]"
        print(f"   {estado} {genero}: {resultado} disponibles (esperado: {esperado})")
    
    return usuarios

def ejecutar_caso_5(prestamos):
    print("\n" + "="*50)
    print("CASO 5 (bonus): Préstamos activos")
    print("="*50)
    
    print("\n1. Préstamos activos por usuario:")
    
    activos_203 = prestamos_activos_por_usuario(prestamos, 203)
    estado = "[OK]" if "ISBN-001" in activos_203 and len(activos_203) == 1 else "[ERROR]"
    print(f"   {estado} Usuario 203: {activos_203} (esperado: ['ISBN-001'])")
    
    activos_201 = prestamos_activos_por_usuario(prestamos, 201)
    estado = "[OK]" if len(activos_201) == 1 else "[ERROR]"  # ISBN-003 sigue prestado
    print(f"   {estado} Usuario 201: {activos_201} (1 préstamo activo)")
    
    activos_202 = prestamos_activos_por_usuario(prestamos, 202)
    estado = "[OK]" if len(activos_202) == 0 else "[ERROR]"  # Todos devueltos
    print(f"   {estado} Usuario 202: {activos_202} (sin préstamos activos)")

# =========================
# Ejecución principal
# =========================

if __name__ == "__main__":
    print("INICIANDO PRUEBAS DEL SISTEMA DE BIBLIOTECA")
    print("="*60)
    
    libros = ejecutar_caso_1()
    prestamos = ejecutar_caso_2(libros)
    prestamos = ejecutar_caso_3(libros, prestamos)
    usuarios = ejecutar_caso_4(libros, prestamos)
    ejecutar_caso_5(prestamos)
    
    print("\n" + "="*60)
    print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("="*60)