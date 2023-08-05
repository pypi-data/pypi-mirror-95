import numpy as np

def splitIntoWords(str, badChars):
    return np.array(str.translate(str.maketrans( '', '', badChars)).split(" "))

BAD_CHARS = "\""
BAD_WORDS = "of and to for Book Page in by on from with See"

class Entries:
    def __init__(self, entries):
        self.entries = entries

    def sorted(self, key):
        """Sort the current entries with the given key function."""
        try:
            self.entries = sorted(self.entries, key=key)
            return self
        except:
            print("No results found. Try running a query first.")

    def entries(self):
        """Return a numpy array of the result entry dictionaries."""
        try:
            return np.array(self.entries);
        except:
            print("No results found. Try running a query first.")

    def headers(self):
        """Return a numpy array of the result header strings."""
        try:
            return np.array([i["header"] for i in self.entries])
        except:
            print("No results found. Try running a query first.")

    def content(self):
        """Return a numpy array of the result content strings."""
        try:
            return np.array([i["content"] for i in self.entries])
        except:
            print("No results found. Try running a query first.")

    def dates(self):
        """Return a numpy array of the result date dictionaries."""
        try:
            return np.array([d for i in self.entries for d in i["dates"]])
        except:
            print("No results found. Try running a query first.")

    def indexes(self):
        """Return a numpy array of the result index dictionaries."""
        try:
            return np.array([d for i in self.entries for d in i["indexes"]])
        except:
            print("No results found. Try running a query first.")

    def headerWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.headers()), badChars)
        except:
            print("No results found. Try running a query first.")

    def headerCounts(self):
        """Count the appearances of each unique header."""
        unique, counts = np.unique(self.headers(), return_counts=True)
        return dict(zip(unique, counts))

    def contentWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.content()), badChars)
        except:
            print("No results found. Try running a query first.")

    def words(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in each entry. Equivalent to headerWords + contentWords."""
        try:
            return np.concatenate((self.headerWords(badChars),self.contentWords(badChars)))
        except:
            print("No results found. Try running a query first.")

    def associate(self, words, badWords=BAD_WORDS):
        """Count the appearances of each unique word in indexes that contain the given words. """
        indexes = self.indexes()
        if indexes.any():
            containedStrs = [s["content"] for s in indexes for word in words if s["content"] is not None if word in s["content"]]
            words = [word for s in containedStrs for word in s.split(" ") ]
            return {word:words.count(word) for word in words if word not in badWords}
