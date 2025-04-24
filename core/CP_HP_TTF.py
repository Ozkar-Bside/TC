import re
import docx
import pandas as pd
import openai
import tiktoken  # Para contar los tokens
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
MODELO_AI = "gpt-4-turbo"
MAX_TOKENS = 4000  # Límite de tokens para GPT-4-turbo (8192)

# Función para contar los tokens en el texto
def contar_tokens(texto):
    encoding = tiktoken.get_encoding("cl100k_base")  # Usar el codificador apropiado
    tokens = encoding.encode(texto)
    return len(tokens)

# 📥 Leer texto desde un archivo .docx
def leer_docx(ruta):
    doc = docx.Document(ruta)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return texto

# 🤖 Llamar a GPT para generar casos de prueba clasificados
def generar_casos(texto, modelo=MODELO_AI):
    prompt = f"""
Eres un experto en QA.
Con base en este texto funcional, genera una tabla Markdown con los casos de prueba divididos en "Happy Path" y "Test to Fail". 

Debe tener columnas: Tipo, Nombre del caso, Paso a paso, Resultado esperado.

Texto funcional:
{texto}
"""
    # y "Test to Fail" "Happy Path"
    # Contar los tokens del prompt
    num_tokens = contar_tokens(prompt)
    print(f"🔢 Tokens en el texto de entrada (prompt): {num_tokens}")

    if num_tokens > MAX_TOKENS:
        print(f"⚠️ El texto excede el límite de tokens ({MAX_TOKENS}). Dividiendo el texto...")
        # Aquí dividimos el texto para no exceder el límite de tokens
        # Se divide el texto por secciones para que cada sección no exceda el límite
        max_tokens_por_seccion = MAX_TOKENS - num_tokens
        partes = [texto[i:i+max_tokens_por_seccion] for i in range(0, len(texto), max_tokens_por_seccion)]
        resultados = []

        # Procesar cada parte por separado
        for i, parte in enumerate(partes):
            print(f"📄 Procesando parte {i+1} de {len(partes)}...")
            prompt_parte = f"{prompt}\n\nParte del texto:\n{parte}"
            respuesta = openai.ChatCompletion.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Eres un generador de casos de prueba."},
                    {"role": "user", "content": prompt_parte}
                ],
                temperature=0.3
            )
            resultados.append(respuesta.choices[0].message.content)
        
        return "\n".join(resultados)
    else:
        # Si no excede el límite, procesar normalmente
        print(f"✅ El texto tiene {num_tokens} tokens, dentro del límite.")
        respuesta = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un generador de casos de prueba."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return respuesta.choices[0].message.content

# 🧼 Convertir respuesta de texto a lista de diccionarios
def parsear_tabla_markdown(texto):
    filas = []
    dentro_de_tabla = False

    for linea in texto.splitlines():
        if linea.strip().startswith('|') and not re.match(r'\|\s*-+\s*\|', linea):
            dentro_de_tabla = True
            columnas = [col.strip() for col in linea.strip().split('|') if col.strip()]
            if len(columnas) == 4 and columnas[0] not in ['Tipo']:  # Evita cabeceras
                filas.append({
                    "Tipo": columnas[0],
                    "Nombre del caso": columnas[1],
                    "Paso a paso": columnas[2].replace("<br>", "\n"),
                    "Resultado esperado": columnas[3].replace("<br>", "\n")
                })
        elif '###' in linea:  # reinicia cuando hay nuevos encabezados
            dentro_de_tabla = False
    return filas

# 🔄 Ejecutar todo el flujo
def main():
    ruta_docx = "requisitos.docx"  # Archivo .docx con las descripciones funcionales
    ruta_csv = "casos_de_prueba_All.csv"  # Archivo donde se guardarán los casos de prueba generados
    ruta_excel = "casos_de_prueba.xlsx"

    print(f"📘 Leyendo documento: {ruta_docx}")
    texto = leer_docx(ruta_docx)
    if not texto.strip():
        print("❌ El documento está vacío.")
        return

    print("🤖 Generando casos de prueba con modelo:", MODELO_AI)
    texto_generado = generar_casos(texto)
    print("🧾 Texto generado por la IA:\n", texto_generado)

    casos = parsear_tabla_markdown(texto_generado)
    if not casos:
        print("⚠️ No se encontraron filas válidas en el formato Markdown.")
        return

    df = pd.DataFrame(casos)
    df.to_csv(ruta_csv, index=False, encoding='utf-8-sig')
    #df.to_excel(ruta_excel, index=False)
    print(f"✅ Guardado CSV: {ruta_csv}")
    #print(f"✅ Guardado Excel: {ruta_excel}")

if __name__ == "__main__":
    main()
