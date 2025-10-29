import numpy as np
import itertools
import re
import argparse
import os


def compute_fairness_score(A):
    """
    Compute the fairness score among subgroups.

    Args:
        A (list or np.ndarray): Scores of each subgroup.

    Returns:
        float: Fairness score (0 if less than two groups).
    """
    A = np.array(A)
    if len(A) < 2:
        return 0.0

    total, count = 0.0, 0
    for i, j in itertools.combinations(range(len(A)), 2):
        diff = abs(A[i] - A[j])
        max_val = max(A[i], A[j])
        if max_val > 0:
            total += (100 * diff) / max_val
        count += 1

    return total / count if count > 0 else 0.0


def parse_results(filename, metric):
    """
    Parse system-attribute scores from a result file.

    Args:
        filename (str): Path to the input result file.
        metric (str): Metric name, e.g. 'AES' or 'CLAP'.

    Returns:
        list of (sysname, attribute, score)
    """
    with open(filename, "r") as f:
        content = f.read()

    sections = content.strip().split("\n\n")

    # Pattern differs only in the metric field
    pattern = re.compile(
        rf"=====(?P<sysname>[a-zA-Z0-9_-]+)_fairness_(?P<attribute>\w+)=====\s*"
        rf"count: \d+\s*"
        rf"Average {metric.upper()}: (?P<pq_value>\d+\.\d+)"
    )

    results = []
    for section in sections:
        match = pattern.search(section)
        if match:
            sysname = match.group("sysname")
            attribute = match.group("attribute")
            pq_value = float(match.group("pq_value"))
            results.append((sysname, attribute, pq_value))
    return results


def main(args):
    results = parse_results(args.input, args.metric)
    system_scores = {}

    for sysname, attribute, pq_value in results:
        if sysname not in system_scores:
            system_scores[sysname] = {
                "gender_scores": [],
                "age_scores": [],
                "language_scores": []
            }

        if attribute in ["male", "female"]:
            system_scores[sysname]["gender_scores"].append(pq_value)
        elif attribute in ["old", "middle", "youth", "child"]:
            system_scores[sysname]["age_scores"].append(pq_value)
        elif attribute in ["en", "zh", "other"]:
            system_scores[sysname]["language_scores"].append(pq_value)

    # Output file path
    output_file = f"fs_result_{args.metric.lower()}.txt"
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    with open(output_file, "a") as f:
        for sysname, scores in system_scores.items():
            fairness_gender = compute_fairness_score(scores["gender_scores"])
            fairness_age = compute_fairness_score(scores["age_scores"])
            fairness_lang = compute_fairness_score(scores["language_scores"])

            print(f"[{args.metric}] System: {sysname}")
            print(f"  Gender Fairness: {fairness_gender:.2f}")
            print(f"  Age Fairness: {fairness_age:.2f}")
            print(f"  Language Fairness: {fairness_lang:.2f}")

            f.write(
                f"{sysname}, {fairness_gender:.2f}, "
                f"{fairness_age:.2f}, {fairness_lang:.2f}\n"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute fairness scores for different metrics.")
    parser.add_argument(
        "--metric", type=str, required=True, choices=["aes", "clap"],
        help="Type of score source (aes or clap)."
    )
    parser.add_argument(
        "--input", type=str, required=True,
        help="Path to the attribute result file."
    )
    args = parser.parse_args()
    main(args)
