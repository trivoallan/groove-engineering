#!/usr/bin/env python3
"""Assert-based tests for schema.py (no pytest — matches compile.py's --check).

Run: python test_schema.py   (or: python schema.py --check)
"""
from pydantic import ValidationError

from schema import (
    Atom,
    Crossing,
    HeldClaim,
    MusicologicalClaim,
    MusicologicalReport,
    Source,
    Status,
    valid_locator,
)


def _raises(fn):
    try:
        fn()
    except ValidationError:
        return True
    return False


def test_source_requires_locator():
    assert _raises(lambda: Source(citation="x"))              # missing locator
    assert _raises(lambda: Source(citation="x", locator=""))  # empty locator
    assert Source(citation="x", locator="https://e.org").locator


def test_musicological_claim_requires_source():
    assert _raises(lambda: MusicologicalClaim(claim="ternary 6/8"))  # no source -> invalid
    c = MusicologicalClaim(claim="6/8", source=Source(citation="W", locator="p. 3"))
    assert c.status is Status.proposed  # defaults to proposed


def test_held_claim_requires_owner():
    assert _raises(lambda: HeldClaim(text="t", held_by=[]))  # a position needs an owner
    assert HeldClaim(text="t", held_by=["author"]).held_by


def test_agent_report_has_no_political_field():
    # the register-3 boundary is structural: the agent's output type can't carry politics
    assert "political" not in MusicologicalReport.model_fields
    assert "musicological" in MusicologicalReport.model_fields


def test_atom_has_no_opacity_field():
    # opacity is a practice, not a field (dropped in CEO review)
    assert "opacity" not in Atom.model_fields


def test_atom_requires_musicological():
    assert _raises(lambda: Atom(atom="maloya"))  # musicological is required
    a = Atom(
        atom="maloya",
        musicological=[
            MusicologicalClaim(claim="6/8", source=Source(citation="W", locator="12:34"))
        ],
    )
    assert a.status is Status.proposed


def test_crossing_requires_six_coherence():
    base = dict(
        crossing="a-x-b", atoms=("a", "b"), frame_from="a", tension="t",
        creolizes="c", opacity_preserved="o", self_implication="s", held_by=["author"],
    )
    assert Crossing(**base)
    for drop in ("creolizes", "opacity_preserved", "self_implication", "held_by"):
        partial = {k: v for k, v in base.items() if k != drop}
        assert _raises(lambda p=partial: Crossing(**p)), f"{drop} should be required"


def test_valid_locator_shape():
    assert valid_locator("https://ich.unesco.org/en/RL/00249")  # URL
    assert valid_locator("doi:10.1234/abc")                     # DOI
    assert valid_locator("Waro live, 12:34")                    # timecode
    assert valid_locator("Marimoutou, pp. 88")                  # page
    assert not valid_locator("trust me")                        # no shape -> fabricated/lazy
    assert not valid_locator("")                                # empty


def _run():
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            n += 1
            print(f"  ok {name}")
    print(f"ok: {n} schema tests passed")


if __name__ == "__main__":
    _run()
