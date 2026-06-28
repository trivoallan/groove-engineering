#!/usr/bin/env python3
"""groove-engineering PoC — the method is the source; models are backends.

A fusion is described ONCE (fusions.json), independently of any model.
A compiler renders it to a target. Suno is just one target among others
(we show two here: Suno and a human brief).

Suno prompts are emitted in English (project rule).

Usage:
    python3 compile.py            # compile all fusions -> Suno + brief
    python3 compile.py --check    # self-check (no model required)
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
    """Reference exemplars (genre-atom properties), validated by experts."""
    out = []
    for side in ("groove_from", "harmony_from"):
        ex = f.get(side, {}).get("exemplar")
        if ex:
            out.append(ex)
    return out


def compile_suno(f):
    """Representation -> Suno style prompt (English, comma-separated tags)."""
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
    """Same representation -> human brief (another backend, proves decoupling)."""
    parts = [f"Fusion {f['genre_a']} x {f['genre_b']}."]
    if f.get("constraints"):
        cs = "; ".join(
            f"{c['claim']} (per {', '.join(c.get('held_by', ['?']))})"
            for c in f["constraints"]
        )
        parts.append(f"Held positions (not objective truths): {cs}.")
    parts += [
        f"Groove from {f['groove_from']['genre']}: {f['groove_from']['desc']}.",
        f"Harmony from {f['harmony_from']['genre']}: {f['harmony_from']['desc']}.",
        f"Instruments: {', '.join(f['instrumentation'])}.",
        f"Production: {f['production']} ({f['tempo_feel']}).",
        f"Tension to hold: {f['tension']}.",
        f"Avoid: {f.get('avoid', '-')}.",
    ]
    ex = exemplars(f)
    if ex:
        ex_str = "; ".join(
            f"{e['track']} ({e.get('cue', '')}, ref. {', '.join(e.get('validated_by', []))})"
            for e in ex
        )
        parts.append(f"Exemplars: {ex_str}.")
    if f.get("ressenti"):
        rs = "; ".join(
            f"{r['text']} (per {', '.join(r.get('held_by', ['?']))})"
            for r in f["ressenti"]
        )
        parts.append(f"Felt: {rs}.")
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
        print("--- HUMAN BRIEF ---")
        print(compile_brief(f))
        print()


def check():
    fusions = load_fusions()
    assert fusions, "no fusions"
    for f in fusions:
        missing = REQUIRED - f.keys()
        assert not missing, f"{f.get('id', '?')} missing {missing}"
        prompt, _ = compile_suno(f)
        assert f["genre_a"].lower() in prompt.lower(), f"{f['id']}: genre_a missing from prompt"
        assert compile_brief(f), f"{f['id']}: empty brief"
    print(f"ok: {len(fusions)} fusions -> Suno + brief (2 backends from 1 source)")


if __name__ == "__main__":
    check() if "--check" in sys.argv else render_all()
