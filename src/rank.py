# Take list of words and a main word to compare to
# Loop through each letter of each word in the list
# and rank each word by its similarity to the main word
# Retrun the list sorted by rank


# This algorithm is definitely not efficient. But since
# it is only ran when there is a refernce error, it is fine


def sort(arr: list[dict[str, int]]):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        sort(L)
        sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i]["score"] >= R[j]["score"]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr


def rank(list_of_words: list[str], main_word: str, len_thresh: float):
    ranked_words: list[dict[str, str | int]] = []

    for word in list_of_words:
        word_score = 0
        if len(word) <= len_thresh * len(main_word):
            for i, letter in enumerate(word):
                if i < len(main_word):
                    if letter == main_word[i]:
                        word_score += 1
        ranked_words.append({"word": word, "score": word_score})

    ranked_words = sort(ranked_words)  # type: ignore

    return ranked_words
