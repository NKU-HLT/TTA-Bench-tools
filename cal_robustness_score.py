import numpy as np
import re

def calculate_robustness_score(perturbed_scores, original_scores):
    """Calculate robustness score (RS_p) as a percentage ratio."""
    original_scores = np.array(original_scores, dtype=float)
    perturbed_scores = np.array(perturbed_scores, dtype=float)

    # Prevent division by zero
    original_scores = np.where(original_scores == 0, np.nan, original_scores)
    ratios = perturbed_scores / original_scores
    return ratios


if __name__ == "__main__":
    # Define system and perturbation attributes
    sysnames = [f"S{i:03d}" for i in range(1, 11)]
    attributes = ["uppercase", "synonym", "misspelling", "space", "rewrite", "punctuate"]
      
    # ===== Load unperturbed scores =====
    results_unp = {}  
    with open("./preprocess_data2/result_unperturbed_common.txt", "r") as f:
        content_unp = f.read().strip().split("\n\n")

    for section in content_unp:
        match = re.search(
            r"(?P<sysid>[a-zA-Z0-9_-]+)_acc_unperturbed\n"
            r"\d+\.\d+,\d+\.\d+,\d+\.\d+,(?P<quality>\d+\.\d+),\d+\.\d+",
            section
        )
        if match:
            sysid = match.group("sysid")
            pq_score = float(match.group("quality"))
            results_unp[sysid] = pq_score

    # ===== Load perturbed scores =====
    results = []  
    with open("./subjective_results/attr_result_common.txt", "r") as f:
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
            section
        )
        if match:
            sysid = match.group("sysid")
            attribute = match.group("attribute")
            pq_value = float(match.group("quality"))
            results.append((sysid, attribute, pq_value))

    # ===== Organize system scores =====
    system_scores = {sid: {a: 0 for a in attributes} for sid in sysnames}
    for sysid, attribute, pq_value in results:
        if sysid in system_scores:
            system_scores[sysid][attribute] = pq_value

    # ===== Compute and print robustness ratios =====
    for sysid, scores in system_scores.items():
        print(f"==== System: {sysid} ====")
        if sysid not in results_unp:
            print(f"[Warning] Missing unperturbed score for {sysid}. Skipping.")
            continue

        rs_values = {
            attr: calculate_robustness_score(scores[attr], results_unp[sysid])
            for attr in attributes
        }

        for attr, rs in rs_values.items():
            print(f"robust_{attr}: {rs:.4f}")

        rs_mean = np.nanmean(list(rs_values.values()))
        print(f"Mean Robustness: {rs_mean:.4f}\n")
