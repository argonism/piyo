import os, re
with open("workfile.txt") as f:
    dataset = f.read().split("-------------------------------------------------------\n")

for data in dataset:
    http_line = data.split("\n")[0]
    method, path, ver = http_line.strip().split(" ")
    filename = f"{method.lower()}_{'_'.join(path.split('/')[2:])}.json"
    splitted = [ e for e in re.split(r"\n\n", data) if e ]
    with open(filename, "w", newline="") as f:
        res_body = splitted[-1].rstrip()
        if res_body == "HTTP/1.1 204 No Content":
            res_body = ""
        f.write(res_body)