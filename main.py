from lexicalAnalyzer import LexicalAnalyzer
# Read from file
with open('sourcecode.c', 'r') as sourceCodeFile:
    sourceCode = sourceCodeFile.read()
constSourceCode = sourceCode  # A copy of the source code
scanner = LexicalAnalyzer()
sourceCode = scanner.main(sourceCode)
print("<Token type, token value>")
scanner.printTokens()
X = '#include<bits/stdc++.h>  int intx = 5 ; 34;float== y  =1005.458 ;int intRRR = 77; 2234int= x = 3; floatx =3; shortttt x = 3;string xz ="hahahahaz";while(x=5){x++;} float whiley = 23.444;'
Y = "int x(){inttttt x =6 ; x = x+1; int z=20;} int main(){while(z< 3){auto x = 3; x ++; auto y =false;}}"
Z = 'int intvalue=10+5; /* THis is a commentt\t\n to illustrate things.*/'
K = 'bool isPowerOfTwo(int x){ //First x in the below expression  //for the case when x is 0  return x && (!(x&(x-1)));'

