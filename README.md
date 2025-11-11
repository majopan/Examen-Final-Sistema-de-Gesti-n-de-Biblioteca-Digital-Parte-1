# 📚 Examen Final: Sistema de Gestión de Biblioteca Digital - Parte 1

## Descripción del Proyecto

Este repositorio contiene la implementación de un **Sistema de Gestión de Biblioteca Digital** desarrollado como examen final de Programación 2. El sistema permite gestionar libros, usuarios y préstamos utilizando exclusivamente estructuras de datos básicas de Python (listas y diccionarios).

## 🎯 Objetivo de Aprendizaje

Aplicar listas y diccionarios para construir un mini-sistema consistente que separa **registro** (muta datos con validaciones) de **consulta** (no muta y agrega información).

## ✨ Características Principales

- **Gestión completa** de libros, usuarios y préstamos
- **Sistema de multas** automático por retrasos
- **Validaciones robustas** para todas las operaciones
- **Consultas y reportes** avanzados
- **Arquitectura limpia** con separación de responsabilidades

## 🛠️ Funcionalidades Implementadas

### 📖 Gestión de Libros
| Función | Descripción |
|---------|-------------|
| `agregar_libro()` | Registra nuevos libros con validación |
| `validar_isbn()` | Verifica formato ISBN-### |
| `contar_libros_por_genero()` | Estadísticas por género |
| `disponibilidad_por_genero()` | Ejemplares disponibles por categoría |

### 👥 Gestión de Usuarios
| Función | Descripción |
|---------|-------------|
| `usuarios_con_estado()` | Filtra usuarios activos/inactivos |
| `usuarios_con_multas_pendientes()` | Lista usuarios con multas |

### 🔄 Operaciones de Préstamo
| Función | Descripción |
|---------|-------------|
| `registrar_prestamo()` | Controla préstamos con validaciones |
| `registrar_devolucion()` | Gestiona devoluciones y multas |
| `prestamos_activos_por_usuario()` | Consulta préstamos vigentes |

### 💰 Sistema de Multas
| Función | Descripción |
|---------|-------------|
| `calcular_multa()` | Calcula multas ($2000/día) |
| `total_multas_por_usuario()` | Suma multas acumuladas |

### 📊 Consultas y Reportes
| Función | Descripción |
|---------|-------------|
| `libros_mas_prestados()` | Ranking de libros populares |
| `usuarios_con_multas_pendientes()` | Listado ordenado por deuda |
