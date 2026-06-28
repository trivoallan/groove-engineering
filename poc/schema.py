#!/usr/bin/env python3
"""groove-engineering schema — the data contract for genre atoms.

The schema IS the method's attribution rule (§3), encoded in types: a
musicological claim without a source does not validate. The agent's output
type (MusicologicalReport) has no political field, so the register-3 boundary
is enforced by construction, not by good behavior.

  Atom                                  Crossing
   status: proposed|validated|contested  atoms: (a, b)
   musicological[]  (reg.1, sourced)     frame_from
     each: claim + Source                tension / avoid
            (locator REQUIRED)           creolizes / opacity_preserved /
   felt[]           (reg.2)                self_implication   (reg.3, owned)
   political[]      (reg.3, owned)       held_by
   constraints[]  exemplars[]

  status drives compile: --draft renders proposed+validated, --strict only
  validated; contested is stored (the divergence is held, §3) but never compiled.
  Opacity is honored as a practice (we don't decompose some atoms), NOT a field.

See: process/rfc/atoms-knowledge-graph.md  ·  tests: test_schema.py

Run: python schema.py --check    # self-check (requires pydantic)
"""
import re
import sys
from enum import Enum

from pydantic import BaseModel, Field


class Status(str, Enum):
    proposed = "proposed"
    validated = "validated"
    contested = "contested"


# A locator must look machine-checkable, so a fabricated/empty pointer is
# catchable WITHOUT a musicologist (sourcing is traceability, not expertise).
# The schema only requires it non-empty; THIS shape-check is what CI runs.
_LOCATOR_SHAPES = (
    re.compile(r"^https?://", re.I),        # URL
    re.compile(r"\bdoi:\s*10\.", re.I),     # DOI
    re.compile(r"\bISBN\b", re.I),          # ISBN
    re.compile(r"\b\d{1,3}:\d{2}\b"),       # timecode mm:ss
    re.compile(r"\bpp?\.\s*\d+", re.I),     # page ref "p. 42" / "pp. 42"
)


def valid_locator(locator: str) -> bool:
    """True if the locator has a recognizable, checkable shape."""
    return bool(locator) and any(p.search(locator) for p in _LOCATOR_SHAPES)


class Source(BaseModel):
    citation: str                           # "Danyèl Waro, interview, Télérama 2018"
    locator: str = Field(min_length=1)      # REQUIRED: URL / DOI / ISBN+page / timecode


class MusicologicalClaim(BaseModel):        # register 1 — falsifiable
    claim: str
    source: Source                          # no source, no fact
    status: Status = Status.proposed
    signed_by: list[str] = []               # circle members who validated/contested


class HeldClaim(BaseModel):                 # a held position (felt or political) — held, not true
    text: str                               # register = the list it lives in (atom.felt / atom.political)
    held_by: list[str] = Field(min_length=1)  # a position always has an owner


class Constraint(BaseModel):
    claim: str                              # "vocals in Reunion Creole"
    held_by: list[str] = Field(min_length=1)


class Exemplar(BaseModel):
    track: str
    cue: str | None = None
    recognized_by: list[str] = []


class Atom(BaseModel):
    atom: str
    status: Status = Status.proposed
    musicological: list[MusicologicalClaim]
    constraints: list[Constraint] = []
    felt: list[HeldClaim] = []              # register 2 — the circle
    political: list[HeldClaim] = []         # register 3 — owned, agent NEVER fills
    exemplars: list[Exemplar] = []
    curators: list[str] = []


class MusicologicalReport(BaseModel):       # what the agent emits — register 1 only, by construction
    atom: str
    musicological: list[MusicologicalClaim]


class Crossing(BaseModel):
    crossing: str
    atoms: tuple[str, str]
    frame_from: str                         # which atom is the dominant frame
    tension: str
    avoid: str | None = None
    # §6 political coherence — owned answers, required as text (force reflection, not a checkbox):
    creolizes: str
    opacity_preserved: str
    self_implication: str
    held_by: list[str] = Field(min_length=1)


if __name__ == "__main__":
    if "--check" in sys.argv:
        import test_schema
        test_schema._run()
    else:
        print(__doc__)
