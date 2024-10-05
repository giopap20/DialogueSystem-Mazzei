class Frame:
    def __init__(self, keywords) -> None:
        self.keywords = keywords
        self._keywords = [None] * len(keywords)  # Cambiato per adattarsi al numero di keywords

    def fill(self, keywords_found):
        for i, keyword in enumerate(keywords_found, start=0):
            if i < len(self._keywords):  # Assicurati di non andare oltre il numero di keywords
                self._keywords[i] = keyword

    def completeness_score(self):
        filled_keywords = [k for k in self._keywords if k is not None]
        return len(filled_keywords) / len(self._keywords)  # Modificato per usare il numero di keywords

class PosTaggingFrame(Frame):
    name = 'pos tagging'

    def __init__(self, keywords) -> None:
        super().__init__(keywords)  # Passa le keywords al costruttore della classe base

class TokenizationFrame(Frame):
    name = 'tokenization'

    def __init__(self, keywords) -> None:
        super().__init__(keywords)

class NamedEntityRecognitionFrame(Frame):
    name = 'named entity recognition'

    def __init__(self, keywords) -> None:
        super().__init__(keywords)

