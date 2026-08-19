import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import io
import hashlib
import random
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# Cấu hình trang
st.set_page_config(page_title="App Học HSK 1", layout="wide")

# ================= HÀM HỖ TRỢ =================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hsk1_vocab.csv")
    except Exception:
        st.error("Lỗi: Chưa tìm thấy file hsk1_vocab.csv.")
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
        st.error("Không thể tải âm thanh.")

# --- CÁC HÀM VẼ GIẤY LUYỆN CHỮ ---
def draw_base_rect(draw, size, color='#d32f2f', width=6):
    draw.rectangle([0, 0, size-1, size-1], outline=color, width=width)

# 1. Điền tự cách (田字格)
def create_tianzige_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    draw = ImageDraw.Draw(img)
    mid = size // 2
    draw.line([(0, mid), (size, mid)], fill='#e0e0e0', width=3)
    draw.line([(mid, 0), (mid, size)], fill='#e0e0e0', width=3)
    draw_base_rect(draw, size)
    return img

# 2. Mễ tự cách (米字格)
def create_mizige_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    draw = ImageDraw.Draw(img)
    mid = size // 2
    draw.line([(0, mid), (size, mid)], fill='#e0e0e0', width=3)
    draw.line([(mid, 0), (mid, size)], fill='#e0e0e0', width=3)
    draw.line([(0, 0), (size, size)], fill='#e0e0e0', width=3)
    draw.line([(0, size), (size, 0)], fill='#e0e0e0', width=3)
    draw_base_rect(draw, size)
    return img

# 3. Cửu cung cách (九宫格)
def create_jiugongge_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    draw = ImageDraw.Draw(img)
    step = size // 3
    draw.line([(0, step), (size, step)], fill='#e0e0e0', width=3)
    draw.line([(0, step*2), (size, step*2)], fill='#e0e0e0', width=3)
    draw.line([(step, 0), (step, size)], fill='#e0e0e0', width=3)
    draw.line([(step*2, 0), (step*2, size)], fill='#e0e0e0', width=3)
    draw_base_rect(draw, size)
    return img

# 4. Hồi tự cách (回字格)
def create_huizige_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    draw = ImageDraw.Draw(img)
    margin = size // 5
    draw.line([(0, size//2), (size, size//2)], fill='#e0e0e0', width=2)
    draw.line([(size//2, 0), (size//2, size)], fill='#e0e0e0', width=2)
    draw.rectangle([margin, margin, size-margin, size-margin], outline='#e0e0e0', width=3)
    draw_base_rect(draw, size)
    return img

# 5. Phương cách (方格)
def create_fangge_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    draw = ImageDraw.Draw(img)
    draw_base_rect(draw, size)
    return img

# 6. Giấy trắng tự do
def create_blank_bg(size=350):
    img = Image.new('RGB', (size, size), color='#ffffff')
    return img

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
        st.info("Ví dụ:\n- 我 是 学生。(Tôi là học sinh.)\n- 他 是 老师。(Ông ấy là giáo viên.)")
    with tab2:
        st.subheader("Cấu trúc: Câu trần thuật + 吗 (ma) ?")
        st.info("Ví dụ:\n- 你 爱 我 吗？(Bạn có yêu tôi không?)\n- 她 是 护士 吗？(Cô ấy có phải là y tá không?)")
    with tab3:
        st.subheader("Phủ định với 不 (bù) và 没 (méi)")
        st.info("Ví dụ:\n- 我 不 吃 肉。(Tôi không ăn thịt - thói quen.)\n- 我 没 吃饭。(Tôi chưa ăn cơm - sự việc.)")

    st.divider()
    st.subheader("Luyện ghép câu & Phát âm")
    user_sentence = st.text_input("Gõ câu tiếng Trung của bạn tại đây:")
    if user_sentence:
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
        write_mode = st.radio("Chọn chế độ luyện viết:", ["✍️ Viết theo mẫu (Chấm điểm nét)", "🖌️ Viết tự do (Bút thư pháp)"], horizontal=True)
        
        if write_mode == "✍️ Viết theo mẫu (Chấm điểm nét)":
            col_settings, col_writer = st.columns([1, 2])
            
            with col_settings:
                if len(word_to_draw) > 1:
                    char_to_draw = st.radio("Chọn Hán tự:", list(word_to_draw), horizontal=True)
                else:
                    char_to_draw = word_to_draw[0]
                
                paper_type_quiz = st.selectbox("📝 Chọn loại giấy:", ["Điền tự cách (田)", "Mễ tự cách (米)", "Phương cách (方)", "Giấy trắng"], key="quiz_paper")
                
                # Render CSS tùy loại giấy
                if paper_type_quiz == "Điền tự cách (田)":
                    bg_css = "linear-gradient(to bottom, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%), linear-gradient(to right, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%)"
                elif paper_type_quiz == "Mễ tự cách (米)":
                    bg_css = "linear-gradient(to bottom, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%), linear-gradient(to right, transparent 49%, #e0e0e0 49%, #e0e0e0 51%, transparent 51%), linear-gradient(45deg, transparent 49.5%, #e0e0e0 49.5%, #e0e0e0 50.5%, transparent 50.5%), linear-gradient(-45deg, transparent 49.5%, #e0e0e0 49.5%, #e0e0e0 50.5%, transparent 50.5%)"
                elif paper_type_quiz == "Phương cách (方)":
                    bg_css = "none"
                else:
                    bg_css = "none"

            with col_writer:
                border_css = "4px solid #d32f2f" if paper_type_quiz != "Giấy trắng" else "none"
                html_code = f"""
                <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
                <style>
                    .hanzi-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
                    #grid-background {{
                        width: 300px; height: 300px; 
                        background-color: #ffffff;
                        background-image: {bg_css};
                        border: {border_css}; border-radius: 8px; margin-bottom: 15px;
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
                            onMistake: function() {{ document.getElementById('feedback').innerText = "Sai nét hoặc sai chiều!"; document.getElementById('feedback').style.color = "red"; }},
                            onCorrectStroke: function(strokeData) {{ document.getElementById('feedback').innerText = "Nét " + strokeData.strokeNum + " chính xác!"; document.getElementById('feedback').style.color = "blue"; }},
                            onComplete: function() {{ document.getElementById('feedback').innerText = "🎉 Chúc mừng! Bạn đã viết đúng."; document.getElementById('feedback').style.color = "green"; }}
                        }});
                    }});
                </script>
                """
                components.html(html_code, height=450)

        elif write_mode == "🖌️ Viết tự do (Bút thư pháp)":
            col_settings, col_canvas = st.columns([1, 2])
            with col_settings:
                paper_type_free = st.selectbox("📝 Chọn loại giấy:", [
                    "Điền tự cách (田)", 
                    "Mễ tự cách (米)", 
                    "Cửu cung cách (九宫)", 
                    "Hồi tự cách (回)", 
                    "Phương cách (方)", 
                    "Giấy trắng"
                ], key="free_paper")
                stroke_width = st.slider("🖌️ Độ dày nét bút", min_value=1, max_value=30, value=8, step=1)
                stroke_color = st.color_picker("🎨 Màu mực", "#333333")
            
            with col_canvas:
                if paper_type_free == "Điền tự cách (田)": bg_image = create_tianzige_bg(350)
                elif paper_type_free == "Mễ tự cách (米)": bg_image = create_mizige_bg(350)
                elif paper_type_free == "Cửu cung cách (九宫)": bg_image = create_jiugongge_bg(350)
                elif paper_type_free == "Hồi tự cách (回)": bg_image = create_huizige_bg(350)
                elif paper_type_free == "Phương cách (方)": bg_image = create_fangge_bg(350)
                else: bg_image = create_blank_bg(350)
                    
                st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",
                    stroke_width=stroke_width,
                    stroke_color=stroke_color,
                    background_image=bg_image,
                    height=350,
                    width=350,
                    drawing_mode="freedraw",
                    key="canvas_freedraw",
                )

# ----------------- CHỨC NĂNG 5: ĐỀ THI THỬ -----------------
elif menu == "Đề thi thử Mini":
    st.header("📝 Đề Thi Thử HSK 1")
    if not df.empty:
        if 'quiz_data' not in st.session_state: st.session_state.quiz_data = []
        if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False
            
        if st.button("🔄 Tạo đề thi mới", type="primary") or not st.session_state.quiz_data:
            sample_df = df.sample(10)
            questions = []
            for _, row in sample_df.iterrows():
                correct = str(row['Dịch nghĩa'])
                wrong_choices = df[df['Dịch nghĩa'] != correct].sample(3)['Dịch nghĩa'].tolist()
                options = wrong_choices + [correct]
                random.shuffle(options)
                questions.append({"hanzi": row['Tiếng Trung'], "pinyin": row['Pinyin'], "options": options, "answer": correct})
            st.session_state.quiz_data = questions
            st.session_state.quiz_submitted = False
            st.rerun()

        if st.session_state.quiz_data:
            user_answers = {}
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Câu {i+1}:** Nghĩa của từ **<span style='color:red; font-size:22px;'>{q['hanzi']}</span>** ({q['pinyin']}) là gì?", unsafe_allow_html=True)
                user_answers[i] = st.radio(f"Đáp án câu {i+1}:", q['options'], key=f"q_{i}", disabled=st.session_state.quiz_submitted, label_visibility="collapsed")
                if st.session_state.quiz_submitted:
                    if user_answers[i] == q['answer']: st.success(f"✅ Chính xác! ({q['answer']})")
                    else: st.error(f"❌ Sai. Đáp án đúng là: **{q['answer']}**")
                st.write("---")

            if not st.session_state.quiz_submitted:
                if st.button("📤 Nộp bài"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                score = sum(1 for i, q in enumerate(st.session_state.quiz_data) if user_answers[i] == q['answer'])
                st.info(f"🏆 Bạn đã đúng **{score} / 10** câu!")
