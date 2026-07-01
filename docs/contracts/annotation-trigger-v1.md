# Annotation Trigger v1

## Purpose

`annotation-trigger.v1` turns method output into body-adjacent questions the reader can actually annotate near the text. It prevents discussion prompts from floating above the source.

## Required Fields

```json
{
  "contract": "annotation-trigger.v1",
  "material_id": "string",
  "triggers": [
    {
      "trigger_id": "A1",
      "anchor_ref": "string",
      "reader_question": "string",
      "likely_misread": "string",
      "reply_mode": "explain | challenge | connect | boundary | verify"
    }
  ]
}
```

## Gate Rules

- Each chapter probe should output 3-7 annotation triggers.
- Every trigger must have a body-adjacent `anchor_ref`.
- The question must invite a reader judgment, not ask for a summary.
- `likely_misread` should describe the most probable shallow or dangerous reading.
- `reply_mode` must guide how Codex should respond to a future annotation.

## Failure Conditions

- `[FAIL]` An annotation question has no body anchor.
- `[FAIL]` The trigger asks a generic summary question.
- `[FAIL]` The trigger is based only on AI interpretation with no source-adjacent anchor.
