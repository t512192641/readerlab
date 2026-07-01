result: pass
hard_gates:
  - pass: complete body track exists at `10_一手正文/001_正文.md` and matches `docs/product-spec.md` with no diff.
  - pass: reader-facing page explicitly links readers to the body track and does not replace the body with AI explanation.
  - pass: reader-facing page has no exposed internal fields such as source refs, claim trace, lens score, machine/human status, Body Track Gate, Claim Ledger, Candidate Tournament, or Skillization Gate.
  - pass: claim ledger separates direct source claim, composite interpretation, external analogy, and needs verification, and blocks the external-book generalization from reader-facing use.
  - pass: candidate tournament includes real downgrade and reject decisions, not only promoted candidates.
  - pass: skillization gate rejects or downgrades candidates that lack trigger, input, steps, output, boundary, or evidence.
  - pass: annotation triggers contain 6 body-adjacent questions, within the required 3-7 range.
  - pass: reader-facing prose reads as natural companion guidance rather than an audit report.
  - pass: all Demo A JSON contracts parse with `python3 -m json.tool`.
reader_score: 11/12
P0: []
P1: []
P2:
  - Demo A proves a complete body-track pattern for repo-owned longform material, not external copyrighted or public-domain book validation. Landing language must keep this scope explicit.
must_fix_before_landing: []
