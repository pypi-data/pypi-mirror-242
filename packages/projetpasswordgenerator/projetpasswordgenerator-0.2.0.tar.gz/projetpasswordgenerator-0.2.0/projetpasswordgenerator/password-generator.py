import secrets


import secrets

class CodeGenerator:
    def __init__(self):
        self.senbol = ['!', '@', '#', '$', '%']
        self.vale = []

    def generate(self):
        for i in range(ord('!'), ord('z')):
            if 48 <= i <= 57:
                self.vale.append(chr(i))
            elif 64 <= i <= 90:
                self.vale.append(chr(i))
            elif 97 <= i <= 122:
                self.vale.append(chr(i))
            elif chr(i) in self.senbol:
                self.vale.append(chr(i))

        code_secret = ''.join(secrets.choice(self.vale) for _ in range(10))
        return code_secret

code_gen = CodeGenerator()
print(code_gen.generate())
