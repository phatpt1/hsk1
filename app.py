import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import io
import hashlib
import random
import streamlit.components.v1 as components

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

# --- HÀM TẠO NỀN GIẤY SVG NÉT ĐỨT ---
def get_grid_css(grid_type, size=450):
    border = "border: 4px solid #d32f2f; border-radius: 8px;"
    svg = ""
    
    if grid_type == "Điền tự cách (田)":
        svg = f"""<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="{size/2}" x2="{size}" y2="{size/2}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /><line x1="{size/2}" y1="0" x2="{size/2}" y2="{size}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /></svg>"""
    elif grid_type == "Mễ tự cách (米)":
        svg = f"""<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="{size/2}" x2="{size}" y2="{size/2}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /><line x1="{size/2}" y1="0" x2="{size/2}" y2="{size}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /><line x1="0" y1="0" x2="{size}" y2="{size}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /><line x1="0" y1="{size}" x2="{size}" y2="0" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /></svg>"""
    elif grid_type == "Cửu cung cách (九宫)":
        s3 = size/3; s6 = size*2/3
        svg = f"""<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="{s3}" x2="{size}" y2="{s3}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8"/><line x1="0" y1="{s6}" x2="{size}" y2="{s6}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8"/><line x1="{s3}" y1="0" x2="{s3}" y2="{size}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8"/><line x1="{s6}" y1="0" x2="{s6}" y2="{size}" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8"/></svg>"""
    elif grid_type == "Hồi tự cách (回)":
        s2 = size/2; m = size/5; im = size - 2*m
        svg = f"""<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="{s2}" x2="{size}" y2="{s2}" stroke="#e0e0e0" stroke-width="2" stroke-dasharray="8,8" /><line x1="{s2}" y1="0" x2="{s2}" y2="{size}" stroke="#e0e0e0" stroke-width="2" stroke-dasharray="8,8" /><rect x="{m}" y="{m}" width="{im}" height="{im}" fill="none" stroke="#e0e0e0" stroke-width="3" stroke-dasharray="8,8" /></svg>"""
    elif grid_type == "Kẻ ngang (Line)":
        lines = "".join([f'<line x1="0" y1="{i}" x2="{size}" y2="{i}" stroke="#e0e0e0" stroke-width="2" />' for i in range(50, int(size), 50)])
        svg = f"""<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{lines}</svg>"""
        border = "border: 2px solid #ccc; border-radius: 4px;"
    elif grid_type == "Giấy trắng":
        border = "border: 2px solid #ccc; border-radius: 4px;"

    if svg:
        b64 = base64.b64encode(svg.encode('utf-8')).decode()
        bg_image = f"url('data:image/svg+xml;base64,{b64}')"
    else:
        bg_image = "none"

    return f"background-image: {bg_image}; background-color: #ffffff; {border}"

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
        st.info("Ví dụ:\n- 我 是 学生。(Tôi là học sinh.)\n- 他 是 老师。(Ông ấy là giáo viên.)")
    with tab2:
        st.info("Ví dụ:\n- 你 爱 我 吗？(Bạn có yêu tôi không?)\n- 她 是 护士 吗？(Cô ấy có phải là y tá không?)")
    with tab3:
        st.info("Ví dụ:\n- 我 不 吃 肉。(Tôi không ăn thịt.)\n- 我 没 吃饭。(Tôi chưa ăn cơm.)")
    st.divider()
    user_sentence = st.text_input("Gõ câu tiếng Trung của bạn tại đây:")
    if user_sentence: create_audio_button(user_sentence, "🔊 Nghe câu này")

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
        
        # TAB 1: HANZI WRITER (CÓ NHẬN DIỆN SỐ NÉT VÀ BỘ THỦ)
        if write_mode == "✍️ Viết theo mẫu (Chấm điểm nét)":
            col_settings, col_writer = st.columns([1, 2])
            with col_settings:
                if len(word_to_draw) > 1:
                    char_to_draw = st.radio("Chọn Hán tự:", list(word_to_draw), horizontal=True)
                else: char_to_draw = word_to_draw[0]
                
                paper_type_quiz = st.selectbox("📝 Chọn giấy (Cỡ 450px):", ["Điền tự cách (田)", "Mễ tự cách (米)", "Cửu cung cách (九宫)", "Hồi tự cách (回)", "Phương cách (方)", "Giấy trắng"], key="quiz_paper")
                css_style = get_grid_css(paper_type_quiz, size=450)

            with col_writer:
                html_code = f"""
                <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
                <style>
                    .hanzi-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
                    #char-info-box {{ margin-bottom: 15px; font-size: 18px; background: #FFF3E0; padding: 10px 20px; border-radius: 8px; border-left: 5px solid #FF9800; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    #grid-background {{ width: 450px; height: 450px; margin-bottom: 15px; {css_style} }}
                    .btn-action {{ margin: 5px; padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background-color: #f0f2f6; font-weight: bold; }}
                    #quiz-btn {{ background-color: #168F16; color: white; border: none; font-weight: bold; }}
                </style>
                <div class="hanzi-container">
                    <div id="char-info-box">⏳ Đang phân tích dữ liệu chữ...</div>
                    <div id="grid-background"></div>
                    <div><button class="btn-action" id="animate-btn">▶ Xem thứ tự nét</button><button class="btn-action" id="quiz-btn">✍️ Tự luyện (Chế độ Quiz)</button></div>
                    <h4 id="feedback" style="color: #d32f2f; margin-top: 10px; height: 20px;"></h4>
                </div>
                <script>
                    var writer = HanziWriter.create('grid-background', '{char_to_draw}', {{
                        width: 450, height: 450, padding: 20, showOutline: true, 
                        strokeAnimationSpeed: 1, delayBetweenStrokes: 100, 
                        radicalColor: '#E03C31', strokeColor: '#333333' /* Đổi màu bộ thủ thành Đỏ */
                    }});
                    
                    /* Tự động lấy số nét và báo vị trí bộ thủ */
                    writer.characterDataPromise.then(function(data) {{
                        document.getElementById('char-info-box').innerHTML = "🟢 <b>Tổng số nét:</b> " + data.strokes.length + " nét &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 🔴 <b>Bộ thủ:</b> Là phần được tô <span style='color:#E03C31; font-weight:bold;'>MÀU ĐỎ</span>";
                    }});

                    document.getElementById('animate-btn').addEventListener('click', function() {{ writer.animateCharacter(); }});
                    document.getElementById('quiz-btn').addEventListener('click', function() {{
                        document.getElementById('feedback').innerText = "Bắt đầu vẽ! Nếu vẽ sai thứ tự nét, hệ thống sẽ báo.";
                        document.getElementById('feedback').style.color = "#333";
                        writer.quiz({{
                            onMistake: function() {{ document.getElementById('feedback').innerText = "Sai nét hoặc chiều!"; document.getElementById('feedback').style.color = "red"; }},
                            onCorrectStroke: function(strokeData) {{ document.getElementById('feedback').innerText = "Nét " + strokeData.strokeNum + " chính xác!"; document.getElementById('feedback').style.color = "blue"; }},
                            onComplete: function() {{ document.getElementById('feedback').innerText = "🎉 Chúc mừng! Bạn đã viết đúng."; document.getElementById('feedback').style.color = "green"; }}
                        }});
                    }});
                </script>
                """
                components.html(html_code, height=650)

        # TAB 2: FREE DRAW (BẢNG CANVAS CÓ NÚT HOÀN TÁC)
        elif write_mode == "🖌️ Viết tự do (Bút thư pháp)":
            col_settings, col_canvas = st.columns([1, 2])
            with col_settings:
                paper_type_free = st.selectbox("📝 Chọn giấy (Cỡ 500px):", ["Điền tự cách (田)", "Mễ tự cách (米)", "Cửu cung cách (九宫)", "Hồi tự cách (回)", "Phương cách (方)", "Kẻ ngang (Line)", "Giấy trắng"], key="free_paper")
                stroke_width = st.slider("🖌️ Độ dày nét bút", min_value=1, max_value=30, value=12, step=1)
                stroke_color = st.color_picker("🎨 Màu mực", "#333333")
            
            with col_canvas:
                css_style = get_grid_css(paper_type_free, size=500)
                html_code = f"""
                <style>
                    .canvas-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
                    #draw-canvas {{
                        width: 500px; height: 500px;
                        touch-action: none; 
                        {css_style}
                    }}
                    .btn-action {{ padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background-color: #f0f2f6; font-weight: bold; }}
                    .btn-action:hover {{ background-color: #e0e0e0; }}
                </style>
                <div class="canvas-container">
                    <canvas id="draw-canvas" width="500" height="500"></canvas>
                    <div style="margin-top: 15px; display: flex; gap: 15px;">
                        <button class="btn-action" onclick="undoCanvas()">↩️ Hoàn tác</button>
                        <button class="btn-action" onclick="clearCanvas()">🗑️ Xóa toàn bộ</button>
                    </div>
                </div>
                <script>
                    const canvas = document.getElementById('draw-canvas');
                    const ctx = canvas.getContext('2d');
                    let isDrawing = false;
                    let undoStack = []; // Mảng lưu trữ các nét vẽ
                    
                    ctx.strokeStyle = '{stroke_color}';
                    ctx.lineWidth = {stroke_width};
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';

                    // Lưu trạng thái canvas vào Stack
                    function saveState() {{
                        if (undoStack.length > 30) undoStack.shift(); // Chỉ lưu 30 nét gần nhất để nhẹ RAM
                        undoStack.push(canvas.toDataURL());
                    }}

                    // Hàm Hoàn tác
                    function undoCanvas() {{
                        if (undoStack.length > 0) {{
                            let imgData = undoStack.pop();
                            let img = new Image();
                            img.src = imgData;
                            img.onload = function() {{
                                ctx.clearRect(0, 0, canvas.width, canvas.height);
                                ctx.drawImage(img, 0, 0);
                            }}
                        }} else {{
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                        }}
                    }}

                    // Hàm Xóa toàn bộ
                    function clearCanvas() {{ 
                        saveState(); 
                        ctx.clearRect(0, 0, canvas.width, canvas.height); 
                    }}

                    function getPos(evt) {{
                        const rect = canvas.getBoundingClientRect();
                        let clientX = evt.clientX;
                        let clientY = evt.clientY;
                        if (evt.touches && evt.touches.length > 0) {{
                            clientX = evt.touches[0].clientX;
                            clientY = evt.touches[0].clientY;
                        }}
                        return {{ x: clientX - rect.left, y: clientY - rect.top }};
                    }}

                    function start(e) {{
                        saveState(); // Lưu trước khi vẽ nét mới
                        isDrawing = true;
                        const pos = getPos(e);
                        ctx.beginPath(); ctx.moveTo(pos.x, pos.y); ctx.lineTo(pos.x, pos.y); ctx.stroke();
                        e.preventDefault();
                    }}
                    function draw(e) {{
                        if (!isDrawing) return;
                        const pos = getPos(e);
                        ctx.lineTo(pos.x, pos.y); ctx.stroke();
                        e.preventDefault();
                    }}
                    function stop(e) {{
                        if (isDrawing) {{ ctx.stroke(); ctx.closePath(); isDrawing = false; }}
                        e.preventDefault();
                    }}

                    canvas.addEventListener('mousedown', start); canvas.addEventListener('mousemove', draw);
                    canvas.addEventListener('mouseup', stop); canvas.addEventListener('mouseout', stop);
                    canvas.addEventListener('touchstart', start, {{passive: false}});
                    canvas.addEventListener('touchmove', draw, {{passive: false}});
                    canvas.addEventListener('touchend', stop, {{passive: false}});
                    canvas.addEventListener('touchcancel', stop, {{passive: false}});
                </script>
                """
                components.html(html_code, height=650)

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
