
#used to separate 5 letter words from a long list of words

def main():
    input = "data/raw_words.txt"
    output_path = "data/wordle_words.txt"
    
    five_letter_words = []

    with open(input, "r") as f:
        for line in f.readlines():
            word = line.strip()
            if len(word) == 5:
                five_letter_words.append(word)

    with open(output_path, "w") as f:
        for word in five_letter_words:
            f.write(word + "\n")

    print("5 letter words found: ", len(five_letter_words))

    pass

if __name__ == "__main__":
    main()