import html
import requests
import streamlit as st

st.set_page_config(page_title="Talkora | Language Translator", page_icon="🌍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:#f5f7fb;color:#172033;}
.block-container {max-width:1120px;padding-top:1.7rem;padding-bottom:2.5rem;}
.hero {background:linear-gradient(120deg,#101d3a,#173d78 55%,#2563eb);border-radius:24px;padding:34px 38px;color:white;margin-bottom:24px;box-shadow:0 16px 40px rgba(23,61,120,.16);}
.brand {font-size:13px;letter-spacing:2px;text-transform:uppercase;color:#bfdbfe;font-weight:700;}
.hero h1 {color:white!important;font-size:clamp(34px,5vw,48px);line-height:1.1;margin:12px 0 8px;font-weight:800;}
.hero p {color:#dbeafe!important;font-size:16px;margin:0;}
.section-label {color:#64748b;text-transform:uppercase;font-size:11px;font-weight:800;letter-spacing:1.5px;margin-bottom:8px;}
.panel {background:white;border:1px solid #e5eaf2;border-radius:18px;padding:20px;box-shadow:0 5px 18px rgba(15,23,42,.035);}
.result-panel {background:white;border:1px solid #dbeafe;border-left:4px solid #2563eb;border-radius:16px;padding:22px;color:#172033;font-size:20px;line-height:1.65;min-height:105px;overflow-wrap:anywhere;}
div[data-testid="stTextArea"] textarea {background:white!important;color:#172033!important;border:1px solid #d9e1ed!important;border-radius:12px!important;}
div[data-baseweb="select"]>div {background:white;border-radius:11px;border-color:#d9e1ed;}
.stButton>button,.stDownloadButton>button {border-radius:11px;min-height:44px;font-weight:700;border:1px solid #dbe3ef;}
.stButton>button[kind="primary"] {background:#2563eb;border-color:#2563eb;color:white;}
.stButton>button[kind="primary"]:hover {background:#1d4ed8;border-color:#1d4ed8;}
div[data-testid="stMetric"] {background:white;border:1px solid #e7edf5;border-radius:14px;padding:12px 16px;}
.footer {text-align:center;padding:22px 8px 4px;color:#64748b;font-size:13px;}
/* Improve text visibility */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
.stMarkdown p,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #24324a !important;
}

/* Make input labels readable */
label {
    color: #24324a !important;
}

/* Improve placeholder visibility */
textarea::placeholder,
input::placeholder {
    color: #8492a6 !important;
    opacity: 1 !important;
}
/* Improve general text visibility */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
label {
    color: #24324a !important;
}

/* Restore white text in hero banner */
.hero h1,
.hero h2,
.hero p,
.hero div {
    color: #ffffff !important;
}

/* Improve placeholder visibility */
textarea::placeholder,
input::placeholder {
    color: #8492a6 !important;
    opacity: 1 !important;
}

/* Hide heading anchor icon */
.hero a {
    display: none !important;
}
</style>

""", unsafe_allow_html=True)

LANGUAGES = {
    "English":"en", "Kannada":"kn", "Hindi":"hi", "Telugu":"te",
    "Tamil":"ta", "Malayalam":"ml", "French":"fr", "German":"de",
    "Spanish":"es", "Japanese":"ja", "Arabic":"ar",
    "Chinese (Simplified)":"zh-CN", "Portuguese":"pt", "Italian":"it"
}

for key, value in {
    "history": [], "translated": "", "last_provider": "",
    "source_lang": "English", "target_lang": "Kannada"
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

def swap_languages():
    st.session_state.source_lang, st.session_state.target_lang = (
        st.session_state.target_lang, st.session_state.source_lang
    )
    st.session_state.translated = ""

def google_translate(text, source, target):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client":"gtx","sl":source,"tl":target,"dt":"t","q":text}
    response = requests.get(url, params=params, timeout=20,
                            headers={"User-Agent":"Mozilla/5.0"})
    response.raise_for_status()
    data = response.json()
    result = "".join(part[0] for part in data[0] if part and part[0])
    if not result.strip():
        raise ValueError("Translation service returned an empty result.")
    return html.unescape(result)

def mymemory_translate(text, source, target):
    url = "https://api.mymemory.translated.net/get"
    response = requests.get(url, params={"q":text,"langpair":f"{source}|{target}"}, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("responseStatus") != 200:
        raise ValueError(data.get("responseDetails","Translation failed."))
    result = data.get("responseData",{}).get("translatedText","")
    if not result.strip():
        raise ValueError("Fallback service returned an empty result.")
    return html.unescape(result)

def translate_text(text, source, target):
    errors = []
    try:
        return google_translate(text,source,target), "Google web endpoint"
    except Exception as exc:
        errors.append(str(exc))
    try:
        return mymemory_translate(text,source,target), "MyMemory fallback"
    except Exception as exc:
        errors.append(str(exc))
    raise RuntimeError("Translation services unavailable. " + " | ".join(errors))

st.markdown("""
<div class="hero">
  <div class="brand">🌐 Talkora · Language tools</div>
  <h1>Words connect the world.</h1>
  <p>Translate naturally between languages with a clean, simple workspace.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.45,1], gap="large")
with left:
    st.markdown('<div class="section-label">Translator workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    c1, cs, c2 = st.columns([5,1,5])
    with c1:
        source_language = st.selectbox("From", list(LANGUAGES.keys()), key="source_lang")
    with cs:
        st.write("")
        st.write("")
        st.button("⇄", help="Swap source and target languages",
                  on_click=swap_languages, use_container_width=True)
    with c2:
        target_language = st.selectbox("To", list(LANGUAGES.keys()), key="target_lang")
    user_text = st.text_area("Your text", placeholder="Type or paste the text you want to translate...",
                             height=190, max_chars=5000)
    st.caption(f"{len(user_text)} / 5,000 characters")
    clicked = st.button("Translate text  →", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        if not user_text.strip():
            st.warning("Enter some text before translating.")
        elif source_language == target_language:
            st.warning("Choose two different languages.")
        else:
            with st.spinner("Translating your text..."):
                try:
                    result, provider = translate_text(user_text.strip(),
                        LANGUAGES[source_language], LANGUAGES[target_language])
                    st.session_state.translated = result
                    st.session_state.last_provider = provider
                    st.session_state.history.insert(0, {
                        "source":source_language, "target":target_language,
                        "original":user_text.strip(), "translated":result
                    })
                    st.session_state.history = st.session_state.history[:10]
                    st.success("Translation complete.")
                except Exception as exc:
                    st.error(f"Could not translate this text: {exc}")

    if st.session_state.translated:
        st.markdown("#### Translation result")
        st.markdown('<div class="result-panel">'+html.escape(st.session_state.translated)+'</div>',
                    unsafe_allow_html=True)
        st.caption(f"Service: {st.session_state.last_provider}")
        st.code(st.session_state.translated, language=None)
        st.caption("Use the copy icon in the code box to copy the translation.")

with right:
    st.markdown('<div class="section-label">At a glance</div>', unsafe_allow_html=True)
    m1,m2 = st.columns(2)
    m1.metric("Languages",len(LANGUAGES))
    m2.metric("Saved in session",len(st.session_state.history))
    st.markdown("""
    <div class="panel">
      <h3 style="margin-top:0;color:#172033;">Made for clear communication</h3>
      <p style="color:#64748b;line-height:1.65;">Choose a source and target language, enter your text, and get a translated result. Your latest translations stay available in this browser session.</p>
      <hr style="border:0;border-top:1px solid #e8edf5;">
      <p style="margin-bottom:8px;color:#334155;"><b>Included features</b></p>
      <p style="color:#64748b;margin:6px 0;">↔️ Quick language swapping</p>
      <p style="color:#64748b;margin:6px 0;">🕘 Recent translation history</p>
      <p style="color:#64748b;margin:6px 0;">📋 Copy-ready translation output</p>
      <p style="color:#64748b;margin:6px 0;">🌍 14 language options</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
hc, cc = st.columns([4,1])
with hc:
    st.markdown("### Recent translations")
with cc:
    if st.session_state.history and st.button("Clear history"):
        st.session_state.history = []
        st.rerun()

if st.session_state.history:
    for item in st.session_state.history:
        with st.expander(f"{item['source']} → {item['target']} · {item['original'][:45]}"):
            st.markdown("**Original text**")
            st.write(item["original"])
            st.markdown("**Translated text**")
            st.write(item["translated"])
else:
    st.info("Your recent translations will appear here after you translate some text.")

st.markdown("""
<div class="footer">
  <b style="color:#2563eb;">🌍 Talkora</b><br>
  Breaking language barriers, connecting the world.<br>
  <span style="font-size:11px;">A language translation project</span>
</div>
""", unsafe_allow_html=True)
