import os
import shutil
import logging
from typing import Dict, List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mover_pdfs.log'),
        logging.StreamHandler()
    ]
)

# Definir la muestra estratificada
muestra_por_año = {
    "sinfecha": [1],
    "1807": [73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351],
    "1808": [15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347],
    "1809": [21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358],
    "1810": [23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323],
    "1811": [22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355],
    "1812": [21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335],
    "1816": [12, 34, 56, 78, 98, 112],
    "1817": [23, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 311, 323, 334, 345, 356],
    "1818": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 352, 360],
    "1819": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 353, 361],
    "1820": [25, 48, 71, 94, 117, 140, 163, 186, 209, 232, 255, 278, 301, 324, 347, 370, 383, 396, 409, 422, 428],
    "1821": [24, 47, 70, 93, 116, 139, 162, 185, 208, 231, 254, 277, 300, 323, 346, 369, 382, 395, 408, 421, 427],
    "1822": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362],
    "1823": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 359],
    "1824": [24, 46, 68, 90, 112, 134, 156, 178, 200, 222, 244, 266, 288, 310, 332, 344, 355, 363],
    "1825": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 361],
    "1826": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 360],
    "1827": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 352, 359],
    "1828": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362],
    "1829": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 361],
    "1830": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 358]
}


def crear_directorio_validacion(directorio_base: str) -> str:
    """Crea el directorio principal de validación si no existe."""
    dir_validacion = os.path.join(directorio_base, "validacion_estadistica")
    if not os.path.exists(dir_validacion):
        os.makedirs(dir_validacion)
        logging.info(f"Creado directorio de validación: {dir_validacion}")
    return dir_validacion

def crear_subdirectorios_años(dir_validacion: str):
    """Crea subdirectorios para cada año en el directorio de validación."""
    for año in muestra_por_año.keys():
        dir_año = os.path.join(dir_validacion, año)
        if not os.path.exists(dir_año):
            os.makedirs(dir_año)
            logging.info(f"Creado subdirectorio para el año {año}: {dir_año}")

def obtener_pdfs_ordenados(directorio: str) -> List[str]:
    """Obtiene lista de PDFs ordenados alfabéticamente."""
    return sorted([f for f in os.listdir(directorio) if f.lower().endswith('.pdf')])

def mover_pdfs_muestra(directorio_base: str):
    """Mueve los PDFs seleccionados en la muestra a los subdirectorios por año en el directorio de validación."""
    dir_validacion = crear_directorio_validacion(directorio_base)
    crear_subdirectorios_años(dir_validacion)
    total_movidos = 0
    errores = 0

    for año, posiciones in muestra_por_año.items():
        dir_año_origen = os.path.join(directorio_base, año)
        dir_año_destino = os.path.join(dir_validacion, año)
        
        if not os.path.exists(dir_año_origen):
            logging.warning(f"No se encontró el directorio de origen para el año {año}")
            continue

        # Obtener lista ordenada de PDFs
        pdfs_ordenados = obtener_pdfs_ordenados(dir_año_origen)
        
        for posicion in posiciones:
            # Ajustar posición a índice base-0
            indice = posicion - 1
            
            if indice < len(pdfs_ordenados):
                archivo = pdfs_ordenados[indice]
                origen = os.path.join(dir_año_origen, archivo)
                destino = os.path.join(dir_año_destino, archivo)
                
                try:
                    shutil.copy2(origen, destino)
                    logging.info(f"Copiado: {origen} -> {destino}")
                    total_movidos += 1
                except Exception as e:
                    logging.error(f"Error al copiar {origen}: {str(e)}")
                    errores += 1
            else:
                logging.warning(f"Posición {posicion} fuera de rango para {año}. Total archivos: {len(pdfs_ordenados)}")

    logging.info(f"Proceso completado. Total movidos: {total_movidos}, Errores: {errores}")
    return total_movidos, errores

def verificar_muestra(directorio_base: str):
    """Verifica que las posiciones de la muestra no excedan el número de archivos disponibles."""
    for año, posiciones in muestra_por_año.items():
        dir_año = os.path.join(directorio_base, año)
        if os.path.exists(dir_año):
            pdfs_disponibles = len(obtener_pdfs_ordenados(dir_año))
            max_posicion = max(posiciones)
            if max_posicion > pdfs_disponibles:
                logging.warning(f"Año {año}: La posición máxima ({max_posicion}) excede el número de archivos disponibles ({pdfs_disponibles})")

if __name__ == "__main__":
    # Directorio base donde están las carpetas de los años
    DIRECTORIO_BASE = "."  # Modifica esto según tu estructura de directorios
    
    try:
        print("Verificando la muestra...")
        verificar_muestra(DIRECTORIO_BASE)
        
        print("\nProcediendo con la copia de archivos...")
        total_movidos, errores = mover_pdfs_muestra(DIRECTORIO_BASE)
        
        print(f"\nResumen:")
        print(f"Total de archivos copiados: {total_movidos}")
        print(f"Total de errores: {errores}")
    except Exception as e:
        logging.error(f"Error general en la ejecución: {str(e)}")
