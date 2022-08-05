from flask import Flask,request
import subprocess

from flask_cors import CORS
app = Flask(__name__)

CORS(app)

import os
import time
import uuid
import json

@app.route('/')
def index():
  html = '''<html>
  <head>
    <title>repl.it</title>
  </head>
  <body>
    <h3>Click any language : </h3>
    <form action="python" method="GET">
      <textarea id="w3review" name="code" rows="3" cols="50"># This program prints Hello, world!

print('Hello, world!')</textarea><br>Input (if required)<br><textarea id="w3review" name="input" rows="3" cols="50"></textarea><br>
      <input type="submit" value="Run Python Code" />
    </form>

    <form action="java" method="GET">
      <textarea id="w3review" name="code" rows="5" cols="50">class Main{  
  public static void main(String args[]){  
    System.out.println("Hello, world!");  
  }  
}  </textarea><br>
      <input type="submit" value="Run Java Code" />
    </form>

    <form action="cpp" method="GET">
      <textarea id="w3review" name="code" rows="8" cols="50">// Your First C++ Program

#include <iostream>

int main() {
    std::cout << "Hello world!";
    return 0;
}</textarea><br>
      <input type="submit" value="Run C++ Code" />
    </form>

    <form action="c" method="GET">
      <textarea id="w3review" name="code" rows="7" cols="50">#include <stdio.h>
int main() {
   // printf() displays the string inside quotation
   printf("Hello, world!");
   return 0;
}</textarea><br>
      <input type="submit" value="Run C Code" />
    </form>
  </body>
</html>'''


  return html

@app.route('/python/', methods = ['POST', 'GET'])
def hello_world():
    name = str(uuid.uuid1())+".py"
    f = open(name, "a")
  
    if request.method == 'POST':
      if request.is_json:
        dataCode = json.dumps(request.json)
        dataCode = json.loads(dataCode)
        
        f.write(dataCode['code'])
      else:
        f.write(request.args.get('code'))
    else:
      if 'code' in request.args:
        f.write(request.args.get('code'))
      else:
        f.write('''print("Hello from python!!!")''')
    
    f.close()

    begin = time.time()


    proc = subprocess.Popen(['python', name,  'arg1 arg2 arg3 arg4'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    if 'input' in request.args:
        proc.stdin.write(str.encode(request.args.get('input')))

    out = proc.communicate()[0].decode("utf-8")
    os.remove(name)

    end = time.time()

    dataJson = {}
    dataJson['statusCode'] = 200
    dataJson['output'] = out.strip()
    dataJson['cpuTime'] = float("{0:.3f}".format(end - begin))

    return dataJson

@app.route('/java/', methods = ['POST', 'GET'])
def java():
    name = str(uuid.uuid1())
    #name = "Main"

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, name)
    if not os.path.exists(final_directory):
      os.makedirs(final_directory)

    f = open(name+'/'+name+".java", "w")

    if request.method == 'POST':
      if request.is_json:
        dataCode = json.dumps(request.json)
        dataCode = json.loads(dataCode)
        
        f.write(dataCode['code'])
      else:
        f.write(request.args.get('code'))
    else:
      if 'code' in request.args:
        f.write(request.args.get('code'))
      else:
        f.write('''class Main {
            public static void main(String[] args) {
              System.out.println("Hello world!");
            }
          }''')
      
    f.close()


    begin = time.time()
  
    proc = subprocess.Popen(['javac', name+"/"+name+'.java'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    
    
    out = proc.communicate()[0].decode("utf-8")
    if(out == ""):
      proc = subprocess.Popen(['java', '-cp',name, 'Main'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)

      out = proc.communicate()[0].decode("utf-8")

    out = proc.communicate()[0].decode("utf-8")

    #path = os.path.join(name+".java") 
    # os.remove(path)
    # os.remove("Main" + ".class")

    import glob

    files = glob.glob(name+'/*.*')
    for f in files:
        try:
          os.remove(f)
        except OSError as e:
          print("Error: %s : %s" % (f, e.strerror))

    os.rmdir(name)
    end = time.time()

    dataJson = {}
    dataJson['statusCode'] = 200
    dataJson['output'] = out.strip()
    dataJson['cpuTime'] = float("{0:.3f}".format(end - begin))

    return dataJson

@app.route('/c/', methods = ['POST', 'GET'])
def c():
    name = str(uuid.uuid1())
    
    f = open(name+".c", "w")
    
    if request.method == 'POST':
      if request.is_json:
        dataCode = json.dumps(request.json)
        dataCode = json.loads(dataCode)
        
        f.write(dataCode['code'])
      else:
        f.write(request.args.get('code'))
    else:
      if 'code' in request.args:
        f.write(request.args.get('code'))
      else:
        f.write('''#include <stdio.h>

          int main(void) {
            printf("Hello from c!!!");
            return 0;
          }''')

    f.close()
    

    begin = time.time()
  
    proc = subprocess.Popen(['clang-7','-pthread','-lm','-o',name,(name+'.c')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)

    out = proc.communicate()[0].decode("utf-8")
    if(out == ""):
      proc = subprocess.Popen(['./'+name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)

      out = proc.communicate()[0].decode("utf-8")


    # path = os.path.join(name+".java") 
    os.remove(name)
    os.remove(name + ".c")


    end = time.time()

    dataJson = {}
    dataJson['statusCode'] = 200
    dataJson['output'] = out.strip()
    dataJson['cpuTime'] = float("{0:.3f}".format(end - begin))

    return dataJson

@app.route('/cpp/', methods = ['POST', 'GET'])
def cpp():
    name = str(uuid.uuid1())
    
    f = open(name+".cpp", "w")
    #f.write(request.args.get('code'))
    
    
          
    if request.method == 'POST':
      if request.is_json:
        dataCode = json.dumps(request.json)
        dataCode = json.loads(dataCode)
        
        f.write(dataCode['code'])
      else:
        f.write(request.args.get('code'))
    else:
      if 'code' in request.args:
        f.write(request.args.get('code'))
      else:
        f.write('''int main() {
          std::cout << "Hello from c++!!!";
        }''')
          
    f.close()
    

    begin = time.time()
  
    proc = subprocess.Popen(['clang++-7','-pthread','-std=c++17','-o',name,(name+'.cpp')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)

    out = proc.communicate()[0].decode("utf-8")
    if(out == ""):
      proc = subprocess.Popen(['./'+name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.PIPE)

      out = proc.communicate()[0].decode("utf-8")


    # path = os.path.join(name+".java") 
    os.remove(name)
    os.remove(name + ".cpp")


    end = time.time()

    dataJson = {}
    dataJson['statusCode'] = 200
    dataJson['output'] = out.strip()
    dataJson['cpuTime'] = float("{0:.3f}".format(end - begin))

    return dataJson

app.run('0.0.0.0')