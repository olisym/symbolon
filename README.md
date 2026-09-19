# Mensch als Republik (MaR)

*Symbolon: A Self-Verifying Trust Layer for Local-First Networks*

**Can mutual assurance and collective decision-making work without a central authority —
no court, no platform, no admin key?**

Mensch als Republik (MaR) is a protocol under active development that tries to answer that
question by building the thing and measuring what breaks, instead of arguing about it in the
abstract.

The repository and Python package are named `symbolon` — short, pronounceable, and decided
on its own merits (see the decision register, D317); the project's title stays *Mensch als
Republik*, since a repository name doesn't name the actual subject.

This repository is the English entry point. The project's actual working language is German —
the specifications, the decision register, and the day-to-day process are written in German
and will stay that way. This file, along with `CONTRIBUTING.md` and `docs/METHOD.md`, is
written directly for an English-reading audience, not translated from anything.

## The question, more precisely

Most systems that coordinate people rely on either a trusted center — a court, a platform
operator, a custodian holding funds — or a single dominant chain of consensus. MaR asks
whether claims, obligations, and governance can instead be built to be checkable because they
can **contradict each other**, not because an authority signed off on them. A claim nobody can
ever be proven wrong about isn't more trustworthy for it — it's just unfalsifiable.

The project is also deliberately built to survive its own author. One explicit goal is to
resist forgotten decisions, silent drift, and normativity that creeps in unexamined over a
multi-year timeline. The mechanism for that isn't discipline — it's a decision register that
turns every normative choice, and the reasoning behind it, into a permanent, citable, checkable
record.

## What exists today

- A layered specification (Layers 00–08): genesis and constitution, a claim/atom layer with a
  closed, exhaustively tested set of rejection codes, trust-flow and governance layers, and a
  scope layer that defines the criterion for admitting any new mechanism.
- A Python reference implementation with an automated test suite, and a decision register in
  which every normative choice carries a named justification and the alternatives it rejected.
- Layer 01 (the claim/atom layer) has been through an exhaustive mutation-testing campaign:
  over **19,000 generated mutants**, single and paired, across three structural families. Not
  one surviving mutant turned up anything that reading, reasoning, or a rollback probe hadn't
  already found. That's treated as evidence the layer has been read out, not as proof of
  correctness — the distinction matters, and it's recorded as one.
- Independent readings of the specification. Layer 01 was rebuilt in Go from a frozen copy of
  the spec, without access to the Python code, and found spec defects the reference
  implementation's own tests could not surface. Layer 02 (trust flow) was rebuilt three times
  the same way: twice in Haskell, once in Rust. One of the Haskell builds turned out to have
  seen the repository and is not counted as independent; the register records how that was
  established. The useful yield of these builds was less their output than their lists of
  questions to the text, which are kept in `hs/` and `rs/`.
- Recent work concerns time: what a node can still assert when its clock is missing, coarse,
  or wrong. The short answer the register arrived at is that a node without a clock can
  *accuse* — prove that someone contradicted their own signed statements — but cannot *grant*
  trust. That is groundwork for delay-tolerant transports such as LoRa or Reticulum, not yet an
  application of them.

This file deliberately carries no test or entry counts: a number nobody checks drifts. The
current state is what `make check` reports, what the end of `07-decisions.md` says, and what
the newest `sitzungsstart-*.md` hands on to the next working session (in German).

## What does *not* exist yet

No real application. The register (D237) is explicit that a real test needs real people with a
genuine shared concern — not a simulation, not volunteers doing a favor. Waiting for that is
treated as a legitimate state; pretending otherwise is not. Making the project visible — this
repository included — is part of how those people might eventually turn up.

## Repository layout

- `00` – `08`, plus lettered sub-specifications: the layered specification, in German.
- `*-prompt.md`, `*-golden-anchors.md`: implementation prompts and expected-value anchors
  for specific layers. They sit flat in the root, unsorted into folders, on purpose — once a
  prompt file is cited by a docstring (`NAME §X`), it becomes normative text like any spec
  file, and moving it would break that citation. It looks unusual. It's not clutter.
- `07-decisions.md`: the decision register. Large by design — it is the point of the project,
  not overhead to be trimmed. `tools/register_index.py` gives you structured lookup by entry
  number, so you don't have to read the whole thing at once.
- `pruefregeln.md`: the accumulated review rules the project holds itself to.
- `symbolon/`, `tests/`, `tools/`: the Python reference implementation, its test
  suite, and the tooling that enforces the review discipline (spec linting, mutation
  campaigns, register consistency checks).
- `offen.md`: the list of known open questions, each a guess about a gap rather than a
  decision. Numbers are never reused, so a reference stays readable after an item is closed.
- `go/`: the independent Go implementation of Layer 01. It's deliberately pinned to a frozen
  snapshot of the specification — the register explains why that pin, not the repository
  split, is what actually keeps the implementations independent.
- `hs/`, `rs/`: the assignments, frozen spec copies and question lists of the Haskell and Rust
  builds of Layer 02. The code of those builds is not part of the main line.
- `archiv/`: earlier session handoffs and working files, kept so that old references resolve.

## License

Code is licensed under **Apache-2.0** (`LICENSE`). The specification, the decision register,
and other prose documents are licensed under **CC-BY-4.0** (`LICENSE-SPEC`). Both choices, and
the reasoning behind them, are recorded in the register.

## Getting involved

This is currently a one-person project, but it isn't built ad hoc — every change is checked
against the specification, not just against what compiles. See `docs/METHOD.md` for how that
actually works day to day.

If you're working on related problems — decentralized coordination, protocols hardened by
contradiction rather than authority, or you think you might be one of the people the register
(D237) is waiting for — open an issue, or see `CONTRIBUTING.md`.
