import requests
import os

def to_str(lines):
    normal_lines = []
    for line in lines:
        normal_lines.append('"' + str(line, 'utf-8') + '"\n')
    for i in range(len(normal_lines)):
        normal_lines[i] = normal_lines[i].replace('|','","')
    return normal_lines

query = 'https://iatacodes.org/api/v6/cities.csv?api_key=53610b82-09f8-4ced-953c-b062e213ad3f'
response = requests.get(query, verify=False)
text = response.iter_lines()
text = to_str(text)
print(text)
if not os.path.isfile("IATA.csv"):
    with open("IATA.csv", "w") as f:
        for line in text:
            try:
                f.write(line)
            except UnicodeEncodeError:
                pass

