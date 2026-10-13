# Mensch als Republik (MaR)

*Symbolon: A Self-Verifying Trust Layer for Local-First Networks*

**Can a group make binding agreements, vote, and keep its books without anyone in the middle
whom everyone has to trust — no platform, no admin key, no court?**

Mensch als Republik ("the human as a republic") is a protocol and a Python reference
implementation that tries to answer that question by building the thing and measuring what
breaks, rather than arguing about it in the abstract.

The repository and package are called `symbolon`. In ancient Greece a *symbolon* was a token
broken in two; years later, the two halves fitting together proved an agreement without
witnesses or an office. That is the idea here: a statement becomes checkable not because it is
signed, but because it can fit, or collide, with other signed statements (D317).

This file is the English entry point. The project's working language is German: the
specifications, the decision register and the day-to-day process are written in German and will
stay that way (D329). This file, `CONTRIBUTING.md` and `docs/METHOD.md` are written directly for
English readers, not translated.

## The idea

- **Everyone signs what they say**, with their own key, in a chain of their own that they cannot
  rewrite afterwards.
- **Everyone gets the same signatures and computes the result themselves.** There is no shared
  server and no global consensus; nodes agree as far as their knowledge agrees.
- **Whoever signs two contradictory statements has produced the proof against themselves.** As
  soon as both reach anyone, the contradiction is there, signed by its author, and cannot be
  denied.

On top of that sit the things groups do: vouching for someone, joining, owing and settling dues,
accusing and arbitrating, and amending their own rules by vote.

Just as important is what it deliberately does **not** do:

- **It does not check whether a statement is true.** Whether something actually happened is for
  people to judge; the protocol only makes sure everyone has to stand by what they signed.
- **It does not watch anyone.** Only what someone chooses to sign becomes visible. Signing is the
  exception, not the default; you don't need a contract to buy bread.
- **It keeps no reputation score.** Trust is computed by each person from their own position in a
  network of vouches. It cannot be saved up, transferred, or bought, and it gives no extra vote.
- **It holds no one's money.** No mechanism relies on a party that keeps other people's funds
  (D467).

## What works today

- **A club, end to end, in the browser.** Three people found it together from a template, others
  join, members vote on amendments and motions, dues are recorded as debts and settled by
  receipts, and a member who votes yes and no on the same question is shown to everyone, with
  both signatures as proof.
- **A layered specification** (files `00` to `08`): the claim atom, the community and its
  constitution, trust as a flow, profiles for verdicts, debts and membership, governance by
  epochs, and a scope document with the admission test every new mechanism has to pass.
- **Trust as a flow.** How much trust reaches someone is a maximum flow through the network of
  vouches, with a proven bound against mass-produced fake identities, and none against real
  people who collude.
- **Several devices per person**, each with its own key under one root.
- **Sync over Reticulum**, including a simulated radio channel at 1200 bit/s and 5 % loss; a whole
  vote fits through it.
- **Time without trust in clocks.** A node without a clock can still prove a contradiction, but it
  cannot grant trust.
- **Independent rebuilds** of parts of the specification in Go, Haskell and Rust, from frozen
  copies of the text and without the Python code. One Haskell build turned out to have seen the
  repository and is not counted as independent. Their main yield was lists of questions that
  exposed ambiguities in the spec.

This file deliberately carries no counts of tests or decisions: a number nobody checks drifts
(D415). The current state is what `make check` reports and what `LAGE.md` describes.

## What is still open

- **No real group uses it yet.** Everything is tested against itself and with simulated people
  (D237). This is the largest gap, and it is not a technical one.
- **Known gaps in the building blocks.** A cross-check against Fiske's four relational models and
  Ostrom's design principles for commons found what the current blocks cannot express without
  something new: secret ballots, representing a group to the outside, prices and exchange,
  nested groups, and forgiveness (D661). The list is item O105 in `offen.md`; each gap gets its
  own research before anything is built.
- **On phones**, the node runs, but two phones do not yet find each other on their own.

Open questions live in `offen.md`, decisions in `07-decisions.md`. This file names only kinds of
questions, so that it does not have to change every time one is answered.

## Try it

You need Python 3.11 or newer. The user interface is in German.

```sh
python3 -m venv .venv
.venv/bin/pip install 'cbor2>=5.6' 'cryptography>=42.0'
.venv/bin/python -m symbolon.node ~/mar-demo.sqlite --uhr-ab 1000
```

Then open `http://anna.localhost:8470/`, `http://bruno.localhost:8470/` and
`http://chris.localhost:8470/` in three tabs of a Chromium-based browser. In each, enter a name
and create a key; then, as Anna, found a club with the other two. The file passed to the node
holds its data; a fresh file means a fresh start.

To see the contradiction between five simulated devices:

```sh
.venv/bin/python -m tools.netz ~/mar-netz-demo
```

It prints five addresses and the steps to follow. A fresh directory means a fresh start.

## Where to start reading

All of these are in German.

- `LAGE.md` — the current state: what is solved, what is open, how the parts fit, and what was
  rejected and why, each statement with a reference.
- `VISION.md` — why and what for; the assumptions about people the design rests on.
- `08-scope.md` — what the protocol does and does not promise, and the admission test.
- `ROADMAP.md` — the plan.
- `07-decisions.md` — every normative decision with its reasons and the alternatives it rejected.
  `tools/register_index.py` looks entries up by number.

## Repository layout

- `00` – `08`, plus lettered sub-specifications: the layered specification.
- `*-prompt.md`, `*-golden-anchors.md`: implementation prompts and expected-value anchors for
  specific layers. They sit flat in the root on purpose: once code cites a prompt file, it is
  normative text like any spec file, and moving it would break the citation.
- `07-decisions.md`: the decision register. Large by design; it is the point of the project, not
  overhead.
- `LAGE.md`, `VISION.md`, `ROADMAP.md`, `offen.md`: state, purpose, plan, open items.
- `szenario-verein.md`: the club scenario the application is built from.
- `pruefregeln.md`, `arbeitsweise.md`: the review rules and the working method.
- `symbolon/`: the Python reference implementation. `symbolon/node/` is the node with its web
  page, `symbolon/bote/` the messenger that syncs nodes over Reticulum.
- `tests/`, `tools/`: the test suite and the tooling that enforces the review discipline.
- `go/`, `hs/`, `rs/`: the independent rebuilds, pinned to frozen copies of the specification.
- `archiv/`: earlier session handoffs, kept so that old references resolve.

## License

Code is licensed under **Apache-2.0** (`LICENSE`). The specification, the decision register and
other prose are licensed under **CC-BY-4.0** (`LICENSE-SPEC`). Both choices and their reasons are
in the register (D319).

## Getting involved

This is a one-person project, but it is not built ad hoc: every change is checked against the
specification, not just against what compiles. `docs/METHOD.md` describes how.

If you work on related problems — coordination without a center, protocols hardened by
contradiction rather than authority — or if you are part of a group that might actually want to
use this, open an issue or see `CONTRIBUTING.md`.
