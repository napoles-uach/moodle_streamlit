import streamlit as st

def generate_moodle_question_format(question_type, title, body, answers, correct_answer_index):
    """
    Genera el formato de pregunta de Moodle basado en los inputs del usuario.
    """
    question_text = f"// question: XXXXXXX  name: {title}\n::{title}::[html]{body}{{"
    for i, answer in enumerate(answers):
        prefix = "=" if i == correct_answer_index else "~"
        question_text += f"\n\t{prefix}<p>{answer}</p>"
    question_text += "\n}}\n"
    return question_text

def main():
    """
    Función principal para ejecutar la app de Streamlit.
    """
    st.title("Creador de Preguntas Moodle")

    question_type = st.selectbox("Tipo de pregunta", ["Opción múltiple", "Verdadero/Falso"])
    title = st.text_input("Título de la pregunta")
    body = st.text_area("Cuerpo de la pregunta", height=150)
    answers = []
    correct_answer_index = None

    if question_type == "Opción múltiple":
        for i in range(4):
            answer = st.text_input(f"Respuesta {i + 1}", key=f"answer_{i}")
            answers.append(answer)
        correct_answer_index = st.selectbox("Índice de la respuesta correcta", options=list(range(1, 5)), format_func=lambda x: f"Respuesta {x}") - 1
    elif question_type == "Verdadero/Falso":
        answers = ["VERDADERO", "FALSO"]
        correct_answer = st.radio("Respuesta correcta", options=["VERDADERO", "FALSO"])
        correct_answer_index = 0 if correct_answer == "VERDADERO" else 1

    if st.button("Generar Formato de Pregunta"):
        if not all([title, body, answers, correct_answer_index is not None]):
            st.error("Por favor, completa todos los campos.")
        else:
            question_format = generate_moodle_question_format(question_type, title, body, answers, correct_answer_index)
            
            # Mostrar el formato de la pregunta en la pantalla
            st.subheader("Formato de la Pregunta Moodle")
            st.code(question_format, language='plaintext')

            # Crear un link de descarga
            st.download_button(label="Descargar Pregunta Moodle",
                               data=question_format,
                               file_name="moodle_question.txt",
                               mime="text/plain")

if __name__ == "__main__":
    main()
