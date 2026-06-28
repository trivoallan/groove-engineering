🇬🇧 **English** · [🇫🇷 Français](README.fr.md)

# Le Malentendu

> "Music that never existed."
> **non = malentendu** *(no = misunderstanding)*

An **open method** for fusing musical genres. The product is the **method** — a
*model-agnostic* representation of a fusion + a compiler — not the audio, not the
prompt. The models (Suno, Udio, MusicGen, a human musician) are **interchangeable
backends**.

Free, under **AGPLv3**.

> 🗣️ **Open RFC — come comment:** [PR #1 — Methodology](https://github.com/trivoallan/groove-engineering/pull/1) · [comment inline](https://github.com/trivoallan/groove-engineering/pull/1/files)

## This repo

| | |
|---|---|
| [`process/method.md`](process/method.md) | the spec: 2 layers (sound + text), 3 registers (musicological / felt / political), atoms vs molecules, political vision |
| [`process/political-vision.md`](process/political-vision.md) | the political vision in full — six theses: authenticity, commons, creolization, opacity, self-implication, meaning |
| [`process/examples.md`](process/examples.md) | diagrams + 3 real worked examples |
| [`process/rfc/`](process/rfc/) | the RFCs — the method put up for debate. **Discussion happens in the Pull Requests.** |
| [`poc/`](poc/) | the proof: `python3 poc/compile.py` compiles a fusion into a Suno prompt **and** a human brief (two backends, one source) |
| [`catalogue/misunderstandings.md`](catalogue/misunderstandings.md) | the *found misunderstandings* — the happy accidents we keep |
| [`GENESIS.md`](GENESIS.md) | how the project was born, in the open |

## Take part

Read the open RFC and **comment on the Pull Request**. Tag your register:
🎼 musicological (a fact) · 👂 felt (subjective) · ✊ political (values).
Disagreement is the point.

## Run the proof

```bash
python3 poc/compile.py          # compile fusions -> Suno + brief
python3 poc/compile.py --check  # self-check
```

## Languages

**English is canonical** (`*.md`); every document has a French sibling (`*.fr.md`). 100% bilingual.

---

*non = malentendu*
