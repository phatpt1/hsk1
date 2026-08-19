import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import io
import hashlib
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="App Học HSK 1", layout="wide")

# ================= HÀM HỖ TRỢ =================
# Hàm 1: Nạp dữ liệu từ file CSV chuẩn
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hsk1_vocab_final.csv")
    except Exception:
        st.error("Lỗi: Chưa tìm thấy file hsk1_vocab.csv. Hãy đảm bảo bạn đã đẩy file này lên GitHub.")
        return pd.DataFrame(columns=["STT", "Tiếng Trung", "Pinyin", "Từ loại", "Dịch nghĩa"])

# Hàm 2: Tạo nút Audio ẩn thanh player (Dùng HTML/JS)
def create_audio_button(text, button_text="🔊 Phát âm từ này"):
    if not text: return
    try:
        tts = gTTS(text, lang='zh-cn')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        
        # Tạo ID ngẫu nhiên để không bị trùng lặp âm thanh
        html_id = "audio_" + hashlib.md5(text.encode()).hexdigest()
        
        html = f"""
        <audio id="{html_id}" src="data:audio/mp3;base64,{b64}"></audio>
        <button onclick="document.getElementById('{html_id}').play()" 
                style="padding: 10px 20px; font-size: 16px; cursor: pointer; 
                       background-color: #ff4b4b; color: white; border: none; 
                       border-radius: 6px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {button_text}
        </button>
        """
        components.html(html, height=60)
    except Exception as e:
        st.error("Không thể tải âm thanh (lỗi kết nối).")

# ================= GIAO DIỆN CHÍNH =================
df = load_data()

st.sidebar.title("Chức năng HSK 1")
menu = st.sidebar.radio(
    "Chọn bài học", 
    ["Từ vựng", "Luyện nghe", "Ngữ pháp & Mẫu câu", "Luyện viết (Hanzi Writer)"]
)

# ----------------- CHỨC NĂNG 1: TỪ VỰNG -----------------
if menu == "Từ vựng":
    st.header("Danh sách 500 Từ Vựng HSK 1")
    if not df.empty:
        st.dataframe(df, use_container_width=True, height=600)

# ----------------- CHỨC NĂNG 2: LUYỆN NGHE -----------------
elif menu == "Luyện nghe":
    st.header("Luyện Nghe Từ Vựng")
    if not df.empty:
        df['Label'] = df['STT'].astype(str) + ". " + df['Tiếng Trung'] + " (" + df['Pinyin'] + ")"
        selected_label = st.selectbox("Tìm hoặc chọn từ để nghe phát âm:", df["Label"])
        selected_word = df.loc[df["Label"] == selected_label, "Tiếng Trung"].values[0]
        
        st.markdown(f"<h1 style='color: #E03C31;'>{selected_word}</h1>", unsafe_allow_html=True)
        # Nút audio đã được thu gọn, không còn thanh kéo
        create_audio_button(selected_word)

# ----------------- CHỨC NĂNG 3: NGỮ PHÁP -----------------
elif menu == "Ngữ pháp & Mẫu câu":
    st.header("Ngữ pháp HSK 1 Trọng tâm")
    
    tab1, tab2, tab3 = st.tabs(["1. Câu chữ 是", "2. Câu hỏi với 吗", "3. Phủ định 不 / 没"])
    
    with tab1:
        st.subheader("Cấu trúc: Chủ ngữ + 是 (shì) + Danh từ")
        st.write("Dùng để giới thiệu, định nghĩa (nghĩa là: **là**).")
        st.info("Ví dụ:\n- 我 是 学生。(Tôi là học sinh.)\n- 他 是 老师。(Ông ấy là giáo viên.)")
    
    with tab2:
        st.subheader("Cấu trúc: Câu trần thuật + 吗 (ma) ?")
        st.write("Đặt ở cuối câu để tạo thành câu hỏi Có/Không (nghĩa là: **không?**, **phải không?**).")
        st.info("Ví dụ:\n- 你 爱 我 吗？(Bạn có yêu tôi không?)\n- 她 是 护士 吗？(Cô ấy có phải là y tá không?)")
        
    with tab3:
        st.subheader("Phủ định với 不 (bù) và 没 (méi)")
        st.write("- **不 (bù):** Phủ định ở hiện tại/tương lai hoặc ý muốn (Nghĩa là: **không**).")
        st.write("- **没 (méi):** Phủ định hành động trong quá khứ hoặc sở hữu (Nghĩa là: **chưa, không có**).")
        st.info("Ví dụ:\n- 我 不 吃 肉。(Tôi không ăn thịt - thói quen.)\n- 我 没 吃饭。(Tôi chưa ăn cơm - sự việc.)")

    st.divider()
    st.subheader("Luyện ghép câu & Phát âm")
    user_sentence = st.text_input("Gõ câu tiếng Trung của bạn tại đây để kiểm tra:")
    if user_sentence:
        st.success(f"Câu của bạn: {user_sentence}")
        create_audio_button(user_sentence, "🔊 Nghe câu này")

# ----------------- CHỨC NĂNG 4: LUYỆN VIẾT HANZI -----------------
elif menu == "Luyện viết (Hanzi Writer)":
    st.header("Luyện Viết Chữ Hán & Phân Tích Nét")
    st.write("Sử dụng Apple Pencil hoặc chuột. Nền lưới điền tự cách (田字格) giúp bạn canh tỉ lệ.")
    
    if not df.empty:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            df['Label'] = df['STT'].astype(str) + ". " + df['Tiếng Trung'] + " (" + df['Pinyin'] + ")"
            selected_label = st.selectbox("Chọn từ vựng:", df["Label"])
            
            word_info = df[df["Label"] == selected_label].iloc[0]
            word_to_draw = str(word_info['Tiếng Trung'])
            
            st.metric(label="Pinyin", value=word_info["Pinyin"])
            st.metric(label="Nghĩa", value=word_info["Dịch nghĩa"])
            create_audio_button(word_to_draw, "🔊 Phát âm")
            
            st.divider()
            # Bắt lỗi nếu từ có 2 chữ trở lên (VD: 爸爸), cho phép chọn từng chữ để viết
            char_to_draw = word_to_draw[0]
            if len(word_to_draw) > 1:
                st.write("**Chọn từng Hán tự để tập viết:**")
                char_to_draw = st.radio("", list(word_to_draw), horizontal=True)

        with col2:
            # Tích hợp thư viện Hanzi Writer bằng HTML/JS
            html_code = f"""
            <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
            <style>
                .hanzi-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
                /* Tạo lưới 田字格 làm background */
                #grid-background {{
                    width: 300px; height: 300px; 
                    background-color: #fcfcfc;
                    background-image: 
                        linear-gradient(45deg, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(-45deg, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(to right, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(to bottom, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%);
                    border: 3px solid #d32f2f;
                    border-radius: 8px;
                    margin-bottom: 15px;
                }}
                button {{ margin: 5px; padding: 10px 15px; font-size: 15px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; }}
                #quiz-btn {{ background-color: #168F16; color: white; border: none; }}
            </style>
            
            <div class="hanzi-container">
                <div id="grid-background"></div>
                <div>
                    <button id="animate-btn">▶ Xem thứ tự nét</button>
                    <button id="quiz-btn">✍️ Tự luyện (Chế độ Quiz)</button>
                </div>
                <h4 id="feedback" style="color: #d32f2f; margin-top: 10px; height: 20px;"></h4>
            </div>
            
            <script>
                var writer = HanziWriter.create('grid-background', '{char_to_draw}', {{
                    width: 300, height: 300, padding: 15,
                    showOutline: true, strokeAnimationSpeed: 1, delayBetweenStrokes: 100,
                    radicalsColor: '#168F16' // Nhấn mạnh màu bộ thủ
                }});

                document.getElementById('animate-btn').addEventListener('click', function() {{
                    writer.animateCharacter();
                }});

                document.getElementById('quiz-btn').addEventListener('click', function() {{
                    document.getElementById('feedback').innerText = "Bắt đầu vẽ! Nếu vẽ sai thứ tự nét, hệ thống sẽ báo.";
                    document.getElementById('feedback').style.color = "#333";
                    
                    writer.quiz({{
                        onMistake: function(strokeData) {{
                            document.getElementById('feedback').innerText = "Sai nét hoặc sai chiều! Hãy thử lại.";
                            document.getElementById('feedback').style.color = "red";
                        }},
                        onCorrectStroke: function(strokeData) {{
                            document.getElementById('feedback').innerText = "Nét " + strokeData.strokeNum + " chính xác!";
                            document.getElementById('feedback').style.color = "blue";
                        }},
                        onComplete: function(summaryData) {{
                            document.getElementById('feedback').innerText = "🎉 Chúc mừng! Bạn đã viết đúng toàn bộ chữ này.";
                            document.getElementById('feedback').style.color = "green";
                        }}
                    }});
                }});
            </script>
            """
            components.html(html_code, height=450)
