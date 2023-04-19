import base64
source = ''
with open('source.py', 'r') as file:
    for line in file:
        if "import" not in line:
            source += line
encode = base64.b64encode(source)
for _ in range(9):
    encode = base64.b64encode(encode)
print(encode)
