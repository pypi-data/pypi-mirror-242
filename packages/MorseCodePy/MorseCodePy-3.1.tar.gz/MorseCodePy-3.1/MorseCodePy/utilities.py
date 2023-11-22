# Define error messages
error_message1: str = 'Invalid symbols: Dots, dashes, and separators must be single characters!'
error_message2: str = 'Invalid characters in the Morse code string. Use only specified dots, dashes, spaces, and separators!'
error_message3: str = 'KeyboardInterrupt: Morse code playback interrupted by user.'
warning_message1: str = 'The specified delay is longer than recommended (1 second). Playback may be slower than expected.'


# Function to separate words into Morse code letters
def separate_words(words: str, dot: str, dash: str, separator: str, sound_mode: bool = False) -> list:
    letters: list = list()
    current_element: str = str()

    for char in words:
        if char in (dot, dash):
            current_element += char
        elif char == separator:
            if current_element:
                letters.append(current_element)
                current_element = str()
            letters.append(separator)
        elif char == ' ':
            if current_element:
                letters.append(current_element)
                current_element = str()
            if sound_mode:
                letters.append(' ')
        else:
            current_element += char

    if current_element:
        letters.append(current_element)

    return letters


# Function to separate Morse code letters
def separate_letters(letters: list) -> list:
    return [char for letter in letters for char in letter]


# Function to reverse the keys and values of a dictionary
def reverse_dictionary(dictionary: dict) -> dict:
    return {value: key for key, value in dictionary.items()}
