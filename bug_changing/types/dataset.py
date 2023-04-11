import torch
import numpy as np
from transformers import BertTokenizer


class Dataset(torch.utils.data.Dataset):

    def __init__(self, labels=None, texts=None):
        self.labels = labels
        self.texts = texts

    @classmethod
    def convert_bugs_into_dataset(cls, bugs, product_components):
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        pc_index_dict = product_components.get_product_component_pair_index_dict()
        labels = []
        texts = []
        for bug in bugs:
            labels.append(pc_index_dict[bug.product_component_pair])
            texts.append(tokenizer(bug.summary, padding='max_length', max_length=512,
                                   truncation=True, return_tensors="pt"))
        return cls(labels, texts)

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        # Fetch a batch of inputs
        return self.texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y
