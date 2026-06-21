from agents.reviewer import run_full_review
content = ''

try:
    with open("./Test_code_file/Main.java", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("File not found")
     
  
result = run_full_review(code=content , language="Java")    

print (result)




