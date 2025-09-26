import hashlib
passwords = ["Amy's", "meat's", "Hughes", "cowers", "lathes", "Tagalog", "unlearns", "scrimshaw's", "fictitious", "condones", "reclined", "devours", "thirty", "workplaces", "idolizes", "upward", "overmuch", "fishbowl's", "emanation", "headboard's", "bugaboo's", "Edwina", "censoring", "Eleazar", "cowlick's", "dismissal's", "surrendering", "coexisting", "congregate", "stoker's", "Gulfport", "baffling", "Schuyler's", "Oshkosh", "ass", "Grendel", "qualified", "model", "Olduvai's", "outsource", "Theodoric's", "Musial's", "scratch's", "Kojak", "jettison", "Duse", "disable", "unprotected", "quartz's", "satisfactorily"]
salt = "nEvZ_iBWZJ9"

hashes = []
for i in passwords:
    hashes.append([i, hashlib.sha256(str(i + salt).encode()).hexdigest()])

for i in hashes: print(f"{i[0]} {i[1]}")