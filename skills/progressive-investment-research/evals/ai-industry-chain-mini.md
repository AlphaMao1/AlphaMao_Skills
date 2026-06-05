# AI Industry Chain Mini Eval Prompts

These prompts are manual evals for the public fixture. They check whether an agent uses the current dossier contract instead of producing a generic report.

## Eval 1: Current Status Recovery

Prompt:

```text
Using fixtures/ai-industry-chain-mini, tell me the current model in five bullets and name the files you used.
```

Expected behavior:

- Starts from `current-synthesis.md`.
- Mentions `model-map.md` and `open-questions.md` when explaining scope and next work.
- Does not treat illustrative numbers as factual market data.

## Eval 2: Open Question Routing

Prompt:

```text
I found a new source claiming AI workflow products have high gross margin. Where should this go before it changes the model?
```

Expected behavior:

- Routes the source through source quality review.
- Creates or updates evidence rows or a module before changing Current Model.
- Identifies workflow application profit as an active question.

## Eval 3: Fallback Without Local Tools

Prompt:

```text
AnySearch and local PDF tools are unavailable. How should I continue the research?
```

Expected behavior:

- Uses available agent search/browser/file-reading capabilities.
- Records source tier, permission status, and acquisition method.
- Refuses to promote snippets directly into model conclusions.
