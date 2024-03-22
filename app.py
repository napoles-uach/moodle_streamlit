import streamlit as st
import re

def parse_moodle_question(question_text):
    """
    Analiza el texto de una pregunta de Moodle y extrae sus componentes.
    """
    # Extrae el título y el cuerpo de la pregunta.
    title_match = re.search(r"// question: \d+  name: (.+)", question_text)
    body_start = question_text.find("::") + 2
    body_end = question_text.find("{")
    body = question_text[body_start:body_end].strip()

    title = title_match.group(1) if title_match else "Pregunta sin título"

    # Extrae las respuestas
    answers_text = question_text[body_end:]
    answers = re.findall(r"([~=])([^\n]+)", answers_text)
    answers_components = []
    for correct, text in answers:
        answers_components.append({
            "text": text.strip(),
            "correct": True if correct == "=" else False
        })

    components = {
        "title": title,
        "body": body,
        "answers": answers_components
    }
    return components

def display_question(question_components):
    """
    Muestra una pregunta y sus componentes usando Streamlit.
    """
    st.subheader(question_components["title"])
    st.markdown(question_components["body"], unsafe_allow_html=True)
    for answer in question_components["answers"]:
        # Usar markdown para permitir formato HTML en las respuestas
        label = "✅ " + answer["text"] if answer["correct"] else "❌ " + answer["text"]
        st.markdown(label, unsafe_allow_html=True)

def main():
    """
    Función principal para ejecutar la app de Streamlit.
    """
    st.title("Visualizador de Preguntas Moodle")

    # Carga de archivo
    uploaded_file = st.file_uploader("Cargar archivo de preguntas Moodle", type=['txt'])
    
    if uploaded_file is not None:
        # Leer el contenido del archivo
        question_text = uploaded_file.read().decode("utf-8")
        
        # Dividir el contenido en preguntas individuales.
        questions = question_text.split('// question:')
        questions = questions[1:]  # Elimina el primer elemento vacío si existe
        
        for question in questions:
            question = '// question:' + question  # Reañade el prefijo removido al dividir
            components = parse_moodle_question(question)
            display_question(components)

if __name__ == "__main__":
    main()
