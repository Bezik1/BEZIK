import torch
import spacy
from torchtext.data.metrics import bleu_score
import sys


def translate_sentence(model, sentence, question, answer, device, max_length=50):
    spacy_pl = spacy.load("pl_core_news_md")

    if type(sentence) == str:
        tokens = [token.text.lower() for token in spacy_pl(sentence)]
    else:
        tokens = [token.lower() for token in sentence]

    tokens.insert(0, question.init_token)
    tokens.append(question.eos_token)

    text_to_indices = [question.vocab.stoi[token] for token in tokens]

    sentence_tensor = torch.LongTensor(text_to_indices).unsqueeze(1).to(device)

    outputs = [answer.vocab.stoi["<sos>"]]

    for i in range(max_length):
        trg_tensor = torch.LongTensor(outputs).unsqueeze(1).to(device)

        with torch.no_grad():
            output = model(sentence_tensor, trg_tensor)

        best_guess = output.argmax(2)[-1, :].item()
        outputs.append(best_guess)

        if best_guess == answer.vocab.stoi["<eos>"]:
            break
    
    translated_sentence = [answer.vocab.itos[idx] for idx in outputs]


    return translated_sentence[1:]


def bleu(data, model, question, answer, device):
    targets = []
    outputs = []

    for example in data:
        src = vars(example)["src"]
        trg = vars(example)["trg"]

        prediction = translate_sentence(model, src, question, answer, device)
        prediction = prediction[:-1]

        targets.append([trg])
        outputs.append(prediction)

    return bleu_score(outputs, targets)


def save_checkpoint(state, filename="network.pth.tar"):
    print("=> Saving Network")
    torch.save(state, filename)


def load_checkpoint(checkpoint, model, optimizer):
    print("=> Loading Network")
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
