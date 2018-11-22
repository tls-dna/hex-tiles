from yaml import load

def find_oligo(row, item):
    for oligo in row:
        if oligo["seq"] == item["seq"]:
            return oligo
    return None

#file list of the current order
# file_list = (
#     "4R4C_2T.yaml",
#     "4R4C_2T_tube.yaml",
#     "HexagonCrystal.yaml",
#      "TRing.yaml",
#      "4R4C_2T_tube_crystal.yaml"
#     )
#plate_name  = "Ord_77030_Staples_0"

#plate_name = "Ord_55713_Staples_0"
#plate_name = "Ord_55713_Protectors_0"

file_list = (
        "../designs/old_design/3R2C_4T.yaml",
        # "../data/4R0A_cr_2T.yaml",
        # "../data/4R0B_cr_2T.yaml",
        # "../data/4R0C_cr_2T.yaml",
        # "../data/4R0D_cr_2T.yaml",
        # "../data/Tring(AD,BE,CF)_2T.yaml",
        # "../data/Tring(AE)_2T.yaml",
        # "../data/3R0A_cr_2T.yaml",
        # "../data/3R0B_cr_2T.yaml",
        # "../data/3R0C_cr_2T.yaml",
)
plate_name = "Plate_64076_4T"
out_plate = {}
for fp in file_list:
    print("searching staples for plate", plate_name  ,"in ", fp)
    with open("../designs/"+fp) as file:
        plates = load(file)

    if plate_name in plates:
        for row_name, row in plates[plate_name]["rows"].items():
            if not row_name in out_plate:
                out_plate[row_name] = row
            else:
                for item in row:
                    if not find_oligo(out_plate[row_name],item):
                        out_plate[row_name].append(item)


out = []
for row_name in sorted(out_plate.keys()):
    out_row = []
    a = out_row.append
    a(row_name+":")
    for item in sorted(out_plate[row_name], key=lambda i: int(i["plate_id"][1:])):
        seq = "".join(item["seq"])
        name = item["name"] + ("_p" if item["protector"] else "")
        a("\t".join((seq, str(len(seq)),item["plate_id"], name)))
    out.append("\n".join(out_row))
msg = "\n".join(out)

with open("../designs/plates/"+plate_name+".csv", "w") as file:
    file.write(msg)