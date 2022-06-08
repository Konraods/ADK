import hl7

a = 0
with open('hl7.hl7', 'r') as f:
    for line in f:
       if a == 0:
           message = line
           a = 1
       else:
           message += line
h=hl7.parse(message)
for line in h:
    print(line)
