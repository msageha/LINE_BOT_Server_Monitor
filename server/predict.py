from chainer import serializers

from model import AttSeq2Seq
from model import DataConverter

class Predict:
    def __init__(self, model_file, gpu):
        self.data_converter = DataConverter(batch_col_size=20) # データコンバーター
        model = AttSeq2Seq(input_size=200, hidden_size=200, batch_col_size=20)
        serializers.load_npz(f'./{model_file}', model)
        if gpu >= 0:
            model.to_gpu(0)
        self.model = model

    def __call__(self, query):
        self.model.reset()
        enc_query = self.data_converter.sentence2vectors(query, train=False)
        dec_response = self.model(enc_words=enc_query, train=False)
        response = self.data_converter.vectors2sentences(dec_response)
        print(query, "=>", response)
        return response