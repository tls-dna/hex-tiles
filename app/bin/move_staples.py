from yaml import load,dump
from pprint import pprint
def parse_plate_id(plate_id):
    return plate_id[0], plate_id[1:] #row, number

def find_oligo(row, plate_id):
    for oligo in row:
        if oligo["plate_id"] == plate_id:
            return oligo
    return None

def move(plates, plate_name1, plate_id1, plate_name2, plate_id2):
    #and the plates can be also missing
    if not plate_name1 in plates:
        return
    plate1 = plates[plate_name1]["rows"]
    if not plate_name2 in plates:
        plates[plate_name2] = {"rows":{}}
    plate2 = plates[plate_name2]["rows"]

    old_row_id, old_num =  parse_plate_id(plate_id1)
    new_row_id, new_num =  parse_plate_id(plate_id2)

    #as we do batch on all files row might be missing
    if not old_row_id in plate1:
        return
    old_row = plate1[old_row_id]
    oligo = find_oligo(old_row, plate_id1)
    #as we have to batch operation
    #oligo might be missing
    if not oligo:
        return


    if not new_row_id in plate2:
        #create row if plate has not
        plate2[new_row_id] = []
    #get the row
    new_row = plate2[new_row_id]

    #check wherever place is occupied
    if find_oligo(new_row,plate_id2):
        raise Exception("No place to move.")


    #do the move
    #remove from previous location
    old_row.remove(oligo)
    #set new plate pos
    oligo["plate_id"] = plate_id2
    #add to new_row
    new_row.append(oligo)

    pprint(plates[plate_name1]["rows"][old_row_id])
    pprint(plates[plate_name2]["rows"][new_row_id])




# file_list = ("4R4C_2T.yaml","4R4C_2T_tube.yaml", "HexagonCrystal.yaml","TRing.yaml")
# transactions = (
#         #Plate_62129 to Ord_55713_Protectors_0
#         (("Plate_62129", "C7"), ("Ord_55713_Protectors_0", "C7")),
#         (("Plate_62129", "C8"), ("Ord_55713_Protectors_0", "C8")),
#         (("Plate_62129", "D3"), ("Ord_55713_Protectors_0", "D3")),
#         (("Plate_62129", "D4"), ("Ord_55713_Protectors_0", "D4")),
#         #Ord_82847_Staples_0 to Ord_55713_Protectors_0
#         (("Ord_82847_Staples_0", "A1"), ("Ord_55713_Protectors_0", "G1")),
#         (("Ord_82847_Staples_0", "A2"), ("Ord_55713_Protectors_0", "G2")),
#         (("Ord_82847_Staples_0", "A3"), ("Ord_55713_Protectors_0", "G3")),
#         (("Ord_82847_Staples_0", "A4"), ("Ord_55713_Protectors_0", "G4")),
#         (("Ord_82847_Staples_0", "A5"), ("Ord_55713_Protectors_0", "G5")),
#         (("Ord_82847_Staples_0", "A6"), ("Ord_55713_Protectors_0", "G6")),
#         (("Ord_82847_Staples_0", "A7"), ("Ord_55713_Protectors_0", "G7")),
#         (("Ord_82847_Staples_0", "A8"), ("Ord_55713_Protectors_0", "G8")),
#         #Ord_46484_Protectors_0 to Ord_55713_Protectors_0
#         (("Ord_46484_Protectors_0", "A1"), ("Ord_55713_Protectors_0", "F1")),
#         (("Ord_46484_Protectors_0", "A2"), ("Ord_55713_Protectors_0", "F2")),
#         (("Ord_46484_Protectors_0", "A3"), ("Ord_55713_Protectors_0", "F3")),
#         (("Ord_46484_Protectors_0", "A4"), ("Ord_55713_Protectors_0", "F4")),
#         (("Ord_46484_Protectors_0", "A5"), ("Ord_55713_Protectors_0", "F5")),
#         (("Ord_46484_Protectors_0", "A6"), ("Ord_55713_Protectors_0", "F6")),
#         (("Ord_46484_Protectors_0", "A7"), ("Ord_55713_Protectors_0", "F7")),
#         (("Ord_46484_Protectors_0", "A8"), ("Ord_55713_Protectors_0", "F8")),
#         (("Ord_46484_Protectors_0", "A9"), ("Ord_55713_Protectors_0", "F9")),
#         (("Ord_46484_Protectors_0", "A10"), ("Ord_55713_Protectors_0","F10")),
#
#         #Ord_35372_Staples_0 to Ord_55713_Protectors_0
#         (("Ord_35372_Staples_0", "A1"), ("Ord_55713_Protectors_0", "H1")),
#         (("Ord_35372_Staples_0", "A2"), ("Ord_55713_Protectors_0", "H2")),
#         (("Ord_35372_Staples_0", "A3"), ("Ord_55713_Protectors_0", "H3")),
#         (("Ord_35372_Staples_0", "A4"), ("Ord_55713_Protectors_0", "H4")),
#         (("Ord_35372_Staples_0", "A5"), ("Ord_55713_Protectors_0", "H5")),
#         (("Ord_35372_Staples_0", "A6"), ("Ord_55713_Protectors_0", "H6")),
#    )

file_list =(
     "../designs/4R0A_cr_2T.yaml",
     "../designs/4R0B_cr_2T.yaml",
     "../designs/4R0C_cr_2T.yaml",
     "../designs/4R0D_cr_2T.yaml",
     "../designs/Tring(AD,BE,CF).yaml",
     "../designs/Tring(AE).yaml",
     "../designs/3R0A_cr_2T.yaml",
     "../designs/3R0B_cr_2T.yaml",
     "../designs/3R0C_cr_2T.yaml",
)

transactions = (
    (("Ord_90187_Staples_0", "A1"), ("Plate2SpTubes", "A1")),
    (("Ord_90187_Staples_0", "A2"), ("Plate2SpTubes", "A2")),
    (("Ord_90187_Staples_0", "A3"), ("Plate2SpTubes", "A3")),
    (("Ord_90187_Staples_0", "A4"), ("Plate2SpTubes", "A4")),
    (("Ord_90187_Staples_0", "A5"), ("Plate2SpTubes", "A5")),
    (("Ord_90187_Staples_0", "A6"), ("Plate2SpTubes", "A6")),
    (("Ord_90187_Staples_0", "A7"), ("Plate2SpTubes", "A7")),
    (("Ord_90187_Staples_0", "A8"), ("Plate2SpTubes", "A8")),

    (("Ord_34989_Staples_0", "A1"), ("Plate2SpTubes", "B1")),
    (("Ord_34989_Staples_0", "A2"), ("Plate2SpTubes", "B2")),
    (("Ord_34989_Staples_0", "A3"), ("Plate2SpTubes", "B3")),
    (("Ord_34989_Staples_0", "A4"), ("Plate2SpTubes", "B4")),
    (("Ord_34989_Staples_0", "A5"), ("Plate2SpTubes", "B5")),
    (("Ord_34989_Staples_0", "A6"), ("Plate2SpTubes", "B6")),
    (("Ord_34989_Staples_0", "A7"), ("Plate2SpTubes", "B7")),
    (("Ord_34989_Staples_0", "A8"), ("Plate2SpTubes", "B8")),

    (("Ord_41526_Staples_0", "A1"), ("Plate2SpTubes", "C1")),
    (("Ord_41526_Staples_0", "A2"), ("Plate2SpTubes", "C2")),
    (("Ord_41526_Staples_0", "A3"), ("Plate2SpTubes", "C3")),
    (("Ord_41526_Staples_0", "A4"), ("Plate2SpTubes", "C4")),
    (("Ord_41526_Staples_0", "A5"), ("Plate2SpTubes", "C5")),
    (("Ord_41526_Staples_0", "A6"), ("Plate2SpTubes", "C6")),
    (("Ord_41526_Staples_0", "A7"), ("Plate2SpTubes", "C7")),
    (("Ord_41526_Staples_0", "A8"), ("Plate2SpTubes", "C8")),

    (("Ord_01845_Staples_0", "A1"), ("Plate2SpTubes", "D1")),
    (("Ord_01845_Staples_0", "A2"), ("Plate2SpTubes", "D2")),
    (("Ord_01845_Staples_0", "A3"), ("Plate2SpTubes", "D3")),
    (("Ord_01845_Staples_0", "A4"), ("Plate2SpTubes", "D4")),
    (("Ord_01845_Staples_0", "A5"), ("Plate2SpTubes", "D5")),
    (("Ord_01845_Staples_0", "A6"), ("Plate2SpTubes", "D6")),
    (("Ord_01845_Staples_0", "A7"), ("Plate2SpTubes", "D7")),
    (("Ord_01845_Staples_0", "A8"), ("Plate2SpTubes", "D8")),

    (("Ord_30155_Staples_0", "A1"), ("Plate2SpTubes", "E1")),
    (("Ord_30155_Staples_0", "A2"), ("Plate2SpTubes", "E2")),
    (("Ord_30155_Staples_0", "A3"), ("Plate2SpTubes", "E3")),
    (("Ord_30155_Staples_0", "A4"), ("Plate2SpTubes", "E4")),
    (("Ord_30155_Staples_0", "A5"), ("Plate2SpTubes", "E5")),
    (("Ord_30155_Staples_0", "A6"), ("Plate2SpTubes", "E6")),
    (("Ord_30155_Staples_0", "A7"), ("Plate2SpTubes", "E7")),
    (("Ord_30155_Staples_0", "A8"), ("Plate2SpTubes", "E8")),

    (("Ord_24220_Staples_0", "A1"), ("Plate2SpTubes", "F1")),
    (("Ord_24220_Staples_0", "A2"), ("Plate2SpTubes", "F2")),
    (("Ord_24220_Staples_0", "A3"), ("Plate2SpTubes", "F3")),
    (("Ord_24220_Staples_0", "A4"), ("Plate2SpTubes", "F4")),
    (("Ord_24220_Staples_0", "A5"), ("Plate2SpTubes", "F5")),
    (("Ord_24220_Staples_0", "A6"), ("Plate2SpTubes", "F6")),
    (("Ord_24220_Staples_0", "A7"), ("Plate2SpTubes", "F7")),
    (("Ord_24220_Staples_0", "A8"), ("Plate2SpTubes", "F8")),


    (("Ord_51091_Staples_0", "A1"), ("Plate2SpTubes", "G1")),
    (("Ord_51091_Staples_0", "A2"), ("Plate2SpTubes", "G2")),
    (("Ord_51091_Staples_0", "A3"), ("Plate2SpTubes", "G3")),
    (("Ord_51091_Staples_0", "A4"), ("Plate2SpTubes", "G4")),
    (("Ord_51091_Staples_0", "A5"), ("Plate2SpTubes", "G5")),
    (("Ord_51091_Staples_0", "A6"), ("Plate2SpTubes", "G6")),
    (("Ord_51091_Staples_0", "A7"), ("Plate2SpTubes", "G7")),
    (("Ord_51091_Staples_0", "A8"), ("Plate2SpTubes", "G8")),


    (("Ord_73854_Staples_0", "A1"), ("Plate2SpTubes", "H1")),
    (("Ord_73854_Staples_0", "A2"), ("Plate2SpTubes", "H2")),
    (("Ord_73854_Staples_0", "A3"), ("Plate2SpTubes", "H3")),
    (("Ord_73854_Staples_0", "A4"), ("Plate2SpTubes", "H4")),
    (("Ord_73854_Staples_0", "A5"), ("Plate2SpTubes", "H5")),
    (("Ord_73854_Staples_0", "A6"), ("Plate2SpTubes", "H6")),
    (("Ord_73854_Staples_0", "A7"), ("Plate2SpTubes", "H7")),
    (("Ord_73854_Staples_0", "A8"), ("Plate2SpTubes", "H8")),
    (("Ord_73854_Staples_0", "A9"), ("Plate2SpTubes", "H9")),
    (("Ord_73854_Staples_0", "A10"), ("Plate2SpTubes", "H10")),
    (("Ord_73854_Staples_0", "A11"), ("Plate2SpTubes", "H11")),
    (("Ord_73854_Staples_0", "A12"), ("Plate2SpTubes", "H12")),

    (("Ord_99446_Staples_0", "A1"), ("Plate2SpTubes", "G9")),
    (("Ord_99446_Staples_0", "A2"), ("Plate2SpTubes", "G10")),
    (("Ord_99446_Staples_0", "A3"), ("Plate2SpTubes", "G11")),
    (("Ord_99446_Staples_0", "A4"), ("Plate2SpTubes", "G12")),

)

for fp in file_list:
    print("moving staples in ", fp)
    with open("../designs/"+fp) as file:
        plates = load(file)

    for t in transactions:
        (from_plate, from_id), (to_plate, to_id) = t
        move(plates, from_plate, from_id, to_plate, to_id)


    with open("../designs/"+fp, "w") as file:
        file.write(dump(plates))


#move(plates, "Plate_62129", "C7", "Ord_55713_Protectors_0", "C7")
#move(plates, "Plate_62129", "C8", "Ord_55713_Protectors_0", "C8")



