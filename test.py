def produkt_filter(produkte, buchstabe):
    return list(filter(lambda produkt: produkt.startswith(buchstabe), produkte))

print(produkt_filter(["Apfel", "Banane", "Ananas"], "A"))

def gerade(zahlen):
    return list(filter(lambda zahl: zahl % 2 == 0, zahlen))

print(gerade([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))