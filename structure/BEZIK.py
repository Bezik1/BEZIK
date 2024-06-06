import torch
import torch.optim as optim

from structure.Operator import Operator
from structure.Executor import Executor

from utils.index import translate_sentence, load_checkpoint
from utils.vocab import polish_dict

class BEZIK:
    def __init__(self, test_mode) -> None:
        self.test_mode = test_mode

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        learning_rate = 10e-5

        src_vocab_size = len(polish_dict.vocab)
        trg_vocab_size = len(polish_dict.vocab)
        embedding_size = 516
        num_heads = 12
        num_encoder_layers = 6
        num_decoder_layers = 6
        dropout = 0.10
        max_len = 128
        forward_expansion = 4
        src_pad_idx = polish_dict.vocab.stoi["<pad>"]

        self.model = Operator(
            embedding_size,
            src_vocab_size,
            trg_vocab_size,
            src_pad_idx,
            num_heads,
            num_encoder_layers,
            num_decoder_layers,
            forward_expansion,
            dropout,
            max_len,
            self.device,
        ).to(self.device)

        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        load_checkpoint(torch.load("network.pth.tar"), self.model, optimizer)
        #load_checkpoint(torch.load("C:/Users/mateu/Desktop/Operator/network.pth.tar"), self.model, optimizer)
        
        self.executor = Executor()
    
    def __call__(self, req):
        translated_sentence = translate_sentence(
            self.model, req, polish_dict, polish_dict, self.device, max_length=50
        )
        
        if self.test_mode:
            print(translated_sentence)
        
        self.executor.execute(translated_sentence[:-1])

        return " ".join(translated_sentence[:-1])