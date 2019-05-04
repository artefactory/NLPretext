FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini


RUN apt-get update && apt-get install -y build-essential unzip 
RUN apt-get install -y g++-5 && apt-get install -y gcc-5
RUN apt-get install -y python3-pip && alias pip=pip3 && pip3 install --upgrade pip
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 10 && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 20 && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10 && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 20 && update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 30 && update-alternatives --set cc /usr/bin/gcc && update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 30 && update-alternatives --set c++ /usr/bin/g++

RUN wget https://github.com/facebookresearch/fastText/archive/v0.2.0.zip && unzip v0.2.0.zip && cd fastText-0.2.0 && make
RUN git clone https://github.com/facebookresearch/fastText.git 
RUN cd fastText && pip3 install .
RUN  pip3 install pandas schedule nltk pendulum bounter spacy==2.1 jupyterlab confluent-kafka xxhash scikit-learn
RUN python3 -m spacy download fr &&  python3 -m spacy download en && python3 -m spacy download de && python3 -m spacy download it && python3 -m spacy download xx && python3 -m spacy validate
RUN python3 -m nltk.downloader stopwords 

RUN wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip 
    unzip mallet-2.0.8.zip
    rm mallet-2.0.8.zip

RUN sudo add-apt-repository ppa:openjdk-r/ppa  # only Ubuntu 17.4 and earlier
    sudo apt update
    apt search openjdk
    sudo apt install openjdk-8-jdk

RUN echo "alias python='python3'" >> .bash_aliases
RUN echo "alias pip='pip3' ">> ~/.bash_aliases
RUN source ~/.bashrc
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
