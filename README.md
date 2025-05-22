# USO DE INTELIGENCIA ARTIFICIAL PARA LA LOCALIZACIÓN AUTOMÁTICA DE NOTICIAS EN PRENSA HISTÓRICA

_Use of Artificial Intelligence for the automatic localization of news in Historical press._

[![web final](/img/output.png)](https://rafav.github.io/diariomercantil/1807/index.html)

## 1. Introducción

Este artículo detalla cómo la Inteligencia Artificial permite localizar e identificar automáticamente noticias literarias, artísticas y culturales en ejemplares de prensa decimonónica, con énfasis especial en referencias al Siglo de Oro. El procedimiento informático desarrollado, aplicable a diversas cabeceras periodísticas, ha conseguido reducir significativamente el tiempo requerido en la búsqueda manual de información. La validación estadística del método ha otorgado fiabilidad a los resultados obtenidos mediante consultas automatizadas. Además, se describen los entregables generados automáticamente a partir de los hallazgos realizados.

**La propuesta se enmarca dentro de las necesidades de investigación del proyecto [«La institución del "Siglo de Oro". Procesos de construcción en la prensa periódica (1801-1868). SILEM III» (PID2022-136995NB-I00)](http://www.uco.es/servicios/ucopress/silem/), financiado por el Plan Nacional de Investigación del Ministerio de Ciencia e Innovación y dirigido por Mercedes Comellas (Universidad de Sevilla).**

## 2. Caso de estudio: Diario Mercantil de Cádiz

La selección del Diario Mercantil de Cádiz como objeto de análisis fue determinada por el [profesor Jaime Galbarro](https://www.jaimegalbarro.com/) de la Universidad de Sevilla, **en el contexto de investigación del mencionado proyecto.** Los ejemplares se encuentran disponibles en formato digital en el [portal de Prensa Histórica](https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625).

Esta publicación, que abarca desde 1807 hasta 1830, comprende 7.456 ejemplares con un total de 37.381 páginas. Constituye un conjunto documental idóneo por diversos motivos:

**a)** Es un periódico generalista con amplia variedad temática (noticias económicas, culturales y sociales).

**b)** Cubre un período histórico crucial como la Guerra de la Independencia, donde la vida cotidiana experimentó alteraciones significativas, incluyendo interrupciones en la actividad cultural.

**c)** Presenta etapas de suspensión temporal de actividades teatrales y otras diversiones públicas por motivos diversos, como los períodos de Cuaresma.

**d)** Ofrece ejemplares digitalizados de buena calidad para el procesamiento automatizado.


## 3. Diseño del prompt inicial

La implementación de IA en este proyecto ha tenido en cuenta dos consideraciones fundamentales:

**a)** La necesidad de prevenir que la IA alucine y genere datos inexistentes en las fuentes originales.

**b)** La importancia de obtener información sistemática y exhaustiva, sin omisión de referencias relevantes.

Resulta prioritario minimizar posibles alucinaciones en los resultados. Las pruebas realizadas con modelos como Qwen2-VL-72B, Claude y ChatGPT revelaron que actualmente no disponemos de soluciones completamente fiables para el procesamiento integral de textos históricos. Herramientas especializadas como Transkribus o Surya ofrecen mejores resultados en la detección de texto, ya que tratan las fuentes como imágenes, localizando cada frase por separado;aun así tampoco alcanzan una fiabilidad total. En las distintas pruebas con modelos de lenguaje extenso (LLM) se ha constatado que las alucinaciones disminuyen cuando se solicita la localización de información concreta y a continuación la transcripción literal de la información.

Con el objetivo de optimizar la utilidad de los datos extraídos, se ha establecido que los resultados proporcionados por la IA deben presentarse normalizados y organizados sistemáticamente, a fin de facilitar búsquedas posteriores, filtrados y la localización ágil de hallazgos relevantes.

Partiendo de estas consideraciones, se diseñó un *prompt*  específico que fue inicialmente probado con dos ejemplares:

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

La respuesta obtenida adopta un formato como el siguiente:

```json
{
  "Año": 1807,
  "datos": [
    {
      "PDF": "2043097.pdf",
      "Título": "DIARIO MERCANTIL DE CADIZ",
      "Fecha": "1 de enero de 1807",
      "Número": "6348",
      "LITERATURA": true,
      "PAGINAS_LITERATURA": [
        {
          "pdf": 4,
          "periodico": 4,
          "contenido": "TEATRO. = En el de esta Ciudad, en celebridad del dia, se dará la funcion siguiente: empezará la doble orquesta con una sinfonía; seguirá la Comedia titulada: Sancho Ortiz de la Roelas; concluida, se cantará un aria por la Sra. María Puy,cuya música es del celebre Maestro de este teatro D Esteban Cristiani; finalizada, se tocará la Overtura de la Batalla de Austerlitz,se baylarán las boleras por la Sra. Olivares y el Sr. Paz; terminando la funcion con el Saynete: El Remendon y la Prendera."
        }
      ],
      "ARTICULOS_LITERATURA": [
        {
          "tipo": "referencia_directa",
          "autor": "Lope de Vega",
          "obra": {
            "titulo": "Sancho Ortiz de la Roelas",
            "genero": "Comedia",
            "actos": null,
            "autor_obra": "Lope de Vega (adaptación)",
            "lugar de representación": "Teatro de Cádiz"
          },
          "paginas": [
            {
              "pdf": 4,
              "periodico": 4
            }
          ],
          "citas": [],
          "contexto": "Obra representada como parte de las diversiones públicas del día"
        },
        {
          "tipo": "referencia_directa",
          "obra": {
            "titulo": "El Remendon y la Prendera",
            "genero": "Sainete",
            "actos": null,
            "autor_obra": null,
            "lugar de representación": "Teatro de Cádiz"
          },
          "paginas": [
            {
              "pdf": 4,
              "periodico": 4
            }
          ],
          "citas": [],
          "contexto": "Sainete que cierra la función teatral"
        }
      ]
    }
}
```

La verificación manual de las respuestas con estos dos ejemplares confirmó su corrección, lo que permitió avanzar a la siguiente etapa del proyecto.

## 4. Automatizaciones

La incorporación de especialistas en informática a proyectos de Humanidades Digitales permite diseñar procesos automatizados, que optimizan tiempos, sistematizan procedimientos y aportan seguridad cuando se abordan proyectos de análisis a gran escala.

### 4.1 Scrapping

El término *scrapping* designa un conjunto de técnicas destinadas a extraer datos de páginas web. En el caso del portal de Prensa Histórica, los resultados de búsqueda muestran enlaces a ejemplares en formato PDF. Nuestro objetivo consiste en extraer estos enlaces y posteriormente descargarlos. Existen diversas técnicas para lograrlo; en el caso específico de la web de Prensa Histórica, con los resultados organizados por año, es posible emplear el complemento DownThemAll aplicando un filtro rápido con la palabra "pdf".

![downthemall extension](/img/downThemAll-quick-filter-PDF.png)

A continuación presentamos una segunda opción, la implementada en este proyecto, orientada al ámbito educativo. Se basa en consultas desde la consola del navegador mediante expresiones regulares. El procedimiento consiste en localizar un enlace PDF dentro del navegador web, hacer clic derecho y seleccionar "inspeccionar". El navegador muestra entonces la estructura de los enlaces. Para extraer las direcciones se utiliza el siguiente código en la consola:

```javascript
let bodyHtml = document.body.innerHTML;
let regex = /<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>\s*(.*PDF.*)\s*<\/a>/g;
let hrefs = [];
let match;
let totalLinks = 0; // Variable para almacenar el recuento de enlaces coincidentes

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

El resultado obtenido en la consola se guarda y el proceso se repite para cada año. Una vez recopilados todos los enlaces de descarga, existen varias alternativas para obtener los documentos:

**Opción A)** Utilizar directamente la extensión DownThemAll.

**Opción B)** Emplear un script de descarga ética que incorpora pausas entre solicitudes sucesivas, evitando sobrecargar el servidor.

**Opción C)** Recurrir a extensiones específicas de descarga masiva, como las disponibles para Prensa Histórica o la Hemeroteca de la BNE.

Al completar este proceso dispondremos del corpus completo listo para su análisis.

### 4.2 Normalización de datos

Dependiendo de los métodos de descarga empleados, los archivos PDF pueden presentar nomenclaturas variadas que conviene estandarizar. En este caso específico, podríamos encontrar documentos con nombres como *2043097.pdf* o *grupo.dopath.1002043097*. Resulta fundamental mantener la coherencia en la denominación de archivos y directorios para facilitar el procesamiento posterior.

## 5. Validación estadística

En esta etapa del proyecto contamos ya con un prompt validado y el corpus completo. Es necesario verificar que la IA proporciona resultados correctos utilizando una muestra estadísticamente significativa. Para ello, solicitamos a la propia IA la selección de un conjunto representativo de ejemplares. Considerando que disponemos de una población finita de aproximadamente 7.500 documentos, con un nivel de confianza deseado del 95%, un margen de error del 5% y asumiendo una variabilidad esperada del 50% (todos los ejemplares tienen idéntica probabilidad de contener o no la información objeto de estudio), obtenemos la siguiente distribución muestral:

### 5.1 Muestra estratificada por años

#### Sin fecha
- 1 (único ejemplar)

#### 1807 (18 ejemplares)
73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351

#### 1808 (17 ejemplares)
15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347

#### 1809 (18 ejemplares)
21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358

#### 1810 (16 ejemplares)
23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323

#### 1811 (17 ejemplares)
22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355

#### 1812 (16 ejemplares)
21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335

#### 1816 (6 ejemplares)
12, 34, 56, 78, 98, 112

_[Continúa la lista para todos los años hasta 1830]_

## 6. IA para el procesado del dataset

Se ha desarrollado un [programa específico](/sw/mover-pdfs-a-validar.py) que selecciona y copia los ejemplares correspondientes, organizados por año. Este conjunto constituye el *dataset* con el que generaremos los resultados a validar. La plataforma Claude AI permite realizar consultas mediante su interfaz de programación (API), evitando el procesamiento ejemplar por ejemplar. 

Existen dos modalidades principales de procesamiento:

### 6.1 Resultados en tiempo real

Con un coste de 0,01$ por página, esta opción proporciona resultados inmediatos:

```bash
for file in *.pdf; do
  python3 diario-mercantil-a-json.py "$file" > "${file%.pdf}.json";
done
```

### 6.2 Procesamiento por lotes   

Esta alternativa tiene un coste reducido de 0,005$ por página. Las consultas se envían y las respuestas se recuperan posteriormente, con un tiempo máximo de espera de 24 horas, aunque habitualmente el plazo es inferior:

#### 6.2.1 Envío de consultas por lotes 

```bash
for file in *.pdf; do
  if [ -f "$file" ]; then
    python3 batch.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt;
  fi;
done
``` 

#### 6.2.2 Recuperación de resultados 

```bash
# Procesar cada archivo que coincida con el patrón *_batch_order.txt
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

#### 6.2.3 Procesamiento manual para ejemplos individuales

El [panel de control de Anthropic](https://console.anthropic.com/settings/workspaces/default/batches) permite visualizar los lotes y descargar cualquiera de ellos. El resultado se obtiene en formato JSONL que debe convertirse:

```bash
# Obtenemos el custom_id, que es el nombre del pdf
custom_id=$(jq -r .custom_id msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl)
# Procesamos con jq y generamos la salida json con el nombre del pdf
jq -r '.result.message.content[0].text' msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl > "${custom_id}.json"
```

#### 6.2.4 Procesamiento masivo de resultados

Una vez verificada la corrección de la salida, procedemos al procesamiento masivo. Los archivos *_batch_output.txt* contienen toda la información necesaria, que extraemos mediante:

```bash
for file in *_batch_output.txt; do
  cat $file | sed 's/\\n//g' | sed 's/\\/\\\\/g' | grep -o '{.*}' | jq -r . > $(basename "$file" "_batch_output.txt").json;
done
```

#### 6.2.5 Unificación de resultados por año

Unificamos los archivos JSON, añadimos el año (que aparece como nombre de cada carpeta) y eliminamos comentarios adicionales que Claude añade antes y después de los JSON solicitados. Para este caso de uso es necesario que el directorio tenga denominación numérica (por ejemplo, "1819"):

```bash
./combinar_json_add_ejemplares.sh
```

## 7. Desarrollo de la interfaz web para cotejar ejemplares y resultados

En esta fase, disponemos del prompt validado, el corpus completo y los resultados procesados para cada ejemplar. El siguiente objetivo consiste en proporcionar a los filólogos una herramienta efectiva para validar los resultados. Con este fin se ha diseñado una interfaz web que ofrece las siguientes funcionalidades:

- Visualización de resultados por ejemplar
- Consulta simultánea de los documentos PDF originales
- Desplazamiento independiente por resultados y documentos
- Navegación directa a páginas específicas donde aparecen noticias literarias o artísticas

Al tratarse de datos estructurados en formato JSON, la solución implementada consiste en una única página web reutilizable para cada año. La interfaz lee el archivo *combined.json* (que contiene todos los resultados agregados) y presenta la información mediante código JavaScript que itera dinámicamente sobre los datos, independientemente del año, número de ejemplares o cantidad de referencias encontradas.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Mercantil Viewer</title>
    <style>
        /* Definición de variables CSS */
        :root {
            --primary-color: #2c5282;
            --secondary-color: #3182ce;
            --text-color: #2d3748;
            --bg-color: #f7fafc;
            --card-bg: #ffffff;
            --border-color: #e2e8f0;
            --tag-positive: #c6f6d5;
            --tag-positive-text: #22543d;
            --tag-negative: #fed7d7;
            --tag-negative-text: #822727;
        }

        /* Estilos base */
        body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
            color: var(--text-color);
            background: var(--bg-color);
            margin: 0;
            padding: 20px;
        }

        /* Estructura de layout */
        .container {
            width: 90%;
            margin: 0 auto;
            position: relative;
            display: grid;
            grid-template-columns: 1fr 0;
            gap: 20px;
            transition: all 0.3s ease;
        }

        .container.with-pdf {
            grid-template-columns: 1fr 1fr;
        }

        /* Resto de estilos omitidos por brevedad */
    </style>
</head>
<body>
    <div id="app" class="container">
        <div class="content-panel">
            <div class="loading">Cargando datos...</div>
        </div>
    </div>

    <script>
        /* Funciones JavaScript para la interactividad */
        function showPdfPage(pdfName, pageNum) {
            // Código para mostrar el PDF en la página especificada
        }

        function closePdfViewer() {
            // Código para cerrar el visor de PDF
        }

        function createPageLink(pdfName, pageNum) {
            // Código para generar enlaces a páginas específicas
        }

        function renderArticle(article) {
            // Código para renderizar artículos literarios
        }

        function renderEntry(entry) {
            // Código para renderizar cada entrada del diario
        }

        // Carga inicial de datos
        document.addEventListener('DOMContentLoaded', async () => {
            // Código para cargar y mostrar los datos
        });
    </script>
</body>
</html>
```

## 8. Acceso a los datos

Se publica la muestra a validar en GitHub Pages, plataforma que permite alojar sitios web:

[1807](https://rafav.github.io/diariomercantil/1807/index.html)
[1808](https://rafav.github.io/diariomercantil/1808/index.html)
[1809](https://rafav.github.io/diariomercantil/1809/index.html)
[1810](https://rafav.github.io/diariomercantil/1810/index.html)
[1811](https://rafav.github.io/diariomercantil/1811/index.html)
[1812](https://rafav.github.io/diariomercantil/1812/index.html)
[1816](https://rafav.github.io/diariomercantil/1816/index.html)
[1817](https://rafav.github.io/diariomercantil/1817/index.html)
[1818](https://rafav.github.io/diariomercantil/1818/index.html)
[1819](https://rafav.github.io/diariomercantil/1819/index.html)
[1820](https://rafav.github.io/diariomercantil/1820/index.html)
[1821](https://rafav.github.io/diariomercantil/1821/index.html)
[1822](https://rafav.github.io/diariomercantil/1822/index.html)
[1823](https://rafav.github.io/diariomercantil/1823/index.html)
[1824](https://rafav.github.io/diariomercantil/1824/index.html)
[1825](https://rafav.github.io/diariomercantil/1825/index.html)
[1826](https://rafav.github.io/diariomercantil/1826/index.html)
[1827](https://rafav.github.io/diariomercantil/1827/index.html)
[1828](https://rafav.github.io/diariomercantil/1828/index.html)
[1829](https://rafav.github.io/diariomercantil/1829/index.html)
[1830](https://rafav.github.io/diariomercantil/1830/index.html)

Debido al volumen de datos que implica este proyecto, la versión definitiva, con todos los ejemplares procesados, usa archivos locales. Para que Google Chrome permita su lectura, debe iniciarse con el siguiente parámetro:

```bash
google-chrome --allow-file-access-from-files file.html 
```

## 9. Análisis avanzado con Claude Code

En este punto disponemos de una base de datos completa, con archivos organizados, estructurados y con información relevante para la investigación.

Se ha experimentado el potencial de [Claude Code](https://docs.anthropic.com/es/docs/agents-and-tools/claude-code/overview), una herramienta de codificación asistida por IA que opera desde la terminal, comprende la estructura del código y facilita la programación mediante comandos en lenguaje natural. La innovación ha consistido en usarla como herramienta de investigación, solicitando a Claude Code la elaboración de un artículo académico a partir de los datos almacenados localmente, con importantes ventajas:

- Procesamiento integral de todos los datos sin restricciones de tamaño.
- Verificación directa de hipótesis sobre el corpus completo.
- Generación de tablas estadísticas precisas y verificables.

Se ha optado por dar las mínimas instrucciones, sencillas pero específicas:

> "Crea un artículo universitario, con enfoque filológico, que analice la literatura, teatro, obras y poesías, con especial atención a obras y autores del Siglo de Oro"

Y una vez visto el primer resultado:

> "Profundiza el análisis, incorpora datos estadísticos, incluye autores secundarios y establece hipótesis de investigación sobre los autores áureos frente al invasor francés"

Con esto se obtiene [este artículo académico](articulo_literatura_aurea_completo.md).

## 10. Difusión de los resultados

El artículo está en formato Markdown, lenguaje de marcas simple y potente, que puede convertirse a formato PDF con LaTeX:

[![paper](/img/paper.png)](https://drive.google.com/file/d/1jNWCTfDrj9S5mUIwgpp26nYAOhH3f-At/view?usp=sharing)

Y también transformarse en una publicación web que facilite la validación y difusión del trabajo realizado

[![paper](/img/web.png)](https://rafav.github.io/diariomercantil/analisis/)

## 11. Conclusión

La implementación de técnicas de *scrapping* combinadas con sistemas de IA permite sistematizar eficazmente el proceso de extracción y posterior identificación de contenidos específicos en prensa histórica digitalizada así como la creación de artículos académicos y herramientas de divulgación. La metodología desarrollada ha sido validada específicamente para referencias literarias y artísticas, aunque resulta igualmente aplicable a otras áreas de investigación mediante ajustes en el *prompt* según el campo de estudio correspondiente.

## 12. Proyectos similares

El avance de la IA junto con las mejoras en tecnologías OCR/HTR está transformando las posibilidades de las Humanidades Digitales para la extracción y análisis masivo de datos.Algunas iniciativas en este ámbito son:

1. [Digital Douady](https://github.com/phughesmcr/digitaldouay)
2. [LexiMus](https://leximus.es)
3. [Large-Scale Research with Historical Newspapers: A Turning Point through Generative AI – DH Lab](https://dhlab.hypotheses.org/4938)
