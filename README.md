# Restaurante App - Semana 12

## Utilización de colecciones para la mejora de rendimiento

**Estudiante:** Jannneth Talía Males Conejo

---

## Descripción

Aplicación de restaurante desarrollada en Python con Programación Orientada a Objetos.

En la Semana 12 se mejoró el sistema de la Semana 11 mediante el uso de colecciones e índices en memoria para optimizar búsquedas y consultas frecuentes, manteniendo la persistencia de datos mediante archivos JSON.

## Mejoras realizadas

- Se mantienen las listas principales de productos, usuarios y ventas.
- Se implementaron diccionarios (`dict`) como índices para búsquedas rápidas.
- Se optimizó la búsqueda de productos mediante su código.
- Se optimizó la búsqueda de usuarios mediante su identificación.
- Se optimizó la consulta de ventas por usuario mediante un índice.
- Los índices se actualizan al registrar, modificar o eliminar información.
- Al iniciar el sistema, los índices se reconstruyen a partir de los datos almacenados en JSON.
- Se utiliza un conjunto (`set`) para obtener categorías únicas de productos.

## Colecciones utilizadas

- **Listas (`list`):** almacenan los productos, usuarios y ventas.
- **Diccionarios (`dict`):** permiten realizar búsquedas directas por código de producto, identificación de usuario y ventas asociadas a cada usuario.
- **Conjunto (`set`):** permite obtener categorías únicas sin duplicados.

Estas estructuras permiten reducir recorridos innecesarios de las colecciones principales y mejorar el rendimiento de las consultas frecuentes.

## Estructura del proyecto

    restaurante_app/
    ├── datos/
    │   ├── productos.json
    │   ├── usuarios.json
    │   └── ventas.json
    ├── modelos/
    │   ├── __init__.py
    │   ├── producto.py
    │   ├── usuario.py
    │   └── venta.py
    ├── servicios/
    │   ├── __init__.py
    │   ├── archivo_servicio.py
    │   └── restaurante.py
    ├── main.py
    └── README.md

## Forma de ejecución

Desde la carpeta principal del proyecto ejecutar:

    python restaurante_app/main.py

## Pruebas realizadas

Se verificó:

- Registro y carga de usuarios y productos.
- Búsqueda de productos por código.
- Búsqueda de usuarios por identificación.
- Consulta de ventas por usuario.
- Registro de una venta y disminución correcta del stock.
- Actualización de productos y sincronización del índice.
- Obtención de categorías únicas mediante `set`.
- Cierre y nueva ejecución del programa para comprobar la recuperación de datos desde JSON y la reconstrucción de los índices.

## Conclusión

La Semana 12 mejora `restaurante_app` mediante el uso de colecciones adecuadas e índices en memoria, permitiendo realizar búsquedas y consultas frecuentes de forma más eficiente, sin perder las funcionalidades de la Semana 11 ni la persistencia de los datos.