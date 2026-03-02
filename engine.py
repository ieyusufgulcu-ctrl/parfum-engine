import json
from kerykeion import AstrologicalSubject, NatalAspects

NOTE_TR = {
    "Blackberry": "Böğürtlen", "Cucumber": "Salatalık", "Almond": "Badem",
    "Musk": "Misk", "Apricot": "Kayısı", "Lavender": "Lavanta",
    "Amber": "Amber", "Violet": "Menekşe", "Linden": "Ihlamur",
    "Orange": "Portakal", "Rose": "Gül", "Vanilla": "Vanilya",
    "Ocean": "Okyanus", "Tangerine": "Mandalina", "Cinnamon": "Tarçın",
    "Lilac": "Leylak", "Chocolate": "Çikolata", "Jasmine": "Yasemin",
    "Lily": "Zambak", "Sandalwood": "Sandal", "Pine": "Çam",
    "Eucalyptus": "Okaliptüs", "Magnolia": "Manolya", "Narcissus": "Nergis",
    "Chamomile": "Papatya", "Bay Tree": "Defne", "Caramel": "Karamel",
    "Patchouli": "Patchouli", "Coconut": "Hindistan Cevizi",
    "Green Apple": "Yeşil Elma", "Green Tea": "Yeşil Çay", "Latte": "Latte",
    "Royal Oud": "Oud", "Cedar Tree": "Sedir Ağacı", "Ylang Ylang": "Ylang Ylang",
    "Lemon": "Limon", "Melon": "Kavun", "Grape": "Üzüm",
    "Cashmere": "Kaşmir", "Japanese Cherry": "Japon Kirazı", "Mango": "Mango",
    "Baby Powder": "Pudra", "Olive": "Zeytin", "Musk Amber": "Misk Amber",
    "Rosemary": "Biberiye", "Clove": "Karanfil", "Sage": "Ada Çayı",
    "Menthol": "Mentol", "Lotus": "Lotus", "Peach": "Şeftali",
    "Silverberry": "İğde", "Pomegranate": "Nar", "Hyacinth": "Sümbül",
    "Coffee": "Kahve", "Honey": "Bal", "Lilium": "Lilium",
    "Fig": "İncir", "Honeysuckle": "Hanımeli", "Aloe Vera": "Aloe Vera",
    "Lime": "Lime", "Bergamot": "Bergamot", "Gum": "Sakız",
    "Red Flowers": "Kırmızı Çiçekler", "Summer Fresh": "Yaz Ferahlığı",
    "White Poppy": "Komşu Çatlatan", "Banana": "Muz", "Orchid": "Orkide",
    "Acacia": "Akasya", "Juniper": "Ardıç", "L'Afrodizyak d'Or": "L'Afrodizyak d'Or",
    "Avocado": "Avokado", "Istanbul": "İstanbul", "Peony": "Şakayık",
    "Black Pepper": "Karabiber", "Blue Anemone": "Mavi Anemon",
    "Thyme": "Kekik", "Pear": "Armut", "Mastic Gum": "Damla Sakızı",
    "Cardamom": "Kakule",
}

SIGN_TR = {
    "aries": "Koç", "taurus": "Boğa", "gemini": "İkizler", "cancer": "Yengeç",
    "leo": "Aslan", "virgo": "Başak", "libra": "Terazi", "scorpio": "Akrep",
    "sagittarius": "Yay", "capricorn": "Oğlak", "aquarius": "Kova", "pisces": "Balık",
}

ELEM_TR = {"fire": "Ateş", "earth": "Toprak", "air": "Hava", "water": "Su"}

TAG_TR = {
    "floral": "çiçeksi", "woody": "odunsu", "fresh": "ferah", "spicy": "baharatlı",
    "oriental": "oriental", "gourmand": "gourmand", "aquatic": "aquatik",
    "resinous": "reçineli", "powdery": "pudramsı", "earthy": "toprak",
    "citrus": "narenciye", "warm": "sıcak", "sweet": "tatlı", "dark": "derin",
    "sensual": "duyusal", "clean": "temiz", "aromatic": "aromatik",
    "green": "yeşil", "exotic": "egzotik", "creamy": "kremsi",
}

def to_tr(note_name):
    return NOTE_TR.get(note_name, note_name)

def note_family(note):
    """Return primary Turkish family description for a note."""
    tags = note.get("tags", [])
    for tag in ["floral", "woody", "citrus", "spicy", "aquatic", "oriental",
                "resinous", "aromatic", "gourmand", "earthy"]:
        if tag in tags:
            return TAG_TR.get(tag, tag)
    return TAG_TR.get(tags[0], tags[0]) if tags else ""

def generate_description(top, heart, base, target, chart):
    """Generate a personal Turkish description from templates."""
    import random

    ps = chart["planet_signs"]
    sun  = SIGN_TR.get(ps.get("sun", ""), "")
    moon = SIGN_TR.get(ps.get("moon", ""), "")
    asc  = SIGN_TR.get(ps.get("asc", ""), "")

    elem_pcts = {
        "fire": chart["fire_pct"], "earth": chart["earth_pct"],
        "air":  chart["air_pct"],  "water": chart["water_pct"],
    }
    dom_elem = max(elem_pcts, key=elem_pcts.get)
    dom_tr = ELEM_TR[dom_elem]

    # Atmosphere from dominant element
    elem_atmo = {
        "fire":  "tutuşturan, enerjik ve ısıtan",
        "earth": "toprak kokulu, kalıcı ve güven veren",
        "air":   "uçucu, ferah ve özgür",
        "water": "derin, akışkan ve sezgisel",
    }
    atmo = elem_atmo[dom_elem]

    # Tone from darkness/sensuality
    darkness = target.get("darkness", 0)
    sensuality = target.get("sensuality", 0)
    comfort = target.get("comfort", 0)

    if darkness >= 3 and sensuality >= 3:
        tone = "gizemli ve baştan çıkarıcı"
    elif comfort >= 4:
        tone = "sarıp sarmalayan ve güven veren"
    elif sensuality >= 3:
        tone = "duyusal ve akılda kalıcı"
    elif darkness >= 3:
        tone = "derin ve karmaşık"
    else:
        tone = "dengeli ve zarif"

    # Top notes description
    top_names = [to_tr(n["note"]) for n in top]
    top_family = note_family(top[0]) if top else ""
    top_str = " ve ".join(top_names)

    # Heart notes
    heart_names = [to_tr(n["note"]) for n in heart]
    heart_str = ", ".join(heart_names[:-1]) + " ve " + heart_names[-1] if len(heart_names) > 1 else heart_names[0]

    # Base notes
    base_names = [to_tr(n["note"]) for n in base]
    base_str = " ve ".join(base_names[:2])

    # Opening sentences variants
    openings = [
        f"{sun} güneşinin gücü ve {asc} yükselenin hassasiyetiyle yoğrulmuş bu formül, sizi tam olarak yansıtmak için tasarlandı.",
        f"{sun} enerjisi ve {moon} ayının derinliğini taşıyan bu imza koku, astrolojik haritanızdan damıtıldı.",
        f"Haritanızdaki baskın {dom_tr} elementinin (%{elem_pcts[dom_elem]:.0f}) izinden gidilerek kişiselleştirilen bu formül, {atmo} bir karakter taşıyor.",
    ]

    # Layer descriptions
    layer_desc = (
        f"{top_str} ile ferah ve {top_family} bir açılış yapan koku, "
        f"kalbinde {heart_str} ile derinleşiyor. "
        f"Taban notaları {base_str}, kalıcılığı ve imzanızı oluşturuyor."
    )

    # Closing
    closings = [
        f"Tüm bunlar bir araya gelince ortaya {tone} bir imza koku çıkıyor.",
        f"Sonuç; size özel, {tone} ve unutulmaz bir iz.",
        f"Bu denge, {tone} bir kişilik için biçilmiş kaftan.",
    ]

    desc = random.choice(openings) + " " + layer_desc + " " + random.choice(closings)
    return desc


def load_engine():
    with open("fragrance_engine.json", "r", encoding="utf-8") as f:
        return json.load(f)


SIGN_NORMALIZE = {
    # 3-letter abbreviations (Kerykeion default)
    "ari": "aries",   "tau": "taurus",  "gem": "gemini",
    "can": "cancer",  "leo": "leo",      "vir": "virgo",
    "lib": "libra",   "sco": "scorpio",  "sag": "sagittarius",
    "cap": "capricorn","aqu": "aquarius","pis": "pisces",
    # full names pass through unchanged
    "aries": "aries", "taurus": "taurus", "gemini": "gemini",
    "cancer": "cancer", "virgo": "virgo", "libra": "libra",
    "scorpio": "scorpio", "sagittarius": "sagittarius",
    "capricorn": "capricorn", "aquarius": "aquarius", "pisces": "pisces",
}

SIGN_ELEMENT = {
    "aries": "fire", "leo": "fire", "sagittarius": "fire",
    "taurus": "earth", "virgo": "earth", "capricorn": "earth",
    "gemini": "air", "libra": "air", "aquarius": "air",
    "cancer": "water", "scorpio": "water", "pisces": "water",
}

SIGN_MODALITY = {
    "aries": "cardinal", "cancer": "cardinal", "libra": "cardinal", "capricorn": "cardinal",
    "taurus": "fixed", "leo": "fixed", "scorpio": "fixed", "aquarius": "fixed",
    "gemini": "mutable", "virgo": "mutable", "sagittarius": "mutable", "pisces": "mutable",
}

def calc_element_modality(planet_signs):
    """Calculate element and modality percentages from planet signs."""
    # Weighted planets: personal planets count more
    weights = {
        "sun": 3, "moon": 3, "asc": 3,
        "venus": 2, "mars": 2,
        "mercury": 1, "jupiter": 1, "saturn": 1,
        "neptune": 1, "pluto": 1,
    }

    elem_score = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    modal_score = {"cardinal": 0, "fixed": 0, "mutable": 0}
    total = 0

    for planet, sign in planet_signs.items():
        if not sign:
            continue
        w = weights.get(planet, 1)
        elem = SIGN_ELEMENT.get(sign)
        mod  = SIGN_MODALITY.get(sign)
        if elem:
            elem_score[elem] += w
        if mod:
            modal_score[mod] += w
        total += w

    if total == 0:
        return 25.0, 25.0, 25.0, 25.0, 33.3, 33.3, 33.4

    fire_pct      = round(elem_score["fire"]  / total * 100, 1)
    earth_pct     = round(elem_score["earth"] / total * 100, 1)
    air_pct       = round(elem_score["air"]   / total * 100, 1)
    water_pct     = round(elem_score["water"] / total * 100, 1)
    cardinal_pct  = round(modal_score["cardinal"] / total * 100, 1)
    fixed_pct     = round(modal_score["fixed"]    / total * 100, 1)
    mutable_pct   = round(modal_score["mutable"]  / total * 100, 1)

    return fire_pct, earth_pct, air_pct, water_pct, cardinal_pct, fixed_pct, mutable_pct


def get_chart_data(person):
    """Extract all needed data from Kerykeion AstrologicalSubject."""

    def safe_sign(planet_obj):
        try:
            raw = planet_obj.sign.lower().strip()
            return SIGN_NORMALIZE.get(raw, raw)
        except Exception:
            return None

    def safe_house(planet_obj):
        try:
            # Kerykeion stores house as int or string like "First_House"
            h = planet_obj.house
            if isinstance(h, int):
                return h
            # Some versions return "First_House", "Second_House" etc.
            house_map = {
                "First_House": 1, "Second_House": 2, "Third_House": 3,
                "Fourth_House": 4, "Fifth_House": 5, "Sixth_House": 6,
                "Seventh_House": 7, "Eighth_House": 8, "Ninth_House": 9,
                "Tenth_House": 10, "Eleventh_House": 11, "Twelfth_House": 12,
            }
            if str(h) in house_map:
                return house_map[str(h)]
            return int(h)
        except Exception:
            return None

    planet_signs = {
        "sun":     safe_sign(person.sun),
        "moon":    safe_sign(person.moon),
        "venus":   safe_sign(person.venus),
        "mars":    safe_sign(person.mars),
        "asc":     safe_sign(person.first_house),
        "jupiter": safe_sign(person.jupiter),
        "saturn":  safe_sign(person.saturn),
        "neptune": safe_sign(person.neptune),
        "pluto":   safe_sign(person.pluto),
    }

    planet_houses = {
        "sun":     safe_house(person.sun),
        "moon":    safe_house(person.moon),
        "venus":   safe_house(person.venus),
        "mars":    safe_house(person.mars),
        "jupiter": safe_house(person.jupiter),
        "saturn":  safe_house(person.saturn),
        "neptune": safe_house(person.neptune),
        "pluto":   safe_house(person.pluto),
    }

    # Calculate elements & modalities ourselves — avoids Kerykeion version issues
    (fire_pct, earth_pct, air_pct, water_pct,
     cardinal_pct, fixed_pct, mutable_pct) = calc_element_modality(planet_signs)

    # Parse aspects — handle both dict and object style responses
    aspects_raw = []
    try:
        natal_aspects = NatalAspects(person)
        for asp in natal_aspects.relevant_aspects:
            if isinstance(asp, dict):
                p1   = asp.get("p1_name", asp.get("p1", "")).lower()
                p2   = asp.get("p2_name", asp.get("p2", "")).lower()
                atype = asp.get("aspect", asp.get("type", "")).lower()
            else:
                p1    = getattr(asp, "p1_name", getattr(asp, "p1", "")).lower()
                p2    = getattr(asp, "p2_name", getattr(asp, "p2", "")).lower()
                atype = getattr(asp, "aspect", getattr(asp, "type", "")).lower()
            if p1 and p2 and atype:
                aspects_raw.append({"p1": p1, "p2": p2, "type": atype})
    except Exception:
        pass

    return {
        "planet_signs":  planet_signs,
        "planet_houses": planet_houses,
        "aspects":       aspects_raw,
        "fire_pct":      fire_pct,
        "earth_pct":     earth_pct,
        "air_pct":       air_pct,
        "water_pct":     water_pct,
        "cardinal_pct":  cardinal_pct,
        "fixed_pct":     fixed_pct,
        "mutable_pct":   mutable_pct,
        "sun_sign":      safe_sign(person.sun),
        "moon_sign":     safe_sign(person.moon),
        "asc_sign":      safe_sign(person.first_house),
    }


def build_target_profile(chart, engine):
    """Accumulate weighted deltas into a target attribute vector."""
    target = {a: 0.0 for a in ["temperature","density","sweetness","darkness","comfort","freshness","sensuality","projection"]}
    layer_bias = {"top": 0.0, "heart": 0.0, "base": 0.0}
    element_affinity = {"fire": 0.0, "earth": 0.0, "air": 0.0, "water": 0.0}

    weights = engine["weight_hierarchy"]
    planet_mods = engine["astro_modifier_model"]["planet_sign_modifiers"]

    # --- Planet × Sign modifiers ---
    for planet, sign in chart["planet_signs"].items():
        if not sign or planet not in planet_mods:
            continue
        if sign not in planet_mods[planet]:
            continue
        w = weights.get(planet, 0) / 100.0
        mod = planet_mods[planet][sign]
        for attr in target:
            target[attr] += w * mod.get(f"{attr}_delta", 0)
        for layer in layer_bias:
            layer_bias[layer] += w * mod["layer_bias"][layer]
        for elem in element_affinity:
            element_affinity[elem] += w * mod["element_delta"][elem]

    # --- Element distribution modifiers ---
    elem_mods = engine["astro_modifier_model"]["element_distribution_modifiers"]
    elem_w = weights.get("elements", 0) / 100.0
    for elem, pct in [
        ("fire",  chart["fire_pct"]),
        ("earth", chart["earth_pct"]),
        ("air",   chart["air_pct"]),
        ("water", chart["water_pct"]),
    ]:
        per10 = elem_mods[elem]["per_10pct"]
        mult = (pct / 10.0) * elem_w
        for attr in target:
            target[attr] += mult * per10.get(f"{attr}_delta", 0)
        for layer in layer_bias:
            layer_bias[layer] += mult * per10.get("layer_bias", {}).get(layer, 0)

    # --- Modality modifiers ---
    mod_mods = engine["astro_modifier_model"]["modality_modifiers"]
    modal_w = weights.get("modalities", 0) / 100.0
    for modality, pct in [
        ("cardinal", chart["cardinal_pct"]),
        ("fixed",    chart["fixed_pct"]),
        ("mutable",  chart["mutable_pct"]),
    ]:
        if modality not in mod_mods:
            continue
        per10 = mod_mods[modality].get("per_10pct", {})
        mult = (pct / 10.0) * modal_w
        for attr in target:
            target[attr] += mult * per10.get(f"{attr}_delta", 0)
        for layer in layer_bias:
            layer_bias[layer] += mult * per10.get("layer_bias", {}).get(layer, 0)

    # --- House modifiers (one modifier per planet's house) ---
    house_mods = engine["astro_modifier_model"]["house_modifiers"]
    house_w = weights.get("houses", 0) / 100.0
    for planet, house_num in chart["planet_houses"].items():
        if house_num is None:
            continue
        h = str(house_num)
        if h not in house_mods:
            continue
        mod = house_mods[h]
        for attr in target:
            target[attr] += house_w * mod.get(f"{attr}_delta", 0)
        for layer in layer_bias:
            layer_bias[layer] += house_w * mod["layer_bias"][layer]
        for elem in element_affinity:
            element_affinity[elem] += house_w * mod.get("element_delta", {}).get(elem, 0)

    # --- Aspect modifiers ---
    aspect_mods = engine["astro_modifier_model"]["aspect_modifiers"]
    aspect_w = weights.get("aspects", 0) / 100.0
    for asp in chart["aspects"]:
        p1, p2, asp_type = asp["p1"], asp["p2"], asp["type"]
        mod_dict = aspect_mods.get(f"{p1}_{p2}") or aspect_mods.get(f"{p2}_{p1}")
        if not mod_dict or asp_type not in mod_dict:
            continue
        mod = mod_dict[asp_type]
        for attr in target:
            key = f"{attr}_delta"
            if key in mod:
                target[attr] += aspect_w * mod[key]

    # --- Clamp ---
    clamp = {
        "temperature": (-2, 2), "density": (1, 5), "sweetness": (0, 5),
        "darkness": (0, 5), "comfort": (0, 5), "freshness": (0, 5),
        "sensuality": (0, 5), "projection": (1, 5),
    }
    for attr, (lo, hi) in clamp.items():
        target[attr] = max(lo, min(hi, target[attr]))

    return target, layer_bias, element_affinity


def collect_house_tag_bonuses(chart, engine):
    """Return list of note_tag_bonus dicts for all active house modifiers."""
    house_mods = engine["astro_modifier_model"]["house_modifiers"]
    bonuses = []
    for planet, house_num in chart["planet_houses"].items():
        if house_num is None:
            continue
        h = str(house_num)
        if h in house_mods and "note_tag_bonus" in house_mods[h]:
            bonuses.append(house_mods[h]["note_tag_bonus"])
    return bonuses


def score_note(note, target, layer_bias, element_affinity, tag_bonuses):
    attr_weights = {
        "sensuality": 2.0, "darkness": 1.8, "freshness": 1.5,
        "comfort": 1.5, "temperature": 1.3, "sweetness": 1.2,
        "projection": 1.0, "density": 1.0,
    }
    score = 100.0
    for attr, w in attr_weights.items():
        score -= w * abs(note[attr] - target[attr])

    score += layer_bias.get(note["layer"], 0) * 5

    for elem in ["fire", "earth", "air", "water"]:
        score += element_affinity.get(elem, 0) * note["element_affinity"][elem] * 2

    note_tags = set(note.get("tags", []))
    for bonus_map in tag_bonuses:
        for tag, bonus in bonus_map.items():
            if tag in note_tags:
                score += bonus * 3

    return score


def dominant_element(note):
    ea = note["element_affinity"]
    return max(ea, key=ea.get)


def apply_constraints(top, heart, base, all_notes_by_layer, chart, engine):
    """Enforce all 6 constraints. Modifies lists in place."""
    all_selected = top + heart + base

    # Helper: replace lowest-scoring note in a layer list with best alternative
    def force_include(target_list, candidate, layer_list_map):
        layer = candidate["layer"]
        lst = layer_list_map[layer]
        if candidate in lst:
            return
        # Remove lowest score note (last in sorted list = lowest)
        lst.sort(key=lambda n: n["_score"], reverse=True)
        lst.pop()
        lst.append(candidate)

    layer_map = {"top": top, "heart": heart, "base": base}
    all_notes_flat = all_notes_by_layer["top"] + all_notes_by_layer["heart"] + all_notes_by_layer["base"]

    # 1. Base density cap: max 2 notes with density >= 4
    heavy = [n for n in base if n["density"] >= 4]
    if len(heavy) > 2:
        heavy.sort(key=lambda n: n["_score"])
        base.remove(heavy[0])
        # Find replacement: base note, density < 4, not already selected
        selected_names = {n["note"] for n in top + heart + base}
        for candidate in sorted(all_notes_by_layer["base"], key=lambda n: n["_score"], reverse=True):
            if candidate["note"] not in selected_names and candidate["density"] < 4:
                base.append(candidate)
                break

    # 2. Freshness minimum: at least 1 note freshness >= 3
    all_selected = top + heart + base
    if not any(n["freshness"] >= 3 for n in all_selected):
        selected_names = {n["note"] for n in all_selected}
        best_fresh = None
        for layer_key in ["top", "heart", "base"]:
            for candidate in sorted(all_notes_by_layer[layer_key], key=lambda n: n["freshness"], reverse=True):
                if candidate["note"] not in selected_names and candidate["freshness"] >= 3:
                    best_fresh = candidate
                    break
            if best_fresh:
                break
        if best_fresh:
            lst = layer_map[best_fresh["layer"]]
            lst.sort(key=lambda n: n["_score"])
            lst.pop()
            lst.append(best_fresh)

    # 3. Sweetness cap: max 2 notes sweetness >= 4
    all_selected = top + heart + base
    sweet = [n for n in all_selected if n["sweetness"] >= 4]
    while len(sweet) > 2:
        sweet.sort(key=lambda n: n["_score"])
        to_remove = sweet.pop(0)
        lst = layer_map[to_remove["layer"]]
        if to_remove in lst:
            lst.remove(to_remove)
            selected_names = {n["note"] for n in top + heart + base}
            for candidate in sorted(all_notes_by_layer[to_remove["layer"]], key=lambda n: n["_score"], reverse=True):
                if candidate["note"] not in selected_names and candidate["sweetness"] < 4:
                    lst.append(candidate)
                    break
        all_selected = top + heart + base
        sweet = [n for n in all_selected if n["sweetness"] >= 4]

    # 4. Element stacking: max 3 notes sharing same dominant element
    all_selected = top + heart + base
    from collections import Counter
    dom_counts = Counter(dominant_element(n) for n in all_selected)
    for elem, count in dom_counts.items():
        if count > 3:
            over = [n for n in all_selected if dominant_element(n) == elem]
            over.sort(key=lambda n: n["_score"])
            to_remove = over[0]
            lst = layer_map[to_remove["layer"]]
            if to_remove in lst:
                lst.remove(to_remove)
                selected_names = {n["note"] for n in top + heart + base}
                for candidate in sorted(all_notes_by_layer[to_remove["layer"]], key=lambda n: n["_score"], reverse=True):
                    if candidate["note"] not in selected_names and dominant_element(candidate) != elem:
                        lst.append(candidate)
                        break

    # 5. House 8 darkness requirement
    house_8_planets = [p for p, h in chart["planet_houses"].items() if h == 8]
    personal = {"sun", "moon", "venus", "mars", "asc"}
    house_8_high = len(house_8_planets) >= 2 or bool(set(house_8_planets) & personal)
    all_selected = top + heart + base
    if house_8_high and not any(n["darkness"] >= 4 for n in all_selected):
        selected_names = {n["note"] for n in all_selected}
        for layer_key in ["base", "heart", "top"]:
            for candidate in sorted(all_notes_by_layer[layer_key], key=lambda n: n["darkness"], reverse=True):
                if candidate["note"] not in selected_names and candidate["darkness"] >= 4:
                    lst = layer_map[candidate["layer"]]
                    lst.sort(key=lambda n: n["_score"])
                    lst.pop()
                    lst.append(candidate)
                    break
            else:
                continue
            break

    # 6. House 12 mystical requirement
    house_12_planets = [p for p, h in chart["planet_houses"].items() if h == 12]
    house_12_high = len(house_12_planets) >= 2 or bool(set(house_12_planets) & personal)
    qualifying = {"resinous", "powdery", "mystical"}
    all_selected = top + heart + base
    if house_12_high and not any(set(n.get("tags", [])) & qualifying for n in all_selected):
        selected_names = {n["note"] for n in all_selected}
        for layer_key in ["base", "heart", "top"]:
            for candidate in sorted(all_notes_by_layer[layer_key], key=lambda n: n["_score"], reverse=True):
                if candidate["note"] not in selected_names and set(candidate.get("tags", [])) & qualifying:
                    lst = layer_map[candidate["layer"]]
                    lst.sort(key=lambda n: n["_score"])
                    lst.pop()
                    lst.append(candidate)
                    break
            else:
                continue
            break

    return top, heart, base


def generate_explanations(top, heart, base, target, chart):
    reasons = []
    all_notes = top + heart + base

    # 1. Dominant element
    elem_pcts = {
        "fire": chart["fire_pct"], "earth": chart["earth_pct"],
        "air": chart["air_pct"], "water": chart["water_pct"],
    }
    dom_elem = max(elem_pcts, key=elem_pcts.get)
    elem_tr = {"fire": "Ateş", "earth": "Toprak", "air": "Hava", "water": "Su"}
    reasons.append(
        f"Dominant element {elem_tr[dom_elem]} (%{elem_pcts[dom_elem]:.0f}) — "
        f"nota seçimi bu elemente uyumlu kokuları ön plana çıkardı."
    )

    # 2. Sun/Moon/ASC
    sign_tr = {
        "aries": "Koç", "taurus": "Boğa", "gemini": "İkizler", "cancer": "Yengeç",
        "leo": "Aslan", "virgo": "Başak", "libra": "Terazi", "scorpio": "Akrep",
        "sagittarius": "Yay", "capricorn": "Oğlak", "aquarius": "Kova", "pisces": "Balık",
    }
    sun  = sign_tr.get(chart["sun_sign"], chart["sun_sign"].capitalize())
    moon = sign_tr.get(chart["moon_sign"], chart["moon_sign"].capitalize())
    asc  = sign_tr.get(chart["asc_sign"], chart["asc_sign"].capitalize())
    reasons.append(
        f"Güneş {sun}, Ay {moon}, Yükselen {asc} — "
        f"bu üçlü formülün sıcaklık, yoğunluk ve duyusallık hedeflerini belirledi."
    )

    # 3. Sensuality — honest gap reporting
    most_sensual = max(all_notes, key=lambda n: n["sensuality"])
    sens_gap = abs(most_sensual["sensuality"] - target["sensuality"])
    if sens_gap <= 1.0:
        reasons.append(
            f"{most_sensual['note']} duyusallık hedefini karşılıyor "
            f"(duyusallık={most_sensual['sensuality']}, hedef={target['sensuality']:.1f})."
        )
    else:
        reasons.append(
            f"Duyusallık hedefi {target['sensuality']:.1f} iken element uyumu ve kullanım zamanı "
            f"yüksek duyusal notaları baskıladı — {most_sensual['note']} ({most_sensual['sensuality']}) "
            f"en iyi denge noktası olarak seçildi."
        )

    # 4. Freshness — honest gap reporting
    freshest = max(all_notes, key=lambda n: n["freshness"])
    fresh_gap = abs(freshest["freshness"] - target["freshness"])
    if fresh_gap <= 1.5:
        reasons.append(
            f"{freshest['note']} ferahlık dengesini sağlıyor "
            f"(ferahlık={freshest['freshness']}, hedef={target['freshness']:.1f})."
        )
    else:
        reasons.append(
            f"Ferahlık hedefi {target['freshness']:.1f} — ağır base notaları baskın çıktı, "
            f"{freshest['note']} ({freshest['freshness']}) formüle hava katıyor."
        )

    # 5. Darkness
    darkest = max(all_notes, key=lambda n: n["darkness"])
    dark_gap = abs(darkest["darkness"] - target["darkness"])
    if darkest["darkness"] >= 3 and dark_gap <= 1.5:
        reasons.append(
            f"{darkest['note']} formülün karanlık/reçineli karakterini kuruyor "
            f"(derinlik={darkest['darkness']}, hedef={target['darkness']:.1f})."
        )
    elif target["darkness"] >= 3 and darkest["darkness"] < 3:
        reasons.append(
            f"Harita derin ve karanlık notalar işaret etse de element dengesi "
            f"formülü daha açık tuttu — en derin nota {darkest['note']} ({darkest['darkness']})."
        )

    # 6. Top note / açılış
    if top:
        proj_gap = abs(top[0]["projection"] - target["projection"])
        if proj_gap <= 1.5:
            reasons.append(
                f"{top[0]['note']} açılışı güçlü tutuyor "
                f"(projeksiyon={top[0]['projection']}, hedef={target['projection']:.1f})."
            )
        else:
            reasons.append(
                f"{top[0]['note']} formülü açıyor — projeksiyon hedefine ({target['projection']:.1f}) "
                f"kısmen ulaşıyor ({top[0]['projection']})."
            )

    # 7. Comfort — if very high, mention it
    avg_comfort = sum(n["comfort"] for n in all_notes) / len(all_notes)
    if avg_comfort >= 3.5:
        reasons.append(
            f"Genel konfor skoru yüksek ({avg_comfort:.1f}/5) — "
            f"bu formül günlük kullanıma çok uygun."
        )
    elif avg_comfort < 2.5:
        reasons.append(
            f"Formül konfordan çok karakter öncelikli ({avg_comfort:.1f}/5) — "
            f"güçlü ve kendine özgü bir koku."
        )

    return reasons[:8]


def compute_coherence(top, heart, base):
    """Simple coherence: 100 - score std dev penalty."""
    import statistics
    scores = [n["_score"] for n in top + heart + base]
    if len(scores) < 2:
        return 75.0
    std = statistics.stdev(scores)
    coherence = max(0, min(100, 100 - std * 1.5))
    return round(coherence, 1)


def generate_scent(data):
    engine = load_engine()

    person = AstrologicalSubject(
        data["name"],
        data["year"],
        data["month"],
        data["day"],
        data["hour"],
        data["minute"],
        data["city"],
        data["nation"],
    )

    chart = get_chart_data(person)
    target, layer_bias, element_affinity = build_target_profile(chart, engine)
    tag_bonuses = collect_house_tag_bonuses(chart, engine)

    # Score all notes
    notes = engine["note_attribute_matrix"]

    # Apply user preferences
    disliked_tags = set(data.get("disliked_tags") or [])
    usage_time = data.get("usage_time", "")
    if usage_time == "night":
        target["darkness"] = min(5, target["darkness"] + 0.5)
        target["sensuality"] = min(5, target["sensuality"] + 0.5)
        target["freshness"] = max(0, target["freshness"] - 0.3)
    elif usage_time == "day":
        target["freshness"] = min(5, target["freshness"] + 0.5)
        target["darkness"] = max(0, target["darkness"] - 0.3)

    scored = []
    for note in notes:
        # Hard filter: remove disliked tag notes
        if disliked_tags and set(note.get("tags", [])) & disliked_tags:
            continue
        s = score_note(note, target, layer_bias, element_affinity, tag_bonuses)
        note_copy = dict(note)
        note_copy["_score"] = s
        scored.append(note_copy)

    # Partition by layer and sort
    by_layer = {
        "top":   sorted([n for n in scored if n["layer"] == "top"],   key=lambda n: n["_score"], reverse=True),
        "heart": sorted([n for n in scored if n["layer"] == "heart"], key=lambda n: n["_score"], reverse=True),
        "base":  sorted([n for n in scored if n["layer"] == "base"],  key=lambda n: n["_score"], reverse=True),
    }

    # Initial selection
    top   = list(by_layer["top"][:2])
    heart = list(by_layer["heart"][:3])
    base  = list(by_layer["base"][:3])

    # Apply constraints
    top, heart, base = apply_constraints(top, heart, base, by_layer, chart, engine)

    # Compute attribute profile (average of selected notes)
    all_selected = top + heart + base
    attrs = ["temperature","density","sweetness","darkness","comfort","freshness","sensuality","projection"]
    attr_profile = {
        a: round(sum(n[a] for n in all_selected) / len(all_selected), 2)
        for a in attrs
    }

    # Dominant elements (sum of affinities)
    dom_elements = {
        e: round(sum(n["element_affinity"][e] for n in all_selected), 2)
        for e in ["fire","earth","air","water"]
    }

    coherence = compute_coherence(top, heart, base)
    explanations = generate_explanations(top, heart, base, target, chart)

    # Use normalized planet_signs for chart_summary display
    ps = chart["planet_signs"]
    description = generate_description(top, heart, base, target, chart)

    return {
        "selected_notes": {
            "top":   [to_tr(n["note"]) for n in top],
            "heart": [to_tr(n["note"]) for n in heart],
            "base":  [to_tr(n["note"]) for n in base],
        },
        "description": description,
        "chart_summary": {
            "sun_sign":  SIGN_TR.get(ps.get("sun", ""), ps.get("sun", "")),
            "moon_sign": SIGN_TR.get(ps.get("moon", ""), ps.get("moon", "")),
            "asc_sign":  SIGN_TR.get(ps.get("asc", ""), ps.get("asc", "")),
            "dominant_element": ELEM_TR.get(max(
                {"fire": chart["fire_pct"], "earth": chart["earth_pct"],
                 "air": chart["air_pct"], "water": chart["water_pct"]},
                key=lambda k: {"fire": chart["fire_pct"], "earth": chart["earth_pct"],
                               "air": chart["air_pct"], "water": chart["water_pct"]}[k]
            ), ""),
        },
        "coherence_score": coherence,
    }
