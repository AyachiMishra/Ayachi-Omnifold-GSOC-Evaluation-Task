import numpy as np
import h5py
import matplotlib.pyplot as plt


class OmniFoldResult:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self._load_data()

    def _load_data(self):
        with h5py.File(self.file_path, 'r') as f:
            block_num = 0
            while f'/df/block{block_num}_items' in f:
                cols = f[f'/df/block{block_num}_items'][()]
                if cols.dtype.kind in {'S','O'}:
                    cols = cols.astype(str)

                values = f[f'/df/block{block_num}_values'][:]

                for i, col in enumerate(cols):
                    self.data[col] = values[:, i]

                block_num += 1

    def validate(self):
        # Basic validation (minimal guarantee)
        if 'weights_nominal' not in self.data:
            raise ValueError("Missing weights_nominal")

        w = self.data['weights_nominal']

        if not np.isfinite(w).all():
            raise ValueError("Weights contain NaNs or inf")

        if np.sum(w) <= 0:
            raise ValueError("Invalid normalization (sum <= 0)")

        print("Validation passed ✅")

    def get_observable(self, name):
        if name not in self.data:
            raise ValueError(f"{name} not found in dataset")
        return self.data[name]

    def histogram(self, observable, bins=20):
        x = self.get_observable(observable)
        w = self.data['weights_nominal']

        mask = np.isfinite(x) & np.isfinite(w)
        x = x[mask]
        w = w[mask]

        counts, edges = np.histogram(x, bins=bins, weights=w)

        return counts, edges

    def plot(self, observable, bins=20):
        counts, edges = self.histogram(observable, bins)

        plt.figure(figsize=(8,6))
        plt.hist(edges[:-1], bins=edges, weights=counts,
                 alpha=0.6, edgecolor='black')
        plt.title(f"{observable} (weighted)")
        plt.xlabel(observable)
        plt.ylabel("Weighted count")
        plt.grid(alpha=0.3)
        plt.show()    