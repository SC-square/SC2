from stellargraph.mapper import PaddedGraphGenerator
from stellargraph.layer import DeepGraphCNN
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv1D, MaxPool1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy


class GCNModel:
    def __init__(self, graphs=None, model=None):
        self.k = 100
        self.layer_sizes = [256, 128, 1]
        self.activations = ["relu", "relu", "relu"]
        self.filters = 96
        self.dense_units = [1024, 512]
        self.dropout_rate = 0.5
        self.learning_rate = 0.0005

        if model is not None:
            self.model = model
        elif graphs is not None:
            self.generator = PaddedGraphGenerator(graphs=graphs)
            self.model = self.build_model()

    def build_model(self):
        dgcnn_model = DeepGraphCNN(
            layer_sizes=self.layer_sizes,
            activations=self.activations,
            k=self.k,
            bias=False,
            generator=self.generator,
        )
        x_inp, x_out = dgcnn_model.in_out_tensors()

        x_out = Conv1D(filters=self.filters, kernel_size=sum(
            self.layer_sizes), strides=sum(self.layer_sizes))(x_out)
        x_out = MaxPool1D(pool_size=2)(x_out)
        x_out = Conv1D(filters=self.filters, kernel_size=8,
                       strides=1)(x_out)
        x_out = Flatten()(x_out)

        x_out = Dense(units=self.dense_units[0], activation="relu")(x_out)
        x_out = Dropout(rate=self.dropout_rate)(x_out)
        x_out = Dense(units=self.dense_units[1], activation="relu")(x_out)
        x_out = Dropout(rate=self.dropout_rate)(x_out)
        predictions = Dense(units=1, activation="sigmoid")(x_out)

        model = Model(inputs=x_inp, outputs=predictions)
        return model

    def compile(self):
        self.model.compile(optimizer=Adam(learning_rate=self.learning_rate),
                           loss=binary_crossentropy, metrics=['acc'])

    def fit(self, generator, epochs, verbose, **kwargs):
        return self.model.fit(generator, epochs=epochs, verbose=verbose, **kwargs)

    def evaluate(self, generator):
        return self.model.evaluate(generator)

    def predict(self, generator):
        return self.model.predict(generator)

    def save(self, path):
        self.model.save(path)

    @property
    def metrics_names(self):
        return self.model.metrics_names
