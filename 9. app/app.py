import streamlit as st
import pandas as pd
import requests
import io
from urllib.parse import urljoin

# Конфигурация приложения
st.set_page_config(
    page_title="Трансформация координат",
    page_icon="🌍",
    layout="wide"
)




AVAILABLE_SYSTEMS = [
    "СК-42", "СК-95", "ПЗ-90", "ПЗ-90.02",
    "ПЗ-90.11", "WGS-84 (G1150)", "ITRF-2008", "СГК-2011"
]



def main():
    st.title("🌍 Автоматизированная система преобразования координат")
    st.markdown("""
    Этот инструмент позволяет загрузить Excel-файл и получить отчет
    в формате DOCX с преобразованными координатами. Просто загрузите файл и нажмите кнопку "Анализировать".
    """)


    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ Настройки трансформации")

        # Выпадающие списки выбора систем координат
        initial_sk = st.selectbox("Начальная система координат", AVAILABLE_SYSTEMS, index=0)
        final_sk = st.selectbox("Конечная система координат", AVAILABLE_SYSTEMS, index=7)

        if initial_sk == final_sk:
            st.warning("⚠️ Начальная и конечная системы координат совпадают.")

        uploaded_file = st.file_uploader("Выберите Excel файл", type=['xlsx', 'xls'])

    with col2:
        st.subheader("📊 Предварительный просмотр")
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)

                # Проверяем колонки на фронтенде, чтобы сразу подсказать пользователю, если файл не тот
                required_cols = {'Name', 'X', 'Y', 'Z'}
                if not required_cols.issubset(df.columns):
                    st.error(f"Ошибка: файл должен содержать столбцы: {', '.join(required_cols)}")
                else:
                    st.dataframe(df.head(5), use_container_width=True)

                    # Выводим небольшие карточки с метриками данных
                    m1 = st.columns(1)
                    m1.metric("Всего точек (строк)", df.shape[0])


                    # Сбрасываем указатель файла для повторного чтения
                    uploaded_file.seek(0)

                    st.write("---")

            except Exception as e:
                st.error(f"Ошибка чтения файла: {str(e)}")
        else:
            st.info("Пожалуйста, загрузите файл Excel в левой панели для начала работы.")
