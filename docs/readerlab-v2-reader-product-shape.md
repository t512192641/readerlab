# ReaderLab V2 Reader Product Shape

## Status

This document defines the reader-facing product shape that must be met before
ReaderLab output can be called reader-accepted. It is not a smoke-test script
and not a packaging checklist.

The installable package work proved the distribution skeleton: package boundary,
runtime configuration, package audit, install smoke, and route smoke. It did not
by itself prove the final reader product shape. Future work must keep these two
claims separate:

- `installable_release_candidate`: the package can be built, installed, and run
  through route smoke.
- `reader_accepted`: a concrete output package satisfies the reader-facing shape
  below and passes the required reader checks.

ReaderLab has two primary reader-product lines:

1. Book / longform line.
2. Skill / engineering-material line.

They share body-first reading, audit separation, scope clarity, and machine vs
human status separation. They do not share the same reader-facing output shape.

## Why This Exists

The July 2026 installable package chain exposed an integration gap: the package
could run older import / contract-rendering paths, but those paths produced
directories, manifests, route tables, status notes, and pending pages rather than
the V2 reader product that had been designed and pressure-tested in the prototype
line.

Older `import-skills` output is an inventory and regrouping tool. It may be
useful for source discovery, comment preservation, and package bookkeeping, but
it is not the final Skill-line reader product by itself.

V2 reader-product output is an edited reading package. It must let the reader
start reading the material itself, with useful companion explanation nearby, and
must keep machine evidence in audit.

GSTACK `spec` and `review` remain representative pressure samples because they
exercise complex Skill mechanisms. They are not product boundaries and must not
lead to GSTACK-specific adaptation. Any rule learned from them must generalize
to other Skill packages such as Matt-style workflow Skills.

## Shared Non-Negotiables

All ReaderLab reader-facing output must satisfy these rules:

- The reader page serves reading the material, not reading the validator.
- Body or cleaned body appears before audit, status, file paths, or machine
  explanations.
- Reader-facing pages do not expose source ids, hashes, internal paths, claim
  trace, machine status, or JSON contract vocabulary as the main content.
- Scope is visible in plain Chinese: full material, selected chapter, selected
  module, sample, or partial coverage.
- AI companion content must attach to a concrete reading problem: structure,
  mechanism, boundary, misread risk, example, counterexample, transfer, or
  judgment.
- Generic reading instructions are not companion content.
- Machine validation cannot be reported as human reader acceptance.

## Book / Longform Line

### Product Promise

The reader opens a Chinese reading package and feels they are reading the book
or longform material itself, with a thoughtful companion beside the text. The
page must not feel like an EPUB extraction report, audit packet, or demo sample.

### Reader-Facing Shape

A passing book / longform output contains:

1. **Start page**
   - Names the book or longform material.
   - States current coverage in natural Chinese.
   - Tells the reader where to start.
   - Does not expose local file paths, audit paths, source ids, or machine
     status.

2. **Structure map**
   - Explains the material's real structure: parts, chapters, sections,
     argument blocks, interview turns, or report sections.
   - Shows where the current reading unit sits in that structure.
   - Does not flatten front matter, epigraphs, notes, chapter bodies, and
     appendices into the same kind of unit.

3. **Body-first reading page**
   - Uses the original body text and original order as the page subject.
   - Performs only light cleanup unless the user explicitly asks for rewriting.
   - Removes extraction noise such as unknown placeholders, spine file names, or
     internal paths.
   - Gives the reader a short orientation before the body only when it lowers
     entry cost.

4. **Nearby companion explanation**
   - Appears close to the body it explains.
   - Adds concrete value: mechanism, boundary, misread risk, transfer, or
     higher-order interpretation.
   - Does not repeat the same generic frame under every heading.

5. **Closure**
   - If only a chapter is covered, says chapter-only in reader language.
   - If full-book coverage is claimed, includes a whole-book summary layer:
     structure, 3-5 core takeaways, chapter progression, and what the reader
     should carry away.

### Book / Longform Acceptance Checks

A book / longform output is reader-accepted only if all checks pass:

- A non-technical reader can answer within three minutes:
  - What is this material?
  - What scope am I reading?
  - Where am I in the book or longform structure?
  - What is this chapter / unit trying to help me understand?
- The first reading page does not show audit paths, source ids, machine status,
  or fixture/sample language.
- The body is not replaced by AI summary, guide text, or high-order explanation.
- Companion notes are attached to the material and would not work unchanged in
  another unrelated chapter.
- The output does not claim full-book acceptance from a chapter-only run.
- Reader evaluation is separate from machine validation and records pass/fail,
  score or rationale, and must-fix items.

### Book / Longform Failures

The line fails if any of these appear:

- Titles such as "local sample", "contract proof", or "fixture" on a reader page.
- `audit/`, `source-excerpts`, local filesystem paths, source ids, hashes, or
  machine statuses in the main reader content.
- EPUB spine filenames or extraction placeholders presented as content.
- AI guide text before the reader can enter the body.
- A chapter-only output described as whole-book acceptance.

## Skill / Engineering-Material Line

### Product Promise

The reader opens a Chinese package and can understand how a Skill or workflow is
designed, why it works, what can be reused, and where the boundaries are. It
should feel like a product-minded technical lead is helping them read the
engineering material, not like a prompt summary or file inventory.

### Reader-Facing Shape

A passing Skill / engineering-material output contains:

1. **Start page**
   - Names the Skill package or engineering material.
   - Explains what class of problem it solves.
   - States whether the output covers one Skill, one module, or a multi-Skill
     package.
   - Tells the reader where to start.

2. **Capability / module map**
   - Groups materials by problem domain or capability, not by raw file order.
   - Shows which Skills, scripts, templates, checks, examples, and tests support
     each module.
   - Marks unresolved or low-confidence grouping as structure diagnosis, not as
     a finished reading route.

3. **Cleaned-body main reader page**
   - Gives each core Skill or module a readable body-first page.
   - Preserves purpose, trigger conditions, user intent, workflow, constraints,
     failure conditions, output requirements, and design highlights.
   - Removes runtime shell, repeated templates, install commands, local paths,
     hashes, and machine state from the main body.
   - Does not replace the cleaned body with AI explanation.

4. **Nearby companion explanation**
   - Explains concrete design choices near the cleaned body they affect.
   - Clarifies why a constraint, workflow step, output order, or failure rule is
     there.
   - Names misread risks and transfer boundaries.

5. **Technical lead explanation page**
   - Assumes the reader is a product owner, not a full-time engineer.
   - Explains why the Skill is designed this way, why it is effective, what
     would break without the design, and what tradeoffs it accepts.
   - Reads original sources such as `SKILL.md`, README, scripts, templates,
     examples, and tests. It must not only rephrase the cleaned body.

6. **Design asset cards**
   - Serve future background-free Agent reuse.
   - Each card is independently understandable without opening the original
     source.
   - Each card includes problem, use case, reusable move, source basis,
     preconditions, risks, boundaries, when not to use, and first action.

7. **Audit layer**
   - Preserves source registry, location map, source-cleaning map, evidence
     packet, rejected / downgraded notes, and machine / human status.
   - Does not become the normal reading surface.

### Skill / Engineering Acceptance Checks

A Skill / engineering output is reader-accepted only if all checks pass:

- A non-technical human reader can explain what the Skill or module does, why it
  is designed that way, and what failure it prevents.
- A product owner can tell whether the package is an engineering-material
  companion, not a prompt summary or audit dump.
- A background-free Agent can read only the asset-card page and know how to
  reuse at least one design asset safely.
- Every completed core Skill has a cleaned-body main page, not just a checklist
  entry or pending target path.
- Runtime shell stripped from the main body is still accounted for in audit,
  appendix, technical explanation, or asset cards when it carries design value.
- The output reports which check passed: structure, content completeness, human
  reader experience, product expectation, or Agent reuse. It never collapses
  them into one generic reader pass.

### Skill / Engineering Failures

The line fails if any of these appear:

- The output is only a directory, manifest, status table, or list of pending
  pages.
- A completed Skill has no cleaned-body reader page.
- AI explanation replaces the cleaned source body.
- Technical explanation is an implementation log or term glossary rather than a
  product-owner explanation of design choices.
- Asset cards require opening `body.md`, raw source, technical notes, or
  full-source-track to understand how to reuse them.
- Rules are special-cased to GSTACK instead of expressed as general Skill /
  engineering-material requirements.

## Development Implications

Future implementation work must keep these stages distinct:

1. Package / install skeleton.
2. Route smoke.
3. Reader product shape.
4. Reader evaluation.
5. Controller decision and scope-limited acceptance.

The existing installable package chain covers stages 1-2. The next product work
must connect the V2 reader-product shape to the installable package for both
book / longform and Skill / engineering lines.

Recommended next issues:

- Book / longform reader shape integration into the installable package.
- Skill / engineering reader shape integration into the installable package.

Both issues must use real non-GSTACK material in validation after any GSTACK
pressure sample, so the implementation does not overfit to GSTACK.
