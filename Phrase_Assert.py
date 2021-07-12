class TestPhraseAssert:
    def test_phrase(self):
        phrase = input("Set a phrase: ")
        phrase_length = len(phrase)
        assert phrase_length < 15, f"Phrase should be less than 15 characters, you phrase has {phrase_length} characters"
