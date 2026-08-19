import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import io
import hashlib
import random
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas

# Cấu hình trang
st.set_page_config(page_title="App Học HSK 1", layout="wide")

# ================= HÀM HỖ TRỢ =================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hsk1_vocab.csv")
    except Exception:
        st.error("Lỗi: Chưa tìm thấy file hsk1_vocab.csv. Hãy đảm bảo bạn đã đẩy file này lên GitHub.")
        return pd.DataFrame(columns=["STT", "Tiếng Trung", "Pinyin", "Từ loại", "Dịch nghĩa"])

def create_audio_button(text, button_text="🔊 Phát âm từ này"):
    if not text: return
    try:
        tts = gTTS(text, lang='zh-cn')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        
        html_id = "audio_" + hashlib.md5(text.encode()).hexdigest()
        
        html = f"""
        <div style="text-align: center; margin-top: 15px;">
            <audio id="{html_id}" src="data:audio/mp3;base64,{b64}"></audio>
            <button onclick="document.getElementById('{html_id}').play()" 
                    style="padding: 12px 25px; font-size: 18px; cursor: pointer; 
                           background-color: #ff4b4b; color: white; border: none; 
                           border-radius: 8px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                {button_text}
            </button>
        </div>
        """
        components.html(html, height=80)
    except Exception as e:
        st.error("Không thể tải âm thanh (lỗi kết nối).")

# ================= GIAO DIỆN CHÍNH =================
df = load_data()

st.sidebar.title("Chức năng HSK 1")
menu = st.sidebar.radio(
    "Chọn bài học", 
    ["Từ vựng", "Luyện nghe", "Ngữ pháp & Mẫu câu", "Luyện viết", "Đề thi thử Mini"]
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
        word_info = df[df["Label"] == selected_label].iloc[0]
        
        html_display = f"""
        <div style='text-align: center; padding: 20px; background-color: #f9f9f9; border-radius: 15px;'>
            <span style='font-size: 150px; color: #E03C31; line-height: 1.2; font-weight: bold;'>{word_info['Tiếng Trung']}</span><br>
            <span style='font-size: 35px; color: #333;'>[ {word_info['Pinyin']} ]</span><br>
            <span style='font-size: 28px; color: #0066cc; font-weight: 500;'>Nghĩa: {word_info['Dịch nghĩa']}</span>
        </div>
        """
        st.markdown(html_display, unsafe_allow_html=True)
        create_audio_button(word_info['Tiếng Trung'])

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

# ----------------- CHỨC NĂNG 4: LUYỆN VIẾT -----------------
elif menu == "Luyện viết":
    st.header("Luyện Viết Chữ Hán")
    
    if not df.empty:
        df['Label'] = df['STT'].astype(str) + ". " + df['Tiếng Trung'] + " (" + df['Pinyin'] + ")"
        selected_label = st.selectbox("📌 Chọn từ vựng:", df["Label"])
        word_info = df[df["Label"] == selected_label].iloc[0]
        word_to_draw = str(word_info['Tiếng Trung'])
        
        col_info, col_audio = st.columns([2, 1])
        with col_info:
            st.markdown(f"**Pinyin:** {word_info['Pinyin']} &nbsp;&nbsp;|&nbsp;&nbsp; **Nghĩa:** {word_info['Dịch nghĩa']}")
        with col_audio:
            create_audio_button(word_to_draw, "🔊 Phát âm")

        st.divider()
        tab_quiz, tab_free = st.tabs(["✍️ Viết theo mẫu (Chấm điểm nét)", "🖌️ Viết tự do (Bút thư pháp)"])
        
        # TAB 1: HANZI WRITER
        with tab_quiz:
            char_to_draw = word_to_draw[0]
            if len(word_to_draw) > 1:
                st.write("**Chọn từng Hán tự để tập viết theo chuẩn:**")
                char_to_draw = st.radio("", list(word_to_draw), horizontal=True, key="hanzi_radio")

            html_code = f"""
            <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
            <style>
                .hanzi-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
                #grid-background {{
                    width: 300px; height: 300px; 
                    background-color: #fcfcfc;
                    background-image: 
                        linear-gradient(45deg, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(-45deg, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(to right, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%),
                        linear-gradient(to bottom, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%);
                    border: 3px solid #d32f2f; border-radius: 8px; margin-bottom: 15px;
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
                    width: 300, height: 300, padding: 15, showOutline: true, 
                    strokeAnimationSpeed: 1, delayBetweenStrokes: 100, radicalsColor: '#168F16'
                }});

                document.getElementById('animate-btn').addEventListener('click', function() {{ writer.animateCharacter(); }});

                document.getElementById('quiz-btn').addEventListener('click', function() {{
                    document.getElementById('feedback').innerText = "Bắt đầu vẽ! Nếu vẽ sai thứ tự nét, hệ thống sẽ báo.";
                    document.getElementById('feedback').style.color = "#333";
                    
                    writer.quiz({{
                        onMistake: function() {{
                            document.getElementById('feedback').innerText = "Sai nét hoặc sai chiều! Hãy thử lại.";
                            document.getElementById('feedback').style.color = "red";
                        }},
                        onCorrectStroke: function(strokeData) {{
                            document.getElementById('feedback').innerText = "Nét " + strokeData.strokeNum + " chính xác!";
                            document.getElementById('feedback').style.color = "blue";
                        }},
                        onComplete: function() {{
                            document.getElementById('feedback').innerText = "🎉 Chúc mừng! Bạn đã viết đúng toàn bộ chữ này.";
                            document.getElementById('feedback').style.color = "green";
                        }}
                    }});
                }});
            </script>
            """
            components.html(html_code, height=450)

        # TAB 2: FREE DRAW CANVAS
        with tab_free:
            st.write("Sử dụng Apple Pencil hoặc chuột để phác thảo tự do.")
            col_settings, col_canvas = st.columns([1, 2])
            
            with col_settings:
                stroke_width = st.slider("🖌️ Độ dày nét bút", min_value=1, max_value=30, value=8, step=1)
                stroke_color = st.color_picker("🎨 Màu mực", "#000000")
                st.info("💡 Không gian giấy vẽ nằm ở khối màu xám ngay bên cạnh nha!")
            
            with col_canvas:
                # Đã thêm background_color="#F0F2F6" (xám nhạt) để lộ rõ không gian vẽ
                st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",
                    stroke_width=stroke_width,
                    stroke_color=stroke_color,
                    background_color="#F0F2F6",
                    height=350,
                    width=350,
                    drawing_mode="freedraw",
                    key="canvas_freedraw",
                )

# ----------------- CHỨC NĂNG 5: ĐỀ THI THỬ -----------------
elif menu == "Đề thi thử Mini":
    st.header("📝 Đề Thi Thử HSK 1 (Trắc Nghiệm)")
    st.write("Kiểm tra phản xạ từ vựng. Hệ thống sẽ bốc ngẫu nhiên 10 câu hỏi từ 500 từ HSK 1.")
    
    if not df.empty:
        # Khởi tạo trạng thái phiên (Session State) để giữ nguyên đề thi khi chọn đáp án
        if 'quiz_data' not in st.session_state:
            st.session_state.quiz_data = []
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False
            
        # Nút tạo đề mới
        if st.button("🔄 Tạo đề thi mới", type="primary") or not st.session_state.quiz_data:
            sample_df = df.sample(10)
            questions = []
            for _, row in sample_df.iterrows():
                correct = str(row['Dịch nghĩa'])
                # Lấy 3 đáp án sai ngẫu nhiên
                wrong_choices = df[df['Dịch nghĩa'] != correct].sample(3)['Dịch nghĩa'].tolist()
                options = wrong_choices + [correct]
                random.shuffle(options)
                
                questions.append({
                    "hanzi": row['Tiếng Trung'],
                    "pinyin": row['Pinyin'],
                    "options": options,
                    "answer": correct
                })
            
            st.session_state.quiz_data = questions
            st.session_state.quiz_submitted = False
            st.rerun()

        # Hiển thị bài thi
        if st.session_state.quiz_data:
            user_answers = {}
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Câu {i+1}:** Nghĩa của từ **<span style='color:red; font-size:22px;'>{q['hanzi']}</span>** ({q['pinyin']}) là gì?", unsafe_allow_html=True)
                
                # Render Radio button
                user_answers[i] = st.radio(
                    f"Đáp án câu {i+1}:", 
                    q['options'], 
                    key=f"q_{i}", 
                    disabled=st.session_state.quiz_submitted,
                    label_visibility="collapsed"
                )
                
                # Hiển thị kết quả từng câu nếu đã nộp bài
                if st.session_state.quiz_submitted:
                    if user_answers[i] == q['answer']:
                        st.success(f"✅ Chính xác! ({q['answer']})")
                    else:
                        st.error(f"❌ Sai. Đáp án đúng là: **{q['answer']}**")
                st.write("---")

            # Xử lý Nộp bài
            if not st.session_state.quiz_submitted:
                if st.button("📤 Nộp bài"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                score = sum(1 for i, q in enumerate(st.session_state.quiz_data) if user_answers[i] == q['answer'])
                st.info(f"🏆 Bạn đã đúng **{score} / 10** câu!")
