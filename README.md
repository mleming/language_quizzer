Terminal-based language learning tool. Makes you type words out. Feeds you new words as you learn others. Current examples are in Russian, but it should accept others given a fresh CSV file.

Get a CSV, with the first column being non-English-language words and the second being English language definitions. This will present words to you, you type in the definition, and it'll cycle through. You are shown words in blocks; if you get a word correct enough times, it is taken off the queue and you are given a new word. This saves your progress in a json file. If you want to start anew, just delete the json file.

With English definitions, this tries to be smart about accepting flexible input, but it's not exact. Typing out the exact definition word-for-word should work.

This is meant solely for the memorization of a lot of vocabulary and would not help at all with the grammar.

To use, run: python language_quizzer.py <csv_definitions_file.csv>

