# FirstPlaceWins? ¯\_(ツ)_/¯

## When Order Starts Winning

> Does option order influence LLM decisions?
> And does that influence grow when questions become ambiguous?

We assume that when LLMs act as judges, rankers, or evaluators:

```

"Order shouldn't matter."

```

This project tests that assumption.

Spoiler:
It matters.

---

# 1. The Core Idea ^_____^

Imagine four answer choices.

You shuffle them.

You reshuffle them.

You reshuffle them again.

If the model is unbiased:

```
Position 1 -> 25%
Position 2 -> 25%
Position 3 -> 25%
Position 4 -> 25%
```

Clean. Even. Structure-independent.

But if Position 1 keeps winning?

That’s not content.
That’s structure.

This project asks:

```
→ Does first-position bias exist?
→ Does ambiguity amplify it?
```

---

# 2. Experimental Setup ^_____^

## Models Tested

* GPT-4
* Claude 3.5 Sonnet
* LLaMA 3.1 70B

## Dataset

* 23 questions
* 700 total responses
* 3 task categories:

```
[ Objective ]  → High certainty
[ Subjective ] → Moderate ambiguity
[ Ethical ]    → High ambiguity
```

## Method ^_____^

1. Start with `question_base.csv`
2. Shuffle answer order
3. Keep content identical
4. Query model
5. Record selected position
6. Store in `results.csv`

Only order changes.

Nothing else.

---

# 3. Repository Structure ^_____^

```
FirstPlaceWins/
│
├── question_base.csv          # Original questions
├── shuffle.py                 # Generates permutations
├── questions_shuffled.csv     # Shuffled variants
├── query_llm.py               # Model querying script
├── results.csv                # Collected selections
├── position_bias.ipynb        # Analysis notebook
├── .env                       # API keys (not committed)
└── .gitignore
```

Pipeline:

```
question_base.csv
        │
        ▼
     shuffle.py
        │
        ▼
questions_shuffled.csv
        │
        ▼
     query_llm.py
        │
        ▼
      results.csv
        │
        ▼
 position_bias.ipynb
```

Clean. Controlled. Isolated variable: position.

---

# 4. Results ^_____^

## Overall Bias

Observed:

```
First position selected: 30.3%
Expected: 25%
p-value: 0.004
```

Statistically significant.

All three models leaned toward Position 1.

---

## Ambiguity Effect

| Task Type  | First Position Rate | What It Means                  |
| ---------- | ------------------- | ------------------------------ |
| Objective  | Lowest bias         | Content dominates              |
| Subjective | Moderate bias       | Structure creeping in          |
| Ethical    | 37.3%               | Structure strongly influencing |

Pattern:

```
As certainty ↓
Position bias ↑
```

When the model knows the answer,
order barely matters.

When it hesitates,
structure starts guiding decisions.

---

# 5. Why Might This Happen? ^_____^

Possible drivers:

• Transformers process tokens sequentially
• Training data often implies ranking in lists
• Small logit differences amplify via softmax
• Under uncertainty, heuristics kick in

This is likely emergent behavior —
not a hard-coded rule.

But it’s measurable.

---

# 6. Why This Matters ^_____^

LLMs increasingly act as:

```
- Judges
- Evaluators
- Rankers
- Alignment scorers
- Reward models
```

If order influences selection:

```
Leaderboards may shift.
Benchmarks may drift.
Evaluations may not be formatting-invariant.
```

That’s a systems design issue — not a model quality issue.

Structure shapes decisions.

---

# 7. Mitigation Strategies ^_____^

If you're building LLM evaluation systems:

```
[✓] Randomize answer order
[✓] Average across permutations
[✓] Flip pairwise comparisons
[✓] Test for order invariance
[✓] Avoid fixed multi-choice judging prompts
```

Evaluation must be structure-robust.

---

# 8. The Takeaway ^_____^

We expect:

```
Order doesn't matter.
```

We observe:

```
It does.
```

And the less certain the model is,
the more it leans on structure.

---

# 9. Future Directions ^_____^

* Logit-level inspection
* Temperature sensitivity
* Larger datasets
* Additional model families
* Cross-lingual replication
* Bias mitigation benchmarking

---

FirstPlaceWins is a simple experiment with a clear signal:

When ambiguity rises,
position starts winning.

☆*: .｡. o(≧▽≦)o .｡.:*☆

---
