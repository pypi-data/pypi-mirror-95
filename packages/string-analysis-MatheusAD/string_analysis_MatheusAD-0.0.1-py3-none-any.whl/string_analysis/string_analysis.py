import edlib


class StringAnalysis:
    def __init__(self, streaming_string):
        """ Creates an object that is capable of efficiently searching the
        stream of strings.

        streaming_string: iterable of strings
        """
        self.streaming_string = streaming_string
        self.word_set = set()

    def _process_stream(self):
        for word in self.streaming_string:
            self.word_set.add(word)

    def get_most_similar_word(self, target_string):
        """ Finds the most similar (according to Levenshtein distance) word in
        the stream

        target_string: target which will be searched in the stream
        """
        self._process_stream()
        matches = [(word, edlib.align(target_string, word)['editDistance'])
                   for word in self.word_set]
        return min(matches, key=lambda x: x[1])[0]

