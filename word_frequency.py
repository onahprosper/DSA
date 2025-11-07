from typing import List, Dict


def findMostFrequentWord(inputList1: List[str], inputList2: List[str]) -> str:
    # We first need to count the frequency of each word in inputList1 and store it in a dictionary
    # This way we can easily find the most frequent word later
    word_counts = {}
    for word in inputList1:
        if word in word_counts:
            word_counts[word] = word_counts[word] + 1
        else:
            word_counts[word] = 1
    
    # Find most frequent word not in inputList2
    most_frequent_word = None
    max_count = 0
    
    for word in word_counts:
        count = word_counts[word]
        
        # We need to check if a word from the word_counts is in the inputList2, then we exclude such words
        word_is_excluded = False
        for excluded_word in inputList2:
            # What we are doing here is to compare the current word with each excluded word
            if word == excluded_word:
                word_is_excluded = True
                break
        
        # If not excluded and has higher count, update most frequent word
        if not word_is_excluded and count > max_count:
            max_count = count
            most_frequent_word = word
    
    return most_frequent_word if most_frequent_word else ""


def findMostFrequentFollower(inputList: List[str], targetWord: str) -> str:
    # We need to create two dictionaries where we will store every words and their counts in a dictionary
    follower_counts: Dict[str, int] = {}
    # We also need to keep track of the last index where each follower appeared
    follower_last_index: Dict[str, int] = {}
    
    # We can then proceed to find the followers of the targetWord
    for i in range(len(inputList) - 1):
        if inputList[i].lower() == targetWord.lower():
            follower = inputList[i + 1]
            follower_counts[follower] = follower_counts.get(follower, 0) + 1
            follower_last_index[follower] = i + 1
    
    if not follower_counts:
        return "" # Word doesn't exist
    
    # Find the most frequent follower
    # If tied, choose the one with the largest last_index (occurs last)
    most_frequent = None
    max_count = 0
    last_index = -1
    
    # What we are doing here is to iterate through the follower_counts dictionary and find the most frequent follower
    # If there is a tie, we choose the one that occurs last in the inputList
    # We do this by comparing the counts and the last indices
    for follower, count in follower_counts.items():
        if count > max_count or (count == max_count and follower_last_index[follower] > last_index):
            max_count = count
            most_frequent = follower
            last_index = follower_last_index[follower]

    return most_frequent if most_frequent else ""


def main():
    # Optionally run interactive mode
    print("\nWould you like to find the most frequent follower or the most frequent word?")
    print("`y` for the most frequent follower `n` for the most frequent word (y/n): ", end="")
    choice = input().strip().lower()
    
    if choice == 'y':
        print("\n" + "=" * 50)
        print("INTERACTIVE MODE: findMostFrequentFollower")
        print("=" * 50)
        
        # Example sentence - split into individual words
        words_to_check_against = ['This', 'is', 'the', 'way', 'The', 'way', 'is', 'shut', 'The', 'door', 'is', 'the', 'end']

        print(f"\nUsing words: {words_to_check_against}")

        while True:
            target = input("\nEnter a word to find its most frequent follower (or 'quit' to exit): ").strip()
            
            if target.lower() == 'quit':
                print("Exiting interactive mode.")
                break
            
            if not target:
                print("Please enter a valid word.")
                continue
            
            result = findMostFrequentFollower(words_to_check_against, target)
            
            if result:
                print(f"  → Most frequent follower of '{target}': '{result}'\n")
            else:
                print(f"  → No follower found for '{target}'\n")
    
    elif choice == 'n':
        words_to_check_against = ["apple", "banana", "apple", "orange", "banana", "apple"]
        print("\n" + "=" * 50)
        print("INTERACTIVE MODE: findMostFrequentWord")
        while True:
            target = input("Enter a word to find its most frequent occurrence (or 'quit' to exit): ").strip()

            if target.lower() == 'quit':
                print("Exiting interactive mode.")
                break

            if not target:
                print("Please enter a valid word.")
                continue

            result = findMostFrequentWord(words_to_check_against, target)

            if result:
                print(f"  → Most frequent occurrence of '{target}': '{result}'\n")
            else:
                print(f"  → No occurrence found for '{target}'\n")

if __name__ == "__main__":
    main()
