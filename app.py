import streamlit as st
from io import StringIO

def generate_moodle_question_format(question_type, title, body, answers, correct_answer_index):
    """
    Genera el formato de pregunta de Moodle basado en los inputs del usuario.
    """
    # Corrección aplicada aquí para manejar correctamente las llaves dentro de la f-string
    question_text = f"// question: XXXXXXX  name: {title}\n::{title}::[html]{body}{{"
    for i, answer in enumerate(answers):
        prefix = "=" if i == correct_answer_index else "~"
        question_text += f"\n\t{prefix}<p>{answer}</p>"
    question_text += "\n}}\n"  # Se duplican las llaves para cerrar literalmente
    return question_text

def main():
    """
    Función principal para ejecutar la app de Streamlit.
    """
    st.title("Creador de Preguntas Moodle")

    # Entradas para la creación de la pregunta
    question_type = st.selectbox("Tipo de pregunta", ["Opción múltiple", "Verdadero/Falso", "Respuesta corta"])
    title = st.text_input("Título de la pregunta")
    body = st.text_area("Cuerpo de la pregunta", height=150)
    answers = []
    correct_answer_index = None

    if question_type == "Opción múltiple":
        for i in range(4):  # Asumimos 4 respuestas para simplificar
            answer = st.text_input(f"Respuesta {i + 1}", key=f"answer_{i}")
            answers.append(answer)
        correct_answer_index = st.selectbox("Índice de la respuesta correcta", options=range(1, 5), format_func=lambda x: f"Respuesta {x}") - 1
    elif question_type == "Verdadero/Falso":
        answers = ["VERDADERO", "FALSO"]
        correct_answer_index = st.selectbox("Respuesta correcta", options=[1, 2], format_func=lambda x: "VERDADERO" si x == 1 else "FALSO") - 1

    # Botón para generar el formato de la pregunta y escribirlo a un archivo
    if st.button("Generar Formato de Pregunta"):
        if not all([title, body, answers, correct_answer_index is not None]):
            st.error("Por favor, completa todos los campos.")
        else:
            question_format = generate_moodle_question_format(question_type, title, body, answers, correct_answer_index)
            # Crear un objeto StringIO para alojar el texto de la pregunta
            question_file = StringIO()
            question_file.write(question_format)
            question_file.seek(0)  # Moverse al principio del archivo para la descarga

            # Crear un link de descarga
            st.download_button(label="Descargar Pregunta Moodle",
                               data=question_file,
                               file_name="moodle_question.txt",
                               mime="text/plain")

if __name__ == "__main__":
    main()
