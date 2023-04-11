import subprocess

import numpy as np
from rouge import Rouge

from bug_changing.utils.file_util import FileUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL, ROOT_DIR


class MetricsUtil:

    @staticmethod
    def accuracy(result_list):
        # print(len(result_list))
        accuracy = dict()
        accuracy[1] = accuracy.get(1, 0)
        accuracy[3] = accuracy.get(3, 0)
        accuracy[5] = accuracy.get(5, 0)
        accuracy[10] = accuracy.get(10, 0)
        for result in result_list:
            # print(result)
            indexs = np.nonzero(result)[0]

            for index in indexs:
                # print(index)
                if index == 0:
                    accuracy[1] = accuracy.get(1, 0) + 1
                    accuracy[3] = accuracy.get(3, 0) + 1
                    accuracy[5] = accuracy.get(5, 0) + 1
                    accuracy[10] = accuracy.get(10, 0) + 1
                    break
                elif 0 < index < 3:
                    accuracy[3] = accuracy.get(3, 0) + 1
                    accuracy[5] = accuracy.get(5, 0) + 1
                    accuracy[10] = accuracy.get(10, 0) + 1
                    break
                elif 2 < index < 5:
                    accuracy[5] = accuracy.get(5, 0) + 1
                    accuracy[10] = accuracy.get(10, 0) + 1
                    break
                elif 4 < index < 10:
                    accuracy[10] = accuracy.get(10, 0) + 1
                    break
        for key in accuracy.keys():
            if len(result_list) == 0:
                accuracy[key] = 0
            else:
                accuracy[key] = accuracy[key] / len(result_list)
        return accuracy

    @staticmethod
    def dcg_at_k(r, k):
        r = np.asfarray(r)[:k]
        if r.size:
            return np.sum(np.subtract(np.power(2, r), 1) / np.log2(np.arange(2, r.size + 2)))
        return 0.

    @staticmethod
    def ndcg_at_k(r, k):
        # r1 = [1, 1, 1, 1, 1]
        idcg = MetricsUtil.dcg_at_k(sorted(r, reverse=True), k)
        if not idcg:
            return 0.
        return MetricsUtil.dcg_at_k(r, k) / idcg

    @staticmethod
    def ndcg(result_list):
        average_ndcg = dict()
        for result in result_list:
            result = list(result)
            ndcg = dict()
            ndcg[1] = ndcg.get(1, MetricsUtil.ndcg_at_k(result, k=1))
            ndcg[3] = ndcg.get(3, MetricsUtil.ndcg_at_k(result, k=3))
            ndcg[5] = ndcg.get(5, MetricsUtil.ndcg_at_k(result, k=5))
            ndcg[10] = ndcg.get(10, MetricsUtil.ndcg_at_k(result, k=10))
            for key in ndcg.keys():
                average_ndcg[key] = average_ndcg.get(key, 0) + ndcg[key]
        if len(result_list) == 0:
            average_ndcg[1] = average_ndcg.get(1, 0)
            average_ndcg[3] = average_ndcg.get(3, 0)
            average_ndcg[5] = average_ndcg.get(5, 0)
            average_ndcg[10] = average_ndcg.get(10, 0)

        for key in average_ndcg.keys():
            if len(result_list) == 0:
                average_ndcg[key] = 0
            else:
                average_ndcg[key] = average_ndcg[key] / len(result_list)

        return average_ndcg

    @staticmethod
    def rouge(answers, references):
        rouge = Rouge()
        scores = rouge.get_scores(answers, references)
        # or
        avg_scores = rouge.get_scores(answers, references, avg=True)
        return scores, avg_scores

    @staticmethod
    def gleu(sources_path, references_path, answers_path):
        # run compute_gleu
        command = f"{ROOT_DIR}/gleu/scripts/compute_gleu"
        cmd = "python2 " + command + " -s {} -r {} -o {} -n 4 -d"
        cmd = cmd.format(sources_path, references_path, answers_path)
        # output = None
        try:
            output = subprocess.check_output(cmd.split()).decode("utf-8")
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)
        # output = subprocess.check_output(cmd.split()).decode("utf-8")
        lines = [l.strip() for l in output.split('\n') if l.strip()]

        scores = []
        count = 0
        for index, line in enumerate(lines):
            terms = line.split()
            if terms[0] == str(count):
                scores.append(float(terms[1]))
                count = count + 1
        # print(lines[-1])
        avg_score = float(lines[-1].split()[0])
        # print(lines)
        return scores, avg_score

    # @staticmethod
    # def gleu_from_txt(filepath):
    #     gleu_scores = FileUtil.load_txt(filepath)
    #     # print(gleu_scores)
    #     # print(type(gleu_scores))
    #     each_flag = "SID"
    #     mean_flag = "Mean"
    #     interrupt_flag = "===="
    #     gleus = []
    #     for gleu_score in gleu_scores:
    #         gleu_items = gleu_score.split()
    #         if len(gleu_items) >= 1 and gleu_items[0] != interrupt_flag:
    #             if gleu_items[0] == each_flag:
    #                 each_flag = True
    #                 continue
    #             if gleu_items[0] == mean_flag:
    #                 each_flag = False
    #                 mean_flag = True
    #                 continue
    #             if each_flag is True:
    #                 gleus.append(float(gleu_items[1]))
    #             if mean_flag is True:
    #                 gleus.append(float(gleu_items[0]))
    #     # summary_pair_gleu_list = []
    #     # for index, summary_pair in enumerate(summary_pairs):
    #     #     summary_pair_gleu_list.append((summary_pair, gleus[index]))
    #     return gleus[0:len(gleus) - 1], gleus[-1]

    # @staticmethod
    # def show_rouge_score(score):
    #     print(f'Rouge1')

    @staticmethod
    def show_metrics(answers, references,
                     rouges, avg_rouge=None,
                     summary_pairs=None,
                     gleus=None, avg_gleu=None, project=MOZILLA_PROJ):
        for index, reference in enumerate(references):
            if summary_pairs:
                summary_pair = summary_pairs[index]
                if project == MOZILLA_PROJ:
                    print(f'{MOZILLA_URL}{summary_pair.bug.id}')
                elif project == ECLIPSE_PROJ:
                    print(f'{ECLIPSE_URL}{summary_pair.bug.id}')
                print(f"\tsource: {summary_pair.rm_summary.text}")
            print(f"\treference: {reference}")
            print(f"\tanswer: {answers[index]}")
            print(f'\tRouge: {rouges[index]}')
            if gleus:
                print(f'\tGLEU: {gleus[index]}')

        print(f"AvgRough: {avg_rouge}")
        # print(f"what is avg_gleu: {avg_gleu}")
        if avg_gleu is not None:
            print(f"AvgGLEU: {avg_gleu}")
