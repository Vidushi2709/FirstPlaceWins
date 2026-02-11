import pandas as pd
import random

INPUT_FILE = "data/question_base.csv"
OUTPUT_FILE = "data/questions_shuffled.csv"
N_SHUFFLES = 12
RANDOM_SEED = 42

# SET SEED FOR REPRODUCIBILITY
random.seed(RANDOM_SEED)

base_df = pd.read_csv(INPUT_FILE)

required_cols = {
    "question_id",
    "task_type",
    "question_text",
    "opt_1",
    "opt_2",
    "opt_3",
    "opt_4",
}

if not required_cols.issubset(base_df.columns):
    raise ValueError("questions_base.csv is missing required columns")

rows = []

for _, row in base_df.iterrows():
    options = [row["opt_1"], row["opt_2"], row["opt_3"], row["opt_4"]]

    for shuffle_id in range(1, N_SHUFFLES + 1):
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)

        for position, option_text in enumerate(shuffled_options, start=1):
            option_label = chr(ord("A") + position - 1)

            rows.append({
                "question_id": row["question_id"],
                "task_type": row["task_type"],
                "question_text": row["question_text"],
                "shuffle_id": shuffle_id,
                "option_label": option_label,
                "option_text": option_text,
                "option_position": position,
            })

shuffled_df = pd.DataFrame(rows)

shuffled_df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(shuffled_df)} rows → {OUTPUT_FILE}")
