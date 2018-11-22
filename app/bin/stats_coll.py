from yaml import load


def fetch_seq(data, list_sequences=False):
    """
        fetch sequences from yaml design
        spacers excluded
    """
    sequences = []
    for plate_name, plate in data.items():
        # exclude Connectors
        if "Connectors" not in plate_name:
            if list_sequences:
                print(plate_name)
            # fetch sequences
            for _, wells in plate["rows"].items():
                for w in wells:
                    sq = w["seq"]
                    s = "".join((sq[0], sq[2], sq[3]))
                    if list_sequences:
                        print(s, len(s))
                    sequences.append(s)
    return sequences


path = "../designs/Structures/4R0A_cr_2T.yaml"

# load designs
with open(path, "r") as file:
    data = load(file.read())

sequences = fetch_seq(data, list_sequences=False)


def fetch_interesting(s, repeat_length=2):
    """
        fetch all repeats from string s
        which are longer than repeat_length
    """
    lookup = {"C": "G", "G": "C",
              "A": "A", "T": "T"}  # count adjacent G and C as repeat
    repeats = []
    p = ""
    repeat = []
    for c in s:
        if not repeat and not p:
            repeat.append(c)

        if c == p or lookup[c] == p:
            repeat.append(c)
        else:
            if len(repeat) > repeat_length:
                repeats.append("".join(repeat))
            repeat = []
        p = c
    return repeats


# print(fetch_repeats(s))

for s in sequences:
    repeats = fetch_interesting(s)
    repeats = filter(lambda r: not r == "AA", repeats)
    repeats = list(filter(lambda r: not r == "TT", repeats))
    if repeats:
        print(s, repeats)
