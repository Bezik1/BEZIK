import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from structure.Operator import Operator
from utils.index import translate_sentence, bleu, save_checkpoint, load_checkpoint
from utils.vocab import polish_dict, train_iterator, valid_data, test_data

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    load_model = False
    save_model = True
    train_model = True
    test_model = False

    epochs = 90
    learning_rate = 10e-5
    batch_size = 64

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

    writer = SummaryWriter("runs/loss_plot")

    model = Operator(
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
        device,
    ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, factor=0.1, patience=10, verbose=True
    )

    pad_idx = polish_dict.vocab.stoi["<pad>"]
    criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

    if load_model:
        load_checkpoint(torch.load("network.pth.tar"), model, optimizer)

    sentence = "Otwórz edytor tekstowy"

    step = 0
    if train_model:
        for epoch in range(epochs):
            print(f"[Epoch {epoch} / {epochs}]")

            if save_model and epoch % 10 == 0:
                checkpoint = {
                    "state_dict": model.state_dict(),
                    "optimizer": optimizer.state_dict(),
                }
                save_checkpoint(checkpoint)

            model.eval()
            translated_sentence = translate_sentence(
                model, sentence, polish_dict, polish_dict, device, max_length=50
            )

            translated_sentence = " ".join(translated_sentence).replace("<eos>", "").replace("<unk>", "")
            print(f"Sentence: {sentence} \nTranslated Sentence: {translated_sentence}")
            model.train()
            losses = []

            for batch_idx, batch in enumerate(train_iterator):
                inp_data = batch.src.to(device)
                target = batch.trg.to(device)

                output = model(inp_data, target[:-1, :])

                output = output.reshape(-1, output.shape[2])
                target = target[1:].reshape(-1)

                optimizer.zero_grad()

                loss = criterion(output, target)
                losses.append(loss.item())

                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)

                optimizer.step()

                writer.add_scalar("Training loss", loss, global_step=step)
                step += 1

            mean_loss = sum(losses) / len(losses)
            scheduler.step(mean_loss)

    if test_model:
        for data in test_data:
            question, answer = " ".join(data.src), " ".join(data.trg)
            translated_sentence = translate_sentence(
                model, answer, polish_dict, polish_dict, device, max_length=50
            )

            translated_sentence = " ".join(translated_sentence).replace("<eos>", "").replace("<unk>", "")
            print(f"Question: {question} | Answer: {translated_sentence} | Right Answer {answer}")

        test_score = bleu(test_data[1:100], model, polish_dict, polish_dict, device)
        valid_score = bleu(valid_data[1:100], model, polish_dict, polish_dict, device)
        print(f"Bleu score: | Test Data: {test_score} | Validation Data: {valid_score} |")

    # while True:
    #     sentence = input("Write sentence for translation: ")
    #     translated_sentence = translate_sentence(
    #         model, sentence, polish_dict, polish_dict, device, max_length=50
    #     )

    #     answer = " ".join(translated_sentence).replace("<eos>", "").replace("<unk>", "")
    #     print(f"Answer: {answer}")