input_file = open("step4.txt", "r")

print "starting MRZ_parsing"

mrz = {}
i = 0
for line in input_file:
    i = i +1
    mrz[str(i)] = line

output_file = open("ID.txt", "w")

if i > 0:
    #nom
    name = mrz["1"][5:30]
    name = name.replace("<", "") + "\n"
    output_file.write(name)
if i > 1:
    #prenom
    i = mrz["2"].index("<", 13, 27)
    surname = mrz["2"][13:i] + "\n"
    output_file.write(surname)
    #birthdate AAMMJJ
    date = mrz["2"][27:33] + "\n"
    output_file.write(date)
    #sex
    sex = mrz["2"][34] + "\n"
    output_file.write(sex)


output_file.close()
input_file.close()