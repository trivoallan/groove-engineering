#!/usr/bin/env python3
"""Assert-based tests for atomgraph.py (no pytest — matches compile.py's --check).

Run: python test_atomgraph.py   (or: python atomgraph.py --check)
"""
import tempfile
from pathlib import Path

from atomgraph import (
    DRAFT,
    STRICT,
    UnknownAtom,
    check_refs,
    compose_suno,
    load_atoms,
    select_claims,
)
from schema import Atom, Crossing, MusicologicalClaim, Source, Status


def _raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False


def _claim(text, status=Status.proposed):
    return MusicologicalClaim(claim=text, source=Source(citation="c", locator="p. 1"), status=status)


def _atom(name, claims):
    return Atom(atom=name, musicological=claims)


def _crossing(a, b, frame):
    return Crossing(
        crossing=f"{a}-x-{b}", atoms=(a, b), frame_from=frame, tension="t",
        creolizes="c", opacity_preserved="o", self_implication="s", held_by=["author"],
    )


def test_select_claims_draft_includes_proposed():
    atom = _atom("x", [_claim("p", Status.proposed), _claim("v", Status.validated)])
    rendered = {c.claim for c in select_claims(atom, DRAFT)}
    assert rendered == {"p", "v"}


def test_select_claims_strict_excludes_proposed():
    atom = _atom("x", [_claim("p", Status.proposed), _claim("v", Status.validated)])
    rendered = {c.claim for c in select_claims(atom, STRICT)}
    assert rendered == {"v"}  # proposed dropped under strict


def test_select_claims_drops_contested_in_both_modes():
    atom = _atom("x", [_claim("k", Status.contested), _claim("v", Status.validated)])
    assert "k" not in {c.claim for c in select_claims(atom, DRAFT)}
    assert "k" not in {c.claim for c in select_claims(atom, STRICT)}


def test_check_refs_raises_on_missing_atom():
    atoms = {"maloya": _atom("maloya", [_claim("6/8")])}
    bad = _crossing("maloya", "footwork", "maloya")  # footwork absent
    assert _raises(UnknownAtom, lambda: check_refs([bad], atoms))


def test_check_refs_raises_on_frame_not_in_atoms():
    atoms = {"a": _atom("a", [_claim("x")]), "b": _atom("b", [_claim("y")])}
    bad = Crossing(
        crossing="a-x-b", atoms=("a", "b"), frame_from="c", tension="t",
        creolizes="c", opacity_preserved="o", self_implication="s", held_by=["author"],
    )
    assert _raises(UnknownAtom, lambda: check_refs([bad], atoms))


def test_compose_contains_both_genres():
    atoms = {
        "maloya": _atom("maloya", [_claim("ternary 6/8"), _claim("kayamb")]),
        "footwork": _atom("footwork", [_claim("160bpm kicks")]),
    }
    prompt, _ = compose_suno(_crossing("maloya", "footwork", "maloya"), atoms, DRAFT)
    assert "maloya" in prompt and "footwork" in prompt
    assert "ternary 6/8" in prompt and "160bpm kicks" in prompt


def test_compose_strict_drops_proposed_facts():
    atoms = {
        "maloya": _atom("maloya", [_claim("vetted", Status.validated), _claim("draft", Status.proposed)]),
        "footwork": _atom("footwork", [_claim("160bpm", Status.validated)]),
    }
    prompt, _ = compose_suno(_crossing("maloya", "footwork", "maloya"), atoms, STRICT)
    assert "vetted" in prompt and "draft" not in prompt


def test_load_atoms_from_disk_and_refcheck():
    yaml_atom = (
        "atom: maloya\n"
        "musicological:\n"
        "  - claim: ternary 6/8\n"
        "    source: { citation: W, locator: '12:34' }\n"
    )
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "maloya.yaml").write_text(yaml_atom, encoding="utf-8")
        atoms = load_atoms(d)
        assert set(atoms) == {"maloya"}
        assert atoms["maloya"].musicological[0].claim == "ternary 6/8"
        # a crossing into a genre we didn't load must fail loudly
        bad = _crossing("maloya", "footwork", "maloya")
        assert _raises(UnknownAtom, lambda: check_refs([bad], atoms))


def _run():
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            n += 1
            print(f"  ok {name}")
    print(f"ok: {n} atomgraph tests passed")


if __name__ == "__main__":
    _run()
