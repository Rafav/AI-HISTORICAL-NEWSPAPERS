import base64
import sys
from anthropic import Anthropic


if len(sys.argv) != 2:
    print("Usage: python diario.py <pdf_file>")
    sys.exit(1)

    
# While PDF support is in beta, you must pass in the correct beta header
client = Anthropic(
   api_key ='ENTER YOUR API KEY' ,
   default_headers={
    "anthropic-beta": "pdfs-2024-09-25"
  }
  
  
)
# For now, only claude-3-5-sonnet-20241022 supports PDFs
MODEL_NAME = "claude-3-5-sonnet-20241022"


# Start by reading in the PDF and encoding it as base64
file_name = sys.argv[1]

with open(file_name, "rb") as pdf_file:
  binary_data = pdf_file.read()
  base64_encoded_data = base64.standard_b64encode(binary_data)
  base64_string = base64_encoded_data.decode("utf-8")

prompt = """
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
"""
messages = [
    {
        "role": 'user',
        "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": base64_string}},
            {"type": "text", "text": prompt}
        ]
    }
]

def get_completion(client, messages):
    return client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        messages=messages
    ).content[0].text

completion = get_completion(client, messages)
print(completion)
