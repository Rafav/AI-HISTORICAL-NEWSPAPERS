#!/bin/bash

# Función para verificar si pdfinfo está instalado
check_dependencies() {
    if ! command -v pdfinfo &> /dev/null; then
        echo "Error: pdfinfo no está instalado"
        echo "Por favor, instala poppler-utils:"
        echo "En Ubuntu/Debian: sudo apt-get install poppler-utils"
        echo "En CentOS/RHEL: sudo yum install poppler-utils"
        echo "En MacOS: brew install poppler"
        exit 1
    fi
}

# Función para contar páginas de un PDF
count_pdf_pages() {
    local file="$1"
    pdfinfo "$file" 2>/dev/null | grep "Pages:" | awk '{print $2}'
}

# Función principal
main() {
    local directorio="${1:-.}"  # Si no se proporciona directorio, usa el actual
    local total_paginas=0
    local total_archivos=0
    local archivos_error=()
    
    # Verificar dependencias
    check_dependencies
    
    echo "Analizando PDFs en: $directorio"
    echo "----------------------------------------"
    
    # Encontrar todos los archivos PDF y procesarlos
    while IFS= read -r -d '' archivo; do
        paginas=$(count_pdf_pages "$archivo")
        if [ -n "$paginas" ] && [ "$paginas" -eq "$paginas" ] 2>/dev/null; then
            printf "%-70s %5d páginas\n" "$(realpath --relative-to="$directorio" "$archivo")" "$paginas"
            ((total_paginas += paginas))
            ((total_archivos++))
        else
            archivos_error+=("$archivo")
        fi
    done < <(find "$directorio" -type f -name "*.pdf" -print0)
    
    # Mostrar resumen
    echo "----------------------------------------"
    echo "Resumen:"
    echo "Total de archivos PDF: $total_archivos"
    echo "Total de páginas: $total_paginas"
    
    # Mostrar errores si los hay
    if [ ${#archivos_error[@]} -gt 0 ]; then
        echo -e "\nArchivos con error:"
        for archivo in "${archivos_error[@]}"; do
            echo "- $archivo"
        done
    fi
}

# Ejecutar script
main "$@"
