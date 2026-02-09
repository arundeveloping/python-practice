with open(r"D:\Gen AI-course\Assignments\Project-1\content\myfile.txt.txt", mode="r") as myPdf:
    contents = myPdf.read()
    print(contents)

with open("D:\Gen AI-course\Assignments\Project-1\content\output.txt", mode="w") as myOutputPdf:
    myOutputPdf.write(contents)