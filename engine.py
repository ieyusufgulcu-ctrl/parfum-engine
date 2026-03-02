import json
from kerykeion import AstrologicalSubject, NatalAspects


def load_engine():
    with open("fragrance_engine.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_chart_data(person):
    """Extract all needed data from Kerykeion AstrologicalSubject."""

    def safe_sign(planet_obj):
        try:
            return planet_obj.sign.lower()
        except Exception:
            return None

    def safe_house(planet_obj):
        try:
            return int(planet_obj.house)
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

    # Parse aspects
    aspects_raw = []
    try:
        natal_aspects = NatalAspects(person)
        for asp in natal_aspects.relevant_aspects:
            aspects_raw.append({
                "p1": asp.get("p1_name", "").lower(),
                "p2": asp.get("p2_name", "").lower(),
                "type": asp.get("aspect", "").lower(),
            })
    except Exception:
        pass

    return {
        "planet_signs":  planet_signs,
        "planet_houses": planet_houses,
        "aspects":       aspects_raw,
        "fire_pct":      person.fire_perc,
        "earth_pct":     person.earth_perc,
        "air_pct":       person.air_perc,
        "water_pct":     person.water_perc,
        "cardinal_pct":  person.cardinal_perc,
        "fixed_pct":     person.fixed_perc,
        "mutable_pct":   person.mutable_perc,
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

    # Dominant element
    elem_pcts = {
        "fire": chart["fire_pct"], "earth": chart["earth_pct"],
        "air": chart["air_pct"], "water": chart["water_pct"],
    }
    dom_elem = max(elem_pcts, key=elem_pcts.get)
    reasons.append(
        f"Dominant element: {dom_elem.capitalize()} (%{elem_pcts[dom_elem]:.0f}) — "
        f"note selection biased toward matching element affinities."
    )

    # Sun/Moon/ASC
    reasons.append(
        f"Sun in {chart['sun_sign'].capitalize()}, Moon in {chart['moon_sign'].capitalize()}, "
        f"ASC in {chart['asc_sign'].capitalize()} shaped the core attribute targets."
    )

    # Highest sensuality note
    most_sensual = max(all_notes, key=lambda n: n["sensuality"])
    reasons.append(
        f"{most_sensual['note']} selected as sensuality anchor "
        f"(sensuality={most_sensual['sensuality']}, target={target['sensuality']:.1f})."
    )

    # Freshness note
    freshest = max(all_notes, key=lambda n: n["freshness"])
    reasons.append(
        f"{freshest['note']} provides freshness balance "
        f"(freshness={freshest['freshness']}, target={target['freshness']:.1f})."
    )

    # Darkness note
    darkest = max(all_notes, key=lambda n: n["darkness"])
    if darkest["darkness"] >= 3:
        reasons.append(
            f"{darkest['note']} anchors the dark/resinous character "
            f"(darkness={darkest['darkness']})."
        )

    # Top note mention
    if top:
        reasons.append(
            f"{top[0]['note']} opens the fragrance — "
            f"high projection ({top[0]['projection']}) matches target {target['projection']:.1f}."
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

    return {
        "selected_notes": {
            "top":   [n["note"] for n in top],
            "heart": [n["note"] for n in heart],
            "base":  [n["note"] for n in base],
        },
        "attribute_profile": attr_profile,
        "dominant_elements": dom_elements,
        "coherence_score": coherence,
        "chart_summary": {
            "sun_sign":  chart["sun_sign"],
            "moon_sign": chart["moon_sign"],
            "asc_sign":  chart["asc_sign"],
            "elements":  {
                "fire": chart["fire_pct"], "earth": chart["earth_pct"],
                "air":  chart["air_pct"],  "water": chart["water_pct"],
            },
            "modalities": {
                "cardinal": chart["cardinal_pct"],
                "fixed":    chart["fixed_pct"],
                "mutable":  chart["mutable_pct"],
            },
        },
        "explanations": {
            "short_reasoning": explanations
        },
    }
