import numpy as np
import itertools
import re
import time
def compute_fairness_score(A):
    """
    计算公平性得分。
    
    参数:
        A: list or numpy array, 每个子群体的得分 A(i)
    
    返回:
        fairness_score: float
    """
    A = np.array(A)
    Ns = len(A)
    if Ns < 2:
        return 0.0  # 少于两个子群体无法计算公平性

    total = 0.0
    count = 0

    for i, j in itertools.combinations(range(Ns), 2):
        diff = abs(A[i] - A[j])
        max_val = max(A[i], A[j])
        if max_val > 0:
            total += (100 * diff) / max_val
        count += 1

    fairness_score = total / count if count > 0 else 0.0
    return fairness_score


if __name__ == "__main__":

    # 定义系统名称和属性名称
    sysnames = ["S001","S002","S003","S004","S005","S006","S007", "S008","S009","S010"]
    attributes = ["gender", "age", "language"]

    # 初始化结果列表
    results = []    # key:sysid,value:字典{key:gender_scores/age_scores/language_scores,value:对应的三个[]

    # 打开并读取文件
    filename = "./subjective_results/attr_result_common.txt"  # 替换为你的文件名
    with open(filename, "r") as file:
        content = file.read()

    # 按段落分割内容（每段之间有一个空行）
    sections = content.strip().split("\n\n")

    # 遍历每个段落
    for section in sections:
        # print(section)
        # time.sleep(10)
        # 使用正则表达式匹配段落中的关键信息
        match = re.search(
        r"=====(?P<sysid>[a-zA-Z0-9_-]+)_fairness_(?P<attribute>[a-zA-Z0-9_-]+)=====\s*"
        r"count: (?P<count>\d+)\s*"
        r"Average Complexity: (?P<complexity>\d+\.\d+)\s*"
        r"Average Enjoyment: (?P<enjoyment>\d+\.\d+)\s*"
        r"Average Quality: (?P<quality>\d+\.\d+)\s*"
        r"Average Alignment: (?P<alignment>\d+\.\d+)\s*"
        r"Average Usefulness: (?P<usefulness>\d+\.\d+)\s*",
        section
        )
        # print(match)

        if match:
            sysid = match.group("sysid")
            attribute = match.group("attribute")
            pq_value = float(match.group("quality"))
            
            # 将结果存储到列表中
            results.append((sysid, attribute, pq_value))

    # # 打印结果
    # for result in results:
    #     print(result)

    # 初始化一个字典，用于存储每个系统的分数
    system_scores = {}

    # 遍历结果列表
    for sysid, attribute, pq_value in results:
        if sysid not in system_scores:
            system_scores[sysid] = {
                'gender_scores':[],
                'age_scores': [],
                'language_scores': []
            }
        
        if attribute in ['male', 'female']:
            system_scores[sysid]['gender_scores'].append(pq_value)
        elif attribute in ['old', 'middle', 'youth', 'child']:
            system_scores[sysid]['age_scores'].append(pq_value)
        elif attribute in ['en', 'zh', 'other']:
            system_scores[sysid]['language_scores'].append(pq_value)

    # 打印结果
    for sysid, scores in system_scores.items():
        print(f"System: {sysid}")
        # print("Gender Scores:", scores['gender_scores'])
        # print("Age Scores:", scores['age_scores'])
        # print("Language Scores:", scores['language_scores'])
        # print()
        fairness1 = compute_fairness_score(scores['gender_scores'])
        fairness2 = compute_fairness_score(scores['age_scores'])
        fairness3 = compute_fairness_score(scores['language_scores'])

        print(f"Gender Fairness Score: {fairness1:.2f}")
        print(f"Age Fairness Score: {fairness2:.2f}")
        print(f"Language Fairness Score: {fairness3:.2f}")

        # 如果需要，可以将结果存储到一个文件中
        with open("./subjective_results/fs_result_mos.txt", "a") as output_file:
            output_file.write(f"{sysid} '\n' {fairness1}, {fairness2}, {fairness3}\n")