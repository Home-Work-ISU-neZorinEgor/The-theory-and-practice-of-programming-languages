from extended_dlc import ExtendedDLC

mapDLC = ExtendedDLC()

mapDLC["value1"] = 1
mapDLC["value2"] = 2
mapDLC["value3"] = 3
mapDLC["1"] = 10
mapDLC["2"] = 20
mapDLC["3"] = 30
mapDLC["1, 5"] = 100
mapDLC["5, 5"] = 200
mapDLC["10, 5"] = 300

print(mapDLC.iloc[0])  # >>> 10
print(mapDLC.iloc[2])  # >>> 300
print(mapDLC.iloc[5])  # >>> 200
print(mapDLC.iloc[8])  # >>> 3

mapDLC = ExtendedDLC()

mapDLC["value1"] = 1
mapDLC["value2"] = 2
mapDLC["value3"] = 3
mapDLC["1"] = 10
mapDLC["2"] = 20
mapDLC["3"] = 30
mapDLC["(1, 5)"] = 100
mapDLC["(5, 5)"] = 200
mapDLC["(10, 5)"] = 300
mapDLC["(1, 5, 3)"] = 400
mapDLC["(5, 5, 4)"] = 500
mapDLC["(10, 5, 5)"] = 600

print(mapDLC.ploc[">=1"])  # >>> {1=10, 2=20, 3=30}
print(mapDLC.ploc["<3"])  # >>> {1=10, 2=20}

print(mapDLC.ploc[">0, >0"])  # >>> {(1, 5)=100, (5, 5)=200, (10, 5)=300}
print(mapDLC.ploc[">=10, >0"])  # >>> {(10, 5)=300}

print(mapDLC.ploc["<5, >=5, >=3"])  # >>> {(1, 5, 3)=400}
