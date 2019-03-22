import spacy

class spacy_model:

    def __init__(self, lang: str):
        try:
            self.model = spacy.load(lang)
        except Exception as e:
            print(e)
            print(f"Cannot load lang {lang}, loading default")
            self.model = spacy.load("xx")

    def get_spacy_doc(self, text):

        return self.model(text)

    @staticmethod
    def get_tokens_from_document(spacydoc: spacy.tokens.doc.Doc):

        return [tokens for tokens in spacydoc]

    def get_tokens_from_str(self, text: str):
        spacydoc = self.model(text)
        return [tokens for tokens in spacydoc]

    @staticmethod
    def get_sentence_from_document(spacydoc: spacy.tokens.doc.Doc):
        return [sent for sent in spacydoc.sents]

    def get_sentence_from_str(self, text: str):
        spacydoc = self.model(text)
        return [sent for sent in spacydoc.sents]

    @staticmethod
    def get_tokenized_sentence_from_document(spacydoc: spacy.tokens.doc.Doc):
        return [[(token) for token in sent] for sent in spacydoc.sents]

    def get_tokenized_sentence_from_str(self, text: str):
        spacydoc = self.model(text)
        return [[(token) for token in sent] for sent in spacydoc.sents]

    @staticmethod
    def get_entities_from_document(spacydoc):
        return [(ent, ent.label_) for ent in spacydoc.ents]

    @staticmethod
    def get_entities_from_str(self, text: str):
        spacydoc = self.model(text)
        return [(ent, ent.label_) for ent in spacydoc.ents]

    @staticmethod
    def get_lemma_from_document(spacydoc: spacy.tokens.doc.Doc) -> list:
        return [token.lemma_ for token in spacydoc]

    def get_lemma_from_str(self, text: str):
        spacydoc = self.model(text)
        return [token.lemma_ for token in spacydoc]

    def get_pos_from_str(self, text: str):
        spacydoc = self.model(text)
        return [token.pos_ for token in spacydoc]