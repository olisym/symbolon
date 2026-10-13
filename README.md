# Mensch als Republik (MaR)

*Symbolon: a self-verifying trust layer for local-first networks*

MaR is a coordination protocol with a reference implementation in Python. It investigates whether
a group can make binding agreements, take decisions by vote and keep shared accounts without a
trusted central party such as a platform operator, an administrator or a court. The approach is
empirical: the protocol is specified, implemented and tested against concrete scenarios.

The name of the repository refers to the ancient Greek *symbolon*, a token broken in two whose
matching halves later served as proof of an agreement. The protocol follows the same principle:
a statement is verifiable not because it is signed, but because it can be checked for
consistency against other signed statements (D317).

The specification, the decision register and the working process are maintained in German
(D329). This file, `CONTRIBUTING.md` and `docs/METHOD.md` are written in English.

## Principle

Each participant signs statements with a personal key. The statements of one participant form a
hash chain that cannot be altered retroactively. All participants receive the same signed
statements and evaluate them locally; there is no central server and no global consensus. Two
contradictory statements by the same author constitute proof of the contradiction, signed by the
author, and can be verified by anyone who holds both.

Group functions are composed from these statements: vouching, membership, recording obligations
and their settlement, disputes and arbitration, and amendment of a group's own rules by vote.

## Scope and limitations

- **No verification of facts.** The protocol establishes who stated what, not whether a statement
  is true. Whether an event occurred is a matter of human judgement.
- **No observation of behaviour.** Only statements a participant chooses to sign become visible.
  Signing is intended for decisions and commitments, not for routine activity.
- **No reputation score.** Trust is computed by each participant from their own position in a
  network of vouches. It cannot be accumulated, transferred or exchanged, and it confers no
  additional voting weight.
- **No custody.** No mechanism depends on a party holding funds on behalf of others (D467).

## Current state

- **Club scenario in the browser.** Founding by three members from a template, admission of
  members, votes on amendments and motions, membership dues recorded as obligations and settled
  by receipts. A member who votes both for and against the same proposal is shown to all
  members, with both signatures as evidence.
- **Layered specification** (files `00` to `08`): the signed statement, groups and their
  constitutions, trust, verdicts, obligations and membership, governance, and a scope document
  defining the admission criterion for new mechanisms.
- **Trust as network flow.** Trust is computed as a maximum flow through the network of vouches,
  with a proven bound on the trust that fabricated identities can obtain. The bound does not
  apply to collusion between real participants.
- **Multiple devices per person**, each with its own key, attributed to a single identity.
- **Synchronisation over Reticulum**, including a simulated radio channel at 1200 bit/s with 5 %
  packet loss, over which a complete vote can be conducted.
- **Operation without a reliable clock.** A node without a clock can verify contradictions but
  cannot grant trust.
- **Independent reimplementations** of parts of the specification in Go, Haskell and Rust, based
  solely on frozen copies of the text. One Haskell implementation had access to the repository
  and is not counted as independent. Their main result was a set of questions identifying
  ambiguities in the specification.

Counts of tests and decisions are omitted, as such figures become outdated (D415). The current
state is reported by `make check` and described in `LAGE.md`.

## Open questions

- **No deployment.** The protocol has been tested only against itself and with simulated
  participants (D237).
- **Gaps in the building blocks.** A comparison with Fiske's relational models theory and
  Ostrom's design principles for common-pool resources identified functions that the current
  building blocks cannot express: secret ballots, representation of a group towards third
  parties, prices and exchange, nested groups, and forgiveness (D661). These are tracked as item
  O105 in `offen.md`; each will be researched before any change is made.
- **Mobile devices.** The node runs on Android; automatic discovery between phones is not yet
  available.

Open questions are tracked in `offen.md`, decisions in `07-decisions.md`. This section lists
categories only and is not updated for individual items.

## Running the demonstration

Requires Python 3.11 or later. The user interface is in German.

```sh
python3 -m venv .venv
.venv/bin/pip install 'cbor2>=5.6' 'cryptography>=42.0'
.venv/bin/python -m symbolon.node ~/mar-demo.sqlite --uhr-ab 1000
```

Open `http://anna.localhost:8470/`, `http://bruno.localhost:8470/` and
`http://chris.localhost:8470/` in three tabs of a Chromium-based browser, enter a name and create
a key in each, then found a club as Anna together with the other two. The database file holds
the node's state; a new file starts a new instance.

Contradiction detection across five simulated devices:

```sh
.venv/bin/python -m tools.netz ~/mar-netz-demo
```

The command prints five addresses and the sequence of steps. A new directory starts a new run.

## Documentation

All documents listed here are in German.

- `LAGE.md`: current state, solved and open problems, architecture, and rejected alternatives,
  with references for each statement.
- `VISION.md`: purpose, applications, and assumptions about human behaviour.
- `08-scope.md`: guarantees and limitations of the protocol, and the admission criterion.
- `ROADMAP.md`: plan.
- `07-decisions.md`: all normative decisions with their rationale and rejected alternatives;
  `tools/register_index.py` provides lookup by entry number.

## Repository structure

- `00` to `08`, with lettered sub-specifications: the layered specification.
- `*-prompt.md`, `*-golden-anchors.md`: implementation prompts and expected values for individual
  layers. They remain in the root directory because code cites them; a file cited by code is
  normative and is not moved.
- `07-decisions.md`: decision register.
- `LAGE.md`, `VISION.md`, `ROADMAP.md`, `offen.md`: state, purpose, plan, open items.
- `szenario-verein.md`: the club scenario on which the application is based.
- `pruefregeln.md`, `arbeitsweise.md`: review rules and working method.
- `symbolon/`: reference implementation; `symbolon/node/` contains the node and its web
  interface, `symbolon/bote/` the component that synchronises nodes over Reticulum.
- `tests/`, `tools/`: test suite and review tooling.
- `go/`, `hs/`, `rs/`: independent reimplementations, each pinned to a frozen copy of the
  specification.
- `archiv/`: earlier session records, retained so that references remain resolvable.

## License

Code: Apache-2.0 (`LICENSE`). Specification, decision register and other prose: CC BY 4.0
(`LICENSE-SPEC`). Rationale in D319.

## Contributing

MaR is maintained by a single author. Every change is reviewed against the specification; the
method is described in `docs/METHOD.md`. Contact through an issue or via `CONTRIBUTING.md` is
welcome, in particular from people working on decentralised coordination and from groups
interested in using the protocol.
