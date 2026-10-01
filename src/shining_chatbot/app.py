"""Run: uv run streamlit run src/shining_chatbot/app.py"""

from html import escape
import random
import re
import unicodedata
from urllib.parse import quote

import streamlit as st
from catalog import ALBUMS

st.set_page_config(page_title="SOUNDROOM · 오늘의 음악", page_icon="🎧", layout="wide")

GENRE_KEYWORDS = {
    "Hip Hop": "힙합 힙 홉",
    "R&B": "알앤비 알엔비 리듬앤블루스",
    "Rock": "록 락 록음악",
    "Jazz": "재즈",
    "Classical": "클래식 고전음악",
    "Pop": "팝 팝음악 케이팝",
    "Electronic": "일렉트로닉 전자음악 EDM",
}


def search_words(value):
    """Match case, accents and punctuation consistently in both input and catalog."""
    plain = "".join(char for char in unicodedata.normalize("NFKD", value.casefold())
                    if not unicodedata.combining(char))
    return re.findall(r"\w+", plain)


def track_matches(track, words):
    album = ALBUMS[track["album_id"]]
    fields = (track["title"], track["artist"], track["album"], track["genre"],
              track["mood"], album[6], GENRE_KEYWORDS[track["genre"]])
    haystack = " ".join(search_words(" ".join(fields)))
    return all(word in haystack for word in words)

# 샘플 큐레이션은 catalog.py에서 관리합니다. 아트워크는 자체 제작 CSS입니다.
TRACKS = [
    {"id": f"{a}-{t}", "album_id": a, "artist": album[0], "album": album[1],
     "genre": album[2], "title": title, "mood": mood}
    for a, album in enumerate(ALBUMS)
    for t, (title, mood) in enumerate(album[8])
]

st.html("""
<style>
:root {
 --paper:#f6f4ee; --ink:#282c25; --muted:#72756a; --line:#e2e1d8; --orange:#c8512d;
 --header:rgba(246,244,238,.94); --hero:#eae9df; --hero-copy:#666b60;
 --card:#fffdf8; --note:#626759; --label:#606557; --empty:#eae9df70;
 --empty-border:#cccfc2; --button-hover:#fbeee5; --record-shadow:#28302630;
}
.stApp { background:var(--paper); color:var(--ink); }
.stApp, .stApp button, .stApp input { font-family:'Segoe UI','Malgun Gothic',sans-serif; }
[data-testid="stHeader"] { background:var(--header); }
.stMainBlockContainer { max-width:1180px; padding:6rem 2.5rem 2rem; }
.brandbar { display:flex; justify-content:space-between; align-items:center; padding-bottom:24px; gap:16px; }
.brand { font-size:22px; letter-spacing:-1px; font-weight:800; }
.brand span { color:var(--orange); margin-right:8px; }
.edition { font-size:10px; letter-spacing:2px; color:var(--muted); }
.library-count { border:1px solid var(--line); padding:8px 14px; border-radius:30px; font-size:12px; }
.hero { background:var(--hero); border-radius:18px; padding:46px; overflow:hidden; display:flex; align-items:center; justify-content:space-between; min-height:330px; gap:20px; }
.hero-copy { z-index:1; }
.eyebrow { font-size:10px; font-weight:700; letter-spacing:2.3px; color:var(--orange); margin-bottom:18px; }
.hero h1 { font-size:clamp(32px,4.2vw,51px); font-weight:800; line-height:1.3; letter-spacing:-2.5px; margin:0 0 18px; color:var(--ink); }
.hero h1 em { font-style:normal; color:var(--orange); }
.hero p { color:var(--hero-copy); font-size:14px; line-height:1.9; margin:0; }
.hero-foot { margin-top:27px; font-size:10px; letter-spacing:1.5px; color:var(--note); }
.hero-foot span { color:var(--orange); margin-right:10px; }
.record-scene { position:relative; flex:0 0 310px; height:270px; }
.record { position:absolute; width:250px; height:250px; top:10px; right:0; border-radius:50%; background:repeating-radial-gradient(circle,#262b24 0px,#262b24 2px,#353b30 3px,#22271f 4px); box-shadow:12px 18px 26px var(--record-shadow); }
.record::after { content:''; position:absolute; inset:88px; border-radius:50%; background:radial-gradient(circle,var(--hero) 0 5px,var(--orange) 6px 100%); border:1px solid #ef9970; }
.sleeve { position:absolute; left:0; bottom:0; width:178px; height:212px; background:var(--orange); transform:rotate(-9deg); box-shadow:5px 10px 25px var(--record-shadow); padding:20px; color:#f9e9cd; overflow:hidden; }
.sleeve::after { content:''; position:absolute; width:170px; height:170px; border:26px solid #f5c78b; border-radius:50%; bottom:-66px; left:-31px; }
.sleeve b { font-size:39px; line-height:.95; letter-spacing:-2px; }
.sleeve small { display:block; margin-top:14px; font-size:8px; letter-spacing:2px; }
.section-head { display:flex; justify-content:space-between; align-items:end; margin:28px 0 10px; gap:16px; }
.section-head h2 { margin:0; font-size:22px; font-weight:700; letter-spacing:-.8px; }
.section-head span { color:var(--muted); font-size:12px; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border-color:var(--line) !important; border-radius:14px !important; }
[data-testid="stWidgetLabel"] p { color:var(--label); font-size:12px; font-weight:600; }
[data-baseweb="select"] > div, [data-testid="stTextInput"] input { background:var(--card); color:var(--ink); border-color:var(--line); border-radius:9px; }
[data-testid="stTabs"] [role="tablist"] { border-bottom:1px solid var(--line); gap:26px; }
[data-testid="stTabs"] [role="tab"] { color:var(--muted); padding:12px 0; }
[data-testid="stTabs"] [aria-selected="true"] { color:var(--orange); }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background:var(--orange); }
.result-line { color:var(--muted); font-size:12px; margin:22px 0 18px; }
.result-line b { color:var(--ink); }
.art { position:relative; height:160px; border-radius:10px; overflow:hidden; padding:19px; background:var(--cover); color:var(--accent); }
.art::after { content:''; position:absolute; height:220px; width:220px; border:35px solid currentColor; border-radius:50%; opacity:.32; top:30px; right:-90px; }
.art-label { font-size:9px; letter-spacing:2px; }
.art-mark { position:absolute; left:19px; bottom:5px; font-size:90px; font-weight:600; line-height:1; letter-spacing:-8px; }
.art-index { position:absolute; right:17px; top:17px; font-size:10px; border:1px solid currentColor; border-radius:20px; padding:4px 9px; }
.track-info { padding:17px 0 5px; }
.genre { color:var(--orange); font-size:9px; text-transform:uppercase; font-weight:700; letter-spacing:1.6px; }
.track-info h3 { color:var(--ink); font-size:19px; line-height:1.35; margin:7px 0 5px; letter-spacing:-.4px; padding:0; }
.artist { color:var(--muted); font-size:12px; }
.note { color:var(--note); font-size:12px; line-height:1.8; min-height:44px; margin:13px 0 9px; }
.mood-tag { display:inline-block; border:1px solid var(--line); padding:4px 8px; border-radius:5px; color:var(--hero-copy); font-size:10px; }
.stButton button, .stLinkButton a, .stDownloadButton button { background:var(--card); color:var(--ink); border:1px solid var(--line); border-radius:8px; min-height:39px; }
.stButton button:hover, .stLinkButton a:hover { border-color:var(--orange); color:var(--orange); background:var(--button-hover); }
.stButton button[kind="primary"] { background:var(--orange); border-color:var(--orange); color:white; }
.stButton button p, .stLinkButton a p, .stDownloadButton button p { font-size:12px; }
.empty-state { text-align:center; padding:48px 20px; background:var(--empty); border:1px dashed var(--empty-border); border-radius:12px; margin:22px 0; }
.empty-state b { display:block; font-size:19px; margin:10px 0; }
.empty-state p { font-size:13px; color:var(--muted); }
.footer { display:flex; justify-content:space-between; gap:15px; border-top:1px solid var(--line); margin-top:38px; padding-top:20px; color:var(--muted); font-size:10px; line-height:1.9; }
[data-testid="stCaptionContainer"] { color:var(--muted); }
@media (max-width:760px) {
 .stMainBlockContainer { padding:5.5rem 1.2rem 1.5rem; }
 .hero { padding:28px; min-height:0; }
 .hero h1 { font-size:35px; }
 .record-scene { flex-basis:170px; transform:scale(.7); transform-origin:right center; margin-left:-70px; }
 .edition { display:none; }
 .section-head { align-items:start; flex-direction:column; gap:5px; }
}
@media (max-width:520px) { .record-scene { display:none; } .hero h1 { font-size:32px; } .footer { flex-direction:column; } }
</style>
""")

# Streamlit 설정 메뉴에서 선택한 테마를 따라 자체 HTML/CSS 색상도 전환합니다.
if st.context.theme.type == "dark":
    st.html("""
    <style>
    :root {
      --paper:#141a19; --ink:#f0f0e9; --muted:#aab5ad; --line:#3b4842;
      --orange:#f2a57b; --header:rgba(20,26,25,.95); --hero:#24332f;
      --hero-copy:#c5d0c8; --card:#202a27; --note:#bfcbc1; --label:#d7ded6;
      --empty:#202c28; --empty-border:#57655b; --button-hover:#30423a;
      --record-shadow:#070b0a7a;
    }
    .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stHeader"] { background:var(--header); }
    [data-testid="stVerticalBlockBorderWrapper"] > div { background:var(--card); }
    [data-testid="stTextInput"] input::placeholder { color:var(--muted); }
    .sleeve { color:#211e1a; }
    .stButton button[kind="primary"] { color:#22241f; }
    </style>
    """)

# Streamlit의 테마 메뉴는 Python 스크립트를 즉시 다시 실행하지 않을 수 있습니다.
# 기본 테마가 그리는 body 색을 확인해 같은 화면에서 팔레트를 갱신합니다.
st.html(r"""
<style>
html[data-soundroom-theme="light"] {
 --paper:#f6f4ee; --ink:#282c25; --muted:#72756a; --line:#e2e1d8; --orange:#c8512d;
 --header:rgba(246,244,238,.94); --hero:#eae9df; --hero-copy:#666b60;
 --card:#fffdf8; --note:#626759; --label:#606557; --empty:#eae9df70;
 --empty-border:#cccfc2; --button-hover:#fbeee5; --record-shadow:#28302630;
}
html[data-soundroom-theme="dark"] {
 --paper:#141a19; --ink:#f0f0e9; --muted:#aab5ad; --line:#3b4842;
 --orange:#f2a57b; --header:rgba(20,26,25,.95); --hero:#24332f;
 --hero-copy:#c5d0c8; --card:#202a27; --note:#bfcbc1; --label:#d7ded6;
 --empty:#202c28; --empty-border:#57655b; --button-hover:#30423a;
 --record-shadow:#070b0a7a;
}
html[data-soundroom-theme="dark"] [data-testid="stVerticalBlockBorderWrapper"] > div { background:var(--card); }
html[data-soundroom-theme="light"] [data-testid="stVerticalBlockBorderWrapper"] > div { background:transparent; }
html[data-soundroom-theme="dark"] .sleeve { color:#211e1a; }
html[data-soundroom-theme="light"] .sleeve { color:#f9e9cd; }
html[data-soundroom-theme="dark"] .stButton button[kind="primary"] { color:#22241f; }
html[data-soundroom-theme="light"] .stButton button[kind="primary"] { color:white; }
</style>
<script>
(() => {
  if (window.__soundroomThemeTimer) clearInterval(window.__soundroomThemeTimer);
  const brightness = value => {
    const channels = value.match(/[\d.]+/g);
    return channels && channels.length >= 3
      ? (Number(channels[0]) * 299 + Number(channels[1]) * 587 + Number(channels[2]) * 114) / 1000
      : null;
  };
  const update = () => {
    const style = getComputedStyle(document.body);
    const background = style.backgroundColor;
    const transparent = background === 'transparent' || background.endsWith(', 0)');
    const tone = brightness(transparent ? style.color : background);
    if (tone !== null) {
      document.documentElement.dataset.soundroomTheme = transparent
        ? (tone > 145 ? 'dark' : 'light')
        : (tone < 145 ? 'dark' : 'light');
    }
  };
  update();
  window.__soundroomThemeTimer = setInterval(update, 500);
})();
</script>
""", unsafe_allow_javascript=True)

if "saved_tracks" not in st.session_state:
    st.session_state.saved_tracks = []
if "shuffle_seed" not in st.session_state:
    st.session_state.shuffle_seed = 0
if "visible_tracks" not in st.session_state:
    st.session_state.visible_tracks = 12
if "visible_albums" not in st.session_state:
    st.session_state.visible_albums = 12


def toggle_saved(track_id):
    saved = st.session_state.saved_tracks
    if track_id in saved:
        saved.remove(track_id)
    else:
        saved.append(track_id)


def shuffle():
    st.session_state.shuffle_seed += 1


def show_more(kind):
    st.session_state[kind] += 12


def reset_filters():
    st.session_state.genre = "전체 장르"
    st.session_state.mood = "모든 기분"
    st.session_state.search = ""


def card_html(album, title, number, mood=""):
    artist, _, genre, color, accent, mark, note, _, _ = album[:9]
    return f"""<div class="art" aria-hidden="true" style="--cover:{color};--accent:{accent}">
        <div class="art-label">SOUNDROOM / {escape(genre)}</div><div class="art-mark">{escape(mark)}</div>
        <span class="art-index">{number:02d}</span></div><div class="track-info">
        <span class="genre">{escape(genre)}</span><h3>{escape(title)}</h3>
        <div class="artist">{escape(artist)}</div><p class="note">{escape(note)}</p>
        {f'<span class="mood-tag">{escape(mood)}</span>' if mood else ''}</div>"""


def track_grid(tracks, context):
    for start in range(0, len(tracks), 3):
        for number, (column, track) in enumerate(zip(st.columns(3), tracks[start:start + 3]), start + 1):
            with column, st.container(border=True):
                st.html(card_html(ALBUMS[track["album_id"]], track["title"], number, track["mood"]))
                listen, save = st.columns([1.15, 1])
                listen.link_button("YouTube ↗", "https://www.youtube.com/results?search_query="
                                   + quote(f"{track['artist']} {track['title']}"), width="stretch")
                saved = track["id"] in st.session_state.saved_tracks
                save.button("♥ 저장됨" if saved else "♡ 저장", key=f"{context}-{track['id']}",
                            on_click=toggle_saved, args=(track["id"],), width="stretch",
                            type="primary" if saved else "secondary",
                            help="저장 해제" if saved else "내 플레이리스트에 저장")


st.html(f"""<div class="brandbar"><div class="brand"><span>◉</span>SOUNDROOM</div>
    <div class="edition">A LITTLE MUSIC, A BETTER DAY.</div>
    <div class="library-count">내 플레이리스트 · {len(st.session_state.saved_tracks):02d}</div></div>
    <section class="hero"><div class="hero-copy"><div class="eyebrow">YOUR DAILY SOUNDTRACK</div>
    <h1>오늘의 기분에,<br><em>음악 한 스푼.</em></h1>
    <p>어떤 하루를 보내고 있나요?<br>지금의 당신에게 어울리는 사운드를 찾아보세요.</p>
    <div class="hero-foot"><span>▂ ▅ ▇ ▅ ▂</span> HANDPICKED SOUNDS / VOL. 01</div></div>
    <div class="record-scene" aria-hidden="true"><div class="record"></div>
    <div class="sleeve"><b>GOOD<br>MOOD.</b><small>SOUNDROOM SELECTS / VOL. 01</small></div></div></section>
    <div class="section-head"><h2>어떤 음악이 당기세요?</h2><span>장르와 기분을 고르면, 취향에 가까워져요.</span></div>""")

with st.container(border=True):
    genre_col, mood_col, search_col = st.columns([1, 1, 1.5])
    genre = genre_col.selectbox("좋아하는 장르", ["전체 장르"] + list(dict.fromkeys(a[2] for a in ALBUMS)), key="genre")
    mood = mood_col.selectbox("지금의 기분", ["모든 기분", "집중할 때", "쉬고 싶을 때", "기분 올릴 때", "감성에 잠길 때"], key="mood")
    search = search_col.text_input("곡 · 아티스트 · 앨범 검색", placeholder="SHINee, 재즈, 쉬고 싶을 때…", key="search")

query = search_words(search)
matches = [t for t in TRACKS if (genre == "전체 장르" or t["genre"] == genre)
           and (mood == "모든 기분" or t["mood"] == mood)
           and track_matches(t, query)]
random.Random(st.session_state.shuffle_seed).shuffle(matches)

title_col, shuffle_col = st.columns([3, 1])
title_col.markdown("### 당신을 위한 셀렉션")
shuffle_col.button("↻ 순서 섞기", on_click=shuffle, width="stretch", disabled=len(matches) < 2)
song_tab, album_tab, saved_tab = st.tabs(["곡 추천", "앨범 추천", f"내 플레이리스트 · {len(st.session_state.saved_tracks)}"])

with song_tab:
    search_label = f'“{escape(search.strip())}” 검색 결과 · ' if query else ''
    st.html(f'<div class="result-line">{search_label}취향에 맞는 <b>{len(matches)}곡</b> · 마음에 드는 곡은 하트로 담아두세요.</div>')
    if matches:
        track_grid(matches[:st.session_state.visible_tracks], "recommend")
        if len(matches) > st.session_state.visible_tracks:
            st.button("곡 더 보기 ↓", on_click=show_more, args=("visible_tracks",))
    else:
        st.html('<div class="empty-state"><b>아직 맞는 곡을 찾지 못했어요.</b><p>기분이나 장르를 바꾸거나, 검색어를 조금 줄여보세요.</p></div>')
        st.button("필터 초기화", on_click=reset_filters)

with album_tab:
    album_ids = list(dict.fromkeys(t["album_id"] for t in matches))
    st.html(f'<div class="result-line">추천 곡이 담긴 <b>{len(album_ids)}장의 앨범</b> · 한 곡이 좋았다면, 앨범 전체를 만나보세요.</div>')
    visible_album_ids = album_ids[:st.session_state.visible_albums]
    for start in range(0, len(visible_album_ids), 3):
        for number, (column, album_id) in enumerate(zip(st.columns(3), visible_album_ids[start:start + 3]), start + 1):
            album = ALBUMS[album_id]
            with column, st.container(border=True):
                st.html(card_html(album, album[1], number))
                st.caption("추천 수록곡 · " + " / ".join(t[0] for t in album[8]))
                st.link_button("Apple Music에서 앨범 보기 ↗", album[7], width="stretch")
    if len(album_ids) > st.session_state.visible_albums:
        st.button("앨범 더 보기 ↓", on_click=show_more, args=("visible_albums",))
    if not album_ids:
        st.info("현재 조건에 맞는 앨범이 없어요. 곡 추천 탭에서 필터를 초기화해보세요.")

with saved_tab:
    tracks_by_id = {t["id"]: t for t in TRACKS}
    saved_tracks = [tracks_by_id[tid] for tid in st.session_state.saved_tracks if tid in tracks_by_id]
    if saved_tracks:
        st.html('<div class="result-line">당신이 고른 사운드. <b>나만의 플레이리스트</b>가 만들어지고 있어요.</div>')
        st.download_button("↓ 플레이리스트 내려받기", "SOUNDROOM · 내 플레이리스트\n\n" + "\n".join(
            f"{i}. {t['artist']} — {t['title']} ({t['album']})" for i, t in enumerate(saved_tracks, 1)),
            file_name="soundroom-playlist.txt", mime="text/plain; charset=utf-8")
        track_grid(saved_tracks, "saved")
    else:
        st.html('<div class="empty-state"><b>취향을 담아둘 작은 공간.</b><p>곡 추천에서 마음에 드는 곡의 ‘♡ 저장’을 눌러보세요.</p></div>')
    st.caption("저장한 곡은 현재 접속 세션 동안 유지됩니다. 오래 간직하려면 플레이리스트를 내려받으세요.")

st.html('''<div class="footer"><span><b>SOUNDROOM</b> &nbsp; 음악으로 채우는 작은 여유.</span>
    <span>샘플 큐레이션 56장 · 112곡 · 자체 제작 아트워크<br>YouTube 버튼은 검색 결과로, 앨범 버튼은 Apple Music으로 연결됩니다.</span></div>''')
