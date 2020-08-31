import ..\\measurement as ms
result = dict()
with (open("..\\out.txt")) as f:
    for l in f.readlines():
        rd_line = l.split("=")
        result[rd_line[0].strip()] = float(rd_line[1].strip())
pass
