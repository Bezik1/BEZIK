import spacy
from torchtext.data import Field, TabularDataset, BucketIterator, Iterator
import torch

spacy_pl = spacy.load("pl_core_news_md")

def tokenize_pl(text):
    return [tok.text for tok in spacy_pl.tokenizer(text)]

polish_dict = Field(tokenize=tokenize_pl, lower=True, init_token="<sos>", eos_token="<eos>", pad_token="<pad>")

fields = {'question': ('src', polish_dict), 'answer': ('trg', polish_dict)}

train_data, valid_data, test_data = TabularDataset.splits(
    path='./data/operator', train='train.csv', validation='valid.csv', test='test.csv',
    format='csv', fields=fields
)

polish_dict.build_vocab(train_data, max_size=10000)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_iterator, valid_iterator, test_iterator = BucketIterator.splits(
    (train_data, valid_data, test_data), batch_size=32, device=device
)

# for example in train_data.examples[:5]:
#     print("Question:", example.src)
#     print("Answer:", example.trg)
#     print()

# for data in polish_dict.vocab.stoi:
#     print(data)