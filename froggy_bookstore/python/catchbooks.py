import json
import random
import re
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import requests
from tqdm import tqdm


SEARCH_URL = "https://openlibrary.org/search.json"
WORK_URL = "https://openlibrary.org{work_key}.json"

OUTPUT_JSON = Path(__file__).with_name("books.json")
READER_JSON = Path(__file__).with_name("reader.json")

TARGET_COUNT = 200
SEARCH_LIMIT = 100
REQUEST_DELAY = 0.25
RANDOM_SEED = 42
LATEST_LISTED_AT = "2026-04-26"
LATEST_COUNT = 12
DISCOUNTED_COUNT = 90
SPECIAL_OFFER_COUNT = 10

HEADERS = {"User-Agent": "bookstore-web-design-data-loader/1.0"}

CATEGORY_SEARCHES = {
    "C001": ["小說", "文學", "散文", "詩", "fiction", "literature", "novel"],
    "C002": ["商業", "管理", "投資", "經濟", "business", "management", "finance"],
    "C003": ["藝術", "設計", "建築", "攝影", "art", "design", "architecture"],
    "C004": ["歷史", "哲學", "社會", "文化", "history", "philosophy", "culture"],
    "C005": ["心理", "勵志", "人生", "成長", "psychology", "self help", "motivation"],
    "C006": ["宗教", "佛教", "道教", "命理", "religion", "buddhism", "spirituality"],
    "C007": ["科學", "自然", "數學", "物理", "science", "nature", "mathematics"],
    "C008": ["醫療", "健康", "養生", "營養", "health", "medicine", "nutrition"],
    "C009": ["飲食", "料理", "食譜", "茶", "cooking", "food", "recipe"],
    "C010": ["生活", "居家", "手作", "時尚", "lifestyle", "home", "fashion"],
    "C011": ["旅遊", "旅行", "地理", "遊記", "travel", "geography", "journey"],
    "C012": ["童書", "兒童", "青少年", "繪本", "children", "juvenile", "picture book"],
    "C013": ["國小", "國中", "參考書", "教材", "textbook", "school", "learning"],
    "C014": ["親子", "教養", "家庭", "教育", "parenting", "family", "education"],
    "C015": ["電影", "音樂", "影視", "明星", "film", "music", "television"],
    "C016": ["輕小說", "奇幻", "武俠", "科幻", "fantasy", "science fiction", "novel"],
    "C017": ["漫畫", "圖文", "繪本", "動漫", "comic", "manga", "graphic novel"],
    "C018": ["語言", "英語", "日語", "中文", "language", "english", "japanese"],
    "C019": ["考試", "證照", "公職", "測驗", "exam", "test", "certification"],
    "C020": ["電腦", "程式", "資訊", "網路", "computer", "programming", "software"],
    "C021": ["法律", "工程", "專業", "政府", "law", "engineering", "reference"],
}

CATEGORY_NAMES = {
    "C001": "文學小說",
    "C002": "商業理財",
    "C003": "藝術設計",
    "C004": "人文社科",
    "C005": "心理勵志",
    "C006": "宗教命理",
    "C007": "自然科普",
    "C008": "醫療保健",
    "C009": "飲食",
    "C010": "生活風格",
    "C011": "旅遊",
    "C012": "童書/青少年文學",
    "C013": "國中小參考書",
    "C014": "親子教養",
    "C015": "影視偶像",
    "C016": "輕小說",
    "C017": "漫畫/圖文書",
    "C018": "語言學習",
    "C019": "考試用書",
    "C020": "電腦資訊",
    "C021": "專業/教科書/政府出版品",
}

TITLE_CATEGORY_OVERRIDES = {
    "Foundation": "C016",
    "Dracula": "C016",
    "The Last Man": "C016",
    "Dune": "C016",
    "Divergent": "C016",
    "Eclipse": "C016",
    "The Hitch Hiker's Guide to the Galaxy": "C016",
    "The Time Machine": "C016",
    "The Lost World": "C016",
    "The Castle of Otranto": "C016",
    "Vingt mille lieues sous les mers": "C016",
    "The Giver": "C016",
    "Twilight": "C016",
    "The Handmaid's Tale": "C016",
    "A Princess of Mars": "C016",
    "Les Robots": "C016",
    "The Island of Dr. Moreau": "C016",
    "Naruto": "C017",
    "Naruto 5": "C017",
    "Rich Dad, Poor Dad": "C002",
    "Stock Investing for Dummies": "C002",
    "The Richest Man in Babylon": "C002",
    "The Law of Success": "C002",
    "Management information systems": "C020",
    "Managerial Accounting": "C021",
    "Guess How Much I Love You": "C014",
    "Prince Caspian": "C012",
    "Heidi": "C012",
    "Matilda": "C012",
    "Peter Pan": "C012",
    "Artemis Fowl": "C012",
    "Treasure Island": "C012",
    "The Art of War": "C004",
    "A Study of History": "C004",
    "History": "C004",
    "Walden": "C004",
    "Poetics": "C003",
    "Marc Chagall": "C003",
    "Paul Klee": "C003",
    "The Book of Tea": "C010",
    "Boston Cooking-School cook book": "C009",
    "On Cooking": "C009",
    "Joy of Cooking": "C009",
    "A Brief History of Time": "C007",
    "Biology": "C013",
    "Chemistry": "C013",
    "Questions and Answers Exam Oriented Anatomy": "C019",
    "Principles of Anatomy and Physiology": "C021",
    "Educational psychology": "C005",
    "Die Traumdeutung": "C005",
    "The Power of Your Subconscious Mind": "C005",
    "Atomic Habits": "C005",
    "Fit & well": "C008",
    "A dictionary of the English language": "C018",
    "The Elements of Style": "C018",
    "Le fantôme de l'opéra": "C015",
}

CJK_CATEGORY_KEYWORDS = {
    "C006": ["羌佛", "心經", "經藏", "說法", "般若"],
    "C007": ["地質", "自然"],
    "C004": ["歷史", "历史", "奏摺", "中山陵"],
    "C016": ["喪屍", "生還者"],
    "C001": ["小說", "時光", "時代", "故事", "錯誤"],
}

CATEGORY_KEYWORDS = [
    ("C017", ["manga", "comic", "graphic novel"]),
    ("C009", ["cookbook", "cooking", "recipe", "joy of cooking"]),
    ("C020", ["computer", "software", "programming", "processor", "information systems"]),
    ("C019", ["exam oriented", "certification", "questions and answers"]),
    ("C008", ["health", "medicine", "medical", "anatomy", "physiology", "nutrition"]),
    ("C002", ["business", "accounting", "finance", "financial", "investing", "wealth"]),
    ("C006", ["buddh", "religion", "christian", "spirituality"]),
    ("C007", ["biology", "chemistry", "physics", "electricity", "magnetism", "darwin"]),
    ("C018", ["dictionary", "english language", "vocabulary", "grammar"]),
    ("C012", ["children", "juvenile", "picture book", "heidi", "matilda"]),
    ("C016", ["fantasy", "science fiction", "dystopian", "vampire", "zombie"]),
    ("C011", ["travel", "travels", "journey"]),
    ("C003", ["architecture", "design", "aesthetic"]),
    ("C005", ["psychology", "subconscious", "habit", "motivation", "self help"]),
    ("C004", ["history", "historical", "philosophy", "politics", "government", "memoir"]),
    ("C015", ["film", "movie", "television", "music", "cinema"]),
    ("C014", ["parenting", "family education"]),
    ("C021", ["textbook", "manual", "reference", "engineering", "professional"]),
]

LANGUAGE_NAMES = {
    "chi": "中文",
    "cmn": "中文",
    "zho": "中文",
    "eng": "英文",
    "jpn": "日文",
    "jpn": "日文",
    "kor": "韓文",
    "fre": "法文",
    "ger": "德文",
    "spa": "西班牙文",
    "ita": "義大利文",
    "por": "葡萄牙文",
    "rus": "俄文",
    "mul": "多語言",
}

BOOK_SIZE_OPTIONS = [
    (188, 128),
    (190, 130),
    (200, 140),
    (203, 127),
    (210, 140),
    (210, 148),
    (210, 150),
    (215, 150),
    (230, 170),
    (257, 182),
    (260, 185),
    (297, 210),
]

ZH_INTRO_BY_CATEGORY = {
    "C001": "本書以人物與情節推進閱讀節奏，適合喜歡故事感與文字氛圍的讀者。內容在細節中鋪陳情緒與轉折，讀來有餘韻，也適合在安靜時慢慢翻閱。",
    "C002": "本書聚焦商業思考與實務觀念，適合想建立財務、管理或決策基礎的讀者。章節安排清楚，閱讀負擔不重，可作為入門參考。",
    "C003": "本書從藝術、設計或視覺文化切入，適合對創作與美感養成有興趣的讀者。內容保留欣賞空間，也帶出觀察方法與日常細節。",
    "C004": "本書關注歷史、思想與社會文化脈絡，適合想拓展理解角度的讀者。內容以清楚材料與觀點引導閱讀，讓人能在時代與現實之間建立連結。",
}

EN_INTRO_BY_CATEGORY = {
    "C001": "This book offers a readable literary experience with a clear sense of story, atmosphere, or character. It leaves room for thought after the final page.",
    "C002": "This book introduces practical ideas around business, money, management, or decision-making without an overly technical presentation.",
    "C020": "This book introduces computing, programming, software, or digital tools. It is useful before moving into more hands-on practice.",
}

ZH_REVIEW_TEXTS = [
    "讀完很有收穫，內容清楚，適合慢慢品味。",
    "節奏順暢，觀點實用，會想推薦給朋友。",
    "文字容易進入，讀後留下不少思考空間。",
    "內容比預期扎實，適合放在書架常翻。",
    "主題明確，讀起來舒服，也有啟發。",
    "雖然有些段落較慢，但整體很值得閱讀。",
]

EN_REVIEW_TEXTS = [
    "Clear, engaging, and rewarding. I enjoyed the ideas and would recommend it to curious readers.",
    "A thoughtful read with a steady pace. Some parts stayed with me after finishing.",
    "Well written and easy to follow. It offers useful insight without feeling heavy.",
    "A strong book for quiet reading. The subject is handled with care and clarity.",
    "Interesting from start to finish, with enough depth to invite a second look.",
    "Not perfect, but memorable. The best chapters make the whole book worthwhile.",
]

READER_NAMES = [
    "林雨柔",
    "陳柏翰",
    "張雅婷",
    "王志明",
    "李佩珊",
    "黃子軒",
    "吳佳穎",
    "劉冠宇",
    "蔡宜庭",
    "楊承恩",
    "許家豪",
    "鄭心怡",
    "謝孟哲",
    "郭怡君",
    "曾柏宇",
    "洪詩涵",
    "邱建宏",
    "廖婉如",
    "賴俊傑",
    "徐千惠",
    "Amanda Chen",
    "Michael Lin",
    "Emily Wang",
    "Jason Liu",
    "Sophia Huang",
    "Daniel Wu",
    "Olivia Chang",
    "Kevin Tsai",
    "Grace Lee",
    "Ryan Yang",
    "Alice Morgan",
    "David Miller",
    "Emma Wilson",
    "Noah Taylor",
    "Lily Brown",
    "Jack Anderson",
    "Ava Thompson",
    "Leo Martin",
    "Maya Scott",
    "Owen Clark",
    "Claire Evans",
    "Ben Walker",
    "Ruby Harris",
    "James Turner",
    "Ella Cooper",
    "Sam Bennett",
    "Hannah Reed",
    "Alex Carter",
    "Nina Brooks",
    "Luke Foster",
    "Sophie Green",
    "Mark Hill",
    "Julia Price",
    "Adam Ward",
    "Eva Bell",
    "Peter Collins",
    "Laura Gray",
    "Tom Murphy",
    "Sarah Kelly",
    "Chris Bailey",
    "Anna Stone",
    "Brian Cook",
    "Diana Ross",
    "Eric Wood",
    "Fiona Young",
    "George King",
    "Helen Wright",
    "Ian Parker",
    "Jane Fox",
    "Kyle Moore",
    "Rachel Adams",
    "Victor Hall",
    "Irene Lewis",
    "Oscar Allen",
    "Paula James",
    "Neil Watson",
    "Tina Rogers",
    "Bruce Perry",
    "Wendy Cox",
    "Frank Howard",
]


def response_url(url: str, params: dict[str, Any] | None) -> str:
    return requests.Request("GET", url, params=params).prepare().url or url


def get_json(url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"[ERROR] {response_url(url, params)}\n{exc}")
        return None


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value if item)
    return re.sub(r"\s+", " ", str(value)).strip()


def has_cjk(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


def has_latin(value: str) -> bool:
    return any("a" <= char.lower() <= "z" for char in value)


def is_readable_text(value: str) -> bool:
    if not value or "\ufffd" in value:
        return False
    question_marks = value.count("?")
    return question_marks < 2 and question_marks / max(len(value), 1) < 0.1


def category_text(book: dict[str, Any]) -> str:
    text = " ".join(
        clean_text(book.get(field))
        for field in ("title", "author", "publisher", "introduction")
        if book.get(field)
    ).lower()
    return re.sub(r"belongs to the .*? shelf\.?", "", text)


def has_keyword(text: str, keyword: str) -> bool:
    escaped = re.escape(keyword.lower())
    return re.search(rf"(^|[^a-z0-9]){escaped}([^a-z0-9]|$)", text) is not None


def infer_category_id(book: dict[str, Any], default_category_id: str) -> str:
    title = clean_text(book.get("title"))
    if title in TITLE_CATEGORY_OVERRIDES:
        return TITLE_CATEGORY_OVERRIDES[title]

    for category_id, keywords in CJK_CATEGORY_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            return category_id

    text = category_text(book)
    for category_id, keywords in CATEGORY_KEYWORDS:
        if any(has_keyword(text, keyword) for keyword in keywords):
            return category_id

    if default_category_id == "C006":
        return "C006"
    return "C001"


def is_good_title(title: str) -> bool:
    rejected_phrases = [
        "bundle",
        "study guide",
        "summary of",
        "workbook for",
        "instructor's manual",
        "test bank",
    ]
    lowered = title.lower()
    return (
        (has_cjk(title) or has_latin(title))
        and is_readable_text(title)
        and not any(phrase in lowered for phrase in rejected_phrases)
    )


def pick_isbn(isbns: list[str] | None) -> str:
    normalized = [re.sub(r"[^0-9Xx]", "", isbn) for isbn in isbns or []]
    for isbn in normalized:
        if len(isbn) == 13 and isbn.startswith(("978", "979")):
            return isbn
    for isbn in normalized:
        if len(isbn) in {10, 13}:
            return isbn.upper()
    return ""


def parse_publish_date(doc: dict[str, Any]) -> str:
    publish_year = doc.get("first_publish_year")
    if isinstance(publish_year, int):
        return f"{publish_year:04d}-01-01"
    return ""


def cover_url(doc: dict[str, Any], isbn: str) -> str:
    cover_id = doc.get("cover_i")
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else ""


def parse_language(doc: dict[str, Any], preferred_language: str) -> str:
    languages = doc.get("language") or []
    if isinstance(languages, str):
        languages = [languages]
    preferred_codes = ["chi", "cmn", "zho"] if preferred_language == "chi" else [preferred_language]
    for code in preferred_codes:
        if code in languages and code in LANGUAGE_NAMES:
            return LANGUAGE_NAMES[code]
    for code in languages:
        if code in LANGUAGE_NAMES:
            return LANGUAGE_NAMES[code]
    return clean_text(languages[:1]) or "未知"


def random_book_format(rng: random.Random) -> str:
    length, width = rng.choice(BOOK_SIZE_OPTIONS)
    return f"{length}mm X {width}mm，紙本版"


def extract_work_description(work: dict[str, Any] | None) -> str:
    if not work:
        return ""

    description = work.get("description")
    if isinstance(description, dict):
        description = description.get("value")

    text = clean_text(description)
    if text and "?" not in text:
        return text[:900]

    return ""


def fetch_work_description(work_key: str, cache: dict[str, str]) -> str:
    if not work_key:
        return ""
    if work_key in cache:
        return cache[work_key]

    data = get_json(WORK_URL.format(work_key=work_key))
    description = extract_work_description(data)
    cache[work_key] = description
    return description


def introduction_from_open_library(doc: dict[str, Any], work_cache: dict[str, str]) -> str:
    work_description = fetch_work_description(clean_text(doc.get("key")), work_cache)
    if work_description:
        return work_description

    first_sentence = clean_text(doc.get("first_sentence"))
    if first_sentence and "?" not in first_sentence:
        return first_sentence[:650]
    return ""


def generated_introduction(book: dict[str, Any]) -> str:
    category_id = book["categoryIds"][0]
    category_name = CATEGORY_NAMES.get(category_id, "一般圖書")
    title = book["title"]
    author = book["author"] or "作者未詳"

    if has_cjk(title):
        intro = ZH_INTRO_BY_CATEGORY.get(
            category_id,
            (
                f"本書屬於{category_name}類，內容以清楚的節奏整理主題，"
                "適合想在日常閱讀中獲得知識、靈感或放鬆時間的讀者。"
                "它不過度解釋主題，而是保留適度想像與思考空間。"
            ),
        )
        return f"《{title}》由{author}撰寫。{intro}"

    intro = EN_INTRO_BY_CATEGORY.get(
        category_id,
        (
            "This book offers a clear and approachable reading experience without "
            "overexplaining its subject. It gives enough context to enter the topic "
            "while leaving space for reflection."
        ),
    )
    return f"{title} by {author} belongs to the {category_name} shelf. {intro}"


def search_books(query: str, page: int) -> list[dict[str, Any]]:
    language = "chi" if has_cjk(query) else "eng"
    params = {
        "q": f"{query} language:{language}",
        "limit": SEARCH_LIMIT,
        "page": page,
        "fields": ",".join(
            [
                "key",
                "title",
                "author_name",
                "isbn",
                "publisher",
                "first_publish_year",
                "cover_i",
                "subject",
                "first_sentence",
                "language",
            ]
        ),
    }
    data = get_json(SEARCH_URL, params=params)
    return data.get("docs", []) if data else []


def build_book(
    doc: dict[str, Any],
    rng: random.Random,
    category_id: str,
    query: str,
    work_cache: dict[str, str],
) -> dict[str, Any] | None:
    preferred_language = "chi" if has_cjk(query) else "eng"
    isbn = pick_isbn(doc.get("isbn"))
    title = clean_text(doc.get("title"))
    if not isbn or not title or not doc.get("cover_i"):
        return None
    if has_cjk(query) and not has_cjk(title):
        return None
    if not is_good_title(title):
        return None

    author = clean_text(doc.get("author_name"))
    if author and not is_readable_text(author):
        author = ""

    publisher = clean_text(doc.get("publisher"))
    if publisher and not is_readable_text(publisher):
        publisher = ""
    if "," in publisher:
        publisher = publisher.split(",", 1)[0].strip()

    book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "publisher": publisher,
        "bookFormat": random_book_format(rng),
        "language": parse_language(doc, preferred_language),
        "publishDate": parse_publish_date(doc),
        "listedAt": "",
        "price": rng.randint(250, 850),
        "coverUrl": cover_url(doc, isbn),
        "introduction": introduction_from_open_library(doc, work_cache),
        "stock": rng.randint(5, 80),
        "salesCount": rng.randint(0, 500),
        "promotionLabel": "",
        "categoryIds": [category_id],
    }
    book["categoryIds"] = [infer_category_id(book, category_id)]
    if not book["introduction"]:
        book["introduction"] = generated_introduction(book)
    return book


def collect_books(target_count: int = TARGET_COUNT) -> list[dict[str, Any]]:
    rng = random.Random(RANDOM_SEED)
    books: list[dict[str, Any]] = []
    seen_isbns: set[str] = set()
    per_category_target = target_count // len(CATEGORY_SEARCHES)
    extra_slots = target_count % len(CATEGORY_SEARCHES)
    category_counts = {category_id: 0 for category_id in CATEGORY_SEARCHES}
    work_cache: dict[str, str] = {}

    with tqdm(total=target_count, desc="Fetching Open Library books") as progress:
        for index, category_id in enumerate(CATEGORY_SEARCHES):
            wanted = per_category_target + (1 if index < extra_slots else 0)
            for page in range(1, 8):
                for query in CATEGORY_SEARCHES[category_id]:
                    if category_counts[category_id] >= wanted:
                        break
                    for doc in search_books(query, page):
                        if category_counts[category_id] >= wanted or len(books) >= target_count:
                            break
                        book = build_book(doc, rng, category_id, query, work_cache)
                        if not book or book["isbn"] in seen_isbns:
                            continue
                        seen_isbns.add(book["isbn"])
                        books.append(book)
                        category_counts[category_id] += 1
                        progress.update(1)
                if category_counts[category_id] >= wanted:
                    break

        for category_id in CATEGORY_SEARCHES:
            if len(books) >= target_count:
                break
            for page in range(1, 8):
                for query in CATEGORY_SEARCHES[category_id]:
                    for doc in search_books(query, page):
                        if len(books) >= target_count:
                            break
                        book = build_book(doc, rng, category_id, query, work_cache)
                        if not book or book["isbn"] in seen_isbns:
                            continue
                        seen_isbns.add(book["isbn"])
                        books.append(book)
                        progress.update(1)

    return books


def assign_listed_dates(books: list[dict[str, Any]], rng: random.Random) -> None:
    latest_indexes = set(rng.sample(range(len(books)), min(LATEST_COUNT, len(books))))
    start = date(2025, 1, 1)
    end = date(2026, 4, 25)
    max_days = (end - start).days

    for index, book in enumerate(books):
        if index in latest_indexes:
            book["listedAt"] = LATEST_LISTED_AT
        else:
            book["listedAt"] = (start + timedelta(days=rng.randint(0, max_days))).isoformat()


def assign_promotions(books: list[dict[str, Any]], rng: random.Random) -> None:
    indexes = list(range(len(books)))
    special = set(rng.sample(indexes, min(SPECIAL_OFFER_COUNT, len(indexes))))
    remaining = [index for index in indexes if index not in special]
    discounted = special | set(rng.sample(remaining, min(DISCOUNTED_COUNT - len(special), len(remaining))))
    labels = ["95折", "9折", "85折", "79折"]

    for index, book in enumerate(books):
        if index in special:
            book["promotionLabel"] = "65折"
        elif index in discounted:
            book["promotionLabel"] = rng.choice(labels)
        else:
            book["promotionLabel"] = ""


def choose_rating(rng: random.Random) -> int:
    return rng.choices([1, 2, 3, 4, 5], weights=[2, 4, 14, 35, 45], k=1)[0]


def generate_reader_data(books: list[dict[str, Any]], rng: random.Random) -> list[dict[str, Any]]:
    records = []
    for book in books:
        texts = ZH_REVIEW_TEXTS if has_cjk(book["title"]) else EN_REVIEW_TEXTS
        reviews = [
            {
                "readerName": rng.choice(READER_NAMES),
                "rating": choose_rating(rng),
                "content": rng.choice(texts),
            }
            for _ in range(3)
        ]
        book["averageRating"] = round(sum(review["rating"] for review in reviews) / len(reviews), 1)
        book["reviewCount"] = len(reviews)
        records.append({"isbn": book["isbn"], "title": book["title"], "reviews": reviews})
    return records


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    books = collect_books(TARGET_COUNT)
    if len(books) < TARGET_COUNT:
        raise SystemExit(f"Only fetched {len(books)} books; expected {TARGET_COUNT}.")

    assign_listed_dates(books, rng)
    assign_promotions(books, rng)
    reader_data = generate_reader_data(books, rng)

    OUTPUT_JSON.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
    READER_JSON.write_text(json.dumps(reader_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Done. Wrote {len(books)} books to {OUTPUT_JSON}")
    print(f"Done. Wrote {sum(len(item['reviews']) for item in reader_data)} reviews to {READER_JSON}")


if __name__ == "__main__":
    main()
