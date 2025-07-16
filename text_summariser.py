import spacy
from spacy.cli import download
import streamlit as st
import streamlit.components.v1 as components
import time
import json
from streamlit_lottie import st_lottie

# ---- Page Setup ----
st.set_page_config(page_title="📝Summariser.AI", layout="wide")

# -- app startup animation --
def load_lottiefile(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    lottie_intro = load_lottiefile("AI.json")
    splash = st.empty()
    with splash.container():
        st.markdown("<h1 style='text-align:center;'></h1>", unsafe_allow_html=True)
        st_lottie(lottie_intro, height=280, speed=1.0, loop=False)
        time.sleep(3)
    splash.empty()
    st.session_state.show_intro = False
   

# ---- Load spaCy model ----
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_model()

    
# ---- Session State Initialization ----
if "summary" not in st.session_state:
    st.session_state.summary = []
if "manual_text" not in st.session_state:
    st.session_state.manual_text = ""
 

# ---- Sidebar ----
with st.sidebar:
    st.title("🧭 Navigation")
    st.markdown("### 📌 About this app")
    st.info("""
This app uses spaCy (NATURAL LANGUAGE PROCESSING.)for smart sentence segmentation to generate quick summaries.

✨ Features:
- Generate summaries from text            
- Upload `.txt` files or paste text directly
- Adjust summary length with a slider
- Download summaries
- Responsive design with a glowing background animation
""")
    st.caption("Built with ❤️ by Ansh ")

# ---- Header Above Background ----
st.markdown("<h1 style='text-align:center;'>📝 Summariser.AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Generate summaries of text, paragraphs, news ,etc...</p>", unsafe_allow_html=True)

# ---- Background Animation ----
particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1.0
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
components.html(particles_js, height=370, scrolling=False)

# ---- Summarization Functions ----
def extract_text(file_obj):
    if file_obj:
        if file_obj.type == "text/plain":
            return file_obj.read().decode("utf-8")
    return ""

def summarize_with_spacy(text, num_sentences):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    sorted_sentences = sorted(sentences, key=lambda s: len(s), reverse=True)
    return sorted_sentences[:num_sentences]

# ---- Input Panel ----
st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
st.markdown("### ✍️ Paste your text or upload a file for summarization:")

uploaded_file = st.file_uploader("📂 Upload a text file", type=["txt"])
text = st.text_area("Or enter your content manually:", key="manual_text", height=100)

# ---- Summary Settings ----
summary_length = st.slider("🧠 Select number of summary sentences", 1, 10, 3)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Summarize"):
        full_text = extract_text(uploaded_file) or st.session_state.manual_text.strip()
        if full_text:
            st.session_state.summary = summarize_with_spacy(full_text, summary_length)
        else:
            st.warning("⚠️ Please upload a file or enter some text first.")
with col2:
    if st.button("🧹 Clear Summary"):
        st.session_state.summary = []

# ---- Output Panel ----
if st.session_state.summary:
    st.markdown("### 📄 Summary:")
    for sentence in st.session_state.summary:
        st.markdown(f"- {sentence}")

    # 🔻 Prepare summary text for download
    summary_text = "\n".join(st.session_state.summary)

    # 📝 Add download button
    st.download_button(
        label="📥 Download Summary",
        data=summary_text,
        file_name="summary.txt",
        mime="text/plain"
    )

st.markdown("</div>", unsafe_allow_html=True)
