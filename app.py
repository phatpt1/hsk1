import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from gtts import gTTS
import os

st.set_page_config(page_title="App Học HSK 1", layout="wide")

# Nạp file chứa 500 từ vựng
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hsk1_vocab.csv")
    except FileNotFoundError:
        st.error("Chưa tìm thấy file hsk1_vocab.csv. Vui lòng chạy file extract_data.py trước!")
        return pd.DataFrame(columns=["STT", "Tiếng Trung", "Pinyin", "Từ loại", "Dịch nghĩa"])

df = load_data()

st.sidebar.title("Chức năng HSK 1")
menu = st.sidebar.radio(
    "Chọn bài học", 
    ["Từ vựng", "Luyện nghe", "Ngữ pháp & Mẫu câu", "Luyện viết (Apple Pencil)"]
)

if menu == "Từ vựng":
    st.header("Danh sách 500 Từ Vựng HSK 1")
    if not df.empty:
        # Hiển thị bảng full 500 từ có thể cuộn
        st.dataframe(df, use_container_width=True, height=600)

elif menu == "Luyện nghe":
    st.header("Luyện Nghe Từ Vựng")
    if not df.empty:
        # Gộp STT, Tiếng Trung và Pinyin để hiển thị trong thanh chọn
        df['Label'] = df['STT'].astype(str) + ". " + df['Tiếng Trung'] + " (" + df['Pinyin'] + ")"
        selected_label = st.selectbox("Tìm hoặc chọn từ để nghe phát âm:", df["Label"])
        
        selected_word = df.loc[df["Label"] == selected_label, "Tiếng Trung"].values[0]
        
        if st.button("Phát âm từ này"):
            tts = gTTS(selected_word, lang='zh-cn')
            audio_file = "audio.mp3"
            tts.save(audio_file)
            with open(audio_file, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove(audio_file)

elif menu == "Ngữ pháp & Mẫu câu":
    st.header("Ngữ pháp và Mẫu câu Cơ bản")
    st.subheader("Luyện viết và phát âm cả câu")
    user_sentence = st.text_input("Nhập 1 câu tiếng Trung bằng bàn phím của bạn:")
    if user_sentence:
        st.success(f"Câu của bạn: {user_sentence}")
        if st.button("Nghe câu của bạn"):
            tts_sentence = gTTS(user_sentence, lang='zh-cn')
            tts_sentence.save("sentence_audio.mp3")
            with open("sentence_audio.mp3", "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove("sentence_audio.mp3")

elif menu == "Luyện viết (Apple Pencil)":
    st.header("Luyện Viết Chữ Hán")
    st.write("Sử dụng Apple Pencil để luyện viết các nét chữ.")
    
    if not df.empty:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            df['Label'] = df['STT'].astype(str) + ". " + df['Tiếng Trung'] + " (" + df['Pinyin'] + ")"
            word_to_draw_label = st.selectbox("Chọn từ muốn tập viết:", df["Label"])
            
            # Lấy thông tin chi tiết của từ đang chọn
            word_info = df[df["Label"] == word_to_draw_label].iloc[0]
            
            st.metric(label="Pinyin", value=word_info["Pinyin"])
            st.metric(label="Nghĩa", value=word_info["Dịch nghĩa"])
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #E03C31;'>{word_info['Tiếng Trung']}</h1>", unsafe_allow_html=True)
            
        with col2:
            st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=5,
                stroke_color="#000000",
                background_color="#FFFFFF",
                height=450,
                width=450,
                drawing_mode="freedraw",
                key="canvas",
            )