"""Run: uv run streamlit run src/shining_chatbot/app.py"""

from html import escape
import random
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="SOUNDROOM · 오늘의 음악", page_icon="🎧", layout="wide")

# 샘플 큐레이션. 기분 태그는 앱의 편집 기준이며 실시간 추천이 아닙니다.
# 아트워크는 CSS로 만든 그래픽으로, 실제 앨범 커버가 아닙니다.
ALBUMS = [
    ("Nujabes", "Modal Soul", "Hip Hop", "#ad6548", "#efc3a4", "m.",
     "재즈의 온기와 느긋한 비트. 머릿속에 여백이 필요한 날에.",
     "https://music.apple.com/us/album/modal-soul/1078914477",
     [("Feather", "집중할 때"), ("Luv(sic) [pt3]", "쉬고 싶을 때")]),
    ("Frank Ocean", "Blonde", "R&B", "#596e52", "#d9e0a8", "b.",
     "조용한 방, 조금 느린 호흡. 섬세한 목소리에 귀를 기울여보세요.",
     "https://music.apple.com/us/album/blonde/1146195596",
     [("Pink + White", "쉬고 싶을 때"), ("Ivy", "감성에 잠길 때")]),
    ("Radiohead", "In Rainbows", "Rock", "#b95137", "#f4d984", "ir.",
     "겹겹이 쌓이는 기타와 목소리. 한 장에 깊이 빠지고 싶은 날.",
     "https://music.apple.com/us/album/in-rainbows/1109714933",
     [("Weird Fishes / Arpeggi", "집중할 때"), ("Nude", "감성에 잠길 때")]),
    ("Bill Evans Trio", "Waltz for Debby", "Jazz", "#496c78", "#c2e0df", "w.",
     "작은 재즈 바에 앉은 듯한 기분. 커피 한 잔과 함께 들어보세요.",
     "https://music.apple.com/ph/album/waltz-for-debby/684340223",
     [("Waltz for Debby", "집중할 때"), ("My Foolish Heart", "쉬고 싶을 때")]),
    ("Arthur Rubinstein", "Chopin: Nocturnes", "Classical", "#746683", "#e6d8ec", "n°",
     "불을 조금 낮추고, 피아노만 남겨두는 시간. 밤에 어울리는 한 장.",
     "https://music.apple.com/us/album/chopin-nocturnes/594180316",
     [("Nocturne, Op. 9 No. 2", "쉬고 싶을 때"), ("Nocturne, Op. 9 No. 1", "집중할 때")]),
    ("SHINee", "Odd", "Pop", "#368a81", "#bcefe0", "o!",
     "청량한 리듬과 다채로운 보컬. 평범한 하루에 색을 더하는 앨범.",
     "https://music.apple.com/us/album/odd-the-4th-album/994424563",
     [("View", "기분 올릴 때"), ("Love Sick", "감성에 잠길 때")]),
    ("Daft Punk", "Discovery", "Electronic", "#3f4468", "#e7bc71", "d★",
     "반짝이는 신스와 따뜻한 그루브. 익숙한 길도 새롭게 들리게.",
     "https://music.apple.com/us/album/discovery/697194953",
     [("Something About Us", "감성에 잠길 때"), ("Digital Love", "기분 올릴 때")]),
]
TRACKS = [
    {"id": f"{a}-{t}", "album_id": a, "artist": album[0], "album": album[1],
     "genre": album[2], "title": title, "mood": mood}
    for a, album in enumerate(ALBUMS)
    for t, (title, mood) in enumerate(album[8])
]

st.html("""
<style>
:root { --paper:#f6f4ee; --ink:#282c25; --muted:#72756a; --line:#e2e1d8; --orange:#c8512d; }
.stApp { background:var(--paper); color:var(--ink); }
.stApp, .stApp button, .stApp input { font-family:'Segoe UI','Malgun Gothic',sans-serif; }
[data-testid="stHeader"] { background:rgba(246,244,238,.94); }
.stMainBlockContainer { max-width:1180px; padding:2.6rem 2.5rem 2rem; }
.brandbar { display:flex; justify-content:space-between; align-items:center; padding-bottom:24px; gap:16px; }
.brand { font-size:22px; letter-spacing:-1px; font-weight:800; }
.brand span { color:var(--orange); margin-right:8px; }
.edition { font-size:10px; letter-spacing:2px; color:var(--muted); }
.library-count { border:1px solid var(--line); padding:8px 14px; border-radius:30px; font-size:12px; }
.hero { background:#eae9df; border-radius:18px; padding:46px; overflow:hidden; display:flex; align-items:center; justify-content:space-between; min-height:330px; gap:20px; }
.hero-copy { z-index:1; }
.eyebrow { font-size:10px; font-weight:700; letter-spacing:2.3px; color:var(--orange); margin-bottom:18px; }
.hero h1 { font-size:clamp(32px,4.2vw,51px); font-weight:800; line-height:1.3; letter-spacing:-2.5px; margin:0 0 18px; color:var(--ink); }
.hero h1 em { font-style:normal; color:var(--orange); }
.hero p { color:#666b60; font-size:14px; line-height:1.9; margin:0; }
.hero-foot { margin-top:27px; font-size:10px; letter-spacing:1.5px; color:#626759; }
.hero-foot span { color:var(--orange); margin-right:10px; }
.record-scene { position:relative; flex:0 0 310px; height:270px; }
.record { position:absolute; width:250px; height:250px; top:10px; right:0; border-radius:50%; background:repeating-radial-gradient(circle,#262b24 0px,#262b24 2px,#353b30 3px,#22271f 4px); box-shadow:12px 18px 26px #28302630; }
.record::after { content:''; position:absolute; inset:88px; border-radius:50%; background:radial-gradient(circle,#eae9df 0 5px,#c8512d 6px 100%); border:1px solid #ef9970; }
.sleeve { position:absolute; left:0; bottom:0; width:178px; height:212px; background:#c8512d; transform:rotate(-9deg); box-shadow:5px 10px 25px #28302626; padding:20px; color:#f9e9cd; overflow:hidden; }
.sleeve::after { content:''; position:absolute; width:170px; height:170px; border:26px solid #f5c78b; border-radius:50%; bottom:-66px; left:-31px; }
.sleeve b { font-size:39px; line-height:.95; letter-spacing:-2px; }
.sleeve small { display:block; margin-top:14px; font-size:8px; letter-spacing:2px; }
.section-head { display:flex; justify-content:space-between; align-items:end; margin:28px 0 10px; gap:16px; }
.section-head h2 { margin:0; font-size:22px; font-weight:700; letter-spacing:-.8px; }
.section-head span { color:var(--muted); font-size:12px; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border-color:var(--line) !important; border-radius:14px !important; }
[data-testid="stWidgetLabel"] p { color:#606557; font-size:12px; font-weight:600; }
[data-baseweb="select"] > div, [data-testid="stTextInput"] input { background:#fffdf8; color:var(--ink); border-color:var(--line); border-radius:9px; }
[data-testid="stTabs"] [role="tablist"] { border-bottom:1px solid var(--line); gap:26px; }
[data-testid="stTabs"] [role="tab"] { color:#77796f; padding:12px 0; }
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
.note { color:#626759; font-size:12px; line-height:1.8; min-height:44px; margin:13px 0 9px; }
.mood-tag { display:inline-block; border:1px solid var(--line); padding:4px 8px; border-radius:5px; color:#666b60; font-size:10px; }
.stButton button, .stLinkButton a, .stDownloadButton button { background:#fffdf8; color:var(--ink); border:1px solid var(--line); border-radius:8px; min-height:39px; }
.stButton button:hover, .stLinkButton a:hover { border-color:var(--orange); color:var(--orange); background:#fbeee5; }
.stButton button[kind="primary"] { background:var(--orange); border-color:var(--orange); color:white; }
.stButton button p, .stLinkButton a p, .stDownloadButton button p { font-size:12px; }
.empty-state { text-align:center; padding:48px 20px; background:#eae9df70; border:1px dashed #cccfc2; border-radius:12px; margin:22px 0; }
.empty-state b { display:block; font-size:19px; margin:10px 0; }
.empty-state p { font-size:13px; color:var(--muted); }
.footer { display:flex; justify-content:space-between; gap:15px; border-top:1px solid var(--line); margin-top:38px; padding-top:20px; color:var(--muted); font-size:10px; line-height:1.9; }
[data-testid="stCaptionContainer"] { color:var(--muted); }
@media (max-width:760px) {
 .stMainBlockContainer { padding:1.5rem 1.2rem; }
 .hero { padding:28px; min-height:0; }
 .hero h1 { font-size:35px; }
 .record-scene { flex-basis:170px; transform:scale(.7); transform-origin:right center; margin-left:-70px; }
 .edition { display:none; }
 .section-head { align-items:start; flex-direction:column; gap:5px; }
}
@media (max-width:520px) { .record-scene { display:none; } .hero h1 { font-size:32px; } .footer { flex-direction:column; } }
</style>
""")

if "saved_tracks" not in st.session_state:
    st.session_state.saved_tracks = []
if "shuffle_seed" not in st.session_state:
    st.session_state.shuffle_seed = 0


def toggle_saved(track_id):
    saved = st.session_state.saved_tracks
    if track_id in saved:
        saved.remove(track_id)
    else:
        saved.append(track_id)


def shuffle():
    st.session_state.shuffle_seed += 1


def reset_filters():
    st.session_state.genre = "전체 장르"
    st.session_state.mood = "모든 기분"
    st.session_state.search = ""


def card_html(album, title, number, mood=""):
    artist, _, genre, color, accent, mark, note, _, _ = album
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
    genre = genre_col.selectbox("좋아하는 장르", ["전체 장르"] + [a[2] for a in ALBUMS], key="genre")
    mood = mood_col.selectbox("지금의 기분", ["모든 기분", "집중할 때", "쉬고 싶을 때", "기분 올릴 때", "감성에 잠길 때"], key="mood")
    search = search_col.text_input("곡 · 아티스트 · 앨범 검색", placeholder="SHINee, Jazz, 좋아하는 곡…", key="search")

query = search.strip().casefold()
matches = [t for t in TRACKS if (genre == "전체 장르" or t["genre"] == genre)
           and (mood == "모든 기분" or t["mood"] == mood)
           and (not query or query in " ".join([t["title"], t["artist"], t["album"], t["genre"]]).casefold())]
random.Random(st.session_state.shuffle_seed).shuffle(matches)

title_col, shuffle_col = st.columns([3, 1])
title_col.markdown("### 당신을 위한 셀렉션")
shuffle_col.button("↻ 순서 섞기", on_click=shuffle, width="stretch", disabled=len(matches) < 2)
song_tab, album_tab, saved_tab = st.tabs(["곡 추천", "앨범 추천", f"내 플레이리스트 · {len(st.session_state.saved_tracks)}"])

with song_tab:
    st.html(f'<div class="result-line">취향에 맞는 <b>{len(matches)}곡</b> · 마음에 드는 곡은 하트로 담아두세요.</div>')
    if matches:
        track_grid(matches, "recommend")
    else:
        st.html('<div class="empty-state"><b>아직 맞는 곡을 찾지 못했어요.</b><p>기분이나 장르를 바꾸거나, 검색어를 조금 줄여보세요.</p></div>')
        st.button("필터 초기화", on_click=reset_filters)

with album_tab:
    album_ids = list(dict.fromkeys(t["album_id"] for t in matches))
    st.html(f'<div class="result-line">추천 곡이 담긴 <b>{len(album_ids)}장의 앨범</b> · 한 곡이 좋았다면, 앨범 전체를 만나보세요.</div>')
    for start in range(0, len(album_ids), 3):
        for number, (column, album_id) in enumerate(zip(st.columns(3), album_ids[start:start + 3]), start + 1):
            album = ALBUMS[album_id]
            with column, st.container(border=True):
                st.html(card_html(album, album[1], number))
                st.caption("추천 수록곡 · " + " / ".join(t[0] for t in album[8]))
                st.link_button("Apple Music에서 앨범 보기 ↗", album[7], width="stretch")
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
    <span>샘플 큐레이션 14곡 · 자체 제작 아트워크<br>YouTube 버튼은 검색 결과로, 앨범 버튼은 Apple Music으로 연결됩니다.</span></div>''')
