import re

txt = "I am a java Program"
txt2 = "java.lang.something"
txt3 = "somethign.java.util"

x = re.search("java", txt)
print(x)