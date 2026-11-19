import difflib
import json
import math
import random
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

try:
    import tkintermapview
except ImportError:  # shown as a friendly message on the Find Bins page
    tkintermapview = None

# ---------------------- DATA ----------------------
# add more data set

WASTE_DATA = {
    "banana peel": ("Organic Waste", "Compost it.", "#16A34A"),
    "vegetable peels": ("Organic Waste", "Use for composting.", "#16A34A"),
    "leftover food": ("Organic Waste", "Compost if suitable.", "#16A34A"),
    "paper": ("Recyclable Waste", "Keep clean and dry.", "#0284C7"),
    "newspaper": ("Recyclable Waste", "Send for recycling.", "#0284C7"),
    "cardboard": ("Recyclable Waste", "Flatten before recycling.", "#0284C7"),
    "plastic bottle": ("Recyclable Waste", "Empty it and check local rules.", "#0284C7"),
    "glass bottle": ("Recyclable Waste", "Use a glass collection point.", "#0284C7"),
    "aluminium can": ("Recyclable Waste", "Recycle if accepted locally.", "#0284C7"),
    "battery": ("Hazardous Waste", "Use an authorised collection point.", "#DC2626"),
    "medicine": ("Special Waste", "Use a medicine take-back facility.", "#9333EA"),
    "broken bulb": ("Special Waste", "Use an appropriate collection point.", "#9333EA"),
    "old mobile phone": ("E-Waste", "Give it to an authorised collector.", "#D97706"),
    "charger": ("E-Waste", "Send it to an e-waste collector.", "#D97706"),
}

TIPS = [
    "Carry a reusable water bottle.",
    "Avoid single-use plastic bags.",
    "Reuse notebooks with unused pages.",
    "Switch off unused electrical appliances.",
    "Donate usable clothes instead of throwing them away.",
    "Separate wet waste from dry waste.",
    "Repair items instead of replacing them.",
    "Keep Your Surroundings Clean – Never throw garbage on roads.",
    "Use LED Bulbs – They consume less electricity.",
    "Use Public Transport – Travel by bus or metro to reduce pollution.",
    "Spread Environmental Awareness – Encourage others to adopt eco-friendly habits.",
    "Use Solar Energy – Choose solar power where practical.",
    "Avoid Burning Garbage – Burning waste causes air pollution.",
    "Walk or Cycle – Choose these for short distances.",

]
CHALLENGES = [
    "Avoid single-use plastic for one day!",
    "Reuse one item instead of buying a new one!",
    "Separate all your household waste today!",
    "Save water while brushing your teeth!",
    "Collect recyclable paper and keep it dry!",
    "Switch off unnecessary lights today!",
    "Walk or cycle for a short journey.",
    "Segregate wet and dry waste at home.",
    "Reduce paper waste by using the blank side.",

]
QUIZ = [
    ("Which item is generally suitable for composting?",
     ["Plastic bottle", "Banana peel", "Battery"], 2),

    ("Where should an old mobile phone go?",
     ["General waste", "Food waste", "Authorised e-waste collection"], 3),

    ("What should you do with a clean paper item?",
     ["Recycle if accepted locally", "Burn it", "Put it in food waste"], 1),

    ("How can you reduce plastic waste?",
     ["Use more plastic bags", "Carry a reusable bag", "Throw plastic anywhere"], 2),

      ("Which item is generally suitable for composting?",
     ["Plastic bottle", "Banana peel", "Battery"], 2),

    ("Which bag is more eco-friendly for shopping?",
     ["Cloth bag", "Single-use plastic bag", "Disposable paper-plastic bag"], 1),

    ("Which action helps save electricity?",
     ["Leaving lights on", "Keeping the TV running", "Switching off unused lights"], 3),

    ("Which energy source is renewable?",
     ["Coal", "Solar energy", "Petrol"], 2),

    ("Which bin is commonly used for wet waste in India?",
     ["Green bin", "Blue bin", "Red bin"], 1),

    ("Which activity helps conserve water?",
     ["Leaving the tap running", "Fixing leaking taps", "Washing the driveway with a hose"], 2),

    ("Which of these causes air pollution?",
     ["Planting trees", "Cycling to work", "Burning garbage"], 3),

    ("Which material can usually be recycled?",
     ["Used glass bottle", "Food leftovers mixed with oil", "Dirty tissue paper"], 1),

    ("Which transport option produces no direct exhaust emissions?",
     ["Petrol car", "Bicycle", "Diesel bus"], 2),

    ("What should you do with an old battery?",
     ["Throw it into a river", "Burn it", "Take it to an appropriate collection point"], 3),

    ("Which gas is a major contributor to global warming?",
     ["Oxygen", "Carbon dioxide", "Helium"], 2),

    ("What is the main purpose of planting trees?",
     ["To increase plastic waste", "To increase noise", "To support biodiversity and absorb carbon dioxide"], 3),

    ("Which practice helps reduce food waste?",
     ["Planning meals before shopping", "Buying more food than needed", "Throwing away leftovers immediately"], 1),

    ("Which product is reusable?",
     ["Disposable plastic cup", "Stainless steel water bottle", "Single-use straw"], 2),

    ("What does recycling help achieve?",
     ["Increase landfill waste", "Increase resource consumption", "Reduce waste and conserve resources"], 3),

    ("Which appliance generally uses less electricity for lighting?",
     ["LED bulb", "Incandescent bulb", "Halogen bulb"], 1),

    ("What is rainwater harvesting?",
     ["Dumping waste into drains", "Collecting and storing rainwater", "Pumping seawater into rivers"], 2),

    ("Which action helps protect wildlife?",
     ["Destroying forests", "Dumping chemicals into lakes", "Protecting natural habitats"], 3),

    ("Which of these is biodegradable?",
     ["Banana peel", "Aluminium can", "Plastic wrapper"], 1),

    ("What is the best way to reduce single-use plastic waste?",
     ["Use disposable cups daily", "Carry reusable bags and bottles", "Wrap every item in plastic"], 2),
]

# ---------------------- BIN LOCATOR DATA ----------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "ecosort_data"
IMAGE_DIR = DATA_DIR / "bin_images"
BINS_FILE = DATA_DIR / "bins.json"

BIN_CATEGORIES = sorted({v[0] for v in WASTE_DATA.values()})
CATEGORY_COLORS = {v[0]: v[2] for v in WASTE_DATA.values()}
DEFAULT_CENTER = (28.6139, 77.2090)  # map starts here until a location is set

# Demo data so the map isn't empty on first launch. These are NOT verified real
# bins - delete them from ecosort_data/bins.json once you have real data.
SAMPLE_BINS = [
    {
    "id": "sample-1",
    "name": "Manav Rachna Organic Waste Bin",
    "lat": 28.4496,
    "lon": 77.2851,
    "categories": ["Organic Waste", "Recyclable Waste"],
    "notes": "Sample entry near Manav Rachna campus.",
    "photo": None,
    "source": "sample"
},
{
    "id": "sample-2",
    "name": "Manav Rachna Main Gate Bin",
    "lat": 28.4496,
    "lon": 77.2851,
    "categories": ["Recyclable Waste", "Organic Waste"],
    "notes": "Sample entry near main gate.",
    "photo": None,
    "source": "sample"
},
{
    "id": "sample-3",
    "name": "Manav Rachna E-Waste Point",
    "lat": 28.4496,
    "lon": 77.2851,
    "categories": ["E-Waste", "Hazardous Waste"],
    "notes": "Sample e-waste collection point.",
    "photo": None,
    "source": "sample"
},
{
    "id": "sample-4",
    "name": "Manav Rachna Medicine Drop",
    "lat": 28.4496,
    "lon": 77.2851,
    "categories": ["Special Waste"],
    "notes": "Sample special waste collection point.",
    "photo": None,
    "source": "sample"
},
{
    "id": "sample-5",
    "name": "Manav Rachna Battery Bin",
    "lat": 28.4496,
    "lon": 77.2851,
    "categories": ["Hazardous Waste", "E-Waste"],
    "notes": "Sample battery collection point.",
    "photo": None,
    "source": "sample"
}
]


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two coordinates, in kilometres."""
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def format_distance(km):
    return f"{int(km * 1000)} m" if km < 1 else f"{km:.1f} km"


class BinStore:
    """Saves dustbin locations (and their photos) on disk."""

    def __init__(self):
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.bins = self._load()

    def _load(self):
        if BINS_FILE.exists():
            try:
                return json.loads(BINS_FILE.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        bins = [dict(b) for b in SAMPLE_BINS]
        self._write(bins)
        return bins

    @staticmethod
    def _write(bins):
        BINS_FILE.write_text(json.dumps(bins, indent=2), encoding="utf-8")

    def add(self, name, lat, lon, categories, notes="", photo_src=None):
        bin_id = f"user-{int(time.time() * 1000)}"
        photo_name = None
        if photo_src:
            photo_name = f"{bin_id}.jpg"
            with Image.open(photo_src) as im:
                im = im.convert("RGB")
                im.thumbnail((900, 900))
                im.save(IMAGE_DIR / photo_name, "JPEG", quality=85)
        entry = {"id": bin_id, "name": name, "lat": lat, "lon": lon,
                 "categories": categories, "notes": notes,
                 "photo": photo_name, "source": "user"}
        self.bins.append(entry)
        self._write(self.bins)
        return entry

    def remove(self, bin_id):
        for b in list(self.bins):
            if b["id"] == bin_id:
                if b.get("photo"):
                    (IMAGE_DIR / b["photo"]).unlink(missing_ok=True)
                self.bins.remove(b)
        self._write(self.bins)

    def for_category(self, category=None):
        return [b for b in self.bins if category is None or category in b["categories"]]

    def nearest(self, lat, lon, category=None, limit=5):
        pool = self.for_category(category)
        pool.sort(key=lambda b: haversine_km(lat, lon, b["lat"], b["lon"]))
        return pool[:limit]


# ---------------------- THEME ----------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BG = "#F4F7F5"
SIDEBAR = "#102D24"
SIDEBAR_HOVER = "#1D4738"
GREEN = "#21865B"
GREEN_DARK = "#176747"
TEXT = "#172B24"
MUTED = "#708078"
WHITE = "#FFFFFF"
BORDER = "#E3EBE6"


class EcoSortApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EcoSort | Smart Waste Guide")
        self.geometry("1280x800")
        self.minsize(1050, 680)
        self.configure(fg_color=BG)

        self.points = 0
        self.items_checked = 0
        self.category_count = {}
        self.quiz_question = None
        self.quiz_answered = False
        self.active_page = "Overview"
        self.current_result = None
        self.bin_store = BinStore()
        self.user_loc = None
        self.bin_category_preset = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self.show_page("Overview")

    # ---------------------- SHELL ----------------------

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=238, fg_color=SIDEBAR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(8, weight=1)

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(26, 32))
        ctk.CTkLabel(
            brand, text="✿", font=ctk.CTkFont(size=29, weight="bold"),
            text_color="#76E0A7"
        ).pack(side="left", padx=(0, 10))
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")
        brand_text.pack(side="left")
        ctk.CTkLabel(
            brand_text, text="EcoSort", text_color=WHITE,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand_text, text="SMART WASTE GUIDE", text_color="#9BB7AA",
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w", pady=(1, 0))

        ctk.CTkLabel(
            self.sidebar, text="WORKSPACE", text_color="#7D9A8C",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=24, pady=(0, 10))

        nav_items = [
            ("⌂", "Overview"),
            ("⌕", "Waste Checker"),
            ("▤", "Waste Directory"),
            ("⌖", "Find Bins"),
            ("✳", "Eco Tips"),
            ("◎", "Daily Challenge"),
            ("✎", "Recycling Quiz"),
        ]
        self.nav_buttons = {}
        for icon, name in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=f"  {icon}    {name}", anchor="w",
                height=44, corner_radius=10, border_spacing=10,
                fg_color="transparent", hover_color=SIDEBAR_HOVER,
                text_color="#D7E5DD", font=ctk.CTkFont(size=13),
                command=lambda n=name: self.show_page(n)
            )
            btn.pack(fill="x", padx=13, pady=3)
            self.nav_buttons[name] = btn

        self.sidebar.grid_rowconfigure(20, weight=1)
        bottom = ctk.CTkFrame(self.sidebar, fg_color="#193B2F", corner_radius=14)
        bottom.pack(side="bottom", fill="x", padx=14, pady=18)
        ctk.CTkLabel(
            bottom, text="🌱  SMALL STEPS MATTER", text_color="#B6E8C9",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=13, pady=(13, 5))
        ctk.CTkLabel(
            bottom, text="Make today a little greener.", text_color="#D8E7DF",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=13, pady=(0, 13))

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _page_header(self, title, subtitle):
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(26, 16))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text=title, text_color=TEXT,
            font=ctk.CTkFont(size=27, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header, text=subtitle, text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", pady=(5, 0))
        ctk.CTkLabel(
            header, text="●  ECO MODE", text_color=GREEN_DARK,
            fg_color="#DDF5E6", corner_radius=20,
            font=ctk.CTkFont(size=10, weight="bold")
        ).grid(row=0, column=1, rowspan=2, padx=(15, 0), ipadx=12, ipady=8)

    def _body(self):
        body = ctk.CTkScrollableFrame(
            self.content, fg_color="transparent", corner_radius=0
        )
        body.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 24))
        body.grid_columnconfigure(0, weight=1)
        return body

    def _card(self, parent, **kwargs):
        return ctk.CTkFrame(
            parent, fg_color=WHITE, corner_radius=18,
            border_width=1, border_color=BORDER, **kwargs
        )

    def show_page(self, page):
        self.active_page = page
        for name, btn in self.nav_buttons.items():
            btn.configure(
                fg_color=GREEN if name == page else "transparent",
                text_color=WHITE if name == page else "#D7E5DD"
            )
        self._clear_content()
        titles = {
            "Overview": ("Good to see you, eco champion 👋",
                         "Track your progress and make smarter waste decisions."),
            "Waste Checker": ("Waste checker", "Identify an item and find a better way to dispose of it."),
            "Waste Directory": ("Waste directory", "Browse supported items, categories, and disposal guidance."),
            "Find Bins": ("Find a dustbin near you", "See the nearest bin for your waste type, or add one we're missing."),
            "Eco Tips": ("A little greener, every day", "Simple habits can make a meaningful difference."),
            "Daily Challenge": ("Your daily green challenge", "Pick one action and make it count today."),
            "Recycling Quiz": ("Test your eco knowledge", "Answer questions and earn Eco Points."),
        }
        title, subtitle = titles[page]
        self._page_header(title, subtitle)
        if page == "Find Bins":
            self._bins_page()
            return
        body = self._body()

        if page == "Overview":
            self._overview(body)
        elif page == "Waste Checker":
            self._checker(body)
        elif page == "Waste Directory":
            self._directory(body)
        elif page == "Eco Tips":
            self._tips_page(body)
        elif page == "Daily Challenge":
            self._challenge_page(body)
        elif page == "Recycling Quiz":
            self._quiz_page(body)

    # ---------------------- OVERVIEW ----------------------

    def _overview(self, body):
        hero = ctk.CTkFrame(body, fg_color=GREEN_DARK, corner_radius=20)
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        hero.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hero, text="A cleaner planet starts with one choice.",
            text_color=WHITE, font=ctk.CTkFont(size=21, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(23, 7))
        ctk.CTkLabel(
            hero, text="Identify waste correctly. Recycle responsibly. Build better habits.",
            text_color="#D9F4E4", font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 19))
        ctk.CTkButton(
            hero, text="Check an item  →", height=38, corner_radius=10,
            fg_color="#FFFFFF", hover_color="#E5F6EB", text_color=GREEN_DARK,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.show_page("Waste Checker")
        ).grid(row=0, column=1, rowspan=2, padx=24)

        stats = ctk.CTkFrame(body, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1, uniform="stat")
        self._stat_card(stats, 0, "TOTAL ECO POINTS", str(self.points), "✦", "#E8F7EE", GREEN_DARK)
        self._stat_card(stats, 1, "ITEMS CHECKED", str(self.items_checked), "⌕", "#EAF3FF", "#2563A6")
        self._stat_card(stats, 2, "CATEGORIES FOUND", str(len(self.category_count)), "▦", "#FFF3E4", "#B96B13")

        row = ctk.CTkFrame(body, fg_color="transparent")
        row.grid(row=2, column=0, sticky="ew")
        row.grid_columnconfigure(0, weight=3)
        row.grid_columnconfigure(1, weight=2)

        progress_card = self._card(row)
        progress_card.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        ctk.CTkLabel(
            progress_card, text="Your green impact", text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 5))
        ctk.CTkLabel(
            progress_card, text="Keep going — every action adds up.",
            text_color=MUTED, font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=20)
        rank, target = self._rank()
        ctk.CTkLabel(
            progress_card, text=rank, text_color=GREEN_DARK,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(18, 4))
        progress = min(self.points / target, 1.0)
        bar = ctk.CTkProgressBar(progress_card, progress_color=GREEN, fg_color="#E6EEE9", height=10)
        bar.pack(fill="x", padx=20, pady=8)
        bar.set(progress)
        ctk.CTkLabel(
            progress_card, text=f"{self.points} / {target} points toward the next milestone",
            text_color=MUTED, font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=20, pady=(0, 18))

        tip_card = self._card(row)
        tip_card.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        ctk.CTkLabel(
            tip_card, text="TODAY'S ECO TIP", text_color=GREEN_DARK,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=18, pady=(19, 10))
        ctk.CTkLabel(
            tip_card, text="🌿", font=ctk.CTkFont(size=30)
        ).pack(anchor="w", padx=18)
        ctk.CTkLabel(
            tip_card, text=random.choice(TIPS), text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=230, justify="left"
        ).pack(anchor="w", padx=18, pady=(8, 14))
        ctk.CTkButton(
            tip_card, text="More eco tips  →", height=32, corner_radius=9,
            fg_color="#E5F5EB", hover_color="#D0EEDB", text_color=GREEN_DARK,
            command=lambda: self.show_page("Eco Tips")
        ).pack(anchor="w", padx=18, pady=(0, 18))

        ctk.CTkLabel(
            body, text="Disposal guidance can vary by location. Check local collection rules.",
            text_color=MUTED, font=ctk.CTkFont(size=10)
        ).grid(row=3, column=0, sticky="w", pady=(16, 0))

    def _stat_card(self, parent, col, title, value, icon, tint, accent):
        card = self._card(parent)
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 7, 7 if col < 2 else 0))
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(16, 10))
        ctk.CTkLabel(
            top, text=icon, fg_color=tint, text_color=accent,
            corner_radius=10, width=38, height=38,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        ctk.CTkLabel(
            top, text=title, text_color=MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(side="left", padx=10)
        ctk.CTkLabel(
            card, text=value, text_color=TEXT,
            font=ctk.CTkFont(size=29, weight="bold")
        ).pack(anchor="w", padx=17, pady=(0, 17))

    # ---------------------- WASTE CHECKER ----------------------

    def _checker(self, body):
        card = self._card(body)
        card.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(
            card, text="What would you like to throw away?",
            text_color=TEXT, font=ctk.CTkFont(size=17, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 6))
        ctk.CTkLabel(
            card, text="Enter a waste item below. We'll suggest a suitable category.",
            text_color=MUTED, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=24)

        searchrow = ctk.CTkFrame(card, fg_color="transparent")
        searchrow.pack(fill="x", padx=24, pady=18)
        self.search_entry = ctk.CTkEntry(
            searchrow, placeholder_text="e.g. banana peel, battery, cardboard...",
            height=46, corner_radius=11, border_color=BORDER,
            fg_color="#FAFCFA", text_color=TEXT, font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self._identify_waste())
        self.search_entry.bind("<KeyRelease>", self._update_search_suggestions)
        ctk.CTkButton(
            searchrow, text="Identify waste  →", width=150, height=46,
            corner_radius=11, fg_color=GREEN, hover_color=GREEN_DARK,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._identify_waste
        ).pack(side="left")

        self.suggestions_frame = ctk.CTkFrame(
            card, fg_color="transparent", corner_radius=10
        )
        self.suggestions_frame.pack(fill="x", padx=24, pady=(0, 10))

        self.result_frame = self._card(body)
        self.result_frame.grid(row=1, column=0, sticky="ew", pady=16)
        self._show_empty_result()

        chips = ctk.CTkFrame(body, fg_color="transparent")
        chips.grid(row=2, column=0, sticky="ew")
        ctk.CTkLabel(chips, text="TRY AN EXAMPLE", text_color=MUTED,
                     font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(4, 8))
        examples = ctk.CTkFrame(chips, fg_color="transparent")
        examples.pack(anchor="w")
        for item in ["banana peel", "plastic bottle", "battery", "old mobile phone"]:
            ctk.CTkButton(
                examples, text=item.title(), height=30, corner_radius=15,
                fg_color="#E7F3EB", hover_color="#D2E9DA", text_color=GREEN_DARK,
                font=ctk.CTkFont(size=10),
                command=lambda value=item: self._set_example(value)
            ).pack(side="left", padx=(0, 7))

    def _show_empty_result(self):
        for child in self.result_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(
            self.result_frame, text="♻", text_color="#9AB7A5",
            font=ctk.CTkFont(size=35)
        ).pack(anchor="w", padx=23, pady=(18, 0))
        ctk.CTkLabel(
            self.result_frame, text="Your waste result will appear here",
            text_color=TEXT, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=23, pady=(7, 4))
        ctk.CTkLabel(
            self.result_frame, text="Start by entering an item in the search box above.",
            text_color=MUTED, font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=23, pady=(0, 20))

    def _update_search_suggestions(self, event=None):
        """Show live item-name suggestions while the user types."""
        if not hasattr(self, "suggestions_frame"):
            return

        for child in self.suggestions_frame.winfo_children():
            child.destroy()

        term = self.search_entry.get().strip().lower()
        if not term or term in WASTE_DATA:
            return

        matches = [
            name for name in sorted(WASTE_DATA)
            if name.startswith(term) or term in name
        ]

        # Offer spelling suggestions when there are no direct matches.
        if not matches:
            matches = difflib.get_close_matches(
                term, list(WASTE_DATA), n=4, cutoff=0.35
            )

        if not matches:
            return

        ctk.CTkLabel(
            self.suggestions_frame,
            text="SUGGESTED ITEMS",
            text_color=MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w", pady=(0, 4))

        for name in matches[:5]:
            ctk.CTkButton(
                self.suggestions_frame,
                text=f"⌕  {name.title()}",
                height=30,
                corner_radius=8,
                anchor="w",
                fg_color="#EAF5EE",
                hover_color="#D7EBDD",
                text_color=GREEN_DARK,
                font=ctk.CTkFont(size=11),
                command=lambda value=name: self._set_example(value)
            ).pack(fill="x", pady=2)

    def _set_example(self, value):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, value)
        self._identify_waste()

    def _identify_waste(self):
        item = self.search_entry.get().strip().lower()
        if hasattr(self, "suggestions_frame"):
            for child in self.suggestions_frame.winfo_children():
                child.destroy()
        if not item:
            messagebox.showinfo("Enter an item", "Type a waste item to identify it.")
            return
        self.items_checked += 1
        data = WASTE_DATA.get(item)
        for child in self.result_frame.winfo_children():
            child.destroy()
        if data:
            category, suggestion, accent = data
            self.points += 5
            self.category_count[category] = self.category_count.get(category, 0) + 1
            ctk.CTkLabel(
                self.result_frame, text=category.upper(),
                text_color=accent, fg_color="#E8F5EC",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold")
            ).pack(anchor="w", padx=23, pady=(22, 9), ipadx=10, ipady=6)
            ctk.CTkLabel(
                self.result_frame, text=item.title(), text_color=TEXT,
                font=ctk.CTkFont(size=23, weight="bold")
            ).pack(anchor="w", padx=23)
            ctk.CTkLabel(
                self.result_frame, text=suggestion, text_color=MUTED,
                font=ctk.CTkFont(size=13), wraplength=700, justify="left"
            ).pack(anchor="w", padx=23, pady=(7, 14))
            ctk.CTkLabel(
                self.result_frame, text="✓  +5 Eco Points earned",
                text_color=GREEN_DARK, fg_color="#E2F6E9",
                corner_radius=8, font=ctk.CTkFont(size=11, weight="bold")
            ).pack(anchor="w", padx=23, pady=(0, 12), ipadx=10, ipady=7)
            ctk.CTkButton(
                self.result_frame, text="⌖  Find nearest bin for this waste", height=38,
                corner_radius=10, fg_color=GREEN, hover_color=GREEN_DARK,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda c=category: self._go_find_bin(c)
            ).pack(anchor="w", padx=23, pady=(0, 22))
        else:
            ctk.CTkLabel(
                self.result_frame, text="Item not found",
                text_color="#B45309", font=ctk.CTkFont(size=20, weight="bold")
            ).pack(anchor="w", padx=23, pady=(22, 8))
            ctk.CTkLabel(
                self.result_frame,
                text="This item is not in the current directory. Check local disposal rules. No points awarded.",
                text_color=MUTED, font=ctk.CTkFont(size=12),
                wraplength=700, justify="left"
            ).pack(anchor="w", padx=23, pady=(0, 22))
        self._refresh_overview_if_needed()

    # ---------------------- DIRECTORY ----------------------

    def _directory(self, body):
        top = self._card(body)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            top, text=f"{len(WASTE_DATA)} supported items",
            text_color=TEXT, font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=18, pady=(15, 4))
        ctk.CTkLabel(
            top, text="Search by item name or filter by waste category.",
            text_color=MUTED, font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=18, pady=(0, 15))

        controls = ctk.CTkFrame(body, fg_color="transparent")
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search = ctk.CTkEntry(controls, placeholder_text="Search waste items...", height=38)
        search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        categories = ["All categories"] + sorted({v[0] for v in WASTE_DATA.values()})
        filter_box = ctk.CTkOptionMenu(
            controls, values=categories, width=205, height=38,
            fg_color=GREEN, button_color=GREEN_DARK,
            command=lambda _: populate()
        )
        filter_box.pack(side="left")

        list_frame = self._card(body)
        list_frame.grid(row=2, column=0, sticky="ew")
        list_frame.grid_columnconfigure(0, weight=1)
        rows_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        rows_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def populate(*_):
            for child in rows_frame.winfo_children():
                child.destroy()
            term = search.get().strip().lower()
            chosen = filter_box.get()
            filtered = [
                (item, data) for item, data in sorted(WASTE_DATA.items())
                if term in item and (chosen == "All categories" or data[0] == chosen)
            ]
            if not filtered:
                ctk.CTkLabel(rows_frame, text="No matching items found.", text_color=MUTED).pack(pady=20)
                return
            for item, (category, suggestion, accent) in filtered:
                row = ctk.CTkFrame(rows_frame, fg_color="#F8FBF9", corner_radius=10)
                row.pack(fill="x", pady=4)
                ctk.CTkLabel(row, text=item.title(), width=165, anchor="w",
                             text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=12, pady=12)
                ctk.CTkLabel(row, text=category, text_color=accent, width=155,
                             anchor="w", font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=6)
                ctk.CTkLabel(row, text=suggestion, text_color=MUTED, anchor="w",
                             font=ctk.CTkFont(size=10), wraplength=390).pack(side="left", padx=8, pady=10, fill="x", expand=True)
        search.bind("<KeyRelease>", populate)
        populate()

    # ---------------------- TIPS / CHALLENGES ----------------------

    def _tips_page(self, body):
        ctk.CTkLabel(
            body, text="Small habits. Lasting impact.",
            text_color=TEXT, font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 14))
        for i, tip in enumerate(TIPS):
            card = self._card(body)
            card.grid(row=i + 1, column=0, sticky="ew", pady=5)
            ctk.CTkLabel(card, text="✦", text_color=GREEN, font=ctk.CTkFont(size=19)).pack(side="left", padx=17, pady=15)
            ctk.CTkLabel(card, text=tip, text_color=TEXT, font=ctk.CTkFont(size=12),
                         wraplength=700, justify="left").pack(side="left", padx=5, pady=15)

    def _challenge_page(self, body):
        hero = ctk.CTkFrame(body, fg_color="#FFF2D9", corner_radius=20)
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        ctk.CTkLabel(hero, text="TODAY'S MISSION", text_color="#A45B0A",
                     font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=25, pady=(24, 8))
        self.challenge_text = ctk.CTkLabel(
            hero, text=random.choice(CHALLENGES), text_color="#5B3A12",
            font=ctk.CTkFont(size=22, weight="bold"), wraplength=650, justify="left"
        )
        self.challenge_text.pack(anchor="w", padx=25, pady=(0, 22))
        ctk.CTkButton(
            hero, text="Get another challenge ↻", height=40, corner_radius=10,
            fg_color="#C47B19", hover_color="#A9630D",
            command=lambda: self.challenge_text.configure(text=random.choice(CHALLENGES))
        ).pack(anchor="w", padx=25, pady=(0, 24))
        info = self._card(body)
        info.grid(row=1, column=0, sticky="ew")
        ctk.CTkLabel(info, text="A challenge is a commitment, not a score.",
                     text_color=TEXT, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=20, pady=(18, 5))
        ctk.CTkLabel(info, text="Choose one action you can realistically complete today. Points are awarded through the waste checker and quiz.",
                     text_color=MUTED, font=ctk.CTkFont(size=12), wraplength=700,
                     justify="left").pack(anchor="w", padx=20, pady=(0, 18))

    # ---------------------- QUIZ ----------------------

    def _quiz_page(self, body):
        card = self._card(body)
        card.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(card, text="♻  ECO KNOWLEDGE CHECK",
                     text_color=GREEN_DARK, font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=24, pady=(23, 8))
        self.question_label = ctk.CTkLabel(
            card, text="Ready to test your recycling knowledge?",
            text_color=TEXT, font=ctk.CTkFont(size=19, weight="bold"),
            wraplength=700, justify="left"
        )
        self.question_label.pack(anchor="w", padx=24, pady=(0, 18))
        self.answer_var = ctk.IntVar(value=0)
        self.answer_radios = []
        for i in range(3):
            radio = ctk.CTkRadioButton(
                card, text="", variable=self.answer_var, value=i + 1,
                radiobutton_width=19, radiobutton_height=19,
                fg_color=GREEN, hover_color=GREEN_DARK,
                text_color=TEXT, font=ctk.CTkFont(size=12)
            )
            radio.pack(anchor="w", padx=27, pady=10)
            self.answer_radios.append(radio)
        self.quiz_feedback = ctk.CTkLabel(card, text="", text_color=MUTED, font=ctk.CTkFont(size=12))
        self.quiz_feedback.pack(anchor="w", padx=24, pady=(12, 8))
        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(anchor="w", padx=24, pady=(5, 24))
        ctk.CTkButton(
            buttons, text="New question", height=40, corner_radius=10,
            fg_color="#E6F4EB", hover_color="#D2EBDD", text_color=GREEN_DARK,
            command=self._new_question
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            buttons, text="Submit answer  →", height=40, corner_radius=10,
            fg_color=GREEN, hover_color=GREEN_DARK, command=self._submit_answer
        ).pack(side="left")
        self._new_question()

    def _new_question(self):
        self.quiz_question = random.choice(QUIZ)
        self.quiz_answered = False
        question, options, _ = self.quiz_question
        self.question_label.configure(text=question)
        self.answer_var.set(0)
        self.quiz_feedback.configure(text="")
        for radio, option in zip(self.answer_radios, options):
            radio.configure(text=option, state="normal")

    def _submit_answer(self):
        if self.quiz_question is None or self.quiz_answered:
            messagebox.showinfo("Quiz", "Choose 'New question' to continue.")
            return
        selected = self.answer_var.get()
        if not selected:
            messagebox.showinfo("Quiz", "Please select an answer first.")
            return
        _, options, correct = self.quiz_question
        self.quiz_answered = True
        for radio in self.answer_radios:
            radio.configure(state="disabled")
        if selected == correct:
            self.points += 10
            self.quiz_feedback.configure(text="✓ Correct! +10 Eco Points earned.", text_color=GREEN_DARK)
        else:
            self.quiz_feedback.configure(text=f"Not quite. Correct answer: {options[correct - 1]}", text_color="#B45309")
        self._refresh_overview_if_needed()

    # ---------------------- FIND BINS (MAP) ----------------------

    def _go_find_bin(self, category):
        self.bin_category_preset = category
        self.show_page("Find Bins")

    def _bins_page_alive(self):
        try:
            return self.active_page == "Find Bins" and self.map_widget.winfo_exists()
        except Exception:
            return False

    def _bins_page(self):
        wrap = ctk.CTkFrame(self.content, fg_color="transparent")
        wrap.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 24))
        wrap.grid_columnconfigure(1, weight=1)
        wrap.grid_rowconfigure(0, weight=1)

        if tkintermapview is None:
            card = self._card(wrap)
            card.grid(row=0, column=0, columnspan=2, sticky="new")
            ctk.CTkLabel(card, text="Map library not installed", text_color="#B45309",
                         font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=24, pady=(22, 6))
            ctk.CTkLabel(card, text="Run this in your terminal, then restart EcoSort:\n\n    pip install tkintermapview pillow",
                         text_color=MUTED, justify="left", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=24, pady=(0, 22))
            return

        self.bin_markers = []
        self.selected_bin = None
        self._detail_img = None

        panel = ctk.CTkScrollableFrame(wrap, width=320, fg_color="transparent", corner_radius=0)
        panel.grid(row=0, column=0, sticky="ns", padx=(0, 14))

        # --- waste type
        c1 = self._card(panel)
        c1.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(c1, text="WASTE TYPE", text_color=MUTED,
                     font=ctk.CTkFont(size=9, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))
        self.bin_category_var = ctk.StringVar(value=self.bin_category_preset or "All types")
        self.bin_category_preset = None
        ctk.CTkOptionMenu(
            c1, values=["All types"] + BIN_CATEGORIES, variable=self.bin_category_var,
            height=34, fg_color=GREEN, button_color=GREEN_DARK,
            command=lambda _: self._refresh_bins(fit=True)
        ).pack(fill="x", padx=16)
        self.bin_item_entry = ctk.CTkEntry(
            c1, placeholder_text="...or type an item, e.g. battery", height=34,
            border_color=BORDER, fg_color="#FAFCFA", text_color=TEXT)
        self.bin_item_entry.pack(fill="x", padx=16, pady=(8, 14))
        self.bin_item_entry.bind("<Return>", lambda e: self._bin_item_lookup())

        # --- location
        c2 = self._card(panel)
        c2.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(c2, text="YOUR LOCATION", text_color=MUTED,
                     font=ctk.CTkFont(size=9, weight="bold")).pack(anchor="w", padx=16, pady=(14, 4))
        self.loc_status = ctk.CTkLabel(c2, text="Not set yet", text_color=TEXT,
                                       font=ctk.CTkFont(size=12), wraplength=270, justify="left")
        self.loc_status.pack(anchor="w", padx=16)
        ctk.CTkButton(c2, text="◎  Detect my location", height=34, fg_color=GREEN,
                      hover_color=GREEN_DARK, command=self._detect_location
                      ).pack(fill="x", padx=16, pady=(10, 6))
        row = ctk.CTkFrame(c2, fg_color="transparent")
        row.pack(fill="x", padx=16)
        self.coord_entry = ctk.CTkEntry(row, placeholder_text="lat, lon", height=32,
                                        border_color=BORDER, fg_color="#FAFCFA", text_color=TEXT)
        self.coord_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.coord_entry.bind("<Return>", lambda e: self._set_manual_location())
        ctk.CTkButton(row, text="Set", width=56, height=32, fg_color="#E5F5EB",
                      hover_color="#D0EEDB", text_color=GREEN_DARK,
                      command=self._set_manual_location).pack(side="left")
        ctk.CTkLabel(c2, text="Tip: right-click anywhere on the map to set your location or add a bin there.",
                     text_color=MUTED, font=ctk.CTkFont(size=10), wraplength=270,
                     justify="left").pack(anchor="w", padx=16, pady=(8, 14))
        self._update_loc_status("Location set" if self.user_loc else None)

        # --- results
        c3 = self._card(panel)
        c3.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(c3, text="NEAREST BINS", text_color=MUTED,
                     font=ctk.CTkFont(size=9, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))
        self.results_frame = ctk.CTkFrame(c3, fg_color="transparent")
        self.results_frame.pack(fill="x", padx=10, pady=(0, 10))

        # --- selected bin details
        self.detail_card = self._card(panel)
        self.detail_card.pack(fill="x", pady=(0, 10))
        self.detail_frame = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        self.detail_frame.pack(fill="x")

        ctk.CTkButton(panel, text="＋  Add a dustbin I found", height=42, corner_radius=11,
                      fg_color="#FFFFFF", hover_color="#E5F6EB", text_color=GREEN_DARK,
                      border_width=1, border_color=GREEN, font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda: self._open_add_bin_dialog()).pack(fill="x", pady=(0, 6))

        # --- map
        map_card = self._card(wrap)
        map_card.grid(row=0, column=1, sticky="nsew")
        self.map_widget = tkintermapview.TkinterMapView(map_card, corner_radius=16)
        self.map_widget.pack(fill="both", expand=True, padx=3, pady=3)
        if self.user_loc:
            self.map_widget.set_position(*self.user_loc)
            self.map_widget.set_zoom(15)
        else:
            self.map_widget.set_position(*DEFAULT_CENTER)
            self.map_widget.set_zoom(11)
        self.map_widget.add_right_click_menu_command(
            label="📍 Set my location here", command=self._map_set_location, pass_coords=True)
        self.map_widget.add_right_click_menu_command(
            label="➕ Add dustbin here", command=self._map_add_bin, pass_coords=True)

        self._refresh_bins(fit=bool(self.user_loc))
        self._render_detail(None)

    # ---- location

    def _update_loc_status(self, text):
        if not self.user_loc:
            self.loc_status.configure(text="Not set yet. Detect it, enter coordinates, or right-click the map.")
            return
        lat, lon = self.user_loc
        self.loc_status.configure(text=f"{text}\n{lat:.5f}, {lon:.5f}")

    def _set_user_location(self, lat, lon, label):
        self.user_loc = (lat, lon)
        if self._bins_page_alive():
            self._update_loc_status(label)
            self._refresh_bins(fit=True)

    def _detect_location(self):
        self.loc_status.configure(text="Detecting location...")
        threading.Thread(target=self._detect_worker, daemon=True).start()

    def _detect_worker(self):
        """Approximate (IP-based) location. A desktop PC has no GPS."""
        providers = [
            ("https://ipapi.co/json/", lambda d: (float(d["latitude"]), float(d["longitude"]), d.get("city", ""))),
            ("https://ipinfo.io/json", lambda d: (*map(float, d["loc"].split(",")), d.get("city", ""))),
        ]
        for url, parse in providers:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "EcoSort/1.0"})
                with urllib.request.urlopen(req, timeout=7) as resp:
                    lat, lon, city = parse(json.load(resp))
                label = f"Approximate location ({city})" if city else "Approximate location"
                self.after(0, lambda: self._set_user_location(lat, lon, label))
                return
            except Exception:
                continue
        self.after(0, self._detect_failed)

    def _detect_failed(self):
        if self._bins_page_alive():
            self.loc_status.configure(
                text="Couldn't detect your location (no internet?). Enter coordinates or right-click the map.")

    @staticmethod
    def _parse_coords(text):
        try:
            lat, lon = [float(p) for p in text.replace(";", ",").split(",")]
        except ValueError:
            return None
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        return None

    def _set_manual_location(self):
        coords = self._parse_coords(self.coord_entry.get())
        if not coords:
            messagebox.showinfo("Coordinates", "Enter coordinates like:  28.6139, 77.2090")
            return
        self._set_user_location(*coords, "Location set manually")

    def _map_set_location(self, coords):
        self._set_user_location(coords[0], coords[1], "Location set from map")

    def _map_add_bin(self, coords):
        self._open_add_bin_dialog(coords)

    # ---- map + results

    def _bin_item_lookup(self):
        term = self.bin_item_entry.get().strip().lower()
        if not term:
            return
        key = term if term in WASTE_DATA else next(iter(
            difflib.get_close_matches(term, list(WASTE_DATA), n=1, cutoff=0.5)), None)
        if not key:
            messagebox.showinfo("Item not found", "That item isn't in the directory. Pick a waste type from the menu.")
            return
        self.bin_category_var.set(WASTE_DATA[key][0])
        self._refresh_bins(fit=True)

    def _refresh_bins(self, fit=False):
        if not self._bins_page_alive():
            return
        m = self.map_widget
        m.delete_all_marker()
        m.delete_all_path()
        category = self.bin_category_var.get()
        category = None if category == "All types" else category
        bins = self.bin_store.for_category(category)

        for b in bins:
            color = CATEGORY_COLORS.get(category or b["categories"][0], GREEN)
            m.set_marker(b["lat"], b["lon"], text=b["name"][:28], text_color=TEXT,
                         marker_color_circle="#FFFFFF", marker_color_outside=color,
                         command=lambda marker, bb=b: self._select_bin(bb))
        if self.user_loc:
            m.set_marker(*self.user_loc, text="You are here", text_color="#1D4ED8",
                         marker_color_circle="#FFFFFF", marker_color_outside="#2563EB")

        for child in self.results_frame.winfo_children():
            child.destroy()

        label = category or "any waste type"
        if not bins:
            ctk.CTkLabel(self.results_frame, wraplength=270, justify="left", text_color=MUTED,
                         font=ctk.CTkFont(size=11),
                         text=f"No bins for {label} yet. Know one? Right-click the map and choose 'Add dustbin here'."
                         ).pack(anchor="w", padx=6, pady=6)
            return

        if self.user_loc:
            shown = self.bin_store.nearest(*self.user_loc, category=category, limit=5)
        else:
            shown = bins[:5]
            ctk.CTkLabel(self.results_frame, text="Set your location to sort by distance.",
                         text_color=MUTED, font=ctk.CTkFont(size=10)).pack(anchor="w", padx=6, pady=(0, 4))

        for b in shown:
            dist = ""
            if self.user_loc:
                dist = format_distance(haversine_km(*self.user_loc, b["lat"], b["lon"])) + "  ·  "
            cats = ", ".join(c.replace(" Waste", "") for c in b["categories"])
            ctk.CTkButton(
                self.results_frame, text=f"{b['name']}\n{dist}{cats}", anchor="w", height=48,
                corner_radius=9, fg_color="#F3F8F5", hover_color="#E1F0E7", text_color=TEXT,
                font=ctk.CTkFont(size=11), command=lambda bb=b: self._select_bin(bb, center=True)
            ).pack(fill="x", pady=3)

        if self.user_loc:
            nearest = shown[0]
            m.set_path([self.user_loc, (nearest["lat"], nearest["lon"])], color=GREEN, width=3)
            if fit:
                lats = [self.user_loc[0], nearest["lat"]]
                lons = [self.user_loc[1], nearest["lon"]]
                pad = 0.002
                m.fit_bounding_box((max(lats) + pad, min(lons) - pad), (min(lats) - pad, max(lons) + pad))

    # ---- details

    def _select_bin(self, b, center=False):
        self.selected_bin = b
        if center and self._bins_page_alive():
            self.map_widget.set_position(b["lat"], b["lon"])
        self._render_detail(b)

    def _render_detail(self, b):
        for child in self.detail_frame.winfo_children():
            child.destroy()
        if b is None:
            ctk.CTkLabel(self.detail_frame, text="Select a bin on the map or list to see details and its photo.",
                         text_color=MUTED, font=ctk.CTkFont(size=11), wraplength=270, justify="left"
                         ).pack(anchor="w", padx=16, pady=14)
            return
        ctk.CTkLabel(self.detail_frame, text=b["name"], text_color=TEXT, wraplength=270, justify="left",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=16, pady=(14, 4))
        if self.user_loc:
            d = format_distance(haversine_km(*self.user_loc, b["lat"], b["lon"]))
            ctk.CTkLabel(self.detail_frame, text=f"{d} away (straight line)", text_color=GREEN_DARK,
                         font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=16)
        chips = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        chips.pack(anchor="w", padx=14, pady=6)
        for cat in b["categories"]:
            ctk.CTkLabel(chips, text=cat, text_color=CATEGORY_COLORS.get(cat, GREEN),
                         fg_color="#EEF5F0", corner_radius=8,
                         font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=2, ipadx=6, ipady=2)
        if b.get("notes"):
            ctk.CTkLabel(self.detail_frame, text=b["notes"], text_color=MUTED, wraplength=270,
                         justify="left", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=16, pady=(0, 6))
        if b.get("photo"):
            path = IMAGE_DIR / b["photo"]
            if path.exists():
                with Image.open(path) as im:
                    im = im.copy()
                w = 270
                self._detail_img = ctk.CTkImage(light_image=im, size=(w, max(1, int(im.height * w / im.width))))
                ctk.CTkLabel(self.detail_frame, image=self._detail_img, text="").pack(padx=16, pady=(0, 8))
        if b.get("source") == "sample":
            ctk.CTkLabel(self.detail_frame, text="Sample data - not a verified location",
                         text_color="#B45309", font=ctk.CTkFont(size=10)).pack(anchor="w", padx=16, pady=(0, 6))
        ctk.CTkButton(self.detail_frame, text="Get directions ↗", height=34, fg_color=GREEN,
                      hover_color=GREEN_DARK, command=lambda: self._open_directions(b)
                      ).pack(fill="x", padx=16, pady=(2, 6))
        if b.get("source") == "user":
            ctk.CTkButton(self.detail_frame, text="Remove this bin", height=30, fg_color="#FDECEC",
                          hover_color="#FAD7D7", text_color="#B91C1C",
                          command=lambda: self._remove_bin(b)).pack(fill="x", padx=16, pady=(0, 14))
        else:
            ctk.CTkFrame(self.detail_frame, height=8, fg_color="transparent").pack()

    def _open_directions(self, b):
        params = {"api": 1, "destination": f"{b['lat']},{b['lon']}", "travelmode": "walking"}
        if self.user_loc:
            params["origin"] = f"{self.user_loc[0]},{self.user_loc[1]}"
        webbrowser.open("https://www.google.com/maps/dir/?" + urllib.parse.urlencode(params))

    def _remove_bin(self, b):
        if messagebox.askyesno("Remove bin", f"Remove '{b['name']}' from EcoSort?"):
            self.bin_store.remove(b["id"])
            self._render_detail(None)
            self._refresh_bins()

    # ---- add-a-bin dialog

    def _open_add_bin_dialog(self, coords=None):
        coords = coords or self.user_loc
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add a dustbin")
        dlg.geometry("460x740")
        dlg.configure(fg_color=BG)
        dlg.transient(self)
        dlg.after(150, lambda: dlg.winfo_exists() and dlg.grab_set())

        form = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=14, pady=14)

        def label(text):
            ctk.CTkLabel(form, text=text, text_color=MUTED,
                         font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(12, 4))

        ctk.CTkLabel(form, text="Found a bin that's missing?", text_color=TEXT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(form, text="Add it so others can find it too. You'll earn +15 Eco Points.",
                     text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w")

        label("NAME / LANDMARK")
        name_entry = ctk.CTkEntry(form, placeholder_text="e.g. Blue bin outside City Mall gate 2", height=36)
        name_entry.pack(fill="x")

        label("LOCATION (latitude, longitude)")
        loc_entry = ctk.CTkEntry(form, placeholder_text="28.6139, 77.2090", height=36)
        loc_entry.pack(fill="x")
        if coords:
            loc_entry.insert(0, f"{coords[0]:.6f}, {coords[1]:.6f}")

        def use_my_location():
            if self.user_loc:
                loc_entry.delete(0, "end")
                loc_entry.insert(0, f"{self.user_loc[0]:.6f}, {self.user_loc[1]:.6f}")
            else:
                messagebox.showinfo("Location", "Set your location first (Detect, or right-click the map).", parent=dlg)

        ctk.CTkButton(form, text="Use my current location", height=30, fg_color="#E5F5EB",
                      hover_color="#D0EEDB", text_color=GREEN_DARK, command=use_my_location
                      ).pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(form, text="Tip: if you're standing next to the bin, your location is the bin's location.\n"
                                "Otherwise right-click the exact spot on the map and choose 'Add dustbin here'.",
                     text_color=MUTED, font=ctk.CTkFont(size=10), justify="left", wraplength=400
                     ).pack(anchor="w", pady=(4, 0))

        label("WHAT CAN GO IN IT?")
        cat_vars = {}
        for cat in BIN_CATEGORIES:
            var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(form, text=cat, variable=var, fg_color=GREEN, hover_color=GREEN_DARK,
                            text_color=TEXT, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=3)
            cat_vars[cat] = var

        label("NOTES (optional)")
        notes_box = ctk.CTkTextbox(form, height=64, border_width=1, border_color=BORDER)
        notes_box.pack(fill="x")

        label("PHOTO (optional)")
        photo = {"path": None, "img": None}
        photo_label = ctk.CTkLabel(form, text="No photo selected", text_color=MUTED, font=ctk.CTkFont(size=11))

        def choose_photo():
            path = filedialog.askopenfilename(
                parent=dlg, title="Choose a photo of the bin",
                filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
            if not path:
                return
            try:
                with Image.open(path) as im:
                    im = im.convert("RGB")
                    im.thumbnail((200, 200))
                    preview = im.copy()
            except Exception:
                messagebox.showerror("Photo", "That file couldn't be opened as an image.", parent=dlg)
                return
            photo["path"] = path
            photo["img"] = ctk.CTkImage(light_image=preview, size=preview.size)
            photo_label.configure(image=photo["img"], text="")

        ctk.CTkButton(form, text="Choose photo...", height=34, fg_color=GREEN,
                      hover_color=GREEN_DARK, command=choose_photo).pack(anchor="w")
        photo_label.pack(anchor="w", pady=6)

        def submit():
            name = name_entry.get().strip()
            pos = self._parse_coords(loc_entry.get())
            cats = [c for c, v in cat_vars.items() if v.get()]
            if not name:
                messagebox.showinfo("Missing name", "Please give the bin a name or landmark.", parent=dlg)
            elif not pos:
                messagebox.showinfo("Location", "Enter a valid location like: 28.6139, 77.2090", parent=dlg)
            elif not cats:
                messagebox.showinfo("Waste types", "Select at least one type of waste it accepts.", parent=dlg)
            else:
                try:
                    entry = self.bin_store.add(name, pos[0], pos[1], cats,
                                               notes_box.get("1.0", "end").strip(), photo["path"])
                except Exception as exc:
                    messagebox.showerror("Couldn't save", f"Saving failed: {exc}", parent=dlg)
                    return
                self.points += 15
                dlg.destroy()
                if self._bins_page_alive():
                    self._refresh_bins()
                    self._select_bin(entry, center=True)
                messagebox.showinfo("Thank you!", "Dustbin added. +15 Eco Points earned.")
                return

        ctk.CTkButton(form, text="Save dustbin", height=42, corner_radius=11, fg_color=GREEN,
                      hover_color=GREEN_DARK, font=ctk.CTkFont(size=13, weight="bold"),
                      command=submit).pack(fill="x", pady=(18, 10))

    # ---------------------- HELPERS ----------------------

    def _rank(self):
        if self.points >= 50:
            return "Planet Protector", 100
        if self.points >= 20:
            return "Green Champion", 50
        return "Eco Beginner", 20

    def _refresh_overview_if_needed(self):
        if self.active_page == "Overview":
            self.show_page("Overview")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = EcoSortApp()
    app.run()
