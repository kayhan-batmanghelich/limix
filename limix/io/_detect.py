from os.path import exists, basename

recognized_file_types = [
    "image",
    "hdf5",
    "csv",
    "npy",
    "grm.raw",
    "bed",
    "bgen",
    "bimbam-pheno",
]


def detect_file_type(filepath):
    # TODO document

    filepath, spec = _get_file_type_spec(filepath)
    if spec is not None:
        if spec in recognized_file_types:
            return filepath, spec

    imexts = [".png", ".bmp", ".jpg", "jpeg"]
    if filepath.endswith(".hdf5") or filepath.endswith(".h5"):
        return filepath, "hdf5"
    if filepath.endswith(".csv"):
        return filepath, "csv"
    if filepath.endswith(".npy"):
        return filepath, "npy"
    if filepath.endswith(".grm.raw"):
        return filepath, "grm.raw"
    if _is_bed(filepath):
        return filepath, "bed"
    if any([filepath.endswith(ext) for ext in imexts]):
        return filepath, "image"
    if filepath.endswith(".txt"):
        return filepath, "csv"
    if filepath.endswith(".bgen"):
        return filepath, "bgen"
    if filepath.endswith(".gemma"):
        return filepath, "bimbam-pheno"
    return filepath, "unknown"


def get_fetch_specification(filepath_spec):
    import re

    filepath, filetype = detect_file_type(filepath_spec)
    rest = filepath_spec[len(filepath) + len(filetype) + 1 :]
    if len(rest) == 0:
        rest = ":"
        matrix_spec = None
    else:
        if ":" != rest[0]:
            raise ValueError("Invalid fetch specification syntax.")

        rest = rest[1:].strip()
        match = re.match(r"^trait\[(.+)\]$", rest)
        if match is None:
            raise ValueError("Invalid fetch specification syntax.")
        else:
            matrix_spec = match.group(0)

    return {"filepath": filepath, "filetype": filetype, "matrix_spec": matrix_spec}


def _is_bed(filepath):
    files = [filepath + ext for ext in [".bed", ".bim", ".fam"]]
    ok = [exists(f) for f in files]

    if sum(ok) > 0 and sum(ok) < 3:
        mfiles = ", ".join([files[i] for i in range(3) if not ok[i]])
        print("The following file(s) are missing:", mfiles)
        return False

    return all(ok)


def _get_file_type_spec(filepath):
    filename = basename(filepath)
    if ":" not in filename:
        return filepath, None

    split = filename.split(":")
    return split[0], split[1]
