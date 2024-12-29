# AI-HISTORICAL-NEWSPAPERS
Workflow for scrapping, AI parsing and creating web pages for historical Newspapers.



# 1. Introducción.

Este artículo detalla proceso de uso de la IA para la localización e identificación automática noticias literarias,artísticas y culturales, con especial atención al Siglo de Oro, en ejemplares de prensa del siglo XIX. Este procedimiento informático, aplicable a otras cabeceras, ha supuesto una reducción del  %[por determinar] del tiempo de localización de datos frente a la revisión manual de cada página. Así mismo se ha validado estadísticamente, lo que ha permitido a los investigadores dar por bueno el resultado de las consultas a la IA. Por último se detallan los entregables que de manera automática se generan con la información localizada.


# 2. Caso de Estudio: El Diario Mercantil de Cádiz
La elección del Diario Mercantil de Cádiz como objeto de análisis ha sido determinada por el profesor Jaime Galbarro, de la Universidad de Sevilla. Los ejemplares se encuentran digitalizados en el portal de Prensa Histórica https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625 Esta cabecera comienza en 1807 y se extingue en 1830, con 7.456 ejemplares y un total de  37.381 páginas a procesar. Ha resultado ser un conjunto de datos excelente, por distintos motivos:

a) Es un periódico generalista, que incluye noticias económicas, culturales, sociales. 
b) Incluye períodos históricos donde se cortaron todas las actividades culturales por motivos bélicos 
c) Hay períodos con ausencia de teatro y danza por motivos religiosos, por ejemplo durante la Cuaresma. 
d) Los ejemplares digitalizados tienen buena calidad 
e) No están uniformados los números de página de cada ejemplar.


# 3. Prompt incial para estudiar la viabilidad del método. 

Hay dos aspectos clave para el uso de IA en este caso de uso:
a) La IA no puede inventarse datos que no figuren en las noticias.
b) La información que devuelve la IA debe ser sistemática.


Debemos por tanto minimizar la posibilidad de que se incluyan alucinaciones en los resultados, que aparecen tanto si el origen de la información son páginas escaneadas como si fuera texto escrito. Pruebas con Qwen2-VL-72B, Claude y ChatGPT han demostrado que aún no tenemos disponibles IA que sean 100% fiables en textos completos. Herramientas como Transkribus o Surya dan mejores resultados en tanto que no añaden información pero aun no llegan al 100% de fiablidad y tampoco resultan útiles cuando hay maquetación diferente a la estándar, porque intercalan filas y columnas. En modelos LLM se ha evidenciado que las alucinaciones son menores cuando se pide que localice información y luego transcriba el párrafo. 

Tanto con datos en forma de imagen como textuales, para usar los datos de forma óptima en las investigaciones posteriores, pediremos que los resultados que devuelva la IA estén normalizados, organizados, faciliten posteriores búsquedas y filtrados así como la localización de forma ágil de los hallazgos.


Con estas premisas se diseña un prompt, que se prueba en dos ejemplares. El prompt es el siguiente:
```
1. TRANSCRIPCIÓN BASE:
- Realiza el OCR y transcribe el texto completo manteniendo el formato original en español
- Preserva la estructura por columnas, secciones, titulares y fechas
- Mantén todos los elementos tipográficos (cursivas, negritas, etc.)
- Indica texto poco legible con [...]
- Conserva notas al pie, encabezados y pies de página
- Para cada página, indica tanto el número del PDF como el número impreso del periódico (ej: "PDF p.1 / Periódico p.774")

2. ANÁLISIS LITERARIO:
Identifica y extrae sistemáticamente:
a) Referencias directas a:
- Autores clásicos españoles (especialmente Siglo de Oro)
- Obras literarias específicas, indicando:
  * Título completo
  * Género (comedia, drama, loa, auto, entremés, etc.)
  * Autor (si se menciona)
  * Número de actos o jornadas (si se especifica)
- Citas textuales de obras
- Notas al pie sobre literatura
b) Referencias indirectas:
- Imitaciones estilísticas
- Parodias literarias
- Adaptaciones de géneros o formas literarias clásicas
- Métrica o estructuras poéticas reconocibles

3. ANÁLISIS CULTURAL:
Identifica referencias a:
- Música y teatro (incluyendo:
  * Tipo de pieza musical/teatral
  * Intérpretes/compañías
  * Lugar de representación
  * Horario)
- Artes plásticas
- Educación y academia
- Costumbres y vida social
- Política y sociedad
- Religión y moral

Devuelve un JSON con la siguiente estructura:
{
    "Título": "",
    "Fecha": "",
    "Número": "",
    "LITERATURA": boolean,
    "PAGINAS_LITERATURA": [{
        "pdf": número,
        "periodico": número,
        "contenido": "Transcripción completa de la sección. Todos los párrafos, sin acortar"
    }],
    "ARTICULOS_LITERATURA": [{
        "tipo": "referencia_directa|indirecta",
        "autor": "nombre del autor referenciado",
        "obra": {
            "titulo": "",
            "genero": "",
            "actos": número,
            "autor_obra": "si se especifica",
            "lugar de representación": ""
        },
        "paginas": [{
            "pdf": número,
            "periodico": número
        }],
        "citas": ["citas textuales si existen"],
        "contexto": "explicación del uso o relevancia"
    }],
    "MUSICA": boolean,
    "PAGINAS_MUSICA": [{
        "pdf": número,
        "periodico": número
    }],
    "ARTICULOS_MUSICA": [{
        "tipo": "genero_musical",
        "interprete": "nombre",
        "lugar": "ubicación",
        "paginas": [{
            "pdf": número,
            "periodico": número
        }],
        "contexto": "descripción"
    }],
    "OTRAS_REFERENCIAS_CULTURALES": [{
        "tema": "categoría cultural",
        "paginas": [{
            "pdf": número,
            "periodico": número
        }],
        "descripcion": "explicación del contenido",
        "conexiones": ["referencias a otros elementos del documento"]
    }]
}

Para cada elemento identificado, proporciona:
- Ubicación exacta (números de página PDF y periódico)
- Transcripción literal de las secciones completas. Mínimo el párrafo.
- Contexto y significación en el documento
- Conexiones con otros elementos identificados
- Para obras literarias y musicales busca el autor y fecha de la obra

```

La comprobación manual de 2 ejemplares es correcta, por lo que pasamos a la siguiente fase.

# 4. Automatizaciones.

La gran ventaja de las Humanidades digitales es que incorporando informáticos a los proyectos surgen automatismos que ahorran tiempo, sistematizan los procesos y dan seguridad a la hora de abordar proyectos masivos.

## 4.1 Scrapping.

Por scrapping entendemos un conjunto de técnicas para extraer datos de páginas web. En el caso de Prensa histórica, los resultados de la web muestran enlaces con el texto PDF y la dirección URL del ejemplar digitalizado. Nos interesa extraer esas direcciones para descargarlas posteriormente. Para ello existen varias técnicas, en el caso de la web de Prensa Histórica, al mostrar resultdos por año podemos usar el complemento DownThemAll y en filtro rápido escribir PDF.

Mostramos aquí una segunda opción, la usada en el proyecto, orientada al ámbito educativo porque usa búsquedas desde la consola del navegador usando expresiones regulares. Dentro del navegador web, localizar PDF -> botón derecho ->inspeccionar. Con esto se nos muestra como se construyen los enlaces.Para descargarlos, en la consola del navegador, se pega este código:

```
let bodyHtml = document.body.innerHTML;let regex = /<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>\s*(.*PDF.*)\s*<\/a>/g;
let hrefs = [];
let match;
let totalLinks = 0; // Variable to store the count of matching links

// Busca todas las coincidencias
while ((match = regex.exec(bodyHtml)) !== null) {
    // Añade el href a la lista
    hrefs.push(match[1]);
   
    // Si el sitio tiene una base para la URL de descarga
    let url_pdf = match[1].startsWith('http') ? match[1] : 'https://prensahistorica.mcu.es/' + match[1];
   
    // Muestra el enlace en la consola
    console.log('Enlace a PDF: ' + url_pdf);
   
    // Aumenta el contador de enlaces
    totalLinks++;
}

// Muestra el total de enlaces encontrados
console.log('Total de enlaces PDF encontrados: ' + totalLinks);
```
Se guarda el resultado de la consola y se repite para cada año.Una vez obtenidos los enlaces de descarga, se procede a descargarlos.

Opción a) Con el propio DownThemAll.
Opcion b) Script de descarga ética. Si bien DownThemAll permite una descarga rápida y eficaz, se ha creado un programa que descargue uno a uno pero añadiendo pausas entre descarga que impidan saturar el servidor.
Opción c) Extensiones específicas de descarga para esa web concreta, si las hubiera. Para Prensa Histórica, HemerotecaBNE hay extensiones para Chrome que permiten descargas masivas de los resultados de búsqueda. 

Al finalizar este paso ya tenemos el corpus a investigar.


## 4.2. Unificación de datos.

En función de los distintos métodos de descarga usados, los pdf descargados pueden tener nomenclatura distinta que es aconsejable normalizar. En este caso concreto podríamos tener pdf con nombres como 2043097.pdf y como grupo.dopath.1002043097 Es clave mantener la coherencia de los nombres de archivo y directorios.


# 5. Validación estadística. 

En esta fase del proyecto disponemos ya de un prompt válido y el corpus completo. Es necesario comprobar que los resultados correctos, usando una  muestra estadísticamente significativa. Para ello se le pide a la IA que seleccione un conjunto de muestras, considerado que tenemos una población finita de 7500 documentos y que queremos tener nivel de confianza 95%, margen de error 5% y una variabilidad esperada del 50%. Nos propone estos ejemplares a analizar

# Muestra estratificada por años

## Sin fecha
- 1 (único ejemplar)

## 1807 (18 ejemplares)
73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351

## 1808 (17 ejemplares)
15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347

## 1809 (18 ejemplares)
21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358

## 1810 (16 ejemplares)
23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323

## 1811 (17 ejemplares)
22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355

## 1812 (16 ejemplares)
21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335

## 1816 (6 ejemplares)
12, 34, 56, 78, 98, 112

## 1817 (18 ejemplares)
23, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 311, 323, 334, 345, 356

## 1818 (18 ejemplares)
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 352, 360

## 1819 (18 ejemplares)
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 353, 361

## 1820 (21 ejemplares)
25, 48, 71, 94, 117, 140, 163, 186, 209, 232, 255, 278, 301, 324, 347, 370, 383, 396, 409, 422, 428

## 1821 (21 ejemplares)
24, 47, 70, 93, 116, 139, 162, 185, 208, 231, 254, 277, 300, 323, 346, 369, 382, 395, 408, 421, 427

## 1822 (18 ejemplares)
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362

## 1823 (18 ejemplares)
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 359

## 1824 (18 ejemplares)
24, 46, 68, 90, 112, 134, 156, 178, 200, 222, 244, 266, 288, 310, 332, 344, 355, 363

## 1825 (18 ejemplares)
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 361

## 1826 (18 ejemplares)
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 360

## 1827 (18 ejemplares)
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 352, 359

## 1828 (18 ejemplares)
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362

## 1829 (18 ejemplares)
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 361

## 1830 (17 ejemplares)
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 358


Se crea un pequeño programa que copia los ejemplares correspondientes, por año, para empezar a crear los resultados. Claude AI tiene la posibilidad de usar una API (Application Programming Interface) en lugar de preguntar uno a uno. Se crea un pequeño programa en Python se lanza para cada ejemplar. Tenemos dos posibilidades

## 6.1. Resultados en tiempo real. Coste de 0,01$ por página y resultados inmediatos.

```
for file in *.pdf; do
  python3 diario-mercantil-a-json.py "$file" > "${file%.pdf}.json";
done
```

## 6.2. Lotes. Coste de 0,005$ por página. Se lanzan las preguntas y posteriormente (24 horas, aunque suele ser menor el tiempo de espera) se recupera la salida.

### 6.2.1. Procesamos 

for file in *.pdf; do     if [ -f "$file" ]; then         python3 /home/rafa/Descargas/Diario\ Mercantil/diario-claude/batch.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt;     fi; done


### 6.2.2. Descargamos la salida de los lotes. 
```
#!/bin/bash

# Procesar cada archivo que coincida con el patrón
for file in *_batch_order.txt; do
    if [ -f "$file" ]; then
        # Extraer el ID usando grep
        id=$(grep -o "msgbatch_[[:alnum:]]\+" "$file")
        
        # Procesar el nombre del archivo para obtener el nuevo nombre
        # Quita _batch_order del nombre del archivo
        output_file=$(basename "$file" "_batch_order.txt")_batch_output.txt
        
        if [ ! -z "$id" ]; then
            echo "Procesando archivo $file con ID: $id"
            echo "Guardando resultado en: $output_file"
            python recuperar_batch.py "$id" > "$output_file"
        else
            echo "No se encontró ID en el archivo $file"
        fi
    fi
done
```


### 6.2.3. Bajamos manualmente desde la consola un único resultado,que convertimos a JSON

En la consola https://console.anthropic.com/settings/workspaces/default/batches podemos ver los lotes y descargar cualquiera de ellos. El resultado es un JSONL que convertimos.
```
#Obtenemos el custom_id, que es el nombre del pdf.
custom_id=$(jq -r .custom_id msgbatch_****_results.jsonl)
# procesamos con jq y generamos la salida json con el nombre del pdf

jq -r '.result.message.content[0].text' msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl > "${custom_id}.json"
```
### 6.2.4. Limpiamos la salida descargada de cada id, para resultado bajado con pyth0n y msg_id
Una vez que comproibamos que la salida es correcta, lo precesmoa masivamente, en los ficheros *_batch_output.txt tenemos toda la onformación, que hay que extraer.

``
for file in *_batch_output.txt ;do  cat $file | sed 's/\\n//g' | sed 's/\\/\\\\/g' |grep -o '{.*}'| jq -r . >$(basename "$file" "_batch_output.txt").json; done
```

### 6.2.5. Unimos los resultados de cada año

Unimos los json, añadimos el año (que aparece en cada carpeta) y borramos frases extra que Claude añade al final de cada archivo,a modo de conclusión general.
```
./combinar_json_add_ejemplares.sh
```

OJO NECESITA QUE LA CARPETA SEA NUMÉRICA, I.E. 1819, DE LO CONTRARIO DA PROBLEMA

# 7. Generamos la web.

En este paso tenemos el prompt, el corpus y los resultados de investigar cada ejemplar. Necesitamos dar a los filólogos una herramienta útil de validar los resultados. Se diseña una web que da la posibilidad mostrar losa resultados y en la misma pestaña abrir los pdf, pudiendo hacer scroll de forma indendiente en los resultados y en el propio pdf, así como ir directamente a las páginas donde hay noticias literarias o artísticas.

Al ser datos organizados en JSON, nuestro proyecto requiere solo de 1 página web, la misma para cada año ,que lee el archivo combined.json y muestra los datos. Tiene una parte de código Javascript que itera y muestra los resultados, con independencia del año, del número de ejemplares, cuantas noticias ha encontrado, etc.

# 8. Compartimos los datos.
Para comprobar que la web diseñada es útil se opta por subir una pequeña muestra a Github, repositorio que permite mostrar páginas web. Una vez comprobada, dado el volumen de datos de este encargo, toda la información y los pdf se leen desde archivos locales.

(Añadir nota técnica para lanzar chrome que permita leer archivos locales)


copiamos el html  ojo, el de 1807 que no necesita carpeta pdfs

