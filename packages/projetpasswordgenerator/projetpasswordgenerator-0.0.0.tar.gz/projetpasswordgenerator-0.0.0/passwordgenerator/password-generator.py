import secrets


senbol = ['!','@','#','$','%']
def generate():
    vale = list()
    for i in range(ord('!'), ord('z')):
        if 48 <= i <= 57:
            vale.append(chr(i))
        elif 64 <= i <= 90:
            vale.append(chr(i))
        elif 97 <= i <= 122:
            vale.append(chr(i))
        elif chr(i) in senbol:
            vale.append(chr(i))
            
        else:
            vale = vale
    code_secret = ''.join(secrets.choice(vale) for _ in range(10))
    return code_secret
    
print(generate())
