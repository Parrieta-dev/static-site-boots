import re

text = "I'm a little teapot, short and stout. Here is my handle, here is my spout. And I'm a teapot teapot and also teapotery"
matches = re.findall(r"teapot", text)
# print(matches)  # ['teapot']

text = "Hello ![cat](cat.png) and ![dog](dog.png)"
pattern = r"!\["
matches = re.findall(pattern, text)
print(matches)

pattern1 = r"!\[([^\]]*)\]"
pattern2 = r"\(([^\)]*)\)"
matches1 = re.findall(pattern1, text)
matches2 = re.findall(pattern2, text)
print(matches1, matches2)

pattern3 = r"!\[([^\]]*)\]\(([^\)]*)\)"
matches3 = re.findall(pattern3, text)
print(matches3)

text = "Hello tienes que encontrar el link [curso](www.boot.dev) pero NO encontrar la perroimagen ![dog](dog.png)"
pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
matches = re.findall(pattern, text)
print(matches)