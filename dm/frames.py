class Frame:
    def __init__(self) -> None:
        raise NotImplementedError("Each subclass must implement its own constructor.")

    def fill(self, keywords_found):
        for i, keyword in enumerate(keywords_found, start=1):
            setattr(self, f'_keyword{i}', keyword)

    def completeness_score(self):
        filled_keywords = [getattr(self, f'_keyword{i}') for i in range(1, 6)]
        return len([k for k in filled_keywords if k is not None]) / 5


class PosTaggingFrame(Frame):
    name = 'pos tagging'

    def __init__(self) -> None:
        self._keyword1 = None
        self._keyword2 = None
        self._keyword3 = None
        self._keyword4 = None
        self._keyword5 = None


class TokenizationFrame(Frame):
    name = 'tokenization'

    def __init__(self) -> None:
        self._keyword1 = None
        self._keyword2 = None
        self._keyword3 = None
        self._keyword4 = None
        self._keyword5 = None


class NamedEntityRecognitionFrame(Frame):
    name = 'named entity recognition'

    def __init__(self) -> None:
        self._keyword1 = None
        self._keyword2 = None
        self._keyword3 = None
        self._keyword4 = None
        self._keyword5 = None
