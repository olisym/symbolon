"""Domänen-Separatoren für Claim-Atom v1 (01 §4)."""

DOM_SIG = b"claim-atom/v1/sig"
DOM_CID = b"claim-atom/v1/cid"
DOM_ID_GEN = b"claim-atom/v1/id-genesis"

# Nur für Vektor-Reproduktion (Governance-Schicht 00), nicht im Atom-Code verwenden.
DOM_NUC_GEN = b"claim-atom/v1/nucleus-genesis"

# Epochen- und Vorschlagsidentität (04 §1.1, 04 §2.4).
DOM_NUC_EPOCH = b"claim-atom/v1/nucleus-epoch"
DOM_NUC_PROPOSAL = b"claim-atom/v1/nucleus-proposal"

# Sachantragsidentität (04 §2.5).
DOM_NUC_MOTION = b"claim-atom/v1/nucleus-motion"
