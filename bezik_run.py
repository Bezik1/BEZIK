from structure.BEZIK import BEZIK

if __name__ == "__main__":
    model = BEZIK(test_mode=True)

    print("------------------BEZIK-----------------------")
    print("----------AI COMPUTER ASSISTANT---------------")
    while True:
        sentence = input("Co mam zrobić?: ")
        model(sentence)