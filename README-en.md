# USE OF ARTIFICIAL INTELLIGENCE FOR AUTOMATIC LOCALIZATION OF NEWS IN HISTORICAL PRESS

[![web final](/img/output.png)](https://rafav.github.io/diariomercantil/1807/index.html)

## 1. Introduction

This article details how Artificial Intelligence allows for the automatic localization and identification of literary, artistic, and cultural news in nineteenth-century press examples, with special emphasis on references to the Spanish Golden Age. The developed computational procedure, applicable to various newspaper publications, has significantly reduced the time required for manual information searching. Statistical validation of the method has provided reliability to the results obtained through automated queries. Additionally, the article describes the deliverables automatically generated from the findings.

**The proposal is framed within the research needs of the project ["The institution of the 'Golden Age'. Construction processes in the periodical press (1801-1868). SILEM III" (PID2022-136995NB-I00)](http://www.uco.es/servicios/ucopress/silem/), funded by the National Research Plan of the Ministry of Science and Innovation and directed by Mercedes Comellas (University of Seville).**

## 2. Case study: Diario Mercantil de Cádiz

The selection of the Diario Mercantil de Cádiz as the object of analysis was determined by [Professor Jaime Galbarro](https://www.jaimegalbarro.com/) from the University of Seville, **in the context of research for the mentioned project.** The issues are available in digital format on the [Historical Press portal](https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625).

This publication, covering from 1807 to 1830, comprises 7,456 issues with a total of 37,381 pages. It constitutes an ideal documentary collection for various reasons:

**a)** It is a general newspaper with a wide thematic variety (economic, cultural, and social news).

**b)** It covers a crucial historical period such as the War of Independence, where daily life experienced significant alterations, including interruptions in cultural activities.

**c)** It presents stages of temporary suspension of theatrical activities and other public entertainment for various reasons, such as the Lent periods.

**d)** It offers digitized issues of good quality for automated processing.

## 3. Initial prompt design

The implementation of AI in this project has taken into account two fundamental considerations:

**a)** The need to prevent AI from hallucinating and generating data that doesn't exist in the original sources.

**b)** The importance of obtaining systematic and exhaustive information, without omission of relevant references.

It is a priority to minimize possible hallucinations in the results. Tests conducted with models such as Qwen2-VL-72B, Claude, and ChatGPT revealed that we currently do not have completely reliable solutions for the comprehensive processing of historical texts. Specialized tools such as Transkribus or Surya offer better results in text detection, as they treat sources as images, locating each sentence separately; even so, they do not achieve total reliability. In various tests with large language models (LLMs), it has been found that hallucinations decrease when requesting the localization of specific information and then the literal transcription of the information.

With the aim of optimizing the utility of the extracted data, it has been established that the results provided by the AI must be presented normalized and systematically organized, in order to facilitate subsequent searches, filtering, and agile location of relevant findings.

Based on these considerations, a specific prompt was designed that was initially tested with two issues:

```
1. BASE TRANSCRIPTION:
- Perform OCR and transcribe the complete text maintaining the original format in Spanish
- Preserve the structure by columns, sections, headlines, and dates
- Maintain all typographic elements (italics, bold, etc.)
- Indicate text that is difficult to read with [...]
- Preserve footnotes, headers, and footers
- For each page, indicate both the PDF number and the printed number of the newspaper (e.g.: "PDF p.1 / Newspaper p.774")

2. LITERARY ANALYSIS:
Systematically identify and extract:
a) Direct references to:
- Spanish classic authors (especially Golden Age)
- Specific literary works, indicating:
  * Complete title
  * Genre (comedy, drama, praise, auto, interlude, etc.)
  * Author (if mentioned)
  * Number of acts or days (if specified)
- Textual quotes from works
- Footnotes about literature
b) Indirect references:
- Stylistic imitations
- Literary parodies
- Adaptations of classical literary genres or forms
- Recognizable poetic metrics or structures

3. CULTURAL ANALYSIS:
Identify references to:
- Music and theater (including:
  * Type of musical/theatrical piece
  * Performers/companies
  * Place of representation
  * Schedule)
- Visual arts
- Education and academia
- Customs and social life
- Politics and society
- Religion and morality

Return a JSON with the following structure:
{
    "Title": "",
    "Date": "",
    "Number": "",
    "LITERATURE": boolean,
    "LITERATURE_PAGES": [{
        "pdf": number,
        "newspaper": number,
        "content": "Complete transcription of the section. All paragraphs, unabridged"
    }],
    "LITERATURE_ARTICLES": [{
        "type": "direct_reference|indirect",
        "author": "name of the referenced author",
        "work": {
            "title": "",
            "genre": "",
            "acts": number,
            "work_author": "if specified",
            "place of representation": ""
        },
        "pages": [{
            "pdf": number,
            "newspaper": number
        }],
        "quotes": ["textual quotes if they exist"],
        "context": "explanation of the use or relevance"
    }],
    "MUSIC": boolean,
    "MUSIC_PAGES": [{
        "pdf": number,
        "newspaper": number
    }],
    "MUSIC_ARTICLES": [{
        "type": "musical_genre",
        "performer": "name",
        "place": "location",
        "pages": [{
            "pdf": number,
            "newspaper": number
        }],
        "context": "description"
    }],
    "OTHER_CULTURAL_REFERENCES": [{
        "theme": "cultural category",
        "pages": [{
            "pdf": number,
            "newspaper": number
        }],
        "description": "explanation of the content",
        "connections": ["references to other elements of the document"]
    }]
}

For each identified element, provide:
- Exact location (PDF and newspaper page numbers)
- Literal transcription of the complete sections. Minimum the paragraph.
- Context and significance in the document
- Connections with other identified elements
- For literary and musical works, search for the author and date of the work
```

The response obtained adopts a format like the following:

```json
{
    "Title": "DIARIO MERCANTIL DE CADIZ",
    "Date": "1 de Enero de 1807",
    "Number": "N.1",
    "LITERATURE": true,
    "LITERATURE_PAGES": [
        {
            "pdf": 4,
            "newspaper": 4,
            "content": "TEATRO. — En el de esta Ciudad, en celebridad del dia, se dará la funcion siguiente: empezará la doble orquesta con una sinfonía; seguirá la Comedia titulada: Sancho Ortiz de las Roelas; concluida, se cantará un aria por la Sra. María Puy, cuya música es del celebre Maestro de este teatro D Esteban Cristiani; finalizada, se tocará la Overtura de la Batalla de Austerlitz, se baylarán las boleras por la Sra. Olivares y el Sr. Paz; terminando la funcion con el Saynete: El Remendon y la Prendera. El teatro estará vistosamente iluminado."
        }
    ],
    "LITERATURE_ARTICLES": [
        {
            "type": "direct_reference",
            "author": "Lope de Vega (adaptación de Cándido María Trigueros)",
            "work": {
                "title": "Sancho Ortiz de las Roelas",
                "genre": "Comedia",
                "acts": 3,
                "work_author": "Cándido María Trigueros (adaptación de 'La Estrella de Sevilla' de Lope de Vega)",
                "place of representation": "Teatro de Cádiz"
            },
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "quotes": [],
            "context": "Mencionada como la obra principal que se representará en el teatro de la ciudad de Cádiz en celebración del día 1 de enero de 1807. Es una adaptación neoclásica de 'La Estrella de Sevilla' atribuida a Lope de Vega."
        },
        {
            "type": "direct_reference",
            "author": "Anónimo",
            "work": {
                "title": "El Remendon y la Prendera",
                "genre": "Saynete",
                "acts": 1,
                "work_author": "No especificado",
                "place of representation": "Teatro de Cádiz"
            },
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "quotes": [],
            "context": "Obra corta cómica (sainete) que se representará al final de la función teatral del día."
        }
    ],
    "MUSIC": true,
    "MUSIC_PAGES": [
        {
            "pdf": 4,
            "newspaper": 4
        }
    ],
    "MUSIC_ARTICLES": [
        {
            "type": "sinfonía",
            "performer": "doble orquesta del teatro",
            "place": "Teatro de Cádiz",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "context": "Pieza musical de apertura interpretada por una doble orquesta del teatro"
        },
        {
            "type": "aria",
            "performer": "Sra. María Puy",
            "place": "Teatro de Cádiz",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "context": "Aria cantada por la Sra. María Puy, con música compuesta por D. Esteban Cristiani, maestro del teatro"
        },
        {
            "type": "obertura",
            "performer": "orquesta del teatro",
            "place": "Teatro de Cádiz",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "context": "Obertura musical titulada 'La Batalla de Austerlitz', posiblemente conmemorando la victoria de Napoleón en dicha batalla (2 de diciembre de 1805)"
        },
        {
            "type": "danza",
            "performer": "Sra. Olivares y Sr. Paz",
            "place": "Teatro de Cádiz",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "context": "Interpretación de boleras, una danza española popular, por la Sra. Olivares y el Sr. Paz"
        }
    ],
    "OTHER_CULTURAL_REFERENCES": [
        {
            "theme": "Religión",
            "pages": [
                {
                    "pdf": 1,
                    "newspaper": 1
                }
            ],
            "description": "Referencia a 'LA CIRCUNCISION DEL SEÑOR' y a indulgencias en la Santa Iglesia Catedral, reflejando la importancia del calendario religioso católico",
            "connections": ["Festividad religiosa del día 1 de enero"]
        },
        {
            "theme": "Astronomía",
            "pages": [
                {
                    "pdf": 1,
                    "newspaper": 1
                }
            ],
            "description": "Sección 'Afecciones Astronómicas de hoy' con datos precisos sobre salida y puesta del sol, posición lunar, etc.",
            "connections": ["Información de utilidad pública y científica"]
        },
        {
            "theme": "Comercio e industria",
            "pages": [
                {
                    "pdf": 1,
                    "newspaper": 1
                },
                {
                    "pdf": 2,
                    "newspaper": 2
                }
            ],
            "description": "Extracto de un informe al Ministro del Interior de Francia sobre lanas y paños, destacando la calidad de distintas fábricas francesas",
            "connections": ["Relaciones comerciales con Francia", "Industria textil"]
        },
        {
            "theme": "Comercio internacional",
            "pages": [
                {
                    "pdf": 2,
                    "newspaper": 2
                },
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Descripción detallada del estado de la industria y comercio en Sajonia, mencionando sus fábricas, productos de exportación y la importancia de Leipzig como centro comercial",
            "connections": ["Relaciones comerciales internacionales", "Información económica"]
        },
        {
            "theme": "Arte y patrimonio",
            "pages": [
                {
                    "pdf": 2,
                    "newspaper": 2
                },
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Referencia a la colección de arte del Palacio Electoral de Dresde, destacando obras de Correggio como 'San Jorge', 'San Sebastián', 'La Magdalena' y 'La Noche del Correggio'",
            "connections": ["Cultura europea", "Apreciación artística"]
        },
        {
            "theme": "Bibliofilia",
            "pages": [
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Menciones a libros raros en la Biblioteca de Dresde, incluyendo el 'Ars memorandi', 'Biblia pauperum', un salterio de 1457, manuscritos del Mariscal de Sajonia, un ejemplar del Corán de Bayaceto II, y primeras ediciones de Homero",
            "connections": ["Cultura del libro", "Patrimonio bibliográfico europeo"]
        },
        {
            "theme": "Navegación y comercio marítimo",
            "pages": [
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Noticias sobre embarcaciones entradas en los puertos de San Ciprián de Bureta y Algeciras, con detalles sobre sus cargamentos, procedencias y destinos",
            "connections": ["Comercio marítimo", "Actividad portuaria española"]
        },
        {
            "theme": "Diplomacia",
            "pages": [
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Mención del Embajador de Marruecos Alfach Quevez que viaja a Tánger",
            "connections": ["Relaciones diplomáticas con Marruecos"]
        },
        {
            "theme": "Presencia militar",
            "pages": [
                {
                    "pdf": 3,
                    "newspaper": 3
                }
            ],
            "description": "Información sobre buques de guerra ingleses presentes en Gibraltar: dos fragatas de 40 cañones, una corbeta de 24, un bergantín de 18, un navío de 74 y cuatro cañoneras",
            "connections": ["Contexto militar", "Presencia inglesa en Gibraltar"]
        },
        {
            "theme": "Anuncios personales",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "description": "Anuncio de una joven de 20 años que solicita trabajo como nodriza en casa decente",
            "connections": ["Costumbres sociales", "Vida cotidiana"]
        },
        {
            "theme": "Economía",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "description": "Información sobre Vales Reales de diferentes meses (Septiembre, Mayo, Enero) con sus respectivas cotizaciones",
            "connections": ["Sistema financiero", "Economía española"]
        },
        {
            "theme": "Ciencia y divulgación",
            "pages": [
                {
                    "pdf": 4,
                    "newspaper": 4
                }
            ],
            "description": "Anuncio de una demostración de física y mecánica por Don Antonio Luquini en los intermedios de un espectáculo de Sombras Chinescas en la calle Nueva",
            "connections": ["Divulgación científica", "Entretenimiento educativo"]
        }
    ]
}
```

Manual verification of the responses with these two examples confirmed their correctness, which allowed advancing to the next stage of the project.

## 4. Automations

The incorporation of computer specialists in Digital Humanities projects allows the design of automated processes that optimize time, systematize procedures, and provide security when addressing large-scale analysis projects.

### 4.1 Scraping

The term *scraping* designates a set of techniques designed to extract data from web pages. In the case of the Historical Press portal, search results show links to issues in PDF format. Our objective is to extract these links and subsequently download them. There are various techniques to achieve this; in the specific case of the Historical Press website, with results organized by year, it is possible to use the DownThemAll plugin applying a quick filter with the word "pdf".

![downthemall extension](/img/downThemAll-quick-filter-PDF.png)

Below we present a second option, the one implemented in this project, oriented to the educational field. It is based on queries from the browser console using regular expressions. The procedure consists of locating a PDF link within the web browser, right-clicking, and selecting "inspect". The browser then shows the structure of the links. To extract the addresses, the following code is used in the console:

```javascript
let bodyHtml = document.body.innerHTML;
let regex = /<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>\s*(.*PDF.*)\s*<\/a>/g;
let hrefs = [];
let match;
let totalLinks = 0; // Variable to store the count of matching links

// Search for all matches
while ((match = regex.exec(bodyHtml)) !== null) {
    // Add the href to the list
    hrefs.push(match[1]);
   
    // If the site has a base for the download URL
    let url_pdf = match[1].startsWith('http') ? match[1] : 'https://prensahistorica.mcu.es/' + match[1];
   
    // Show the link in the console
    console.log('Link to PDF: ' + url_pdf);
   
    // Increase the link counter
    totalLinks++;
}

// Show the total links found
console.log('Total PDF links found: ' + totalLinks);
```

The result obtained in the console is saved and the process is repeated for each year. Once all the download links have been collected, there are several alternatives to obtain the documents:

**Option A)** Use the DownThemAll extension directly.

**Option B)** Use an ethical download script that incorporates pauses between successive requests, avoiding overloading the server.

**Option C)** Use specific extensions for mass downloading, such as those available for Historical Press or the BNE Newspaper Library.

Upon completing this process, we will have the complete corpus ready for analysis.

### 4.2 Data normalization

Depending on the download methods used, PDF files may present varied nomenclatures that should be standardized. In this specific case, we might find documents with names like *2043097.pdf* or *grupo.dopath.1002043097*. It is essential to maintain consistency in the naming of files and directories to facilitate subsequent processing.

## 5. Statistical validation

At this stage of the project, we already have a validated prompt and the complete corpus. It is necessary to verify that the AI provides correct results using a statistically significant sample. For this, we asked the AI itself to select a representative set of specimens. Considering that we have a finite population of approximately 7,500 documents, with a desired confidence level of 95%, an error margin of 5%, and assuming an expected variability of 50% (all specimens have an identical probability of containing or not the information under study), we obtain the following sample distribution:

### 5.1 Stratified sample by years

#### Without date
- 1 (single specimen)

#### 1807 (18 specimens)
73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351

#### 1808 (17 specimens)
15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347

#### 1809 (18 specimens)
21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358

#### 1810 (16 specimens)
23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323

#### 1811 (17 specimens)
22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355

#### 1812 (16 specimens)
21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335

#### 1816 (6 specimens)
12, 34, 56, 78, 98, 112

_[The list continues for all years until 1830]_

## 6. AI for dataset processing

A [specific program](/sw/mover-pdfs-a-validar.py) has been developed that selects and copies the corresponding specimens, organized by year. This set constitutes the *dataset* with which we will generate the results to validate. The Claude AI platform allows queries through its application programming interface (API), avoiding processing specimen by specimen.

There are two main processing modalities:

### 6.1 Real-time results

With a cost of $0.01 per page, this option provides immediate results:

```bash
for file in *.pdf; do
  python3 diario-mercantil-a-json.py "$file" > "${file%.pdf}.json";
done
```

### 6.2 Batch processing

This alternative has a reduced cost of $0.005 per page. Queries are sent and responses are retrieved later, with a maximum waiting time of 24 hours, although usually the timeframe is shorter:

#### 6.2.1 Sending batch queries

```bash
for file in *.pdf; do
  if [ -f "$file" ]; then
    python3 batch.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt;
  fi;
done
```

#### 6.2.2 Retrieving results

```bash
# Process each file that matches the pattern *_batch_order.txt
for file in *_batch_order.txt; do
  if [ -f "$file" ]; then
    # Extract the ID using grep
    id=$(grep -o "msgbatch_[[:alnum:]]\+" "$file")
    
    # Process the filename to get the new name
    # Remove _batch_order from the filename
    output_file=$(basename "$file" "_batch_order.txt")_batch_output.txt
    
    if [ ! -z "$id" ]; then
      echo "Processing file $file with ID: $id"
      echo "Saving result in: $output_file"
      python recuperar_batch.py "$id" > "$output_file"
    else
      echo "ID not found in file $file"
    fi
  fi
done
```

#### 6.2.3 Manual processing for individual examples

The [Anthropic control panel](https://console.anthropic.com/settings/workspaces/default/batches) allows viewing batches and downloading any of them. The result is obtained in JSONL format that must be converted:

```bash
# We get the custom_id, which is the name of the pdf
custom_id=$(jq -r .custom_id msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl)
# We process with jq and generate the json output with the name of the pdf
jq -r '.result.message.content[0].text' msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl > "${custom_id}.json"
```

#### 6.2.4 Mass processing of results

Once the correctness of the output has been verified, we proceed to mass processing. The *_batch_output.txt* files contain all the necessary information, which we extract using:

```bash
for file in *_batch_output.txt; do
  cat $file | sed 's/\\n//g' | sed 's/\\/\\\\/g' | grep -o '{.*}' | jq -r . > $(basename "$file" "_batch_output.txt").json;
done
```

#### 6.2.5 Unifying results by year

We unify the JSON files, add the year (which appears as the name of each folder), and eliminate additional comments that Claude adds before and after the requested JSONs. For this use case, it is necessary that the directory has a numerical denomination (for example, "1819"):

```bash
./combinar_json_add_ejemplares.sh
```

## 7. Development of the web interface to compare specimens and results

At this phase, we have the validated prompt, the complete corpus, and the processed results for each specimen. The next objective is to provide philologists with an effective tool to validate the results. To this end, a web interface has been designed that offers the following functionalities:

- Visualization of results by specimen
- Simultaneous consultation of the original PDF documents
- Independent scrolling through results and documents
- Direct navigation to specific pages where literary or artistic news appear

Since these are structured data in JSON format, the implemented solution consists of a single reusable web page for each year. The interface reads the *combined.json* file (which contains all the aggregated results) and presents the information through JavaScript code that dynamically iterates over the data, regardless of the year, number of specimens, or amount of references found.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Mercantil Viewer</title>
    <style>
        /* CSS variables definition */
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

        /* Base styles */
        body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
            color: var(--text-color);
            background: var(--bg-color);
            margin: 0;
            padding: 20px;
        }

        /* Layout structure */
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

        /* Rest of styles omitted for brevity */
    </style>
</head>
<body>
    <div id="app" class="container">
        <div class="content-panel">
            <div class="loading">Loading data...</div>
        </div>
    </div>

    <script>
        /* JavaScript functions for interactivity */
        function showPdfPage(pdfName, pageNum) {
            // Code to show the PDF on the specified page
        }

        function closePdfViewer() {
            // Code to close the PDF viewer
        }

        function createPageLink(pdfName, pageNum) {
            // Code to generate links to specific pages
        }

        function renderArticle(article) {
            // Code to render literary articles
        }

        function renderEntry(entry) {
            // Code to render each diary entry
        }

        // Initial data loading
        document.addEventListener('DOMContentLoaded', async () => {
            // Code to load and display the data
        });
    </script>
</body>
</html>
```

## 8. Data access

The sample to be validated is published on GitHub Pages, a platform that allows hosting websites:

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

Due to the volume of data involved in this project, the definitive version, with all the processed specimens, uses local files. For Google Chrome to allow reading, it must be started with the following parameter:

```bash
google-chrome --allow-file-access-from-files file.html 
```

## 9. Advanced analysis with Claude Code

At this point, we have a complete database, with files organized, structured, and with relevant information for research.

The potential of [Claude Code](https://docs.anthropic.com/es/docs/agents-and-tools/claude-code/overview) has been experimented with, an AI-assisted coding tool that operates from the terminal, understands the code structure, and facilitates programming through natural language commands. The innovation has consisted of using it as a research tool, requesting Claude Code to elaborate an academic article from the data stored locally, with important advantages:

- Comprehensive processing of all data without size restrictions.
- Direct verification of hypotheses on the complete corpus.
- Generation of precise and verifiable statistical tables.

The choice was made to give minimal instructions, simple but specific:

> "Create a university article, with a philological approach, that analyzes literature, theater, works, and poetry, with special attention to works and authors of the Golden Age"

And once the first result was seen:

> "Deepen the analysis, incorporate statistical data, include secondary authors, and establish research hypotheses about Golden Age authors against the French invader"

With this, [this academic article](articulo_literatura_aurea_completo.md) is obtained.

## 10. Dissemination of results

The article is in Markdown format, a simple and powerful markup language, which can be converted to PDF format with LaTeX:

[![paper](/img/paper.png)](https://drive.google.com/file/d/1jNWCTfDrj9S5mUIwgpp26nYAOhH3f-At/view?usp=sharing)

And also transformed into a web publication that facilitates the validation and dissemination of the work done:

[![paper](/img/web.png)](https://rafav.github.io/diariomercantil/analisis/)

## 11. Conclusion

The implementation of scraping techniques combined with AI systems allows for effectively systematizing the process of extraction and subsequent identification of specific contents in digitized historical press, as well as the creation of academic articles and dissemination tools. The methodology developed has been specifically validated for literary and artistic references, although it is equally applicable to other research areas through adjustments in the prompt according to the corresponding field of study.

## 11. Similar projects

The advancement of AI along with improvements in OCR/HTR technologies is transforming the possibilities of Digital Humanities for the extraction and massive analysis of data. Some initiatives in this field are:

1. [Digital Douady](https://github.com/phughesmcr/digitaldouay)
2. [LexiMus](https://leximus.es)
3. [Large-Scale Research with Historical Newspapers: A Turning Point through Generative AI – DH Lab](https://dhlab.hypotheses.org/4938)