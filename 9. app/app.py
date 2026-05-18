{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP5mq+VoBQSZpkEuuaRfOvx",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Medrodi/tranformation_coordinates_app/blob/main/9.%20app/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "zoUmFoUk-qhh"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import requests\n",
        "import io\n",
        "from urllib.parse import urljoin\n",
        "\n",
        "# Конфигурация приложения\n",
        "st.set_page_config(\n",
        "    page_title=\"Трансформация координат\",\n",
        "    page_icon=\"🌍\",\n",
        "    layout=\"wide\"\n",
        ")\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "AVAILABLE_SYSTEMS = [\n",
        "    \"СК-42\", \"СК-95\", \"ПЗ-90\", \"ПЗ-90.02\",\n",
        "    \"ПЗ-90.11\", \"WGS-84 (G1150)\", \"ITRF-2008\", \"СГК-2011\"\n",
        "]\n",
        "\n",
        "\n",
        "\n",
        "def main():\n",
        "    st.title(\"🌍 Автоматизированная система преобразования координат\")\n",
        "    st.markdown(\"\"\"\n",
        "    Этот инструмент позволяет загрузить Excel-файл и получить отчет\n",
        "    в формате DOCX с преобразованными координатами. Просто загрузите файл и нажмите кнопку \"Анализировать\".\n",
        "    \"\"\")\n",
        "\n",
        "\n",
        "    col1, col2 = st.columns([1, 2])\n",
        "\n",
        "    with col1:\n",
        "        st.subheader(\"⚙️ Настройки трансформации\")\n",
        "\n",
        "        # Выпадающие списки выбора систем координат\n",
        "        initial_sk = st.selectbox(\"Начальная система координат\", AVAILABLE_SYSTEMS, index=0)\n",
        "        final_sk = st.selectbox(\"Конечная система координат\", AVAILABLE_SYSTEMS, index=7)\n",
        "\n",
        "        if initial_sk == final_sk:\n",
        "            st.warning(\"⚠️ Начальная и конечная системы координат совпадают.\")\n",
        "\n",
        "        uploaded_file = st.file_uploader(\"Выберите Excel файл\", type=['xlsx', 'xls'])\n",
        "\n",
        "    with col2:\n",
        "        st.subheader(\"📊 Предварительный просмотр\")\n",
        "        if uploaded_file is not None:\n",
        "            try:\n",
        "                df = pd.read_excel(uploaded_file)\n",
        "\n",
        "                # Проверяем колонки на фронтенде, чтобы сразу подсказать пользователю, если файл не тот\n",
        "                required_cols = {'Name', 'X', 'Y', 'Z'}\n",
        "                if not required_cols.issubset(df.columns):\n",
        "                    st.error(f\"Ошибка: файл должен содержать столбцы: {', '.join(required_cols)}\")\n",
        "                else:\n",
        "                    st.dataframe(df.head(5), use_container_width=True)\n",
        "\n",
        "                    # Выводим небольшие карточки с метриками данных\n",
        "                    m1 = st.columns(1)\n",
        "                    m1.metric(\"Всего точек (строк)\", df.shape[0])\n",
        "\n",
        "\n",
        "                    # Сбрасываем указатель файла для повторного чтения\n",
        "                    uploaded_file.seek(0)\n",
        "\n",
        "                    st.write(\"---\")\n",
        "\n",
        "            except Exception as e:\n",
        "                st.error(f\"Ошибка чтения файла: {str(e)}\")\n",
        "        else:\n",
        "            st.info(\"Пожалуйста, загрузите файл Excel в левой панели для начала работы.\")"
      ]
    }
  ]
}