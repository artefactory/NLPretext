import spacy


class spacy_model:
    def __init__(self, lang: str):
        try:
            self.model = spacy.load("lang")
        except Exception as e:
            print(e)
            print(f"Cannot load lang {lang}, loading default")
            self.model = spacy.load("xx")

    @staticmethod
    def get_tokens_from_document(spacydoc: spacy.tokens.doc.Doc):

        return [tokens for tokens in spacydoc]

    @staticmethod
    def get_tokenized_sentence_from_document(spacydoc: spacy.tokens.doc.Doc):
        return [[(token) for token in sent] for sent in spacydoc.sents]

    def get_tokens_from_str(self, text: str):
        doc = self.model(text)
        return [tokens for tokens in doc]

    def get_tokenized_sentence_from_str(self, text: str):
        doc = self.model(text)
        return [[(token) for token in sent] for sent in doc.sents]

    @staticmethod
    def get_entities_from_document(spacydoc):
        return [(ent, ent.label_) for ent in spacydoc.ents]

    @staticmethod
    def get_entities_from_str(self, text: str):
        doc = self.model(text)
        return [(ent, ent.label_) for ent in doc.ents]
