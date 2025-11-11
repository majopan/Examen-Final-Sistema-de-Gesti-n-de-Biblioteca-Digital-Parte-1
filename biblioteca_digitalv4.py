# ===========================================
# 📚 SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL
# Examen Final - Parte 1 (Versión con respuestas)
# ===========================================

from datetime import datetime

# ===========================================
# 📌 FUNCIONES BASE
# ===========================================

def contar_libros_por_genero(libros):
    """Cuenta cuántos libros hay por cada género."""
    conteo = {}
    for libro in libros:
        genero = libro["genero"]
        conteo[genero] = conteo.get(genero, 0) + 1
    return conteo


def usuarios_con_estado(usuarios, estado):
    """Filtra los usuarios por estado ('activo' o 'inactivo')."""
    return [u for u in usuarios if u["estado"] == estado]


def validar_isbn(isbn):
    """Valida si el ISBN tiene 13 dígitos numéricos."""
    return isinstance(isbn, str) and isbn.isdigit() and len(isbn) == 13


def agregar_libro(libros, nuevo_libro):
    """Agrega un libro si el ISBN es válido y no está duplicado."""
    if not validar_isbn(nuevo_libro["isbn"]):
        return False
    for libro in libros:
        if libro["isbn"] == nuevo_libro["isbn"]:
            return False
    libros.append(nuevo_libro)
    return True


# ===========================================
# 💰 MULTAS Y FECHAS
# ===========================================

def calcular_multa(fecha_limite, fecha_devolucion_real):
    """Calcula la multa según días de retraso (1000 por día)."""
    formato = "%Y-%m-%d"
    f_limite = datetime.strptime(fecha_limite, formato)
    f_real = datetime.strptime(fecha_devolucion_real, formato)
    dias_atraso = (f_real - f_limite).days
    return max(0, dias_atraso * 1000)


# ===========================================
# 📦 PRÉSTAMOS Y DEVOLUCIONES
# ===========================================

def registrar_prestamo(prestamos, libros, id_usuario, isbn, fecha_prestamo, fecha_devolucion):
    """Registra un préstamo si el libro está disponible."""
    for libro in libros:
        if libro["isbn"] == isbn and libro["disponible"]:
            libro["disponible"] = False
            prestamo = {
                "usuario_id": id_usuario,
                "isbn": isbn,
                "fecha_prestamo": fecha_prestamo,
                "fecha_devolucion": fecha_devolucion,
                "estado": "activo",
                "multa": 0
            }
            prestamos.append(prestamo)
            return True
    return False


def registrar_devolucion(prestamos, libros, id_usuario, isbn, fecha_devolucion_real):
    """Registra la devolución, calcula multa y cambia estado del libro."""
    for prestamo in prestamos:
        if (prestamo["usuario_id"] == id_usuario and
            prestamo["isbn"] == isbn and
            prestamo["estado"] == "activo"):
            
            prestamo["fecha_devolucion_real"] = fecha_devolucion_real
            prestamo["estado"] = "devuelto"
            
            multa = calcular_multa(prestamo["fecha_devolucion"], fecha_devolucion_real)
            prestamo["multa"] = multa
            
            for libro in libros:
                if libro["isbn"] == isbn:
                    libro["disponible"] = True
                    break
            
            return True
    return False


def total_multas_por_usuario(prestamos, id_usuario):
    """Suma todas las multas de un usuario."""
    total = 0
    for p in prestamos:
        if p["usuario_id"] == id_usuario:
            total += p.get("multa", 0)
    return total


# ===========================================
# 📊 REPORTES
# ===========================================

def libros_mas_prestados(prestamos):
    """Retorna los libros más prestados en orden descendente."""
    conteo = {}
    for p in prestamos:
        conteo[p["isbn"]] = conteo.get(p["isbn"], 0) + 1
    return sorted(conteo.items(), key=lambda x: x[1], reverse=True)


def usuarios_con_multas_pendientes(prestamos):
    """Devuelve lista de usuarios que tienen multas > 0."""
    usuarios = set()
    for p in prestamos:
        if p.get("multa", 0) > 0:
            usuarios.add(p["usuario_id"])
    return list(usuarios)


def disponibilidad_por_genero(libros):
    """Devuelve cantidad de libros disponibles por género."""
    conteo = {}
    for libro in libros:
        if libro["disponible"]:
            conteo[libro["genero"]] = conteo.get(libro["genero"], 0) + 1
    return conteo


def prestamos_activos_por_usuario(prestamos, id_usuario):
    """Devuelve todos los préstamos activos de un usuario."""
    return [p for p in prestamos if p["usuario_id"] == id_usuario and p["estado"] == "activo"]


# ===========================================
# 🧪 CASOS DE PRUEBA CON RESULTADOS VISIBLES
# ===========================================

if __name__ == "__main__":
    print("\n=== 📘 EXAMEN FINAL: SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL ===\n")

    libros = [
        {"isbn": "9780140328721", "titulo": "Matilda", "genero": "Infantil", "disponible": True},
        {"isbn": "9788497594257", "titulo": "El Principito", "genero": "Ficción", "disponible": True},
    ]
    usuarios = [
        {"id": 1, "nombre": "Ana", "estado": "activo"},
        {"id": 2, "nombre": "Luis", "estado": "inactivo"},
    ]
    prestamos = []

    # === CASO 1 ===
    print("📖 CASO 1: Contar libros por género")
    resultado1 = contar_libros_por_genero(libros)
    print("Resultado:", resultado1)
    print("Esperado: {'Infantil': 1, 'Ficción': 1}\n")

    # === CASO 2 ===
    print("👥 CASO 2: Filtrar usuarios activos")
    resultado2 = usuarios_con_estado(usuarios, "activo")
    print("Resultado:", resultado2)
    print("Esperado: [{'id': 1, 'nombre': 'Ana', 'estado': 'activo'}]\n")

    # === CASO 3 ===
    print("📚 CASO 3: Agregar un nuevo libro con ISBN válido")
    nuevo_libro = {"isbn": "9780307474278", "titulo": "1984", "genero": "Ficción", "disponible": True}
    exito3 = agregar_libro(libros, nuevo_libro)
    print("Libro agregado:", exito3)
    print("Listado actual de libros:", libros, "\n")

    # === CASO 4 ===
    print("📦 CASO 4: Registrar préstamo y devolución con multa")
    registrar_prestamo(prestamos, libros, 1, "9780307474278", "2024-05-01", "2024-05-10")
    registrar_devolucion(prestamos, libros, 1, "9780307474278", "2024-05-12")
    print("Listado de préstamos:", prestamos)
    print("Libros actualizados:", libros)
    print("Esperado: multa = 2000, estado préstamo = 'devuelto', libro disponible = True\n")

    # === CASO 5 BONUS ===
    print("⭐ CASO 5 (BONUS): Libros más prestados")
    resultado5 = libros_mas_prestados(prestamos)
    print("Resultado:", resultado5)
    print("Esperado: [('9780307474278', 1)]\n")

    # === RESULTADO FINAL ===
    print("✅ Todos los casos ejecutados correctamente si los resultados coinciden con los esperados.\n")
