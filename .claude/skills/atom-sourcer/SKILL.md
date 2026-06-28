---
name: atom-sourcer
description: >-
  Research a music genre and produce a sourced, schema-valid genre atom
  (poc/atoms/<genre>.yaml) for the groove-engineer knowledge graph. Use this
  whenever the user wants to add, source, research, or create an atom for a genre
  in groove-engineer — e.g. "source the dub atom", "add gqom to the graph",
  "research maloya for the atoms", "we need a footwork atom", or any time you are
  filling poc/atoms/. Every musicological fact must carry a real, verified
  citation with a checkable locator; the agent fills register 1 (musicological)
  only and never writes the felt or political layers, which belong to humans.
---

# Atom sourcer

A genre **atom** is the unit of the groove-engineer method: cure the atom once and
you repair all of its fusions (see [`process/rfc/atoms-knowledge-graph.md`](../../../process/rfc/atoms-knowledge-graph.md)
and [`process/method.md`](../../../process/method.md)). This skill produces one
atom file — `poc/atoms/<genre>.yaml` — by researching the genre and writing down
**musicological facts that each carry a real, checkable source.**

You are a **passer**, not an oracle. Your job is to report what named sources say,
attributed, in status `proposed`, so a human can later validate or contest it. You
are not the expert and you are not the author. That distinction is the whole point
of the method, and most of this skill is about respecting it.

## The job, in one line

Produce `poc/atoms/<genre>.yaml` such that `cd poc && python validate.py atoms crossings`
prints `ok: N atom(s) valid` — every claim sourced with a checkable locator, and
nothing in it that isn't yours to write.

## Four rules, and why they matter

**1. Fill `musicological` only. Leave `felt`, `political`, `constraints`, and `exemplars` empty.**
The schema has three registers (method §2): musicological facts (yours, falsifiable),
*felt* experience (the circle's — "it's trance-inducing"), and *political* reading
(the author's — "a music of resistance"). An AI sourcing facts about music from
colonized cultures is *already* close to the extraction the method critiques; the
one thing that keeps it honest is that you never put words in the author's mouth.
So write facts, attribute them, and stop. The human assembles the rest. The agent's
output type even has no political field by construction — honor that in spirit.

**2. Every locator must be real and verified — open the source, do not cite from memory.**
A fabricated-but-plausible citation is *worse* than no citation: it launders an
invention into something that looks rigorous. The premise of the whole system is
that sourcing = traceability, so the locator has to actually resolve and actually
support the claim. Use web search to find a source, then **fetch the page and
confirm it says what you're about to write.** If you only "know" a fact, you cannot
source it — see rule 3. A `locator` is a URL, a DOI, an ISBN + page, or a timecode.

**3. Drop any claim you cannot source. That is the system working, not failing.**
When you reach a fact you can't tie to a real source, do not soften it, do not
invent a plausible-looking reference. Drop it. A fact you can't source was an
opinion wearing a fact's clothes. If it's really a *feeling* (tempo "feels like
trance", "hypnotic"), it is register 2 — leave it for the circle, don't smuggle it
into `musicological`. Reviewers should see a short atom of solid facts, not a long
atom of confident guesses.

**4. Status is `proposed`.** No musicologist has validated this yet (method §8
admits the gap). `proposed` means "sourced, awaiting the circle." Never set
`validated` — that's a human signing their name (`signed_by`).

## How to do it

1. **Research.** Search for the genre, then **fetch** the most reliable sources and
   read them. Good starting points: an authoritative encyclopedia (UNESCO ICH for
   heritage genres, Grove/Britannica), then a secondary source (Wikipedia is
   acceptable as `proposed` — the circle validates against primary sources later).
   Aim for the structural facts that define the genre: origin, characteristic
   instrumentation, vocal/rhythmic form, social/ritual context, notable history.
2. **Write `poc/atoms/<genre>.yaml`** in the format below. One claim per fact, each
   with `citation` (the source named) and `locator` (the checkable pointer).
3. **Validate.** `cd poc && python validate.py atoms crossings`. If a locator is
   flagged as uncheckable, it isn't a real pointer — fix it or drop the claim. Green
   means every fact is sourced.

The schema is the contract: read [`poc/schema.py`](../../../poc/schema.py) if you
need the exact field names. Do not duplicate or restate the schema in the atom file.

## Atom format

```yaml
# <Genre> — genre atom. Status: proposed. Musicological claims sourced and
# verified against <sources>. The agent fills `musicological` only; the
# human-owned layers (constraints / felt / political / exemplars) are left empty.
atom: <genre>            # lowercase, matches the filename and any crossing reference
status: proposed

musicological:
  - claim: "<a single structural fact, plainly stated>"
    source:
      citation: "<the source, named — e.g. 'UNESCO ICH, Representative List — Maloya'>"
      locator: "<URL / DOI / ISBN+page / timecode that resolves and supports the claim>"
  # ... more claims, each independently sourced
```

That is the whole file. No `felt`, no `political`, no `constraints`, no `exemplars` —
those are added by humans in a later pass.

## Worked example: maloya

Research turned up the UNESCO Intangible Cultural Heritage page and the English
Wikipedia article. Two facts the maker had asserted in the old `fusions.json` —
"6/8 ternary" and a specific tempo — could **not** be found in either source, so
they were dropped (the tempo-as-trance feeling moved to the human's `felt` layer,
the 6/8 was discarded). What remained was eight facts that each resolve:

```yaml
atom: maloya
status: proposed
musicological:
  - claim: "created by enslaved Malagasy and Africans on Réunion's sugar plantations"
    source:
      citation: "UNESCO ICH, Representative List — Maloya (inscribed 2009, 4.COM)"
      locator: "https://ich.unesco.org/en/RL/maloya-00249"
  - claim: "traditionally accompanied by percussion and a musical bow: roulèr, kayamb, pikér, sati, and bob"
    source:
      citation: "Wikipedia (EN), 'Maloya', accessed June 2026"
      locator: "https://en.wikipedia.org/wiki/Maloya"
  # ... six more, each with its own resolving locator
```

The lesson is in what was *cut*. A shorter, fully-sourced atom beats a longer one
padded with things you merely believe.

## Verify (always end here)

```bash
cd poc && python validate.py atoms crossings
# -> ok: N atom(s) valid (schema + refs + locators)
```

If validation needs dependencies: `pip install -r poc/requirements.txt` (pydantic +
pyyaml). A red result naming an "uncheckable locator" is the guard doing its job:
that claim is not really sourced.
