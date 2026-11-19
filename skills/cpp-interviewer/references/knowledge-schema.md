# Knowledge Index Schema

The knowledge index is a JSON object with `domains`. Each domain contains interview topics.

```json
{
  "meta": {
    "version": "1.0",
    "description": "面试知识点索引"
  },
  "domains": [
    {
      "name": "C++语言",
      "topics": [
        {
          "id": "cpp_vtable",
          "name": "虚函数表（vtable）",
          "keywords": ["虚函数表", "vtable", "vptr"],
          "sources": [
            {"type": "book", "path": "books/C++/...", "relevance": "high"},
            {"type": "url", "url": "https://...", "relevance": "medium"}
          ],
          "interview_frequency": "very_high",
          "related_topics": ["cpp_oop", "os_memory_layout"]
        }
      ]
    }
  ]
}
```

## Rules

- Keep topic ids stable, lowercase, and underscore-separated.
- Use `interview_frequency` values: `very_high`, `high`, `medium`, `low`, or `very_low`.
- Keep `sources` relative to the repository when possible.
- A listed source is not evidence that it was read. Check availability before consulting it. Book PDFs may be user-supplied and absent; skip missing sources without blocking basic learning, and never invent citations or extracted content.
- Add `related_topics` only when the connection is useful for interview follow-up.
- Validate the JSON after every edit.
