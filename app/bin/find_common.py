from yaml import load


files = [
    "../designs/4R0A_cr_2T.yaml",
    "../designs/4R0B_cr_2T.yaml",
    "../designs/4R0C_cr_2T.yaml",
    "../designs/4R0D_cr_2T.yaml",
    #"../designs/Tring(AD,BE,CF)_2T.yaml",
    #"../designs/Tring(AE)_2T.yaml",
    #"../designs/3R0A_cr_2T.yaml",
    #"../designs/3R0B_cr_2T.yaml",
    #"../designs/3R0C_cr_2T.yaml",
    #"../designs/plates/Order Old 1T/design/3R2C_1T.yaml"
]



for f in files[:1]:
    with open(f) as file:
        print(f)
        plates = load(file.read())
        print("plates: %s | one more, cause of the connections" % len(plates))
        print("-"*60)
        for plate_name in filter(lambda x: not "Connectors" in x , plates.keys()):
            if not plate_name in plate_sets:
                plate_sets[plate_name] = Set()

                #plates[plate_name]


