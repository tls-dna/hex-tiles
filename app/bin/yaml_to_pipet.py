from yaml import full_load

to_pipet_staples = 0
def pipetting_description(plate_name, plate):
    global to_pipet_staples
    output_rows = []
    for row_name, row in plate["rows"].items():
        rs = []
        a = rs.append
        for item in row:
            if item["plate_id"][0] != row_name:
                #designs is inconsistent
                raise Exception("Data inconsistent at item:" + str(item["plate_id"]))
            a(int(item["plate_id"][1:])) #first letter in plate_id is the row
            to_pipet_staples += 1
        rs = ", ".join(map(str, sorted(rs)))
        rs = row_name + ": " + rs
        output_rows.append(rs)
    msg = []
    a = msg.append
    a("-"*60)
    a("Take plate: " + plate_name)
    a("-"*60)
    a("\n".join(sorted(output_rows)))
    return "\n".join(msg)

def order_description(plate_name, plate):
    output_rows = []
    for row_name, row in plate["rows"].items():
        out_row = []
        for item in sorted(row, key = lambda i: int(i["plate_id"][1:])):
            seq  = "".join(item["seq"])
            print(item["plate_id"], "\t", item["name"],"\t", seq, "\t", len(seq))



#with open("../designs/4R4C_2T.yaml") as file:
#with open("../designs/4R4C_2T_tube.yaml") as file:
#with open("../designs/TRing.yaml") as file:
#with open("../designs/HexagonCrystal.yaml") as file:
#with open("../designs/4R4C_2T_tube_crystal.yaml") as file:
#with open("../designs/small.yaml") as file:
#with open("../designs/test tube.yaml") as file:
files = [#"../designs/old_design/3R2C_2T.yaml",

#"../designs/Structures/TRing(AE)_2T.yaml",
#"../designs/Structures/4R0B_cr_2T.yaml",
#"../designs/Structures/4R0D_cr_2T.yaml",
#"../designs/Structures/3R0C_cr_2T.yaml",

#"../designs/Structures/4R4C_2T_tube.yaml",
"../designs/Structures/4R4C_2T.yaml",
#"../designs/Structures/TRing.yaml"
#"../designs/Structures/HexagonCrystal.yaml",
    #"../designs/Structures/old_design/3R2C.yaml",
    #"../designs/Structures/old_design/3R2C_4T.yaml",
    # "../designs/old_design/3R2C_1T.yaml",
           #"../designs/Structures/4R0A_cr_2T.yaml",         #0
           #"../designs/Structures/4R0A_cr_2T_tube.yaml",         #1
           #"../designs/Structures/HexagonCrystal.yaml",         #2
           #"../designs/Structures/TRing.yaml",         #3

    #      "../designs/4R0B_cr_2T.yaml",         #1
    #      "../designs/4R0C_cr_2T.yaml",         #2
    #      "../designs/4R0D_cr_2T.yaml",         #3
    #      "../designs/Tring(AD,BE,CF)_2T.yaml", #4
    #      "../designs/Tring(AE)_2T.yaml",       #5
    #      "../designs/3R0A_cr_2T.yaml",
    #      "../designs/3R0B_cr_2T.yaml",
    #      "../designs/3R0C_cr_2T.yaml",
    #      "../designs/plates/Order Old 1T/design/3R2C_1T.yaml"
         ]
f = files[0]
with open(f) as file:
    print(f)
    plates = full_load(file.read())

plate_list_existing = []
plate_list_order = []

for plate_name, plate  in plates.items():
    print("plate_name", plate_name)
    #connectors are not staples to order (exclude them)
    if not "Connectors" in plate_name:
        if "Ord" in plate_name:
            plate_list_order.append(plate_name)
        else:
            plate_list_existing.append(plate_name)

print("-"*80)
print("Existing plates:", plate_list_existing)
print("To order:", plate_list_order)
print("-"*80)
print()

for plate_name in plate_list_existing:
    msg = pipetting_description(plate_name, plates[plate_name])
    print(msg)

for plate_name in plate_list_order:
    msg = pipetting_description(plate_name, plates[plate_name])
    print(msg)

print()
print("oligos total:", to_pipet_staples)
print()

# print("Original:")
# for plate_name in plate_list_existing:
#     print("Plate:",plate_name)
#     order_description(plate_name, plates[plate_name])
#
# print()
# print("Order:")
# for plate_name in plate_list_order:
#     print("Plate:",plate_name)
#     order_description(plate_name, plates[plate_name])
#     print()
