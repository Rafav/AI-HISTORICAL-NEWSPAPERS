# USE OF ARTIFICIAL INTELLIGENCE FOR AUTOMATIC LOCATION OF NEWS IN HISTORICAL PRESS.

Use of Artificial Intelligence for the automatic localization of news in Historical press.

[![final web](/img/output.png)](https://rafav.github.io/diariomercantil/1807/index.html)

# 1. Introduction.

This article details the process of using AI for the automatic location and identification of literary, artistic and cultural news, with special attention to the Golden Age, in 19th century newspapers. This computer procedure, applicable to other newspapers, has meant a reduction of % [to be determined] of the time needed to locate the data manually. It has also been statistically validated, which has allowed the researchers to accept the results of the AI queries as valid. Finally, the deliverables that are automatically generated with the localized information are detailed.

**The proposal is framed within the research needs of the project ["La institución del ‘Siglo de Oro’. Construction processes in the periodical press (1801-1868). SILEM III” (PID2022-136995NB-I00)](http://www.uco.es/servicios/ucopress/silem/), funded by the National Research Plan of the Ministry of Science and Innovation and directed by Mercedes Comellas (University of Seville).**


# 2. Case study: Diario Mercantil de Cádiz.

The choice of the Diario Mercantil de Cádiz as the object of analysis was determined by [Professor Jaime Galbarro](https://www.jaimegalbarro.com/), of the University of Seville, **in the context of research for the aforementioned project.** The copies are digitized in the [Prensa Historica website.](https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625)

This newspaper started in 1807 and ended in 1830, with a total of 7,456 copies totaling 37,381 pages to process. It has proven to be an excellent dataset for various reasons:

a) It is a general newspaper that includes economic, cultural, and social news.

b) It includes a historical period, the War of Independence, in which daily life was notably affected, with the consequent interruption of cultural activity.

c) It has periods of suspension of theatrical activity, and any other entertainment, for various reasons, such as Lent.

d) The digitized copies have good quality.

e) The page numbers of each copy are not standardized.

# 3. Initial Prompt.

There are two key aspects for using AI in this use case:

a) The AI cannot invent data that does not appear in the news.

b) The information returned by the AI must be systematic, without skipping references.

We must therefore minimize the possibility of hallucinations appearing in the results, which occur whether the information source is PDF or written text. Tests with Qwen2-VL-72B, Claude, and ChatGPT have shown that we do not yet have AI available that is 100% reliable in complete texts. Tools like Transkribus or Surya give better results as they don't add information, but they don't achieve 100% reliability, and they're not useful when there's layout different from standard, because they interleave rows and columns. In LLM models, it has been shown that hallucinations are fewer when asked to locate information and then transcribe the paragraph.

To use the data optimally in subsequent research, we will ask that the results returned by the AI be normalized, organized, facilitate subsequent searches and filtering, as well as agile location of findings.

With these premises, a prompt is designed, initially tested on two copies. The prompt is as follows:
```
1. BASE TRANSCRIPTION:
- Perform OCR and transcribe the complete text maintaining the original format in Spanish
- Preserve the structure by columns, sections, headlines, and dates
- Maintain all typographical elements (italics, bold, etc.)
- Indicate poorly legible text with [...]
- Preserve footnotes, headers, and footers
- For each page, indicate both the PDF number and the printed newspaper number (e.g., "PDF p.1 / Newspaper p.774")

2. LITERARY ANALYSIS:
Systematically identify and extract:
a) Direct references to:
- Classical Spanish authors (especially Golden Age)
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
- Recognizable metrics or poetic structures

3. CULTURAL ANALYSIS:
Identify references to:
- Music and theater (including:
  * Type of musical/theatrical piece
  * Performers/companies
  * Place of performance
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
        "content": "Complete transcription of the section. All paragraphs, unshortened"
    }],
    "LITERATURE_ARTICLES": [{
        "type": "direct_reference|indirect",
        "author": "name of referenced author",
        "work": {
            "title": "",
            "genre": "",
            "acts": number,
            "work_author": "if specified",
            "place_of_performance": ""
        },
        "pages": [{
            "pdf": number,
            "newspaper": number
        }],
        "quotes": ["textual quotes if they exist"],
        "context": "explanation of use or relevance"
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
        "description": "content explanation",
        "connections": ["references to other elements in the document"]
    }]
}

For each identified element, provide:
- Exact location (PDF and newspaper page numbers)
- Literal transcription of complete sections. Minimum the paragraph.
- Context and significance in the document
- Connections with other identified elements
- For literary and musical works, search for the author and date of the work
```

The result would look like this:

```
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
          "contenido": "TEATRO. = En el de esta Ciudad, en celebridad del dia, se dará la funcion siguiente: empezará la doble orquesta con una sinfonía; seguirá la Comedia titulada: Sancho Ortiz de la Roelas; 
          concluida, se cantará un aria por la Sra. María Puy,cuya música es del celebre Maestro de este teatro D Esteban Cristiani; finalizada, se tocará la Overtura de la Batalla de Austerlitz, se baylarán las boleras por la Sra. Olivares           y el Sr. Paz; terminando la funcion con el Saynete: El Remendon y la Prendera."
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


The manual verification of the responses for these 2 copies is correct, so we move on to the next phase.

# 4. Automations.

By incorporating computer scientists into digital Humanities projects, automatisms are implemented that save time, systematize processes, and provide security when tackling massive projects.

## 4.1 Scraping.

By *scraping* we mean a set of techniques to extract data from web pages. In the case of Historical Press, the web results show links with the PDF text and the URL of the digitized copy. We are interested in extracting these addresses to download them later. There are several techniques for this; in the case of the Historical Press website, with results ordered by year, we can use the DownThemAll add-on and in quick filter write pdf.

![downthemall extension](/img/downThemAll-quick-filter-PDF.png)

We show here a second option, the one used in this project, which is oriented to the educational field. We use searches from the browser console using regular expressions. Within the web browser, locate PDF -> right click -> inspect. The browser shows us how the links are constructed. To download them, paste the following code in the browser console:

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

Save the console result and repeat for each year. Once the download links are obtained, proceed to download them.

Option a) With DownThemAll itself.

Option b) With an ethical download script. While DownThemAll allows for quick and effective downloading, a program has been created that downloads one by one, but adding download pauses that prevent the server from becoming saturated.

Option c) With specific download extensions for that specific website, if any exist. For Historical Press, HemerotecaBNE there are Chrome extensions that allow mass downloads of search results.

At the end of this step, we already have the corpus to be investigated.

## 4.2. Data Unification.

Depending on the different download methods used, the downloaded PDFs may have different nomenclature, which is advisable to normalize. In this specific case, we could have PDFs with names like *2043097.pdf* or *grupo.dopath.1002043097*. Maintaining consistency in file and directory names is key.

# 5. Statistical Validation.

At this phase of the project, we already have a valid prompt and the complete corpus. It is necessary to verify that the AI returns correct results, using a statistically significant sample. For this, the AI is asked to select a set of samples. Considering that we have a finite population of 7,500 documents and that we want to have a confidence level of 95%, an error margin of 5%, and that there is an expected variability of 50% (all copies have the same possibility of containing or not the information we are studying), we ask the AI to select a sample. The selected copies are the following:

## 5.1. Sample stratified by years.

### No date.
- 1 (single copy)

### 1807 (18 copies).
73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351

### 1808 (17 copies).
15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347

### 1809 (18 copies).
21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358

### 1810 (16 copies).
23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323

### 1811 (17 copies).
22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355

### 1812 (16 copies).
21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335

### 1816 (6 copies).
12, 34, 56, 78, 98, 112

### 1817 (18 copies).
23, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 311, 323, 334, 345, 356

### 1818 (18 copies).
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 352, 360

### 1819 (18 copies).
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 353, 361

### 1820 (21 copies).
25, 48, 71, 94, 117, 140, 163, 186, 209, 232, 255, 278, 301, 324, 347, 370, 383, 396, 409, 422, 428

### 1821 (21 copies).
24, 47, 70, 93, 116, 139, 162, 185, 208, 231, 254, 277, 300, 323, 346, 369, 382, 395, 408, 421, 427

### 1822 (18 copies).
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362

### 1823 (18 copies).
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 359

### 1824 (18 copies).
24, 46, 68, 90, 112, 134, 156, 178, 200, 222, 244, 266, 288, 310, 332, 344, 355, 363

### 1825 (18 copies).
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 361

### 1826 (18 copies).
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 360

### 1827 (18 copies).
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 352, 359

### 1828 (18 copies).
23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362

### 1829 (18 copies).
22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 361

### 1830 (17 copies).
21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 358

# 6. AI for Dataset Processing.
A [program that copies the corresponding copies](/sw/mover-pdfs-a-validar.py) has been created, by year. This set of copies forms the *dataset* with which we will create the results to validate. Claude AI allows queries using an *API (Application Programming Interface)* instead of querying copy by copy.

We have two possibilities:

## 6.1. Real-time Results.

Cost of $0.01 per page and immediate results.

```bash

for file in *.pdf; do
  python3 diario-mercantil-a-json.py "$file" > "${file%.pdf}.json";
done
```

## 6.2. Batches

Cost of $0.005 per page. Questions are submitted and answers are retrieved later. Available within a maximum of 24 hours, although response time is usually shorter.

### 6.2.1. Processing

```bash

for file in *.pdf;
 do
    if [ -f "$file" ];
     then
       python3 batch.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt;
fi;
done
```

### 6.2.2. Downloading Batch Outputs

```bash
# Process each file matching the pattern *_batch_order.txt
for file in *_batch_order.txt; do
    if [ -f "$file" ]; then
        # Extract ID using grep
        id=$(grep -o "msgbatch_[[:alnum:]]\+" "$file")
        
        # Process filename to get new name
        # Remove _batch_order from filename
        output_file=$(basename "$file" "_batch_order.txt")_batch_output.txt
        
        if [ ! -z "$id" ]; then
            echo "Processing file $file with ID: $id"
            echo "Saving result to: $output_file"
            python retrieve_batch.py "$id" > "$output_file"
        else
            echo "No ID found in file $file"
        fi
    fi
done
```

### 6.2.3. Manually Downloading a Single Result and Converting to JSON

In the [Anthropic Console](https://console.anthropic.com/settings/workspaces/default/batches), we can view batches and download any of them. The result is a JSONL that we convert.

```bash
# Get the custom_id, which is the pdf name
custom_id=$(jq -r .custom_id msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl)
# Process with jq and generate json output with pdf name

jq -r '.result.message.content[0].text' msgbatch_016EVpCc8X6HWza3SZ8gPoTN_results.jsonl > "${custom_id}.json"
```

### 6.2.4. Cleaning Downloaded Output for Each ID

Once we verify the output is correct, we process in bulk. In the *_batch_output.txt files we have all the information to extract.

```bash

for file in *batch_output.txt; do  echo $file; cat "$file" |  sed -n "s/.*text='\({.*}\)[^}]*', type=.*/\1/p" | sed 's/\\\\n/\\n/g; s/\\n/\n/g; s/\\t/\t/g; s/\\r//g; s/\\'\''/'\''/g; s/: \([0-9]\+-[0-9]\+\)/: "\1"/g; s/\\\\/\\\\\\/g' | tr -d '\000-\037' | jq -r . >$(basename "$file" "_batch_output.txt").json; done
```

### 6.2.5. Combining Results for Each Year

We combine the json files, add the year (which appears in each folder) and remove extra phrases that Claude adds at the end of each file as a general conclusion. For this use case, the directory needs to be numeric, i.e. 1819.

```bash

./combine_json_add_copies.sh
```

# 7. Generating the Website

At this stage, we have the prompt, corpus, and results to investigate each copy. We need to provide philologists with a useful tool to validate the results, for which a website has been designed that offers the possibility of displaying the results while visualizing the PDFs, allowing independent scrolling in both the results and the PDF itself, as well as directly accessing pages where there are literary or artistic news.

Since the data is organized in JSON, our project only requires one webpage, the same for each year. The website reads the combined.json file (which has all results together) and displays the data. It has a JavaScript code section that iterates and shows the results, independently of the year, number of copies, how many news items were found, etc.

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Mercantil Viewer</title>
    <style>
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

        body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
            color: var(--text-color);
            background: var(--bg-color);
            margin: 0;
            padding: 20px;
        }

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

        .content-panel {
            min-width: 0;
        }

        .year-header {
            background: var(--primary-color);
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 24px;
            font-weight: bold;
        }

        .entry-card {
            background: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }

        .entry-header {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .entry-title {
            font-size: 1.5em;
            color: var(--primary-color);
            margin: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .pdf-link {
            background: var(--bg-color);
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.9em;
            text-decoration: none;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }

        .pdf-link:hover {
            background: var(--border-color);
        }

        .metadata {
            margin-top: 10px;
            color: #666;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }

        .tag {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }

        .tag-true {
            background: var(--tag-positive);
            color: var(--tag-positive-text);
        }

        .tag-false {
            background: var(--tag-negative);
            color: var(--tag-negative-text);
        }

        .content-section {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .section-title {
            font-size: 1.1em;
            color: var(--primary-color);
            margin: 0 0 15px 0;
        }

        .page-reference {
            background: var(--bg-color);
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .page-content {
            white-space: pre-wrap;
            font-family: Georgia, serif;
            line-height: 1.6;
            margin-top: 10px;
            padding: 10px;
            background: white;
            border-radius: 4px;
        }

        .article-card {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .article-title {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 10px;
        }

        .article-metadata {
            font-size: 0.9em;
            color: #666;
        }

        .article-content {
            margin-top: 10px;
        }

        .pdf-panel {
            display: none;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 20px;
            height: calc(100vh - 40px);
            overflow: hidden;
        }

        .pdf-panel.expanded {
            display: block;
        }

        .pdf-controls {
            padding: 10px 20px;
            background: var(--primary-color);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .pdf-frame {
            width: 100%;
            height: calc(100vh - 80px);
            border: none;
        }

        .btn {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 0.9em;
        }

        .btn:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .context {
            font-style: italic;
            color: #666;
            margin-top: 10px;
        }

        .page-link {
            color: var(--secondary-color);
            text-decoration: none;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
        }

        .page-link:hover {
            text-decoration: underline;
        }

        .loading {
            text-align: center;
            padding: 20px;
            font-size: 1.2em;
            color: #666;
        }

        .error {
            background: #fee;
            color: #c00;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>

<body>
    <div id="app" class="container">
        <div class="content-panel">
            <div class="loading">Cargando datos...</div>
        </div>
    </div>

    <script>
        function showPdfPage(pdfName, pageNum) {
            const container = document.querySelector('.container');
            const existingPanel = document.getElementById('pdfPanel');

            if (existingPanel) {
                if (existingPanel.getAttribute('data-pdf') === pdfName && existingPanel.getAttribute('data-page') === String(pageNum)) {
                    container.classList.remove('with-pdf');
                    existingPanel.remove();
                    return;
                }
                existingPanel.remove();
            }

            const pdfPanel = document.createElement('div');
            pdfPanel.id = 'pdfPanel';
            pdfPanel.className = 'pdf-panel expanded';
            pdfPanel.setAttribute('data-pdf', pdfName);
            pdfPanel.setAttribute('data-page', pageNum);
            const pdfUrl = `${pdfName}#page=${pageNum}`;
            pdfPanel.innerHTML = `
        <div class="pdf-controls">
            <span>${pdfName} - Página ${pageNum}</span>
            <button class="btn" onclick="closePdfViewer()">✕</button>
        </div>
        <embed class="pdf-frame" src="${pdfUrl}" type="application/pdf">
    `;

            container.classList.add('with-pdf');
            container.appendChild(pdfPanel);
        }

        function closePdfViewer() {
            const container = document.querySelector('.container');
            const pdfPanel = document.getElementById('pdfPanel');

            container.classList.remove('with-pdf');
            if (pdfPanel) {
                pdfPanel.remove();
            }
        }

        function createPageLink(pdfName, pageNum) {
            return `
                <a class="page-link" onclick="showPdfPage('${pdfName}', ${pageNum})">
                    📄 Ver página ${pageNum}
                </a>
            `;
        }

        function renderArticle(article) {
            const pageLinks = article.paginas?.map(p =>
                `<a class="page-link" onclick="showPdfPage('${article.pdfName}', ${p.pdf})">Página ${p.pdf}</a>`
            ).join(', ') || '';

            return `
                <div class="article-card">
                    <div class="article-title">${article.obra.titulo}</div>
                    <div class="article-metadata">
                        ${article.tipo ? `<div>Tipo: ${article.tipo}</div>` : ''}
                        ${article.autor ? `<div>Autor: ${article.autor}</div>` : ''}
                        ${article.obra.genero ? `<div>Género: ${article.obra.genero}</div>` : ''}
                        ${article.obra.actos ? `<div>Actos: ${article.obra.actos}</div>` : ''}
                        ${article.obra.lugar_de_representación ?
                    `<div>Lugar: ${article.obra.lugar_de_representación}</div>` : ''
                }
                        ${pageLinks ? `<div>Páginas: ${pageLinks}</div>` : ''}
                    </div>
                    ${article.contexto ? `<div class="context">${article.contexto}</div>` : ''}
                </div>
            `;
        }

        function renderEntry(entry) {
            return `
                <div class="entry-card">
                    <div class="entry-header">
                        <h2 class="entry-title">
                            ${entry.Título}
                            <a class="pdf-link" onclick="showPdfPage('${entry.PDF}', 1)">
                                📄 Ver PDF
                            </a>
                        </h2>
                        <div class="metadata">
                            <span>Fecha: ${entry.Fecha}</span>
                            <span>Número: ${entry.Número}</span>
                            <span class="tag tag-${entry.LITERATURA}">
                                Literatura: ${entry.LITERATURA ? 'Sí' : 'No'}
                            </span>
                            <span class="tag tag-${entry.MUSICA}">
                                Música: ${entry.MUSICA ? 'Sí' : 'No'}
                            </span>
                        </div>
                    </div>

                    ${entry.PAGINAS_LITERATURA?.length ? `
                        <div class="content-section">
                            <h3 class="section-title">Páginas de Literatura</h3>
                            ${entry.PAGINAS_LITERATURA.map(pagina => `
                                <div class="page-reference">
                                    <div class="page-header">
                                        <span>Página ${pagina.periodico} (PDF: ${pagina.pdf})</span>
                                        ${createPageLink(entry.PDF, pagina.pdf)}
                                    </div>
                                    ${pagina.contenido ? `
                                        <div class="page-content">${pagina.contenido}</div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}

                    ${entry.ARTICULOS_LITERATURA?.length ? `
                        <div class="content-section">
                            <h3 class="section-title">Artículos de Literatura</h3>
                            ${entry.ARTICULOS_LITERATURA.map(articulo =>
                renderArticle({ ...articulo, pdfName: entry.PDF })
            ).join('')}
                        </div>
                    ` : ''}

                    ${entry.ARTICULOS_MUSICA?.length ? `
                        <div class="content-section">
                            <h3 class="section-title">Artículos de Música</h3>
                            ${entry.ARTICULOS_MUSICA.map(articulo => `
                                <div class="article-card">
                                    <div class="article-title">${articulo.tipo}</div>
                                    <div class="article-metadata">
                                        ${articulo.obra ? `<div>Obra: ${articulo.obra}</div>` : ''}
                                        ${articulo.interprete ? `<div>Intérprete: ${articulo.interprete}</div>` : ''}
                                        ${articulo.lugar ? `<div>Lugar: ${articulo.lugar}</div>` : ''}
                                    </div>
                                    ${articulo.contexto ? `<div class="context">${articulo.contexto}</div>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}

                    ${entry.OTRAS_REFERENCIAS_CULTURALES?.length ? `
                        <div class="content-section">
                            <h3 class="section-title">Otras Referencias Culturales</h3>
                            ${entry.OTRAS_REFERENCIAS_CULTURALES.map(ref => `
                                <div class="article-card">
                                    <div class="article-title">${ref.tema}</div>
                                    <div class="article-content">${ref.descripcion}</div>
                                    ${ref.conexiones?.length ? `
                                        <div class="context">
                                            Conexiones: ${ref.conexiones.join(', ')}
                                        </div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
        }

        document.addEventListener('DOMContentLoaded', async () => {
            const app = document.querySelector('.content-panel');

            try {
                const response = await fetch('combined.json');
                if (!response.ok) throw new Error('Error al cargar el archivo JSON');
                const data = await response.json();

                app.innerHTML = `
                    <div class="year-header">Año ${data.Año}</div>
                    ${data.datos.map(entry => renderEntry(entry)).join('')}
                `;

            } catch (error) {
                app.innerHTML = `
                    <div class="error">
                        Error al cargar los datos: ${error.message}
                    </div>
                `;
                console.error('Error:', error);
            }
        });
    </script>
</body>

</html>
```

# 8. Sharing the Data

To verify that the designed website is useful, we opted to upload a small sample to Github, a repository that allows displaying web pages.

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

Once verified, given the volume of data in this project, all information and PDFs are read from local files.

To allow Google Chrome to read local data, we launch it with:

```bash

google-chrome --allow-file-access-from-files file.html 
```

# 9. Conclusion

The use of scraping techniques and AI queries allows systematization of the download process and subsequent location of news of interest in historical press. The developed procedure has been validated for literary and artistic news, being equally useful for other types of research, which would only need to adjust the prompt to their field of study.

# 10. Similar projects

The rise of AI and improvements in OCR/HTR are enabling the Digital Humanities to mine and analyze massive amounts of data. A number of initiatives for the curious reader can be found at:

1. [Digital Douady](https://github.com/phughesmcr/digitaldouay)
2. [LexiMus](https://leximus.es)
3. [Large-Scale Research with Historical Newspapers: A Turning Point through Generative AI - DH Lab](https://dhlab.hypotheses.org/4938)
