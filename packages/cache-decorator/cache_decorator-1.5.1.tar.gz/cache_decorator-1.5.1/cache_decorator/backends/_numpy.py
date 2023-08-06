try:
    import numpy as np
except ModuleNotFoundError:
    numpy_dict = {}
else:
    def load_npz(path):
        with open(path, "rb") as f:
            objs = np.load(f)
            return [objs[k] for k in objs.files]

    def save_npz(objs, path):
        with open(path, "wb") as f:
            np.savez(f, *objs)

    def save_compressed_npz(objs, path):
        with open(path, "wb") as f:
            np.savez_compressed(f, *objs)

    def load_npy(path):
        with open(path, "rb") as f:
            return np.load(f)

    def dump_npy(obj, path):
        with open(path, "wb") as f:
            np.save(f, obj)

    numpy_dict = {
        "npy":{
            "load":load_npy,
            "dump":dump_npy
        },
        "npz":{
            "load":load_npz,
            "dump":save_compressed_npz
        }
    }