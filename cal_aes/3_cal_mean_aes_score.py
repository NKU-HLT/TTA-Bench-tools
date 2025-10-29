"""
Calculate mean aes scores for each dimension of each system
"""
import os
import json
from utils.config import SYS_NAMES, EVAL_DIMS, AES_RESULT_FILE, AES_RESULTS_JSON_DIR
from utils.common import ensure_dir

def summarize_aes_scores():
    """汇总每个系统的平均 AES 指标"""
    outfile = AES_RESULT_FILE
    ensure_dir(os.path.dirname(outfile))

    with open(outfile, 'w', encoding='utf-8') as f_out:
        for sys_name in SYS_NAMES:
            for eval_dim in EVAL_DIMS:
                tag = f"{sys_name}_{eval_dim}"
                result_jsonl = os.path.join(AES_RESULTS_JSON_DIR, f"{tag}.jsonl")

                if not os.path.exists(result_jsonl):
                    print(f"警告：{result_jsonl} 不存在，跳过")
                    continue

                total_ce = total_cu = total_pc = total_pq = count = 0

                with open(result_jsonl, 'r', encoding='utf-8') as f_in:
                    for line in f_in:
                        data = json.loads(line)
                        total_ce += data.get('CE', 0)
                        total_cu += data.get('CU', 0)
                        total_pc += data.get('PC', 0)
                        total_pq += data.get('PQ', 0)
                        count += 1

                if count > 0:
                    avg_ce = total_ce / count
                    avg_cu = total_cu / count
                    avg_pc = total_pc / count
                    avg_pq = total_pq / count
                else:
                    avg_ce = avg_cu = avg_pc = avg_pq = 0

                print(f"\n==== {tag} ====")
                print(f"样本数: {count}")
                print(f"平均 CE: {avg_ce:.4f}")
                print(f"平均 CU: {avg_cu:.4f}")
                print(f"平均 PC: {avg_pc:.4f}")
                print(f"平均 PQ: {avg_pq:.4f}")

                f_out.write(f"{tag}\n{avg_ce},{avg_cu},{avg_pc},{avg_pq}\n")

    print(f"\n汇总结果已保存至 {outfile}")

if __name__ == "__main__":
    summarize_aes_scores()
