import base64
jpg = open("D:\Program\Python\image.jpg", "rb")
jpg64 =  base64.b64encode(jpg.read())
jpg.close()
with open("base64.txt","w") as f:
    f.write(jpg64.decode().replace('\\','/'))