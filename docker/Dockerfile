from continuumio/miniconda3

RUN apt-get update && apt-get install -y build-essential unzip 
RUN wget https://github.com/facebookresearch/fastText/archive/v0.2.0.zip && unzip v0.2.0.zip && cd fastText-0.2.0 && make
RUN git clone https://github.com/facebookresearch/fastText.git && cd fastText && pip install . 
RUN pip install --upgrade pip && pip install pandas schedule nltk pendulum bounter spacy==2.1 jupyterlab confluent-kafka xxhash scikit-learn
RUN python -m spacy download fr &&  python -m spacy download en && python -m spacy download de && python -m spacy download it && python -m spacy download xx
RUN python -m nltk.downloader stopwords 
#RUN git clone https://github.com/artefactory/nautilus_nlp/ && cd nautilus_nlp && pip install -e . 
