import winreg
key=winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT,r"")
newkey=winreg.CreateKey(key,"FLAG")
winreg.SetValue(newkey,"FLAG",winreg.REG_SZ,"0")
str=winreg.QueryValue(newkey,"FLAG")
winreg.CloseKey(newkey)
winreg.CloseKey(key)
print(str)
str=winreg.QueryValue(newkey,"FLAG")