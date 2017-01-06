import os


# build the 'basic' vbs file and return the file object
def buildVBS(name='temp.vbs'):
    f = open(name, 'wb')
    f.write('Set WshShell = WScript.CreateObject("WScript.Shell")\n')
    return f


# close, run and delete the vbs file
def runVBS(f, name='temp.vbs'):
    f.close()
    os.system(name)
    os.remove(name)


# execute keystrokes
def sendKeys(keys):
    f = buildVBS()
    f.write('WshShell.SendKeys "' + keys + '"')
    runVBS(f)


# activates (brings in the foreground) an application
# for example for taking a screenshot
def activApp(app):
    f = buildVBS()
    f.write('WshShell.AppActivate "' + app + '"')
    runVBS(f)
