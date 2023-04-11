import random


class ListUtil:
    @staticmethod
    def flatten_list_of_groups(nested_list):
        flattened = [val for sublist in nested_list for val in sublist]
        return flattened

    @staticmethod
    def list_of_groups(init_list, children_list_len):
        list_of_groups = zip(*(iter(init_list),) * children_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(init_list) % children_list_len
        end_list.append(init_list[-count:]) if count != 0 else end_list
        return end_list

    @staticmethod
    def zip_two_lists(xs, ys):
        pair_list = []
        for x, y in zip(xs, ys):
            pair_list.append((x, y))
        return pair_list

    @staticmethod
    def sort_list_by_index_number_list(init_list, index_number_list):
        pair_list = ListUtil.zip_two_lists(init_list, index_number_list)
        pair_list.sort(key=lambda x: x[1])
        sorted_list = list(zip(*pair_list))[0]
        return sorted_list

    @staticmethod
    def random_list(init_list):
        random_number_list = random.sample(range(0, len(init_list)), len(init_list))
        random_list = ListUtil.sort_list_by_index_number_list(init_list, random_number_list)
        return random_list

    @staticmethod
    def sort_pair_list_by_specific_order(pair_list, specific_order, pair_index=0):
        order = {key: i for i, key in enumerate(specific_order)}
        pair_list = sorted(pair_list, key=lambda d: order[d[pair_index]])
        return pair_list
