import argparse
import itertools
import os
import re
from typing import Dict, List

import numpy as np

from utils.config import PATHS


GENDER = {"male", "female"}
AGE = {"old", "middle", "youth", "child"}
LANG = {"en", "zh", "other"}


def compute_fairness_score(values: List[float]) -> float:
	values = np.array(values, dtype=float)
	if values.size < 2:
		return 0.0
	total, count = 0.0, 0
	for i, j in itertools.combinations(range(len(values)), 2):
		a, b = values[i], values[j]
		m = max(a, b)
		if m > 0:
			total += 100.0 * abs(a - b) / m
		count += 1
	return total / count if count else 0.0


def parse_mos_attr_file(filename: str):
	with open(filename, "r", encoding="utf-8") as f:
		content = f.read().strip()
	sections = content.split("\n\n") if content else []

	# Capture system id, dimension, attribute, and quality value
	pattern = re.compile(
		r"=====(?P<sysid>[A-Za-z0-9_-]+)_(?P<dim>[A-Za-z0-9_-]+)_(?P<attr>[A-Za-z0-9_-]+)=====\s*"
		r"count: (?P<count>\d+)\s*"
		r"Average Complexity: (?P<complexity>\d+\.\d+)\s*"
		r"Average Enjoyment: (?P<enjoyment>\d+\.\d+)\s*"
		r"Average Quality: (?P<quality>\d+\.\d+)\s*"
		r"Average Alignment: (?P<alignment>\d+\.\d+)\s*"
		r"Average Usefulness: (?P<usefulness>\d+\.\d+)\s*",
		re.MULTILINE,
	)

	records = []
	for section in sections:
		m = pattern.search(section)
		if not m:
			continue
		sysid = m.group("sysid")
		dim = m.group("dim")
		attr = m.group("attr")
		quality = float(m.group("quality"))
		records.append((sysid, dim, attr, quality))
	return records


def main():
	parser = argparse.ArgumentParser(description="Compute fairness scores from MOS attribute results.")
	parser.add_argument("--input", type=str, default=os.path.join(PATHS["subjective_result_dir"], "attr_result_common.txt"),
						help="Path to MOS attribute result file (default: subjective_results/attr_result_common.txt)")
	parser.add_argument("--output", type=str, default=os.path.join(PATHS["subjective_result_dir"], "fs_result_mos.txt"),
						help="Path to output file (default: subjective_results/fs_result_mos.txt)")
	args = parser.parse_args()

	records = parse_mos_attr_file(args.input)
	# Filter fairness dimension only
	fairness_records = [(s, a, q) for (s, d, a, q) in records if d == "fairness"]

	# Aggregate per system
	system_scores: Dict[str, Dict[str, List[float]]] = {}
	for sysid, attr, quality in fairness_records:
		entry = system_scores.setdefault(sysid, {
			"gender": [],
			"age": [],
			"language": [],
		})
		if attr in GENDER:
			entry["gender"].append(quality)
		elif attr in AGE:
			entry["age"].append(quality)
		elif attr in LANG:
			entry["language"].append(quality)

	# Compute and write results
	os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
	with open(args.output, "w", encoding="utf-8") as f:
		for sysid, groups in system_scores.items():
			fair_gender = compute_fairness_score(groups["gender"]) if groups["gender"] else 0.0
			fair_age = compute_fairness_score(groups["age"]) if groups["age"] else 0.0
			fair_lang = compute_fairness_score(groups["language"]) if groups["language"] else 0.0

			print(f"[MOS] System: {sysid}")
			print(f"  Gender Fairness: {fair_gender:.2f}")
			print(f"  Age Fairness: {fair_age:.2f}")
			print(f"  Language Fairness: {fair_lang:.2f}")

			f.write(f"{sysid}, {fair_gender:.2f}, {fair_age:.2f}, {fair_lang:.2f}\n")


if __name__ == "__main__":
	main()
