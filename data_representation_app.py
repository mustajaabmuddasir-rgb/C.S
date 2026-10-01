"""
💾 BitLab - IGCSE / O Level Computer Science, Chapter 1: Data Representation
An interactive study website made with Streamlit.

Run it:
    pip install -r requirements.txt
    streamlit run data_representation_app.py
"""

import random

import streamlit as st

st.set_page_config(page_title="BitLab | Data Representation", page_icon="💾", layout="wide")

# ---------------------------------------------------------------------------
# STYLE
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
footer {visibility: hidden;}
.block-container { padding-top: 2rem; max-width: 1150px; }

.hero {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 45%, #ec4899 100%);
  border-radius: 24px; padding: 2.2rem 2.4rem; margin-bottom: 1.4rem;
  box-shadow: 0 12px 40px rgba(139, 92, 246, 0.35);
}
.hero h1 { color: #fff !important; font-weight: 800; font-size: 2.6rem; margin: 0 0 .3rem 0; padding: 0; }
.hero p  { color: rgba(255,255,255,.92) !important; font-size: 1.1rem; margin: 0; }
.hero .chip { display:inline-block; background: rgba(255,255,255,.2); color:#fff; padding:.25rem .8rem;
  border-radius: 999px; font-size:.8rem; margin: .8rem .4rem 0 0; font-weight:600; }

.card {
  background: rgba(139, 92, 246, 0.10); border: 1px solid rgba(139, 92, 246, 0.35);
  border-radius: 18px; padding: 1.2rem 1.3rem; height: 100%;
}
.card h3 { margin: 0 0 .4rem 0; padding: 0; font-size: 1.15rem; }
.card p  { margin: 0; opacity: .85; font-size: .95rem; }

.callout { border-radius: 14px; padding: .9rem 1.1rem; margin: .8rem 0; border-left: 6px solid; }
.callout b.t { display:block; margin-bottom: .15rem; }
.tip  { background: rgba(34,197,94,.12);  border-color: #22c55e; }
.warn { background: rgba(245,158,11,.14); border-color: #f59e0b; }
.mem  { background: rgba(99,102,241,.14); border-color: #6366f1; }
.exam { background: rgba(236,72,153,.13); border-color: #ec4899; }

.bitrow { display:flex; gap:8px; flex-wrap:wrap; margin: .6rem 0 1rem 0; }
.bitcell { text-align:center; }
.bitw { font-size:.72rem; opacity:.75; margin-bottom:4px; font-family:'JetBrains Mono',monospace; }
.bit { width:54px; height:64px; border-radius:14px; display:flex; align-items:center; justify-content:center;
  font-family:'JetBrains Mono',monospace; font-weight:700; font-size:1.7rem; }
.bit.on  { background: linear-gradient(145deg,#8b5cf6,#ec4899); color:#fff; box-shadow:0 0 18px rgba(236,72,153,.65); }
.bit.off { background: rgba(128,128,128,.18); color: rgba(128,128,128,.8); border:1px solid rgba(128,128,128,.3); }

.pgrid div.r { display:flex; gap:3px; margin-bottom:3px; }
.pgrid span { width:30px; height:30px; border-radius:6px; display:inline-block; }
.pgrid span.on  { background: linear-gradient(145deg,#8b5cf6,#ec4899); }
.pgrid span.off { background: rgba(128,128,128,.2); }

.flash {
  background: linear-gradient(135deg, rgba(99,102,241,.25), rgba(236,72,153,.2));
  border: 2px solid rgba(139,92,246,.5); border-radius: 24px; padding: 3rem 2rem;
  text-align:center; min-height: 190px; display:flex; flex-direction:column; justify-content:center;
}
.flash .big { font-size: 2rem; font-weight: 800; }
.flash .small { opacity:.7; font-size:.85rem; margin-top:.5rem; }

.qcard { background: rgba(139,92,246,.10); border:1px solid rgba(139,92,246,.35); border-radius:18px;
  padding:1.2rem 1.4rem; margin-bottom:.8rem; font-size:1.15rem; font-weight:600; }
.badge { display:inline-block; padding:.2rem .7rem; border-radius:999px; font-size:.75rem; font-weight:700;
  background: rgba(139,92,246,.25); margin-bottom:.5rem; }

div.stButton > button { border-radius: 12px; font-weight: 600; padding: .5rem 1.2rem; }
div[data-testid="stMetric"] { background: rgba(139,92,246,.10); border:1px solid rgba(139,92,246,.3);
  padding: .8rem 1rem; border-radius: 16px; }
.side-title { font-weight: 800; font-size: 1.6rem;
  background: linear-gradient(90deg,#8b5cf6,#ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def html(s: str):
    st.markdown(s, unsafe_allow_html=True)


def callout(kind: str, title: str, text: str):
    html(f'<div class="callout {kind}"><b class="t">{title}</b>{text}</div>')


def bit_row(bits: str, weights=None):
    weights = weights or [128, 64, 32, 16, 8, 4, 2, 1][-len(bits):]
    cells = "".join(
        f'<div class="bitcell"><div class="bitw">{w}</div>'
        f'<div class="bit {"on" if b == "1" else "off"}">{b}</div></div>'
        for w, b in zip(weights, bits)
    )
    html(f'<div class="bitrow">{cells}</div>')


def pixel_grid(rows):
    out = ""
    for r in rows:
        out += '<div class="r">' + "".join(f'<span class="{"on" if c == "1" else "off"}"></span>' for c in r) + "</div>"
    html(f'<div class="pgrid">{out}</div>')


def is_binary(s: str) -> bool:
    return len(s) > 0 and all(c in "01" for c in s)


def to_bin8(n: int) -> str:
    return format(n, "08b")


def human_size(bits: float) -> str:
    b = bits / 8
    return (
        f"- **Bits:** {bits:,.0f}\n- **Bytes:** {b:,.2f}\n- **Kibibytes (KiB):** {b/1024:,.2f}\n"
        f"- **Mebibytes (MiB):** {b/1024**2:,.4f}\n- **Gibibytes (GiB):** {b/1024**3:,.6f}"
    )


def rle_encode(text: str) -> str:
    if not text:
        return ""
    out, count = [], 1
    for prev, cur in zip(text, text[1:]):
        if cur == prev:
            count += 1
        else:
            out.append(f"{count}{prev}")
            count = 1
    out.append(f"{count}{text[-1]}")
    return "".join(out)


def add_xp(n: int):
    st.session_state.xp += n


for key, default in [("xp", 0), ("quiz_best", None), ("game_score", 0), ("game_streak", 0),
                     ("game_best", 0), ("game_msg", ""), ("fc_i", 0), ("fc_show", False)]:
    st.session_state.setdefault(key, default)
for i in range(8):
    st.session_state.setdefault(f"bt{i}", False)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
PAGES = [
    "🏠 Home",
    "📘 Learn 1.1 · Number systems",
    "📗 Learn 1.2 · Text, sound & images",
    "📙 Learn 1.3 · Storage & compression",
    "🧪 Number Labs",
    "🔬 Data Labs",
    "🎮 Binary Game",
    "🃏 Flashcards",
    "📝 Quiz",
    "⚡ Cheat sheet",
]
with st.sidebar:
    html('<div class="side-title">💾 BitLab</div>')
    st.caption("IGCSE & O Level CS · Chapter 1")
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()
    level = st.session_state.xp // 50 + 1
    st.markdown(f"**⭐ Level {level}** · {st.session_state.xp} XP")
    st.progress((st.session_state.xp % 50) / 50)
    st.caption("Earn XP from the quiz and the game!")


# ===========================================================================
# HOME
# ===========================================================================
if page == PAGES[0]:
    html(
        '<div class="hero"><h1>💾 BitLab</h1>'
        "<p>Master <b>Data Representation</b> the fun way: learn, play, test yourself.</p>"
        '<span class="chip">Binary</span><span class="chip">Hex</span><span class="chip">Two\'s complement</span>'
        '<span class="chip">ASCII &amp; Unicode</span><span class="chip">Sound</span><span class="chip">Images</span>'
        '<span class="chip">Compression</span></div>'
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⭐ Level", level)
    c2.metric("✨ XP", st.session_state.xp)
    c3.metric("📝 Best quiz", "-" if st.session_state.quiz_best is None else f"{st.session_state.quiz_best}%")
    c4.metric("🔥 Best streak", st.session_state.game_best)

    st.write("")
    a, b, c = st.columns(3)
    with a:
        html('<div class="card"><h3>📘 1.1 Number systems</h3><p>Binary, denary, hex, addition, overflow, shifts and two\'s complement.</p></div>')
    with b:
        html('<div class="card"><h3>📗 1.2 Text, sound &amp; images</h3><p>ASCII, Unicode, sampling and pixels. See how it all becomes 1s and 0s.</p></div>')
    with c:
        html('<div class="card"><h3>📙 1.3 Storage &amp; compression</h3><p>Units, file-size calculations, lossy vs lossless and RLE.</p></div>')

    st.write("")
    st.subheader("How to study")
    callout("mem", "1️⃣ Learn", "Read the notes pages. Each topic has its own tab.")
    callout("tip", "2️⃣ Practise", "Use the Labs to try conversions, calculations and visualisations yourself.")
    callout("warn", "3️⃣ Play", "Beat your streak in the Binary Game and revise with Flashcards.")
    callout("exam", "4️⃣ Test", "Take the Quiz and review every question you got wrong.")


# ===========================================================================
# LEARN 1.1
# ===========================================================================
elif page == PAGES[1]:
    html('<div class="hero"><h1>📘 1.1 Number systems</h1><p>The foundation of everything a computer does.</p></div>')
    t = st.tabs(["Why binary?", "3 systems", "Hex", "Addition", "Shifts", "Two's complement"])

    with t[0]:
        st.markdown(
            "- Computers contain millions of tiny **switches**, each either **ON** or **OFF**.\n"
            "- **ON = 1** and **OFF = 0**, so computers use the **binary** number system.\n"
            "- **All** data (numbers, text, sound, images) must be converted to binary before it can be processed."
        )
        bit_row("10110010")
        callout("exam", "Exam answer", "Computers are made of switches/transistors that have only two states (on/off), "
                "which can be represented by 1 and 0.")

    with t[1]:
        st.markdown(
            "| System | Base | Digits |\n|---|---|---|\n"
            "| **Denary** | 10 | 0-9 |\n| **Binary** | 2 | 0 and 1 |\n"
            "| **Hexadecimal** | 16 | 0-9 and A-F (A=10 … F=15) |"
        )
        st.subheader("Binary place values")
        bit_row("00101101")
        st.write("**00101101** = 32 + 8 + 4 + 1 = **45**")
        callout("mem", "Binary → denary", "Add up the place values wherever there is a 1.")
        callout("mem", "Denary → binary", "Subtract the biggest place value you can, write 1, repeat. Write 0 where it doesn't fit.")

    with t[2]:
        st.markdown(
            "**Hex ↔ binary:** split the binary into **nibbles** (groups of 4 bits). 1 hex digit = 4 bits."
        )
        bit_row("10101111")
        st.write("`1010` = **A**, `1111` = **F**  →  **AF**")
        st.markdown("#### Why use hexadecimal?")
        st.markdown(
            "- **Shorter** and easier to read than binary\n- **Fewer errors** when copying\n"
            "- **Easy to convert** to/from binary"
        )
        st.markdown("#### Where is it used?")
        st.markdown(
            "- HTML/CSS colour codes (e.g. `#FF0000` = red)\n- MAC addresses and IPv6 addresses\n"
            "- Memory addresses and error messages\n- ASCII/Unicode values\n- Debugging"
        )

    with t[3]:
        st.markdown(
            "| Sum | Result |\n|---|---|\n| 0 + 0 | 0 |\n| 0 + 1 | 1 |\n| 1 + 1 | 0 carry 1 |\n| 1 + 1 + 1 | 1 carry 1 |"
        )
        st.code("  10110101\n+ 01101100\n----------\n 100100001  ← 9 bits!")
        callout("warn", "Overflow error",
                "An 8-bit register holds a maximum of <b>255</b>. If the answer needs a <b>9th bit</b> it cannot "
                "be stored: that is an overflow error.")

    with t[4]:
        st.markdown(
            "Bits move left or right. **Bits pushed off the end are lost** and **0s fill the gaps**."
        )
        st.code("00110101  (53)\nLeft shift 2 →  11010100  (212)  = 53 × 4 \nRight shift 2 → 00001101  (13)   = 53 ÷ 4 (whole part)")
        st.markdown("- **Left shift n** → multiply by **2ⁿ**\n- **Right shift n** → divide by **2ⁿ**")
        callout("warn", "Watch out", "If a <b>1</b> is shifted off the end, the answer is no longer exactly × or ÷ 2ⁿ.")

    with t[5]:
        st.markdown("Used to store **positive and negative** whole numbers. The **MSB has a negative value**.")
        bit_row("11010011", [-128, 64, 32, 16, 8, 4, 2, 1])
        st.write("-128 + 64 + 16 + 2 + 1 = **-45**")
        st.markdown("**8-bit range: -128 to +127**")
        st.markdown("#### Make -45")
        st.markdown(
            "1. Positive 45 → `00101101`\n2. **Invert** → `11010010`\n3. **Add 1** → `11010011`"
        )
        callout("mem", "Quick check", "MSB = 1 → negative number. MSB = 0 → positive number.")


# ===========================================================================
# LEARN 1.2
# ===========================================================================
elif page == PAGES[2]:
    html('<div class="hero"><h1>📗 1.2 Text, sound &amp; images</h1><p>How computers store everything you see and hear.</p></div>')
    t = st.tabs(["Text", "Sound", "Images"])

    with t[0]:
        st.markdown(
            "A **character set** is a list of the characters a computer can recognise, each with a unique binary code. "
            "It lets different devices store and read text in the same way."
        )
        st.markdown(
            "| | **ASCII** | **Unicode** |\n|---|---|---|\n"
            "| Bits per character | 7 or 8 | 8, 16 or 32 |\n| Characters | 128 (256 extended) | Over 1 million possible |\n"
            "| Languages | Mainly English | Almost all languages, symbols, emojis |\n| File size | Smaller | Larger |"
        )
        callout("exam", "Why does Unicode need more bits?", "It has to represent far more characters, so each needs a longer unique code.")

    with t[1]:
        st.markdown(
            "Sound is an **analogue** wave. To store it:\n"
            "1. **Sample**: measure the amplitude at regular time intervals.\n"
            "2. Round each measurement to the nearest available value.\n"
            "3. Store each value as a **binary number**."
        )
        st.markdown(
            "- **Sampling rate:** samples per second (Hz)\n"
            "- **Sample resolution (bit depth):** bits used per sample"
        )
        st.markdown(
            "| Increase… | Quality | File size |\n|---|---|---|\n"
            "| Sampling rate | Better | Bigger |\n| Sample resolution | Better | Bigger |"
        )
        callout("tip", "Try it", "Open <b>🔬 Data Labs → Sound sampler</b> and drag the sliders to see sampling happen.")

    with t[2]:
        st.markdown(
            "A **bitmap image** is a grid of **pixels**. Each pixel is stored as a binary number for its colour."
        )
        st.markdown("- **Resolution:** the number of pixels (e.g. 1920 × 1080)\n- **Colour depth:** bits per pixel")
        st.markdown(
            "| Colour depth | Colours |\n|---|---|\n| 1 bit | 2 |\n| 8 bits | 256 |\n| 24 bits | 16.7 million |"
        )
        st.markdown(
            "| Increase… | Quality | File size |\n|---|---|---|\n"
            "| Resolution | Sharper | Bigger |\n| Colour depth | Better colours | Bigger |"
        )
        callout("mem", "Metadata", "Extra data stored in the file <i>about</i> the image: width, height, colour depth, date, camera…")
        callout("tip", "Try it", "Open <b>🔬 Data Labs → Bitmap builder</b> and draw your own 1-bit image.")


# ===========================================================================
# LEARN 1.3
# ===========================================================================
elif page == PAGES[3]:
    html('<div class="hero"><h1>📙 1.3 Storage &amp; compression</h1><p>Measuring data and making it smaller.</p></div>')
    t = st.tabs(["Units", "File sizes", "Compression", "RLE"])

    with t[0]:
        st.table({
            "Unit": ["Bit", "Nibble", "Byte", "Kibibyte (KiB)", "Mebibyte (MiB)", "Gibibyte (GiB)", "Tebibyte (TiB)", "Pebibyte (PiB)"],
            "Size": ["1 binary digit", "4 bits", "8 bits", "1024 bytes", "1024 KiB", "1024 MiB", "1024 GiB", "1024 TiB"],
        })
        callout("mem", "Remember", "Going <b>up</b> a unit: ÷ 1024. Going <b>down</b>: × 1024.")

    with t[1]:
        st.latex(r"\text{Image (bits)} = \text{width} \times \text{height} \times \text{colour depth}")
        st.latex(r"\text{Sound (bits)} = \text{sample rate} \times \text{resolution} \times \text{seconds}")
        callout("warn", "Don't forget", "Answers come out in <b>bits</b>. ÷ 8 for bytes, then ÷ 1024 for each step up.")
        st.markdown("**Example:** 100 × 100 image, 8-bit colour → 100 × 100 × 8 = 80,000 bits = 10,000 bytes ≈ 9.77 KiB")

    with t[2]:
        st.markdown("#### Why compress?")
        st.markdown("- Less storage space\n- Faster to upload/download/stream\n- Less bandwidth used")
        c1, c2 = st.columns(2)
        with c1:
            html('<div class="card"><h3>🔻 Lossy</h3><p>Permanently <b>removes</b> data. Original cannot be restored. '
                 "Much smaller files.<br><br><b>Examples:</b> JPEG, MP3, MP4<br>"
                 "<b>Methods:</b> lower resolution, colour depth, sample rate or resolution</p></div>")
        with c2:
            html('<div class="card"><h3>♻️ Lossless</h3><p><b>No data lost</b>. Original is rebuilt exactly. '
                 "Files not as small.<br><br><b>Examples:</b> PNG, FLAC, ZIP<br>"
                 "<b>Method:</b> run-length encoding (RLE)</p></div>")

    with t[3]:
        st.markdown("Replace repeated values with **a count and the value**. It is **lossless**.")
        st.code("AAAABBBCC  →  4A3B2C")
        callout("tip", "Try it", "Test your own text in <b>🔬 Data Labs → Compression</b>.")


# ===========================================================================
# NUMBER LABS
# ===========================================================================
elif page == PAGES[4]:
    html('<div class="hero"><h1>🧪 Number Labs</h1><p>Play with binary, hex and two\'s complement.</p></div>')
    t = st.tabs(["⚡ Bit flipper", "🔁 Converter", "➕ Addition", "↔️ Shifts", "➖ Two's complement"])
    W = [128, 64, 32, 16, 8, 4, 2, 1]

    # -- Bit flipper --------------------------------------------------------
    with t[0]:
        st.markdown("**Flip the switches** and watch the number change.")

        def _reset():
            for i in range(8):
                st.session_state[f"bt{i}"] = False

        def _random():
            v = random.randint(0, 255)
            for i in range(8):
                st.session_state[f"bt{i}"] = bool((v >> (7 - i)) & 1)

        cols = st.columns(8)
        for i in range(8):
            cols[i].toggle(str(W[i]), key=f"bt{i}")
        bits = "".join("1" if st.session_state[f"bt{i}"] else "0" for i in range(8))
        bit_row(bits)

        signed = st.checkbox("Show as two's complement (signed)")
        val = int(bits, 2)
        sval = val - 256 if bits[0] == "1" else val
        m1, m2, m3 = st.columns(3)
        m1.metric("Denary", sval if signed else val)
        m2.metric("Binary", bits)
        m3.metric("Hex", format(val, "02X"))
        b1, b2, _ = st.columns([1, 1, 4])
        b1.button("🎲 Random", on_click=_random)
        b2.button("🔄 Reset", on_click=_reset)

    # -- Converter ----------------------------------------------------------
    with t[1]:
        mode = st.radio("Start from:", ["Denary", "Binary", "Hexadecimal"], horizontal=True)
        value = None
        if mode == "Denary":
            value = st.number_input("Denary (0-255)", 0, 255, 45, step=1)
        elif mode == "Binary":
            txt = st.text_input("Binary (up to 8 bits)", "00101101").strip()
            if is_binary(txt) and len(txt) <= 8:
                value = int(txt, 2)
            else:
                st.error("Enter 1-8 binary digits (0 and 1 only).")
        else:
            txt = st.text_input("Hexadecimal (00-FF)", "2D").strip()
            try:
                v = int(txt, 16)
                value = v if 0 <= v <= 255 else None
                if value is None:
                    st.error("Enter a value from 00 to FF.")
            except ValueError:
                st.error("Enter valid hex digits (0-9, A-F).")
        if value is not None:
            b = to_bin8(value)
            c1, c2, c3 = st.columns(3)
            c1.metric("Denary", value)
            c2.metric("Binary", b)
            c3.metric("Hex", format(value, "02X"))
            bit_row(b)
            parts = [str(w) for w, bit in zip(W, b) if bit == "1"]
            st.write(f"Working: {' + '.join(parts) if parts else '0'} = **{value}**")
            st.write(f"Nibbles: `{b[:4]}` → **{int(b[:4], 2):X}**   `{b[4:]}` → **{int(b[4:], 2):X}**")

    # -- Addition -----------------------------------------------------------
    with t[2]:
        a = st.text_input("First number (binary)", "10110101", key="add_a").strip()
        b_ = st.text_input("Second number (binary)", "01101100", key="add_b").strip()
        if is_binary(a) and is_binary(b_) and len(a) <= 8 and len(b_) <= 8:
            a8, b8 = a.zfill(8), b_.zfill(8)
            total = int(a8, 2) + int(b8, 2)
            res = format(total, "09b")
            st.code(f"  {a8}\n+ {b8}\n----------\n {res}")
            st.write(f"Check: {int(a8, 2)} + {int(b8, 2)} = **{total}**")
            if total > 255:
                callout("warn", "⚠️ OVERFLOW ERROR", f"The answer needs 9 bits but only 8 can be stored. The stored result "
                        f"<code>{res[1:]}</code> is wrong.")
            else:
                callout("tip", "✅ No overflow", f"8-bit result: <code>{res[1:]}</code>")
        else:
            st.warning("Enter binary numbers of up to 8 bits.")

    # -- Shifts -------------------------------------------------------------
    with t[3]:
        s = st.text_input("8-bit binary number", "00110101", key="shift_in").strip()
        c1, c2 = st.columns(2)
        direction = c1.radio("Direction", ["Left", "Right"], horizontal=True)
        places = c2.slider("Places", 1, 7, 2)
        if is_binary(s) and len(s) == 8:
            if direction == "Left":
                out, lost = s[places:] + "0" * places, s[:places]
            else:
                out, lost = "0" * places + s[: 8 - places], s[8 - places:]
            st.write("**Before**")
            bit_row(s)
            st.write("**After**")
            bit_row(out)
            st.write(f"{int(s, 2)} → **{int(out, 2)}**   ·   bits lost: `{lost}`")
            if "1" in lost:
                callout("warn", "Data lost", "A 1 was shifted off the end, so this is not exactly × or ÷ 2ⁿ.")
            else:
                op = "multiplied" if direction == "Left" else "divided"
                callout("tip", "Clean shift", f"The number was {op} by 2^{places} = {2 ** places}.")
        else:
            st.warning("Enter exactly 8 binary digits.")

    # -- Two's complement ---------------------------------------------------
    with t[4]:
        m = st.radio("Convert:", ["Denary → two's complement", "Two's complement → denary"], horizontal=True)
        TW = [-128, 64, 32, 16, 8, 4, 2, 1]
        if m.startswith("Denary"):
            n = st.number_input("Denary (-128 to 127)", -128, 127, -45, step=1)
            bits = format(n & 0xFF, "08b")
            bit_row(bits, TW)
            if n < 0:
                pos = to_bin8(-n)
                inv = "".join("1" if c == "0" else "0" for c in pos)
                st.markdown(f"1. Positive {-n}: `{pos}`\n2. Invert: `{inv}`\n3. Add 1: `{bits}`")
        else:
            tx = st.text_input("8-bit two's complement", "11010011", key="tc_in").strip()
            if is_binary(tx) and len(tx) == 8:
                bit_row(tx, TW)
                total = sum(w for w, bit in zip(TW, tx) if bit == "1")
                parts = [f"({w})" if w < 0 else str(w) for w, bit in zip(TW, tx) if bit == "1"]
                st.write(f"{' + '.join(parts) if parts else '0'} = **{total}**")
            else:
                st.warning("Enter exactly 8 binary digits.")


# ===========================================================================
# DATA LABS
# ===========================================================================
elif page == PAGES[5]:
    html('<div class="hero"><h1>🔬 Data Labs</h1><p>Text, sound, images, file sizes and compression.</p></div>')
    t = st.tabs(["🔤 Text codes", "🔊 Sound sampler", "🖼️ Bitmap builder", "📏 File size", "🗜️ Compression"])

    # -- Text ---------------------------------------------------------------
    with t[0]:
        txt = st.text_input("Type something (try an emoji 😎):", "Hi!")
        if txt:
            rows = []
            for ch in txt:
                code = ord(ch)
                rows.append({
                    "Character": ch, "Denary": code, "Hex": format(code, "X"),
                    "Binary": format(code, "08b") if code < 256 else format(code, "016b"),
                    "Set": "ASCII" if code < 128 else "Unicode only",
                })
            st.dataframe(rows, width="stretch")
            if any(ord(c) > 127 for c in txt):
                callout("mem", "Unicode needed", "Some characters are outside ASCII, so they need Unicode.")

    # -- Sound --------------------------------------------------------------
    with t[1]:
        st.markdown("The **grey wave** is the analogue sound. The **pink steps** are what the computer stores.")
        c1, c2 = st.columns(2)
        n = c1.slider("Sampling rate (samples shown)", 4, 80, 16)
        bits_ = c2.slider("Sample resolution (bits)", 1, 6, 3)
        try:
            import altair as alt
            import numpy as np
            import pandas as pd

            tt = np.linspace(0, 2, 500)
            wave = pd.DataFrame({"time": tt, "amp": np.sin(2 * np.pi * tt)})
            ts = np.arange(n) / n * 2
            levels = 2 ** bits_
            idx = np.round((np.sin(2 * np.pi * ts) + 1) / 2 * (levels - 1)).astype(int)
            q = idx / (levels - 1) * 2 - 1
            samp = pd.DataFrame({"time": ts, "amp": q})
            base = alt.Chart(wave).mark_line(color="#9ca3af", strokeWidth=2).encode(
                x=alt.X("time", title="Time"), y=alt.Y("amp", title="Amplitude", scale=alt.Scale(domain=[-1.1, 1.1])))
            steps = alt.Chart(samp).mark_line(color="#ec4899", interpolate="step-after", strokeWidth=2).encode(x="time", y="amp")
            pts = alt.Chart(samp).mark_point(color="#8b5cf6", filled=True, size=70).encode(x="time", y="amp")
            st.altair_chart(base + steps + pts, width="stretch")
            st.markdown("**First samples stored in binary:**")
            st.dataframe(
                [{"Sample": i + 1, "Level": int(v), "Binary": format(int(v), f"0{bits_}b")} for i, v in enumerate(idx[:8])],
                width="stretch",
            )
        except Exception:
            st.info("Install altair/numpy/pandas to see the chart (they come with Streamlit).")
        callout("tip", "Notice", f"{2 ** bits_} possible levels with {bits_}-bit resolution. More samples and more bits → closer to the original, but a bigger file.")

    # -- Bitmap -------------------------------------------------------------
    with t[2]:
        st.markdown("Edit the **1s and 0s** to draw. 1 = pixel on, 0 = pixel off (1-bit colour depth).")
        default = "00111100\n01000010\n10100101\n10000001\n10100101\n10011001\n01000010\n00111100"
        raw = st.text_area("Bitmap (one row per line)", default, height=210)
        rows = [r.strip() for r in raw.splitlines() if r.strip()]
        if rows and all(is_binary(r) for r in rows) and len({len(r) for r in rows}) == 1 and len(rows[0]) <= 24:
            c1, c2 = st.columns([1, 1])
            with c1:
                pixel_grid(rows)
            with c2:
                w, h = len(rows[0]), len(rows)
                st.metric("Resolution", f"{w} × {h}")
                st.metric("File size (1-bit)", f"{w * h} bits = {w * h / 8:g} bytes")
                if w == 8:
                    st.markdown("**Hex per row:** " + " ".join(f"`{int(r, 2):02X}`" for r in rows))
        else:
            st.warning("Use only 0 and 1, keep every row the same length (max 24).")

    # -- File size ----------------------------------------------------------
    with t[3]:
        k1, k2 = st.tabs(["🎵 Sound", "🖼️ Image"])
        with k1:
            st.latex(r"\text{bits} = \text{rate} \times \text{resolution} \times \text{seconds}")
            c1, c2, c3 = st.columns(3)
            rate = c1.number_input("Sample rate (Hz)", 1, 200000, 44100, step=100)
            res = c2.number_input("Resolution (bits)", 1, 64, 16)
            secs = c3.number_input("Length (s)", 1, 36000, 60)
            tb = rate * res * secs
            st.write(f"{rate:,} × {res} × {secs:,} = **{tb:,} bits**")
            st.markdown(human_size(tb))
        with k2:
            st.latex(r"\text{bits} = \text{width} \times \text{height} \times \text{colour depth}")
            c1, c2, c3 = st.columns(3)
            w = c1.number_input("Width (px)", 1, 20000, 1920)
            h = c2.number_input("Height (px)", 1, 20000, 1080)
            d = c3.number_input("Colour depth (bits)", 1, 64, 24)
            tb = w * h * d
            st.write(f"{w:,} × {h:,} × {d} = **{tb:,} bits**")
            st.markdown(human_size(tb))
            st.caption(f"Colours possible: 2^{d} = {2 ** d:,}")

    # -- Compression --------------------------------------------------------
    with t[4]:
        k1, k2 = st.tabs(["Run-length encoding", "Unit converter"])
        with k1:
            txt = st.text_input("Text with repeats:", "AAAAABBBCCCCCCCD")
            enc = rle_encode(txt)
            st.write(f"Encoded: `{enc}`")
            if txt:
                st.write(f"{len(txt)} characters → **{len(enc)}** characters")
                if len(enc) >= len(txt):
                    callout("warn", "No saving", "Few repeats, so RLE didn't help.")
                else:
                    callout("tip", "Smaller!", "RLE is <b>lossless</b>: the original can be rebuilt exactly.")
        with k2:
            units = {"Bit": 1, "Nibble": 4, "Byte": 8, "Kibibyte (KiB)": 8 * 1024, "Mebibyte (MiB)": 8 * 1024 ** 2,
                     "Gibibyte (GiB)": 8 * 1024 ** 3, "Tebibyte (TiB)": 8 * 1024 ** 4}
            c1, c2, c3 = st.columns(3)
            amount = c1.number_input("Amount", 0.0, value=1.0)
            fu = c2.selectbox("From", list(units), index=4)
            tu = c3.selectbox("To", list(units), index=3)
            st.success(f"{amount:,} {fu} = **{amount * units[fu] / units[tu]:,.4f} {tu}**")


# ===========================================================================
# BINARY GAME
# ===========================================================================
elif page == PAGES[6]:
    html('<div class="hero"><h1>🎮 Binary Game</h1><p>Convert as fast as you can. Build a streak!</p></div>')

    MODES = ["Denary → Binary", "Binary → Denary", "Hex → Denary", "Denary → Hex"]

    def new_question():
        n = random.randint(1, 255)
        mode = st.session_state.get("game_mode", MODES[0])
        if mode == MODES[0]:
            q, base, ans = f"Convert **{n}** to binary", 2, n
        elif mode == MODES[1]:
            q, base, ans = f"Convert **{to_bin8(n)}** to denary", 10, n
        elif mode == MODES[2]:
            q, base, ans = f"Convert **{n:02X}** (hex) to denary", 10, n
        else:
            q, base, ans = f"Convert **{n}** to hexadecimal", 16, n
        st.session_state.game_q = {"q": q, "base": base, "n": n}

    st.selectbox("Mode", MODES, key="game_mode", on_change=new_question)
    if "game_q" not in st.session_state:
        new_question()

    gq = st.session_state.game_q
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", st.session_state.game_score)
    c2.metric("🔥 Streak", st.session_state.game_streak)
    c3.metric("🏆 Best", st.session_state.game_best)

    html(f'<div class="qcard">{gq["q"].replace("**", "")}</div>')
    with st.form("game_form", clear_on_submit=True):
        guess = st.text_input("Your answer").strip()
        go = st.form_submit_button("Check ✅")

    if go and guess:
        try:
            ok = int(guess, gq["base"]) == gq["n"]
        except ValueError:
            ok = False
        if ok:
            st.session_state.game_score += 1
            st.session_state.game_streak += 1
            st.session_state.game_best = max(st.session_state.game_best, st.session_state.game_streak)
            add_xp(5)
            st.session_state.game_msg = "✅ Correct! +5 XP"
        else:
            correct = {2: to_bin8(gq["n"]), 10: str(gq["n"]), 16: f"{gq['n']:X}"}[gq["base"]]
            st.session_state.game_streak = 0
            st.session_state.game_msg = f"❌ Not quite. The answer was **{correct}**."
        new_question()
        st.rerun()

    if st.session_state.game_msg:
        (st.success if st.session_state.game_msg.startswith("✅") else st.error)(st.session_state.game_msg)
    st.button("⏭️ Skip", on_click=new_question)
    callout("tip", "Stuck?", "Use the <b>⚡ Bit flipper</b> in Number Labs to check your working.")


# ===========================================================================
# FLASHCARDS
# ===========================================================================
elif page == PAGES[7]:
    html('<div class="hero"><h1>🃏 Flashcards</h1><p>Flip the card and test your memory.</p></div>')

    TERMS = {
        "ASCII": "A character set that uses 7 or 8 bits per character, mainly for English text.",
        "Binary": "A base-2 number system using only 0 and 1.",
        "Bit": "A single binary digit (0 or 1).",
        "Bitmap image": "An image made up of a grid of pixels.",
        "Byte": "A group of 8 bits.",
        "Character set": "A list of all the characters a computer can recognise, each with a unique binary code.",
        "Colour depth": "The number of bits used to represent the colour of each pixel.",
        "Denary": "The base-10 number system using digits 0 to 9.",
        "Hexadecimal": "A base-16 number system using 0-9 and A-F.",
        "Logical shift": "Moving bits left or right, filling gaps with 0s; bits shifted off the end are lost.",
        "Lossless compression": "Compression where no data is lost and the original can be rebuilt exactly.",
        "Lossy compression": "Compression that permanently removes data to make the file smaller.",
        "Metadata": "Data about a file (e.g. an image's width, height and colour depth).",
        "Nibble": "A group of 4 bits.",
        "Overflow": "An error when a result is too large to be stored in the available bits.",
        "Pixel": "The smallest element of a bitmap image (picture element).",
        "Resolution (image)": "The number of pixels in an image.",
        "Run-length encoding (RLE)": "A lossless method that replaces repeated data with a count and a value.",
        "Sampling rate": "The number of sound samples taken each second (Hz).",
        "Sample resolution": "The number of bits used to store each sound sample (bit depth).",
        "Two's complement": "A way to represent positive and negative binary numbers; the MSB has a negative place value.",
        "Unicode": "A character set using 8, 16 or 32 bits that can represent most of the world's languages.",
    }
    names = list(TERMS)
    st.session_state.fc_i %= len(names)

    def _flip():
        st.session_state.fc_show = not st.session_state.fc_show

    def _next():
        st.session_state.fc_i = (st.session_state.fc_i + 1) % len(names)
        st.session_state.fc_show = False

    def _prev():
        st.session_state.fc_i = (st.session_state.fc_i - 1) % len(names)
        st.session_state.fc_show = False

    def _rand():
        st.session_state.fc_i = random.randrange(len(names))
        st.session_state.fc_show = False

    term = names[st.session_state.fc_i]
    if st.session_state.fc_show:
        html(f'<div class="flash"><div class="big" style="font-size:1.3rem">{TERMS[term]}</div>'
             f'<div class="small">Answer · {term}</div></div>')
    else:
        html(f'<div class="flash"><div class="big">{term}</div><div class="small">What does this mean? Tap Flip.</div></div>')

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    c1.button("⬅️ Back", on_click=_prev, width="stretch")
    c2.button("🔄 Flip", on_click=_flip, width="stretch")
    c3.button("➡️ Next", on_click=_next, width="stretch")
    c4.button("🎲 Random", on_click=_rand, width="stretch")
    st.caption(f"Card {st.session_state.fc_i + 1} of {len(names)}")


# ===========================================================================
# QUIZ
# ===========================================================================
elif page == PAGES[8]:
    html('<div class="hero"><h1>📝 Quiz</h1><p>Check your answer after every question. +10 XP for each correct one.</p></div>')

    QUIZ = [
        ("Number systems", "Why do computers use binary?",
         ["It is easier for humans to read", "Computers use switches that are ON or OFF", "It uses fewer digits than denary", "It is faster to type"],
         1, "Computers contain switches with two states: ON (1) and OFF (0)."),
        ("Number systems", "What is the denary value of 00101101?", ["35", "45", "55", "65"], 1, "32 + 8 + 4 + 1 = 45."),
        ("Number systems", "What is binary 10101111 in hexadecimal?", ["AF", "FA", "9E", "BF"], 0, "1010 = A and 1111 = F."),
        ("Number systems", "What is the denary value of hex 2D?", ["35", "43", "45", "47"], 2, "2 × 16 + 13 = 45."),
        ("Number systems", "What is the maximum value of an unsigned 8-bit number?", ["127", "128", "255", "256"], 2, "2⁸ − 1 = 255."),
        ("Number systems", "What is 00001111 + 00000001 in binary?", ["00010000", "00001110", "00011111", "10000000"], 0, "The carries ripple all the way: 15 + 1 = 16 = 00010000."),
        ("Number systems", "Adding 11111111 and 00000001 in an 8-bit register causes…", ["A carry-in", "An overflow error", "A shift", "A rounding error"], 1, "The answer (256) needs 9 bits, so overflow occurs."),
        ("Number systems", "A left shift of 3 places (no 1s lost) does what?", ["Divides by 3", "Multiplies by 3", "Multiplies by 8", "Divides by 8"], 2, "Each left shift ×2, so 3 shifts = ×2³ = ×8."),
        ("Number systems", "What is 00110100 after a right shift of 2 places?", ["00001101", "11010000", "00011010", "00110100"], 0, "00110100 (52) → 00001101 (13), which is 52 ÷ 4."),
        ("Number systems", "What is the 8-bit two's complement range?", ["0 to 255", "-127 to 127", "-128 to 127", "-255 to 255"], 2, "The MSB is worth −128, giving −128 to +127."),
        ("Number systems", "What is 11111111 in 8-bit two's complement?", ["255", "-127", "-128", "-1"], 3, "−128 + 127 = −1."),
        ("Text, sound & images", "Which character set can represent most of the world's languages?", ["ASCII", "Unicode", "Binary", "Hexadecimal"], 1, "Unicode uses more bits per character, so it supports many more characters."),
        ("Text, sound & images", "What is sample resolution?", ["Samples per second", "Bits per sample", "Length of the sound", "Number of speakers"], 1, "Sample resolution (bit depth) is the number of bits used for each sample."),
        ("Text, sound & images", "What happens to a sound file if the sampling rate is increased?", ["Better quality, bigger file", "Worse quality, bigger file", "Better quality, smaller file", "No change"], 0, "More samples per second follow the original wave more closely but need more storage."),
        ("Text, sound & images", "How many colours can an 8-bit colour depth show?", ["8", "64", "256", "65,536"], 2, "2⁸ = 256."),
        ("Text, sound & images", "What is a pixel?", ["A unit of storage", "The smallest element of a bitmap image", "A type of compression", "A character set"], 1, "Pixel = picture element."),
        ("Storage & compression", "How many bytes are in 1 kibibyte?", ["1000", "1024", "8", "512"], 1, "1 KiB = 1024 bytes."),
        ("Storage & compression", "File size in bits of a 100 × 100 image with 8-bit colour depth?", ["800", "8,000", "80,000", "800,000"], 2, "100 × 100 × 8 = 80,000 bits."),
        ("Storage & compression", "Which type of compression permanently removes data?", ["Lossless", "Lossy", "RLE", "ZIP"], 1, "Lossy removes data for good. RLE and ZIP are lossless."),
        ("Storage & compression", "What is the RLE of AAAABBC?", ["4A2B1C", "A4B2C1", "4A2B", "AABBC"], 0, "4 As, 2 Bs, 1 C → 4A2B1C."),
    ]

    def start_quiz():
        n = st.session_state.get("qz_n", 10)
        order = random.sample(range(len(QUIZ)), n)
        st.session_state.update(qz_order=order, qz_i=0, qz_score=0, qz_checked=False, qz_done=False, qz_wrong=[], qz_run=st.session_state.get("qz_run", 0) + 1)

    def next_q():
        st.session_state.qz_i += 1
        st.session_state.qz_checked = False
        if st.session_state.qz_i >= len(st.session_state.qz_order):
            st.session_state.qz_done = True
            pct = round(100 * st.session_state.qz_score / len(st.session_state.qz_order))
            best = st.session_state.quiz_best
            st.session_state.quiz_best = pct if best is None else max(best, pct)

    def quit_quiz():
        for k in ("qz_order", "qz_i", "qz_score", "qz_checked", "qz_done", "qz_wrong"):
            st.session_state.pop(k, None)

    if "qz_order" not in st.session_state:
        st.markdown(f"**{len(QUIZ)} questions** in the bank. Choose how many you want:")
        st.select_slider("Number of questions", options=[5, 10, 15, 20], value=10, key="qz_n")
        st.button("🚀 Start quiz", on_click=start_quiz, type="primary")

    elif st.session_state.qz_done:
        total = len(st.session_state.qz_order)
        score = st.session_state.qz_score
        pct = round(100 * score / total)
        st.header(f"Score: {score} / {total} ({pct}%)")
        if pct >= 90:
            callout("tip", "🏆 Legend!", "Outstanding. You really know this chapter.")
            st.balloons()
        elif pct >= 70:
            callout("mem", "💪 Good job!", "Solid. Review the ones you missed and you'll be unstoppable.")
        elif pct >= 50:
            callout("warn", "📚 Getting there", "Revisit the notes and flashcards, then try again.")
        else:
            callout("exam", "🔁 Keep going", "Everyone starts somewhere. Read the notes, then retry.")
        if st.session_state.qz_wrong:
            st.subheader("Review your mistakes")
            for topic, q, correct, why in st.session_state.qz_wrong:
                with st.expander(f"❌ {q}"):
                    st.write(f"**Correct answer:** {correct}")
                    st.write(why)
                    st.caption(topic)
        c1, c2 = st.columns(2)
        c1.button("🔁 Try again", on_click=start_quiz, type="primary")
        c2.button("🏠 Back to menu", on_click=quit_quiz)

    else:
        order = st.session_state.qz_order
        i = st.session_state.qz_i
        topic, q, opts, correct, why = QUIZ[order[i]]
        st.progress(i / len(order), text=f"Question {i + 1} of {len(order)}  ·  Score {st.session_state.qz_score}")
        html(f'<span class="badge">{topic}</span><div class="qcard">{q}</div>')
        key = f"qz_choice_{st.session_state.qz_run}_{i}"
        choice = st.radio("Choose one:", opts, index=None, key=key, disabled=st.session_state.qz_checked, label_visibility="collapsed")

        if not st.session_state.qz_checked:
            if st.button("Check answer ✅", type="primary"):
                if choice is None:
                    st.warning("Pick an answer first!")
                else:
                    st.session_state.qz_checked = True
                    if choice == opts[correct]:
                        st.session_state.qz_score += 1
                        add_xp(10)
                    else:
                        st.session_state.qz_wrong.append((topic, q, opts[correct], why))
                    st.rerun()
        else:
            if choice == opts[correct]:
                callout("tip", "✅ Correct! +10 XP", why)
            else:
                callout("exam", f"❌ Not quite. Answer: {opts[correct]}", why)
            last = i + 1 >= len(order)
            st.button("See results 🏁" if last else "Next ➡️", on_click=next_q, type="primary")
        st.button("Quit quiz", on_click=quit_quiz)


# ===========================================================================
# CHEAT SHEET
# ===========================================================================
elif page == PAGES[9]:
    html('<div class="hero"><h1>⚡ Cheat sheet</h1><p>Everything you need to remember on one page.</p></div>')

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔢 Numbers")
        st.markdown(
            "- Denary = base **10**, binary = base **2**, hex = base **16**\n"
            "- 8-bit max = **255** (unsigned)\n- 1 hex digit = **4 bits** (nibble)\n"
            "- Left shift = **× 2ⁿ**, right shift = **÷ 2ⁿ**\n"
            "- Two's complement 8-bit: **−128 to 127**\n- Make negative: **invert + 1**\n"
            "- Overflow = result too big for the bits available"
        )
        st.subheader("📦 Units")
        st.markdown("bit → nibble (4) → byte (8) → KiB (1024 B) → MiB → GiB → TiB → PiB (×1024 each)")
    with c2:
        st.subheader("🔊 Sound & 🖼️ Images")
        st.markdown(
            "- **Sampling rate** = samples per second (Hz)\n- **Resolution** = bits per sample\n"
            "- **Sound bits** = rate × resolution × seconds\n- **Image bits** = width × height × colour depth\n"
            "- ÷ 8 = bytes, ÷ 1024 = each unit up"
        )
        st.subheader("🗜️ Compression")
        st.markdown(
            "- **Lossy** = data removed forever (JPEG, MP3)\n- **Lossless** = nothing lost (PNG, ZIP, RLE)\n"
            "- RLE: `AAAABB` → `4A2B`"
        )

    st.subheader("🎯 Exam tips")
    callout("exam", "Use the key terms", "Marks are awarded for words like <i>sampling rate</i>, <i>amplitude</i>, <i>pixel</i>, <i>colour depth</i> and <i>lossless</i>.")
    callout("exam", "'Explain' = reason", "Give a point <b>and</b> why. e.g. 'Unicode uses more bits <b>because</b> it has more characters.'")
    callout("exam", "Show your working", "In calculations you can earn method marks even if the final answer is wrong.")
    callout("exam", "Units!", "Check what unit the question wants (bits, bytes, KiB, MiB).")