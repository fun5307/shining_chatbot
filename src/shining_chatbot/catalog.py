"""Handpicked sample albums, grouped by genre and listening mood."""

from urllib.parse import quote


MOODS = ("집중할 때", "쉬고 싶을 때", "기분 올릴 때", "감성에 잠길 때")

# Each genre has two albums for each mood; every album has exactly two tracks.
# Apple Music search links are used for new albums so regional editions can vary.
CATALOG = {
    "Hip Hop": {
        "집중할 때": [
            ("Nujabes", "Modal Soul", "Feather", "Luv(sic) [pt3]"),
            ("J Dilla", "Donuts", "Workinonit", "Time: The Donut of the Heart"),
        ],
        "쉬고 싶을 때": [
            ("A Tribe Called Quest", "Midnight Marauders", "Electric Relaxation", "Award Tour"),
            ("The Roots", "Things Fall Apart", "You Got Me", "The Next Movement"),
        ],
        "기분 올릴 때": [
            ("Kendrick Lamar", "DAMN.", "HUMBLE.", "DNA."),
            ("Tyler, The Creator", "Flower Boy", "See You Again", "Who Dat Boy"),
        ],
        "감성에 잠길 때": [
            ("Kanye West", "808s & Heartbreak", "Heartless", "Love Lockdown"),
            ("Mac Miller", "Circles", "Good News", "Blue World"),
        ],
    },
    "R&B": {
        "집중할 때": [
            ("Sade", "Love Deluxe", "No Ordinary Love", "Kiss of Life"),
            ("Daniel Caesar", "Freudian", "Get You", "Best Part"),
        ],
        "쉬고 싶을 때": [
            ("Frank Ocean", "Blonde", "Pink + White", "Ivy"),
            ("H.E.R.", "H.E.R.", "Focus", "Every Kind of Way"),
        ],
        "기분 올릴 때": [
            ("The Weeknd", "Starboy", "Starboy", "I Feel It Coming"),
            ("Beyoncé", "RENAISSANCE", "CUFF IT", "BREAK MY SOUL"),
        ],
        "감성에 잠길 때": [
            ("SZA", "Ctrl", "The Weekend", "Broken Clocks"),
            ("Giveon", "Give or Take", "Lie Again", "For Tonight"),
        ],
    },
    "Rock": {
        "집중할 때": [
            ("Radiohead", "In Rainbows", "Weird Fishes / Arpeggi", "Nude"),
            ("Pink Floyd", "The Dark Side of the Moon", "Time", "Money"),
        ],
        "쉬고 싶을 때": [
            ("Fleetwood Mac", "Rumours", "Dreams", "Go Your Own Way"),
            ("Coldplay", "Parachutes", "Yellow", "Trouble"),
        ],
        "기분 올릴 때": [
            ("Queen", "A Night at the Opera", "Bohemian Rhapsody", "You're My Best Friend"),
            ("Arctic Monkeys", "AM", "Do I Wanna Know?", "R U Mine?"),
        ],
        "감성에 잠길 때": [
            ("Nirvana", "Nevermind", "Come as You Are", "Something in the Way"),
            ("The Beatles", "Abbey Road", "Something", "Here Comes the Sun"),
        ],
    },
    "Jazz": {
        "집중할 때": [
            ("Bill Evans Trio", "Waltz for Debby", "Waltz for Debby", "My Foolish Heart"),
            ("Miles Davis", "Kind of Blue", "So What", "Freddie Freeloader"),
        ],
        "쉬고 싶을 때": [
            ("Chet Baker", "Chet Baker Sings", "My Funny Valentine", "I Fall in Love Too Easily"),
            ("John Coltrane Quartet", "Ballads", "Say It (Over and Over Again)", "You Don't Know What Love Is"),
        ],
        "기분 올릴 때": [
            ("The Dave Brubeck Quartet", "Time Out", "Take Five", "Blue Rondo à la Turk"),
            ("Ella Fitzgerald & Louis Armstrong", "Ella and Louis", "Cheek to Cheek", "They Can't Take That Away from Me"),
        ],
        "감성에 잠길 때": [
            ("Nina Simone", "I Put a Spell on You", "Feeling Good", "I Put a Spell on You"),
            ("John Coltrane", "Blue Train", "Blue Train", "Moment's Notice"),
        ],
    },
    "Classical": {
        "집중할 때": [
            ("Arthur Rubinstein", "Chopin: Nocturnes", "Nocturne, Op. 9 No. 2", "Nocturne, Op. 9 No. 1"),
            ("Glenn Gould", "Bach: Goldberg Variations (1981)", "Aria", "Variation 1"),
        ],
        "쉬고 싶을 때": [
            ("Pascal Rogé", "Debussy: Piano Works", "Clair de lune", "Arabesque No. 1"),
            ("Ludovico Einaudi", "Una Mattina", "Una Mattina", "Nuvole Bianche"),
        ],
        "기분 올릴 때": [
            ("Nigel Kennedy", "Vivaldi: The Four Seasons", "Spring: I. Allegro", "Summer: III. Presto"),
            ("Ludovico Einaudi", "Divenire", "Divenire", "Primavera"),
        ],
        "감성에 잠길 때": [
            ("Yiruma", "First Love", "River Flows in You", "May Be"),
            ("Max Richter", "The Blue Notebooks", "On the Nature of Daylight", "The Blue Notebooks"),
        ],
    },
    "Pop": {
        "집중할 때": [
            ("Taylor Swift", "folklore", "cardigan", "exile"),
            ("Lorde", "Melodrama", "Green Light", "Liability"),
        ],
        "쉬고 싶을 때": [
            ("Billie Eilish", "Happier Than Ever", "my future", "Happier Than Ever"),
            ("IU", "Palette", "Through the Night", "Palette"),
        ],
        "기분 올릴 때": [
            ("SHINee", "Odd", "View", "Love Sick"),
            ("Dua Lipa", "Future Nostalgia", "Don't Start Now", "Levitating"),
        ],
        "감성에 잠길 때": [
            ("Adele", "30", "Easy on Me", "I Drink Wine"),
            ("BTS", "BE", "Life Goes On", "Blue & Grey"),
        ],
    },
    "Electronic": {
        "집중할 때": [
            ("Tycho", "Awake", "Awake", "Montana"),
            ("Boards of Canada", "Music Has the Right to Children", "Roygbiv", "Aquarius"),
        ],
        "쉬고 싶을 때": [
            ("Moby", "Play", "Porcelain", "Natural Blues"),
            ("Air", "Moon Safari", "La femme d'argent", "All I Need"),
        ],
        "기분 올릴 때": [
            ("Justice", "Cross", "D.A.N.C.E.", "Genesis"),
            ("The Chemical Brothers", "Push the Button", "Galvanize", "Believe"),
        ],
        "감성에 잠길 때": [
            ("Daft Punk", "Discovery", "Something About Us", "Digital Love"),
            ("Porter Robinson", "Nurture", "Blossom", "Trying to Feel Alive"),
        ],
    },
}

PALETTES = {
    "Hip Hop": (("#ad6548", "#efc3a4"), ("#755e4e", "#e5c5a0")),
    "R&B": (("#596e52", "#d9e0a8"), ("#896c73", "#f0d2d3")),
    "Rock": (("#b95137", "#f4d984"), ("#53596f", "#d4d7e9")),
    "Jazz": (("#496c78", "#c2e0df"), ("#75624d", "#e7cf9f")),
    "Classical": (("#746683", "#e6d8ec"), ("#748092", "#dce7ed")),
    "Pop": (("#368a81", "#bcefe0"), ("#b27a88", "#f7d5de")),
    "Electronic": (("#3f4468", "#e7bc71"), ("#667397", "#d4daf2")),
}

NOTES = {
    "집중할 때": "흐름을 타고, 생각을 차분히 정리하고 싶은 순간에.",
    "쉬고 싶을 때": "한 박자 천천히. 음악과 함께 가볍게 쉬어가요.",
    "기분 올릴 때": "볼륨을 조금 높이고 하루의 분위기를 바꿔보세요.",
    "감성에 잠길 때": "조용한 시간에 오래 곁에 두고 싶은 멜로디.",
}

KNOWN_LINKS = {
    ("Nujabes", "Modal Soul"): "https://music.apple.com/us/album/modal-soul/1078914477",
    ("Frank Ocean", "Blonde"): "https://music.apple.com/us/album/blonde/1146195596",
    ("Radiohead", "In Rainbows"): "https://music.apple.com/us/album/in-rainbows/1109714933",
    ("Bill Evans Trio", "Waltz for Debby"): "https://music.apple.com/ph/album/waltz-for-debby/684340223",
    ("Arthur Rubinstein", "Chopin: Nocturnes"): "https://music.apple.com/us/album/chopin-nocturnes/594180316",
    ("Daft Punk", "Discovery"): "https://music.apple.com/us/album/discovery/697194953",
    ("John Coltrane Quartet", "Ballads"): "https://music.apple.com/us/album/ballads/1440747672",
    ("H.E.R.", "H.E.R."): "https://music.apple.com/us/album/h-e-r/1294890052",
}

ALBUMS = []
for genre, moods in CATALOG.items():
    for mood, records in moods.items():
        for position, (artist, title, first, second) in enumerate(records):
            color, accent = PALETTES[genre][position]
            initials = "".join(word[0] for word in title.split()[:2]).lower() + "."
            link = KNOWN_LINKS.get((artist, title))
            if link is None:
                link = "https://music.apple.com/us/search?term=" + quote(f"{artist} {title}")
            ALBUMS.append((artist, title, genre, color, accent, initials,
                           NOTES[mood], link, [(first, mood), (second, mood)], mood))
