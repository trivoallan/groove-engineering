#!/usr/bin/env python3
"""groove-engineering — compile genre atoms + crossings into a backend prompt.

The repo IS the graph: atoms/<genre>.yaml + crossings/<a>-x-<b>.yaml, validated
by schema.py. This module loads them, checks referential integrity, filters
claims by compile mode, and composes a crossing into a Suno prompt + human brief.

  load_atoms()  load_crossings()
        │              │
        ▼              ▼
   {name: Atom}   [Crossing]
        └──────┬───────┘
               ▼
        check_refs()  ── crossing.atoms / frame_from must exist ──▶ UnknownAtom
               ▼
   select_claims(atom, mode)          mode = draft | strict
     draft  : proposed + validated    (the ear judges, §7)
     strict : validated only          (vetted, once a musicologist exists)
     contested: NEVER compiled        (the divergence is held in storage, §3)
               ▼
        compose_suno(crossing, atoms, mode) ──▶ (prompt, avoid)

See: process/rfc/atoms-knowledge-graph.md  ·  tests: test_atomgraph.py
Run: python atomgraph.py --check
     python atomgraph.py <atoms_dir> <crossings_dir> [--strict]
"""
import sys
from pathlib import Path

import yaml

from schema import Atom, Crossing, MusicologicalClaim, Status

DRAFT, STRICT = "draft", "strict"
MODE_STATUSES = {
    DRAFT: frozenset({Status.proposed, Status.validated}),
    STRICT: frozenset({Status.validated}),
}  # contested is in neither set -> never compiled


class UnknownAtom(Exception):
    """A crossing references an atom (or frame_from) that does not exist."""


def select_claims(atom: Atom, mode: str) -> list[MusicologicalClaim]:
    """Musicological claims of `atom` that render under `mode` (contested always dropped)."""
    allowed = MODE_STATUSES[mode]
    return [c for c in atom.musicological if c.status in allowed]


def check_refs(crossings: list[Crossing], atoms: dict[str, Atom]) -> None:
    """Every crossing's two atoms and its frame_from must resolve. Else UnknownAtom."""
    for c in crossings:
        for name in (*c.atoms, c.frame_from):
            if name not in atoms:
                raise UnknownAtom(f"crossing {c.crossing!r} references unknown atom {name!r}")
        if c.frame_from not in c.atoms:
            raise UnknownAtom(
                f"crossing {c.crossing!r} frame_from {c.frame_from!r} is not one of its atoms"
            )


def _load_dir(directory, model):
    for f in sorted(Path(directory).glob("*.yaml")):
        yield model.model_validate(yaml.safe_load(f.read_text(encoding="utf-8")))


def load_atoms(directory) -> dict[str, Atom]:
    return {a.atom: a for a in _load_dir(directory, Atom)}


def load_crossings(directory) -> list[Crossing]:
    return list(_load_dir(directory, Crossing))


def compose_suno(crossing: Crossing, atoms: dict[str, Atom], mode: str = DRAFT):
    """Compose one crossing into (suno_prompt, avoid). Per-genre facts come from the atoms."""
    check_refs([crossing], atoms)
    frame = atoms[crossing.frame_from]
    guest = atoms[next(n for n in crossing.atoms if n != crossing.frame_from)]
    parts = [f"{crossing.atoms[0]} x {crossing.atoms[1]} fusion", f"frame from {frame.atom}"]
    parts += [c.claim for c in select_claims(frame, mode)]
    parts += [c.claim for c in select_claims(guest, mode)]
    parts.append(f"tension: {crossing.tension}")
    return ", ".join(parts), (crossing.avoid or "")


def render_all(atoms_dir, crossings_dir, mode=DRAFT):
    atoms = load_atoms(atoms_dir)
    crossings = load_crossings(crossings_dir)
    check_refs(crossings, atoms)  # fail fast before rendering anything
    for c in crossings:
        prompt, avoid = compose_suno(c, atoms, mode)
        print("=" * 72)
        print(f"{c.crossing}  [mode={mode}]")
        print(prompt)
        if avoid:
            print(f"[avoid] {avoid}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args or not args:
        import test_atomgraph
        test_atomgraph._run()
    else:
        mode = STRICT if "--strict" in args else DRAFT
        pos = [a for a in args if not a.startswith("--")]
        render_all(pos[0], pos[1], mode)
