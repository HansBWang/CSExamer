import os, filecmp, shutil

errorCodes = {200:'success',404:'file not found',400:'error',408:'timeout'}

def compile(path, file,output):
    class_file = file[:-4]+"class"
    if (os.path.isfile(file)):
        os.system('javac -cp '+path+' '+file+' 2> '+output)
        if (os.path.isfile(class_file)):
            return 200
        else:
            return 400
    else:
        return 404

def run(file,testOutput):
    cmd = 'java -cp '+file
    r = os.system(cmd+' > '+testOutput)
    if r==0:
        return 200
    else:
        return 400

# def match(output):
#     if os.path.isfile('out.txt') and os.path.isfile(output):
#         b = filecmp.cmp('out.txt',output)
#         os.remove('out.txt')
#         return b
#     else:
#         return 404

class Checker(object):
    """Checker object for checking the code"""

    checkerCount = 0

    def __init__(self):
        super(Checker, self).__init__()
        self.__class__.checkerCount = self.__class__.checkerCount + 1
        self.id = self.__class__.checkerCount
        self.checkerPath = './tmp/'+str(self.id)+'/'

    def runCheck(self, code, graderCode):

        if not os.path.exists(self.checkerPath):
            os.makedirs(self.checkerPath)
        
        codePath = self.checkerPath+'Quiz.java'
        graderPath = self.checkerPath+'Grader.java'
        compileOutput = self.checkerPath+'compileOutput.txt'
        graderCompileOutput = self.checkerPath+'graderCompileOutput.txt'
        graderClassPath = self.checkerPath+' Grader'
        testOutput = self.checkerPath+'graderOutput.txt'

        f = open(codePath,'w')
        f.write(code)
        f.close()

        f = open(graderPath,'w')
        f.write(graderCode)
        f.close()

        r = compile(self.checkerPath,codePath,compileOutput)
        if r == 200:
            r = compile(self.checkerPath,graderPath,graderCompileOutput)
            if r == 200:
                r = run(graderClassPath,testOutput)
                f = open(testOutput,'r')
                output = f.read()
                r = 'Test result:\n'+output
            else:
                f = open(graderCompileOutput,'r')
                output = f.read()
                r = 'Grader Compile Error:\n'+output
        else:
            f = open(compileOutput,'r')
            output = f.read()
            r = 'Compile Error:\n'+output
            
        # shutil.rmtree(self.checkerPath)
        
        return r
