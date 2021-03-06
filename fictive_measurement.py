import measurement as ms
result = dict()
with (open("out_1.txt")) as f:
    for l in f.readlines():
        rd_line = l.split("=")
        result[rd_line[0].strip()] = float(rd_line[1].strip())

ms.measurement_storage.set_binom_measured_signal(1, num_binom=0, **result)

with (open("out_2.txt")) as f:
    for l in f.readlines():
        rd_line = l.split("=")
        result[rd_line[0].strip()] = float(rd_line[1].strip())

ms.measurement_storage.set_binom_measured_signal(2, num_binom=0, **result)

with (open("out_3.txt")) as f:
    for l in f.readlines():
        rd_line = l.split("=")
        result[rd_line[0].strip()] = float(rd_line[1].strip())

ms.measurement_storage.set_binom_measured_signal(3, num_binom=0, **result)