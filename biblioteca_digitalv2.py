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

def contar_libros_por_genero(libros):
    """
    Cuenta cuántos libros hay de cada género.

    Esta función NO modifica la lista original.
    """
    resultado = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for l in libros:
        genero = l.get("genero", "")
        if isinstance(genero, str):
            g = genero.strip().upper()
            if g in resultado:
                resultado[g] += 1
    return resultado

def usuarios_con_estado(usuarios, estado_activo):
    """
    Devuelve los códigos (sin repetidos y en orden de aparición) de usuarios
    con un estado dado. NO modifica la lista original.
    """
    vistos = set()
    salida = []
    for u in usuarios:
        codigo = u.get("codigo")
        activo = u.get("activo")
        if activo == estado_activo and codigo not in vistos:
            salida.append(codigo)
            vistos.add(codigo)
    return salida

def validar_isbn(isbn):
    """
    Valida el formato ISBN-### (ignora mayúsculas/minúsculas y espacios).
    """
    if not isinstance(isbn, str):
        return False
    s = isbn.strip().upper()
    # Debe empezar por "ISBN-" y luego exactamente 3 dígitos
    if not s.startswith("ISBN-"):
        return False
    suf = s[5:]
    if len(suf) != 3:
        return False
    if not suf.isdigit():
        return False
    return True

def _buscar_libro_por_isbn(libros, isbn):
    """
    Helper: retorna (indice, libro) donde isbn coincide (case-insensitive),
    o (None, None) si no existe.
    """
    if not isinstance(isbn, str):
        return None, None
    target = isbn.strip().upper()
    for idx, l in enumerate(libros):
        if l.get("isbn", "").upper() == target:
            return idx, l
    return None, None

def agregar_libro(libros, isbn, titulo, autor, genero, ejemplares):
    """
    Agrega un libro si validaciones pasan. Retorna nuevo len(libros) si agrega,
    -1 si no agrega.
    """
    # Validar formato ISBN
    if not validar_isbn(isbn):
        return -1
    # Validar ejemplares
    if not isinstance(ejemplares, int) or ejemplares <= 0:
        return -1
    # Validar genero
    gen = genero.strip().upper() if isinstance(genero, str) else ""
    validos = {"FICCION", "CIENCIA", "HISTORIA", "ARTE"}
    if gen not in validos:
        return -1
    # Verificar no exista ISBN en libros (case-insensitive)
    _, existente = _buscar_libro_por_isbn(libros, isbn)
    if existente is not None:
        return -1
    libro = {
        "isbn": isbn.strip().upper(),
        "titulo": titulo,
        "autor": autor,
        "genero": gen,
        "ejemplares_totales": ejemplares,
        "ejemplares_disponibles": ejemplares
    }
    libros.append(libro)
    return len(libros)

def calcular_multa(dias_retraso):
    """
    Retorna dias_retraso * 2000 si >0, sino 0.
    """
    try:
        d = int(dias_retraso)
    except Exception:
        return 0
    if d <= 0:
        return 0
    return d * 2000

def registrar_prestamo(libros, prestamos, isbn, codigo_usuario, dias_prestamo):
    """
    Registra un préstamo si libro existe, hay ejemplares y usuario no tiene
    ese libro activo. Retorna nuevo len(prestamos) si registra, -1 si rechaza.
    """
    if not isinstance(codigo_usuario, int):
        return -1
    # Buscar libro
    idx, libro = _buscar_libro_por_isbn(libros, isbn)
    if libro is None:
        return -1
    if libro.get("ejemplares_disponibles", 0) <= 0:
        return -1
    # Verificar usuario no tenga préstamo activo del mismo ISBN
    isbn_up = isbn.strip().upper()
    for p in prestamos:
        if p.get("isbn", "").upper() == isbn_up and p.get("codigo_usuario") == codigo_usuario and p.get("devuelto") == False:
            return -1
    # Registrar préstamo
    prest = {
        "isbn": isbn_up,
        "codigo_usuario": codigo_usuario,
        "dias_prestamo": dias_prestamo,
        "dias_retraso": 0,
        "devuelto": False
    }
    prestamos.append(prest)
    # Reducir ejemplares disponibles
    libros[idx]["ejemplares_disponibles"] = libros[idx].get("ejemplares_disponibles", 0) - 1
    return len(prestamos)

def registrar_devolucion(libros, prestamos, isbn, codigo_usuario, dias_retraso):
    """
    Marca préstamo como devuelto si existe uno activo; actualiza dias_retraso,
    incrementa ejemplares disponibles y retorna la multa (int). Retorna -1 si no hay préstamo activo.
    """
    if not isinstance(codigo_usuario, int):
        return -1
    isbn_up = isbn.strip().upper()
    # Buscar préstamo activo
    encontrado = None
    for p in prestamos:
        if p.get("isbn", "").upper() == isbn_up and p.get("codigo_usuario") == codigo_usuario and p.get("devuelto") == False:
            encontrado = p
            break
    if encontrado is None:
        return -1
    # Marcar devuelto y actualizar dias_retraso
    try:
        d = int(dias_retraso)
    except Exception:
        d = 0
    encontrado["devuelto"] = True
    encontrado["dias_retraso"] = d
    # Incrementar ejemplares disponibles del libro
    idx, libro = _buscar_libro_por_isbn(libros, isbn_up)
    if libro is not None:
        libros[idx]["ejemplares_disponibles"] = libros[idx].get("ejemplares_disponibles", 0) + 1
    # Retornar multa calculada
    return calcular_multa(d)

def total_multas_por_usuario(prestamos, codigo_usuario):
    """
    Suma multas (dias_retraso > 0) * 2000 para un usuario. NO modifica prestamos.
    """
    total = 0
    for p in prestamos:
        if p.get("codigo_usuario") == codigo_usuario:
            dr = p.get("dias_retraso", 0)
            if isinstance(dr, int) and dr > 0:
                total += dr * 2000
    return total

def libros_mas_prestados(libros, prestamos, top_n):
    """
    Retorna lista de tuplas (isbn, titulo, total_prestamos) ordenada desc por total.
    """
    conteo = {}
    for p in prestamos:
        key = p.get("isbn", "").upper()
        if key == "":
            continue
        conteo[key] = conteo.get(key, 0) + 1
    # Relacionar con título
    resultados = []
    for isbn_key, cnt in conteo.items():
        # buscar titulo en libros
        _, libro = _buscar_libro_por_isbn(libros, isbn_key)
        titulo = libro.get("titulo") if libro is not None else ""
        resultados.append((isbn_key, titulo, cnt))
    # Ordenar por cnt desc, luego por isbn asc para estabilidad
    resultados.sort(key=lambda x: (-x[2], x[0]))
    return resultados[:max(0, int(top_n))]

def usuarios_con_multas_pendientes(usuarios, prestamos):
    """
    Retorna list[(codigo, nombre, total_multas)] ordenada desc por total_multas.
    Solo incluye usuarios con multas > 0. NO modifica listas originales.
    """
    pendientes = []
    for u in usuarios:
        codigo = u.get("codigo")
        nombre = u.get("nombre", "")
        total = total_multas_por_usuario(prestamos, codigo)
        if total > 0:
            pendientes.append((codigo, nombre, total))
    pendientes.sort(key=lambda x: (-x[2], x[0]))
    return pendientes

def disponibilidad_por_genero(libros):
    """
    Suma ejemplares_disponibles por género. NO modifica libros.
    """
    resultado = {"FICCION": 0, "CIENCIA": 0, "HISTORIA": 0, "ARTE": 0}
    for l in libros:
        gen = l.get("genero", "")
        if isinstance(gen, str):
            g = gen.strip().upper()
            if g in resultado:
                try:
                    resultado[g] += int(l.get("ejemplares_disponibles", 0))
                except Exception:
                    pass
    return resultado

def prestamos_activos_por_usuario(prestamos, codigo_usuario):
    """
    Retorna lista de ISBNs (en mayúsculas) de préstamos activos (devuelto==False) de ese usuario.
    NO modifica prestamos.
    """
    salida = []
    for p in prestamos:
        if p.get("codigo_usuario") == codigo_usuario and p.get("devuelto") == False:
            salida.append(p.get("isbn", "").upper())
    return salida

# =========================
# Zona de pruebas manuales (ejecución de los casos de prueba solicitados)
# =========================
if __name__ == "__main__":
    # Variables compartidas para los tests
    libros = []
    usuarios = []
    prestamos = []

    # Para llevar control de resultados de cada caso
    resultados_casos = {}

    # ---------- Caso 1 ----------
    caso = 1
    ok_caso = True
    try:
        # ISBNs válidos
        r1 = validar_isbn("ISBN-001") == True
        r2 = validar_isbn("ISBN-999") == True
        r3 = validar_isbn(" isbn-042 ") == True  # espacios y minúsculas

        # ISBNs inválidos
        r4 = validar_isbn("ISBN001") == False
        r5 = validar_isbn("ISBN-1") == False
        r6 = validar_isbn("ISB-123") == False

        if not all([r1, r2, r3, r4, r5, r6]):
            ok_caso = False

        # Alta de libros válidos
        a1 = agregar_libro(libros, "ISBN-001", "1984", "George Orwell", "FICCION", 3) == 1
        a2 = agregar_libro(libros, "ISBN-002", "Sapiens", "Yuval Harari", "HISTORIA", 2) == 2
        a3 = agregar_libro(libros, "ISBN-003", "Cosmos", "Carl Sagan", "CIENCIA", 4) == 3

        if not all([a1, a2, a3]):
            ok_caso = False

        # Rechazos esperados
        rej1 = agregar_libro(libros, "ISBN-001", "Otro libro", "Otro autor", "FICCION", 2) == -1
        rej2 = agregar_libro(libros, "ISBN004", "Libro", "Autor", "FICCION", 1) == -1
        rej3 = agregar_libro(libros, "ISBN-005", "Libro", "Autor", "FICCION", 0) == -1
        rej4 = agregar_libro(libros, "ISBN-006", "Libro", "Autor", "TERROR", 1) == -1

        if not all([rej1, rej2, rej3, rej4]):
            ok_caso = False

    except Exception as e:
        ok_caso = False

    resultados_casos[caso] = ok_caso
    if ok_caso:
        print("✅ Caso 1 superado")
    else:
        print("❌ Caso 1 falló")

    # ---------- Caso 2 ----------
    caso = 2
    ok_caso = True
    try:
        prestamos = []
        # Multas
        if not (calcular_multa(0) == 0 and calcular_multa(-5) == 0 and calcular_multa(3) == 6000 and calcular_multa(10) == 20000):
            ok_caso = False

        # Registrar préstamos válidos
        t0 = len(prestamos)
        r = registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14)
        if r != t0 + 1:
            ok_caso = False
        if libros[0]["ejemplares_disponibles"] != 2:
            ok_caso = False

        t1 = len(prestamos)
        r = registrar_prestamo(libros, prestamos, "ISBN-002", 202, 14)
        if r != t1 + 1:
            ok_caso = False

        t2 = len(prestamos)
        r = registrar_prestamo(libros, prestamos, "ISBN-003", 201, 14)
        if r != t2 + 1:
            ok_caso = False

        # Rechazos
        if registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14) != -1:
            ok_caso = False
        if registrar_prestamo(libros, prestamos, "ISBN-999", 203, 14) != -1:
            ok_caso = False

        # Agotar ejemplares de ISBN-001 (tenía 3, ya se prestó 1 a 201; ahora prestamos a 202 y 203)
        registrar_prestamo(libros, prestamos, "ISBN-001", 202, 14)
        registrar_prestamo(libros, prestamos, "ISBN-001", 203, 14)
        if libros[0]["ejemplares_disponibles"] != 0:
            ok_caso = False
        if registrar_prestamo(libros, prestamos, "ISBN-001", 204, 14) != -1:
            ok_caso = False

    except Exception as e:
        ok_caso = False

    resultados_casos[caso] = ok_caso
    if ok_caso:
        print("✅ Caso 2 superado")
    else:
        print("❌ Caso 2 falló")

    # ---------- Caso 3 ----------
    caso = 3
    ok_caso = True
    try:
        # Devolución sin retraso (usuario 201 devuelve ISBN-001)
        multa1 = registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0)
        if multa1 != 0:
            ok_caso = False
        if libros[0]["ejemplares_disponibles"] != 1:
            ok_caso = False

        # Devolución con retraso (usuario 202 devuelve ISBN-002 con 5 días)
        multa2 = registrar_devolucion(libros, prestamos, "ISBN-002", 202, 5)
        if multa2 != 10000:
            ok_caso = False

        # Rechazos: ya devuelto o inexistente
        if registrar_devolucion(libros, prestamos, "ISBN-001", 201, 0) != -1:
            ok_caso = False
        if registrar_devolucion(libros, prestamos, "ISBN-999", 201, 0) != -1:
            ok_caso = False

    except Exception as e:
        ok_caso = False

    resultados_casos[caso] = ok_caso
    if ok_caso:
        print("✅ Caso 3 superado")
    else:
        print("❌ Caso 3 falló")

    # ---------- Caso 4 ----------
    caso = 4
    ok_caso = True
    try:
        usuarios = [
            {"codigo": 201, "nombre": "Ana López", "activo": True},
            {"codigo": 202, "nombre": "Luis Gómez", "activo": True},
            {"codigo": 203, "nombre": "María Torres", "activo": False},
        ]

        # Más préstamos y devoluciones para agregaciones
        # registrar préstamo ISBN-001 a 201
        registrar_prestamo(libros, prestamos, "ISBN-001", 201, 14)
        # devolver con 7 días de retraso
        registrar_devolucion(libros, prestamos, "ISBN-001", 201, 7)  # multa 14000

        # Total multas por usuario
        if total_multas_por_usuario(prestamos, 201) != 14000:
            ok_caso = False
        if total_multas_por_usuario(prestamos, 202) != 10000:
            ok_caso = False
        if total_multas_por_usuario(prestamos, 203) != 0:
            ok_caso = False

        # Usuarios con multas pendientes
        multas_pend = usuarios_con_multas_pendientes(usuarios, prestamos)
        if not (len(multas_pend) == 2 and multas_pend[0][0] == 201 and multas_pend[0][2] == 14000):
            ok_caso = False

        # Libros más prestados
        top = libros_mas_prestados(libros, prestamos, 2)
        if not (len(top) >= 1 and top[0][0] == "ISBN-001" and top[0][2] == 4):
            # según los préstamos realizados en los pasos anteriores ISBN-001 debe tener 4 préstamos
            ok_caso = False

        # Contar libros por género
        conteo = contar_libros_por_genero(libros)
        if not (conteo["FICCION"] == 1 and conteo["CIENCIA"] == 1 and conteo["HISTORIA"] == 1 and conteo["ARTE"] == 0):
            ok_caso = False

        # Usuarios activos
        activos = usuarios_con_estado(usuarios, True)
        if not (201 in activos and 202 in activos and 203 not in activos):
            ok_caso = False

        # Disponibilidad por género
        disp = disponibilidad_por_genero(libros)
        # Esperados según la secuencia de préstamos y devoluciones:
        # ISBN-001: originalmente 3, prestamos: varios, devoluciones: 2 => esperamos 1 disponible
        # ISBN-002: originalmente 2, fue prestado y devuelto => 1 disponible (según pasos previos)
        # ISBN-003: originalmente 4, se prestó 1 y no fue devuelto => 3 disponibles
        if not (disp["FICCION"] == 1 and disp["HISTORIA"] == 1 and disp["CIENCIA"] == 3):
            ok_caso = False

    except Exception as e:
        ok_caso = False

    resultados_casos[caso] = ok_caso
    if ok_caso:
        print("✅ Caso 4 superado")
    else:
        print("❌ Caso 4 falló")

    # ---------- Caso 5 (bonus) ----------
    caso = 5
    ok_caso = True
    try:
        # Préstamos activos del usuario 203
        activos_203 = prestamos_activos_por_usuario(prestamos, 203)
        if not ("ISBN-001" in activos_203 and len(activos_203) == 1):
            ok_caso = False

        # Préstamos activos del usuario 201 (según flujo, debe quedar 1: ISBN-003)
        activos_201 = prestamos_activos_por_usuario(prestamos, 201)
        if not (len(activos_201) == 1 and "ISBN-003" in activos_201):
            ok_caso = False

    except Exception as e:
        ok_caso = False

    resultados_casos[caso] = ok_caso
    if ok_caso:
        print("✅ Caso 5 (bonus) superado")
    else:
        print("❌ Caso 5 (bonus) falló")

    # Resultado final global
    todos_ok = all(resultados_casos.values())
    if todos_ok:
        print("✅ Todos los casos de prueba pasaron correctamente")
    else:
        print("❌ Algunos casos fallaron. Detalle por caso:")
        for c, res in resultados_casos.items():
            print(f"  - Caso {c}: {'OK' if res else 'NO'}")

    # ---- Informe detallado de cumplimiento de cada requisito ----
    print("\nInforme de requisitos (OK / NO):")
    checks = {}

    # 1) contar_libros_por_genero no modifica y retorna dict con las 4 claves
    try:
        copia = [dict(l) for l in libros]
        res = contar_libros_por_genero(libros)
        checks["contar_libros_por_genero"] = isinstance(res, dict) and all(k in res for k in ["FICCION","CIENCIA","HISTORIA","ARTE"]) and libros == copia
    except Exception:
        checks["contar_libros_por_genero"] = False

    # 2) usuarios_con_estado devuelve códigos sin repetidos y en orden
    try:
        utest = [{"codigo": 1, "activo": True}, {"codigo": 2, "activo": True}, {"codigo": 1, "activo": True}]
        r = usuarios_con_estado(utest, True)
        checks["usuarios_con_estado"] = r == [1,2]
    except Exception:
        checks["usuarios_con_estado"] = False

    # 3) validar_isbn pruebas directas
    try:
        checks["validar_isbn"] = (validar_isbn("ISBN-001") and not validar_isbn("ISBN1") and validar_isbn(" isbn-042 "))
    except Exception:
        checks["validar_isbn"] = False

    # 4) agregar_libro validaciones
    try:
        lib_tmp = []
        ok_a = agregar_libro(lib_tmp, "ISBN-010", "T", "A", "FICCION", 1) == 1
        ok_a &= agregar_libro(lib_tmp, "ISBN-010", "T2", "A2", "FICCION", 1) == -1  # repetido
        ok_a &= agregar_libro(lib_tmp, "ISBN011", "T", "A", "FICCION", 1) == -1  # ISBN inválido
        checks["agregar_libro"] = ok_a
    except Exception:
        checks["agregar_libro"] = False

    # 5) calcular_multa
    try:
        checks["calcular_multa"] = (calcular_multa(5) == 10000 and calcular_multa(0) == 0 and calcular_multa(-1) == 0)
    except Exception:
        checks["calcular_multa"] = False

    # 6) registrar_prestamo reglas
    try:
        lt = []
        pt = []
        agregar_libro(lt, "ISBN-020", "TT", "AA", "CIENCIA", 1)
        r1 = registrar_prestamo(lt, pt, "ISBN-020", 300, 14) == 1
        r2 = registrar_prestamo(lt, pt, "ISBN-020", 300, 14) == -1  # ya tiene el libro
        r3 = registrar_prestamo(lt, pt, "ISBN-999", 301, 14) == -1  # inexistente
        checks["registrar_prestamo"] = r1 and r2 and r3
    except Exception:
        checks["registrar_prestamo"] = False

    # 7) registrar_devolucion
    try:
        lt2 = []
        pt2 = []
        agregar_libro(lt2, "ISBN-030", "TT", "AA", "ARTE", 1)
        registrar_prestamo(lt2, pt2, "ISBN-030", 400, 14)
        multa = registrar_devolucion(lt2, pt2, "ISBN-030", 400, 2)
        okd = (multa == 4000 and lt2[0]["ejemplares_disponibles"] == 1 and pt2[0]["devuelto"] == True)
        checks["registrar_devolucion"] = okd and registrar_devolucion(lt2, pt2, "ISBN-030", 400, 0) == -1
    except Exception:
        checks["registrar_devolucion"] = False

    # 8) total_multas_por_usuario
    try:
        ptest = [{"codigo_usuario": 1, "dias_retraso": 3}, {"codigo_usuario": 1, "dias_retraso": 0}, {"codigo_usuario": 2, "dias_retraso": 2}]
        checks["total_multas_por_usuario"] = total_multas_por_usuario(ptest, 1) == 6000 and total_multas_por_usuario(ptest, 2) == 4000
    except Exception:
        checks["total_multas_por_usuario"] = False

    # 9) libros_mas_prestados
    try:
        lbs = [{"isbn": "ISBN-A", "titulo": "A"}]
        pms = [{"isbn": "ISBN-A"}, {"isbn": "ISBN-A"}, {"isbn": "ISBN-B"}]
        lm = libros_mas_prestados(lbs, pms, 2)
        checks["libros_mas_prestados"] = isinstance(lm, list) and lm[0][0] == "ISBN-A" and lm[0][2] == 2
    except Exception:
        checks["libros_mas_prestados"] = False

    # 10) usuarios_con_multas_pendientes
    try:
        us = [{"codigo": 1, "nombre":"X"}, {"codigo":2, "nombre":"Y"}]
        pm = [{"codigo_usuario":1,"dias_retraso":3},{"codigo_usuario":2,"dias_retraso":0}]
        uc = usuarios_con_multas_pendientes(us, pm)
        checks["usuarios_con_multas_pendientes"] = (len(uc) == 1 and uc[0][0] == 1 and uc[0][2] == 6000)
    except Exception:
        checks["usuarios_con_multas_pendientes"] = False

    # 11) disponibilidad_por_genero
    try:
        lbs2 = [{"genero":"FICCION","ejemplares_disponibles":2},{"genero":"FICCION","ejemplares_disponibles":1},{"genero":"CIENCIA","ejemplares_disponibles":3}]
        dg = disponibilidad_por_genero(lbs2)
        checks["disponibilidad_por_genero"] = (dg["FICCION"] == 3 and dg["CIENCIA"] == 3)
    except Exception:
        checks["disponibilidad_por_genero"] = False

    # 12) prestamos_activos_por_usuario
    try:
        pms2 = [{"isbn":"ISBN-X","codigo_usuario":5,"devuelto":False},{"isbn":"ISBN-Y","codigo_usuario":5,"devuelto":True}]
        pa = prestamos_activos_por_usuario(pms2, 5)
        checks["prestamos_activos_por_usuario"] = (pa == ["ISBN-X"])
    except Exception:
        checks["prestamos_activos_por_usuario"] = False

    # Imprimir resumen de requisitos
    for req, val in checks.items():
        print(f"{req}: {'OK' if val else 'NO'}")