# Coach Mode

Use this mode for active interview practice. The coach asks one question, waits for the user's answer, evaluates, saves state when possible, and then asks the next question.

Before the first evaluation in a training session, read [coach-scoring.md](coach-scoring.md) for scoring anchors, the total-score formula, and non-applicable code handling. Read only the relevant example in [answer-examples.md](answer-examples.md) if the response shape needs clarification; do not reload all examples for each question.

## Commands

- `start`: ask which topic or direction the user wants, then enter the training loop.
- `weak`: train weak topics from `python -m coach.cli weak --json`.
- `due`: train due review topics from `python -m coach.cli due --json`.
- `status`: show the mastery dashboard from `python -m coach.cli status --json`.
- `plan`: show today's plan from `python -m coach.cli plan --json`.
- `reset`: reset local training state only after explicit user confirmation; run `python -m coach.cli reset --yes --json`. The knowledge index must remain intact.
- `export`: let the user choose `md`, `doc`, `txt`, or `json`; if no path is given, use `coach-export.<format>`. Run `python -m coach.cli export --format <format> --output <path> --json`.
- Any other text: treat as a topic keyword and resolve it with `python -m coach.cli topic search "<keyword>" --json`.

## Training Loop

1. Resolve the topic id and topic name.
2. Load mastery with `python -m coach.cli topic-info "<topic_id>" --json`.
3. Pick difficulty:
   - mastery `< 0.3`: difficulty 1, basic.
   - mastery `0.3-0.7`: difficulty 2, intermediate.
   - mastery `> 0.7`: difficulty 3, deep or edge-case.
4. Ask exactly one interview question. Keep it under two sentences.
5. Stop and wait for the user's answer. Do not give the answer, score, or save a result before the user responds. Handle exit requests before any evaluation or next question; a status/help command is not an answer to grade.
6. Score the actual answer using `coach-scoring.md` on six dimensions from 0.0 to 1.0:
   - correctness
   - completeness
   - depth
   - clarity
   - code_accuracy
   - edge_case_awareness
7. If persistence is available, save this answer and evaluation once with `python -m coach.cli save-result ... --json`. Check the command result before saying it was saved; do not automatically repeat a write whose outcome is uncertain.
8. Give short feedback grounded in the answer, distinguish missing points from wrong points, and show a mastery update only when confirmed by state. Then ask one follow-up or next question if training is still active.

## Topic Context

Before writing a question, call `python -m coach.cli topic-context "<topic_id>" --json` when the CLI is available. Use `keywords`, `related_topics`, and `related_topic_names` as the hard scope for the question.

Question templates:

| Difficulty | Template | Use for |
|------------|----------|---------|
| 1 | Concept or usage scenario | Core terms, when to use it, what breaks without it |
| 2 | Mechanism or comparison | Runtime behavior, data structures, two related concepts |
| 3 | Code result or edge-case scenario | Inheritance edges, concurrency edges, ABI/platform caveats |

Question constraints:

- Cover at least two `keywords`, or directly test the relationship between those keywords.
- For difficulty 2 or 3, hook at least one `related_topic` when it is available.
- Keep the question body under two sentences.
- Prefer "why", "when", "compare", and "what happens in this code" over dictionary-definition prompts.
- Do not invent APIs, language rules, compiler behavior, or data structures.

Example for a virtual-function topic with `keywords=["vtable","vptr","dynamic binding"]` and `related_topic_names=["C++ object model","multiple inheritance"]`:

- difficulty 1: "What is a vtable, and how is it related to objects that store a vptr?"
- difficulty 2: "What does dynamic binding decide at compile time versus runtime, and where does the vptr participate?"
- difficulty 3: "Under multiple inheritance, how many vptrs might an object contain, and how does that affect virtual dispatch?"

## Evaluation JSON

```json
{
  "rating": "good",
  "score_total": 0.82,
  "correctness": 0.9,
  "completeness": 0.8,
  "depth": 0.7,
  "clarity": 0.9,
  "code_accuracy": 0.8,
  "edge_case_awareness": 0.7,
  "missing_points": [],
  "wrong_points": [],
  "weakness_tags": [],
  "hallucinated_points": [],
  "evaluator_confidence": 0.9
}
```

Calculate `score_total` using the applicable-dimension formula in `coach-scoring.md`, then use `rating=good` for `score_total >= 0.7`, `okay` for `>= 0.4`, and `poor` below `0.4`. The example above has all six dimensions applicable; do not copy its scores to unrelated answers.

## Output Discipline

- Do not give long teaching paragraphs during training unless the user asks.
- Do not ask multiple questions at once.
- End the loop when the user says "退出", "不练了", "够了", or equivalent.
- If persistence fails, continue in pure conversation mode and say that state was not saved.
- If mastery or history cannot be read, do not invent it. For a new conversational session, start at a basic question or honor an explicitly requested difficulty; keep persistence-disabled behavior visible without repeatedly interrupting training.
