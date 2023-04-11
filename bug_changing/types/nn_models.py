from bug_changing.utils.path_util import PathUtil
import torch
from torch import nn
from transformers import BertModel, get_linear_schedule_with_warmup
from torch.optim import Adam
from tqdm import tqdm


class BertClassifier(nn.Module):

    def __init__(self, class_num, dropout=0.5):

        super(BertClassifier, self).__init__()

        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, class_num)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):

        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer

    def train(self, train_data, val_data, batch_size, learning_rate, epochs):

        # train, val = Dataset(train_data), Dataset(val_data)

        train_dataloader = torch.utils.data.DataLoader(train_data, batch_size, shuffle=True)
        val_dataloader = torch.utils.data.DataLoader(val_data, batch_size)

        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")

        criterion = nn.CrossEntropyLoss()
        optimizer = Adam(self.parameters(), lr=learning_rate)
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_dataloader) * epochs)

        if use_cuda:
            self = self.cuda()
            criterion = criterion.cuda()

        for epoch_num in range(epochs):

            total_acc_train = 0
            total_loss_train = 0

            for train_input, train_label in tqdm(train_dataloader):
                train_label = train_label.to(device)
                mask = train_input['attention_mask'].to(device)
                input_id = train_input['input_ids'].squeeze(1).to(device)

                output = self(input_id, mask)

                batch_loss = criterion(output, train_label)
                total_loss_train += batch_loss.item()

                acc = (output.argmax(dim=1) == train_label).sum().item()
                total_acc_train += acc

                self.zero_grad()
                batch_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

            total_acc_val = 0
            total_loss_val = 0

            # with torch.no_grad():

            #     for val_input, val_label in val_dataloader:

            #         val_label = val_label.to(device)
            #         mask = val_input['attention_mask'].to(device)
            #         input_id = val_input['input_ids'].squeeze(1).to(device)

            #         output = self(input_id, mask)

            #         batch_loss = criterion(output, val_label)
            #         total_loss_val += batch_loss.item()

            #         acc = (output.argmax(dim=1) == val_label).sum().item()
            #         total_acc_val += acc

            print(
                f'Epochs: {epoch_num + 1} | Train Loss: {total_loss_train / len(train_data): .3f} | Train Accuracy: {total_acc_train / len(train_data): .3f} | Val Loss: {total_loss_val / len(val_data): .3f} | Val Accuracy: {total_acc_val / len(val_data): .3f}')

        torch.save(self.state_dict(), PathUtil.load_bert_model_filepath())

    def evaluate(self, test_data):

        # test = Dataset(test_data)

        test_dataloader = torch.utils.data.DataLoader(test_data, batch_size=2)

        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")

        if use_cuda:
            self = self.cuda()

        total_acc_test = 0
        with torch.no_grad():

            for test_input, test_label in test_dataloader:
                test_label = test_label.to(device)
                mask = test_input['attention_mask'].to(device)
                input_id = test_input['input_ids'].squeeze(1).to(device)

                output = self(input_id, mask)

                acc = (output.argmax(dim=1) == test_label).sum().item()
                total_acc_test += acc

        print(f'Test Accuracy: {total_acc_test / len(test_data): .3f}')
