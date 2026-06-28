#!/usr/bin/env python3
"""groove-engineer PoC — la methode est la source ; les modeles sont des backends.

Une fusion est decrite UNE fois (fusions.json), independamment de tout modele.
Un compilateur la rend vers une cible. Suno n'est qu'une cible parmi d'autres
(on en montre deux : Suno et un brief humain).

Prompts Suno emis en anglais (regle projet).

Usage:
    python3 compile.py            # compile toutes les fusions -> Suno + brief
    python3 compile.py --check    # self-check (pas de modele requis)
"""
import json
import sys
from pathlib import Path

FUSIONS = Path(__file__).parent / "fusions.json"

REQUIRED = {"id", "genre_a", "genre_b", "groove_from", "harmony_from",
            "instrumentation", "production", "tempo_feel", "references"}


def load_fusions():
    return json.loads(FUSIONS.read_text(encoding="utf-8"))


def exemplars(f):
    """Exemplaires de reference (proprietes d'atomes de genre), valides par des experts."""
    out = []
    for side in ("groove_from", "harmony_from"):
        ex = f.get(side, {}).get("exemplar")
        if ex:
            out.append(ex)
    return out


def compile_suno(f):
    """Representation -> prompt de style Suno (anglais, tags separes par virgules)."""
    refs = list(f["references"]) + [e["track"] for e in exemplars(f)]
    parts = [f"{f['genre_a']} x {f['genre_b']} fusion"]
    if f.get("constraints"):
        parts.append("; ".join(c["claim"] for c in f["constraints"]))
    parts += [
        f["groove_from"]["desc"],
        f["harmony_from"]["desc"],
        ", ".join(f["instrumentation"]),
        f["production"],
        f["tempo_feel"],
        "in the spirit of " + ", ".join(refs),
    ]
    if f.get("vocal"):
        parts.append(f["vocal"])
    return ", ".join(parts), f.get("avoid", "")


def compile_brief(f):
    """Meme representation -> brief humain (autre backend, prouve le decouplage)."""
    parts = [f"Fusion {f['genre_a']} x {f['genre_b']}."]
    if f.get("constraints"):
        cs = "; ".join(
            f"{c['claim']} (selon {', '.join(c.get('held_by', ['?']))})"
            for c in f["constraints"]
        )
        parts.append(f"Positions tenues (pas des verites objectives) : {cs}.")
    parts += [
        f"Groove de {f['groove_from']['genre']} : {f['groove_from']['desc']}.",
        f"Harmonie de {f['harmony_from']['genre']} : {f['harmony_from']['desc']}.",
        f"Instruments : {', '.join(f['instrumentation'])}.",
        f"Prod : {f['production']} ({f['tempo_feel']}).",
        f"Tension a tenir : {f['tension']}.",
        f"A eviter : {f.get('avoid', '-')}.",
    ]
    ex = exemplars(f)
    if ex:
        ex_str = "; ".join(
            f"{e['track']} ({e.get('cue', '')}, ref. {', '.join(e.get('validated_by', []))})"
            for e in ex
        )
        parts.append(f"Exemplaires : {ex_str}.")
    return " ".join(parts)


def render_all():
    for f in load_fusions():
        prompt, exclude = compile_suno(f)
        print("=" * 72)
        print(f["id"])
        print("--- SUNO (style prompt, EN) ---")
        print(prompt)
        if exclude:
            print(f"[exclude] {exclude}")
        print("--- BRIEF HUMAIN (FR) ---")
        print(compile_brief(f))
        print()


def check():
    fusions = load_fusions()
    assert fusions, "no fusions"
    for f in fusions:
        missing = REQUIRED - f.keys()
        assert not missing, f"{f.get('id', '?')} missing {missing}"
        prompt, _ = compile_suno(f)
        assert f["genre_a"].lower() in prompt.lower(), f"{f['id']}: genre_a absent du prompt"
        assert compile_brief(f), f"{f['id']}: brief vide"
    print(f"ok: {len(fusions)} fusions -> Suno + brief (2 backends depuis 1 source)")


if __name__ == "__main__":
    check() if "--check" in sys.argv else render_all()
