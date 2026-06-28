🇬🇧 **English** · [🇫🇷 Français](README.fr.md)

# PoC — the method, not the model

Principle: **the product is the method**, not the audio or the Suno prompt.

A fusion is described **once** (`fusions.json`), independently of any model. A
compiler renders it to a target. **Suno is just one interchangeable backend** —
we show two here to prove it.

| File | Role |
|---|---|
| `fusions.json` | **the source** — model-agnostic fusion representations (groove, harmony, instrumentation, production, tension, references) |
| `compile.py` | **the compiler** — `compile_suno()` (EN prompt) + `compile_brief()` (human brief) from the same source |

## Run

```bash
python3 compile.py          # compile all fusions -> Suno + brief
python3 compile.py --check  # self-check, no model required
```

## Validate the method

Paste a Suno prompt into Suno, listen. **If it sounds right, the method holds** —
Suno was just the first render. The day you switch models (Udio, self-hosted
MusicGen…), you write a new compiler; **the source doesn't move.**

That's the whole PoC: proving the value lives in the *representation*, not the
pipe. (Suno prompts in English, per project rule.)

---

*non = malentendu*
