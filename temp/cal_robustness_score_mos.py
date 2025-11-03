import numpy as np
import itertools
import re
import time
def calculate_robustness_score(perturbed_scores, original_scores):
    """
    计算鲁棒性得分 RS_p（百分比形式）
    
    参数:
        original_scores (list/np.array): 原始分数列表
        perturbed_scores (list/np.array): 扰动后分数列表
    
    返回:
        float: 鲁棒性得分 RS_p (%)
    """
    original_scores = np.array(original_scores)
    perturbed_scores = np.array(perturbed_scores)
    
    # 返回该扰动类型与未扰动组的比值
    ratios = perturbed_scores / original_scores
    # print(ratios)
    return ratios


if __name__ == "__main__":

    # 定义系统名称和属性名称
    sysnames = ["S001","S002","S003","S004","S005","S006","S007", "S008","S009","S010"]
    attributes = ["uppercase", "synonym", "misspelling", "space", "rewrite", "punctuate"]
      
    #===========未扰动===========
    # key:sysid,value:该系统未扰动组的PQ均分
    results_unp = {}  
    unperturb_file = "./preprocess_data2/result_unperturbed_common.txt"
    with open(unperturb_file, "r") as file1:
        content_unp = file1.read()
    sections_unp = content_unp.strip().split("\n\n")
    for section in sections_unp:
        # print(section)
        # time.sleep(10)
        # 使用正则表达式匹配段落中的关键信息
        match = re.search(
            r"(?P<sysid>[a-zA-Z0-9_-]+)_acc_unperturbed\n(\d+\.\d+),(\d+\.\d+),(\d+\.\d+),\d+\.\d+,\d+\.\d+",
            section
        )

        if match:
            sysid = match.group("sysid")
            if sysid not in results_unp:
                results_unp[sysid] = 0
            pq_score = float(match.group(4))
            # print(f"quality score是: {pq_score}")
            # 将结果存储到列表中
            results_unp[sysid] = pq_score
    # for sysid,score_up in results_unp.item():
    #     print(sysid,",",score_up)


    #===========扰动后===========
    # 初始化结果列表
    results = []  
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
        r"=====(?P<sysid>[a-zA-Z0-9_-]+)_robustness_(?P<attribute>[a-zA-Z0-9_-]+)=====\s*"
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

    # 打印结果
    # for result in results:
    #     print(result)

    
    # 整出来一个字典，用于存储每个系统的6种扰动后均分
    # key:sysid,value:字典{key:6种扰动类型名称,value:对应的Quality值
    system_scores = {}

    # 遍历结果列表
    for sysid, attribute, pq_value in results:
        if sysid not in system_scores:
            system_scores[sysid] = {
                'uppercase': 0,
                'synonym': 0, 
                'misspelling': 0, 
                'space': 0, 
                'rewrite': 0, 
                'punctuate': 0
            }
        system_scores[sysid][attribute] = pq_value

    # 打印结果
    for sysid, scores in system_scores.items():
        print(f"====System: {sysid}====")
        
        robust_up = calculate_robustness_score(scores['uppercase'],results_unp[sysid])
        robust_sy = calculate_robustness_score(scores['synonym'],results_unp[sysid])
        robust_mi = calculate_robustness_score(scores['misspelling'],results_unp[sysid])
        robust_sp = calculate_robustness_score(scores['space'],results_unp[sysid])
        robust_re = calculate_robustness_score(scores['rewrite'],results_unp[sysid])
        robust_pu = calculate_robustness_score(scores['punctuate'],results_unp[sysid])

        print("robust_up:",robust_up,",robust_sy:",robust_sy,",robust_mi:",robust_mi,",robust_sp:",robust_sp,",robust_re:",robust_re,",robust_pu:",robust_pu)
        # 如果需要，可以将结果存储到一个文件中
        # with open("./subjective_results/rs_result_mos.txt", "a") as output_file:
        #     output_file.write(f"====={sysid}=====\n")
        #     output_file.write(f"robust1:{robust1}\nrobust2:{robust2}\nrobust3:{robust3}\nrobust4:{robust4}\nrobust5:{robust5}\nrobust6:{robust6}\n")

        robust_mean = (robust_up+robust_sy+robust_mi+robust_sp+robust_re+robust_pu) / 6
        print(robust_mean)
        # with open("./subjective_results/rs_result_mos_mean.txt", "a") as output_file:
        #     output_file.write(f"====={sysid}=====\n")
        #     output_file.write(f"{robust_mean}\n")
          
        