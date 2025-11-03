import numpy as np
import re
import os
from utils.config import PATHS

def calculate_robustness_score(perturbed_scores, original_scores):
    """Calculate robustness score (RS_p) as a percentage ratio."""
    original_scores = np.array(original_scores, dtype=float)
    perturbed_scores = np.array(perturbed_scores, dtype=float)

    # Prevent division by zero
    original_scores = np.where(original_scores == 0, np.nan, original_scores)
    ratios = perturbed_scores / original_scores
    return ratios


if __name__ == "__main__":
    # Define expected robustness attributes (should match prompt annotations)
    attributes = ["uppercase", "synonym", "misspelling", "space", "rewrite", "punctuate"]

    # ===== Load baseline (unperturbed) quality per system for robustness dimension =====
    results_unp = {}
    baseline_file = os.path.join(PATHS["subjective_result_dir"], "result_common.txt")
    if not os.path.exists(baseline_file):
        raise FileNotFoundError(f"Baseline file not found: {baseline_file}")
    with open(baseline_file, "r", encoding="utf-8") as f:
        content_unp = f.read().strip().split("\n\n")

    for section in content_unp:
        match = re.search(
            r"=====(?P<sysid>[a-zA-Z0-9_-]+)_robustness=====\s*"
            r"count: (?P<count>\d+)\s*"
            r"Average Complexity: (?P<complexity>\d+\.\d+)\s*"
            r"Average Enjoyment: (?P<enjoyment>\d+\.\d+)\s*"
            r"Average Quality: (?P<quality>\d+\.\d+)\s*"
            r"Average Alignment: (?P<alignment>\d+\.\d+)\s*"
            r"Average Usefulness: (?P<usefulness>\d+\.\d+)\s*",
            section,
        )
        if match:
            sysid = match.group("sysid")
            pq_score = float(match.group("quality"))
            results_unp[sysid] = pq_score

    # ===== Load perturbed (attribute-level) scores =====
    attr_file = os.path.join(PATHS["subjective_result_dir"], "attr_result_common.txt")
    if not os.path.exists(attr_file):
        raise FileNotFoundError(f"Attribute file not found: {attr_file}")
    results = []
    with open(attr_file, "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n\n")

    for section in content:
        match = re.search(
            r"=====(?P<sysid>[a-zA-Z0-9_-]+)_robustness_(?P<attribute>[a-zA-Z0-9_-]+)=====\s*"
            r"count: (?P<count>\d+)\s*"
            r"Average Complexity: (?P<complexity>\d+\.\d+)\s*"
            r"Average Enjoyment: (?P<enjoyment>\d+\.\d+)\s*"
            r"Average Quality: (?P<quality>\d+\.\d+)\s*"
            r"Average Alignment: (?P<alignment>\d+\.\d+)\s*"
            r"Average Usefulness: (?P<usefulness>\d+\.\d+)\s*",
            section,
        )
        if match:
            sysid = match.group("sysid")
            attribute = match.group("attribute")
            pq_value = float(match.group("quality"))
            results.append((sysid, attribute, pq_value))

    # ===== Organize system scores =====
    system_scores = {}
    for sysid, attribute, pq_value in results:
        system_scores.setdefault(sysid, {a: np.nan for a in attributes})
        if attribute in system_scores[sysid]:
            system_scores[sysid][attribute] = pq_value

    # ===== Compute and print robustness ratios =====
    for sysid, scores in system_scores.items():
        print(f"==== System: {sysid} ====")
        if sysid not in results_unp or results_unp[sysid] == 0:
            print(f"[Warning] Missing or zero baseline for {sysid}. Skipping.")
            continue

        baseline = results_unp[sysid]
        rs_values = {attr: (scores[attr] / baseline) for attr in attributes}

        for attr, rs in rs_values.items():
            print(f"robust_{attr}: {rs:.4f}")

        rs_mean = np.nanmean(list(rs_values.values()))
        print(f"Mean Robustness: {rs_mean:.4f}\n")
