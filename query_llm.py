import os
import time
import json
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

# CONFIG
INPUT_FILE = "questions_shuffled.csv"
OUTPUT_FILE = "results.csv"
TEMPERATURE = 0
MAX_TOKENS = 5
SLEEP_SECONDS = 1.2

# OpenRouter models
MODELS = {
    "gpt4": "openai/gpt-4",
    "claude_sonnet": "anthropic/claude-3.5-sonnet",
    "llama": "meta-llama/llama-3.1-70b-instruct",
}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# LOAD ENV
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# PROMPT TEMPLATE
PROMPT_TEMPLATE = """You are participating in a controlled evaluation.

Choose the best answer.
Respond with ONLY the option letter (A, B, C, or D). Do not explain.

Question:
{question}

Options:
A. {A}
B. {B}
C. {C}
D. {D}

Answer:
"""

# QUERY FUNCTION
def query_model(model_name, prompt):
    payload = {
        "model": MODELS[model_name],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=HEADERS,
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()

    text = response.json()["choices"][0]["message"]["content"].strip()
    return text

print(f"Loading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} total rows")

results = []

grouped = df.groupby(["question_id", "shuffle_id"])
total_combinations = len(grouped)
print(f"Found {total_combinations} question/shuffle combinations")
print(f"Will make {total_combinations * len(MODELS)} total API calls")
print("Starting queries...\n")

for idx, ((question_id, shuffle_id), group) in enumerate(grouped, 1):
    print(f"[{idx}/{total_combinations}] Processing {question_id}, Shuffle {shuffle_id}")
    group = group.sort_values("option_position")

    question_text = group["question_text"].iloc[0]
    task_type = group["task_type"].iloc[0]

    options = {
        row["option_label"]: row["option_text"]
        for _, row in group.iterrows()
    }

    # Debug: Check if all options are present
    expected_options = ["A", "B", "C", "D"]
    missing_options = [opt for opt in expected_options if opt not in options]
    
    if missing_options:
        print(f"    WARNING: Missing options {missing_options} for Q{question_id}, Shuffle {shuffle_id}")
        print(f"    Available options: {list(options.keys())}")
        print(f"    Group size: {len(group)} rows")
        continue  # Skip this combination
    
    prompt = PROMPT_TEMPLATE.format(
        question=question_text,
        A=options["A"],
        B=options["B"],
        C=options["C"],
        D=options["D"],
    )

    for model_name in MODELS:
        print(f"  -> Querying {model_name}...")
        try:
            raw_answer = query_model(model_name, prompt)
            choice_letter = raw_answer[:1].upper()
        except Exception as e:
            print(f"    ERROR with {model_name}: {e}")
            raw_answer = f"ERROR: {e}"
            choice_letter = None

        chosen_row = group[group["option_label"] == choice_letter]
        chosen_position = (
            int(chosen_row["option_position"].iloc[0])
            if not chosen_row.empty
            else None
        )

        results.append({
            "timestamp": datetime.utcnow().isoformat(),
            "model": model_name,
            "question_id": question_id,
            "task_type": task_type,
            "shuffle_id": shuffle_id,
            "model_choice_letter": choice_letter,
            "model_choice_position": chosen_position,
            "raw_response": raw_answer,
        })

        print(f"    > {model_name} chose: {choice_letter}")
        time.sleep(SLEEP_SECONDS)
    
    if idx % 10 == 0:
        print(f"Progress: {idx}/{total_combinations} combinations completed ({idx/total_combinations*100:.1f}%)\n")

print(f"\nAll queries completed! Saving results...")
results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved {len(results_df)} rows -> {OUTPUT_FILE}")
print(f"Breakdown: {total_combinations} questions x {len(MODELS)} models = {len(results_df)} total responses")
