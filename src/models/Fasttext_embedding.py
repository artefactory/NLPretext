import fastText

class FasttextEmbedding(object):

    def __init__(self,path=None):
        try:
            self.model=fastText.load_model(path)
        except Exception as e:
            print(e)
            self.model=None
    

    def get_word_vector(self,word :str):
        """Return the wordvector of a word according to pretrained model"""
        return self.model.get_word_vector(word)

    def get_document_vector(self, document:str):
        """Return the wordvector of a full document according to pretrained model
            To build the vector,  each word-wordvector is divided by its norm, then the array of vector is averaged
            The document must be cleaned beforehand (no EOL)
        """
        return self.model.get_sentence_vector(document)