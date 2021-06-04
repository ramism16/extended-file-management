import zipfile
import os
import sys

def menu():
    print("1: Zip a folder")
    print("2: Unzip and extract a zip file")
    print("3: Delete the same name files from folder and sub-folders")
    print("4: Label a code file (add label in comment form to the top of file)")
    print("5: Brute-force to recover a password-protected zip file")
    print("6: Exit")

def pathOrFileInput(prompt):
    pathInput = input("\n"+prompt)
    print("\nEntered path is: ", pathInput)
    return pathInput

def checkPath(pathIn, isFile = False):
    if isFile:
        if os.path.isfile(os.path.relpath(pathIn)):
            return True
    else:
        if os.path.isdir(os.path.relpath(pathIn)):
            return True

    return False

def zipFolder():
    pathIn = pathOrFileInput("Please enter the name of directory to zip: ")
    if not checkPath(pathIn):
        print("Invalid path entered\n")
        return
    else:
        zipf = zipfile.ZipFile('newZip.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(pathIn):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.path.join(pathIn, '..'))
                )
        zipf.close()
        print(pathIn, " zipped to newZip.zip in current directory")


def unzip_brute(brute = False):
    pathIn = pathOrFileInput("Please enter name of the zipfile: ")
    if not checkPath(pathIn, True):
        print("Invalid path/file does not exist\n")
        return

    zip_file = zipfile.ZipFile(pathIn)
    if not brute:
        passwordChoice = input("Is the zip password-protected? (y/n): ")
        if passwordChoice == 'y':
            password = input("\nEnter zip password: ")
            try:
                zip_file.extractall(pwd = password.encode())
                print(pathIn, " unzipped to current directory")
            except:
                print(pathIn, "could not be unzipped or wrong password was entered")
        else:
            zip_file.extractall()
            print(pathIn, " unzipped to current directory")
    else:
        print("Working on finding password, please wait..\n")
        lineNumber = 0
        with open("rockyou.txt", 'rb') as file:
            for line in file:
                #this loop will not increase complexity as split is run only once
                for word in line.split():
                    # file contains some special characters and hence
                    # UnicodeDecodeError will be thrown
                    try:
                        lineNumber += 1
                        zip_file.extractall(pwd=word)
                        #next steps will run if password is found
                        print("Password found at line number", lineNumber)
                        print("password is", word.decode())
                        return True
                    except:
                        continue
        print("\nCould not find password")

def deleteSameNameFiles():
    pathIn = pathOrFileInput("Please enter the name of files: ")
    i = 0

    #remove first instance of file (non-directory/in the root folder)
    if os.path.exists(os.path.join(os.getcwd(), pathIn)):
        os.remove(os.path.join(dir, pathIn))
        i = 1

    for root, subdirpaths, files in os.walk(os.getcwd()):
        for file in files:
            if file == pathIn:
                os.remove(os.path.join(root,file))
                i+=1

    if i > 0:
        print(i, "number of", pathIn, "files deleted in root and subfolders")
    else:
        print("No files with the name", pathIn, "found in root and subfolders")

def tagCodeFile():
    pathIn = pathOrFileInput("Please enter the name of the code file to tag/label: ")
    if not checkPath(pathIn, True):
        print("Invalid file/path entered")
        return

    flag = False
    tagLine = input("Enter the tag/label: ")
    with open(pathIn, 'r+') as tag_file:
        if pathIn.endswith(".py"):
            tagLine = "# " + tagLine + "\n"
        elif pathIn.endswith(".pas"):
            tagLine = "{ " + tagLine + " }\n"
        elif pathIn.endswith(".html"):
            tagLine = "<!-- " + tagLine + " -->\n"
        elif pathIn.endswith(".vb"):
            tagLine = "' " + tagLine + "\n"
        else:
            tagLine = "/* " + tagLine + " */\n"

        Lines = tag_file.readlines()
        Lines.insert(0, tagLine)
        tag_file.seek(0,0)
        tag_file.writelines(Lines)
        flag = True

    if flag:
        print("File", pathIn, "tagged with", tagLine)
    else:
        print("could not tag file")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()
    choice = input("\n\n Please enter your option: ")
    while not choice == '6':
        if choice == '1':
            zipFolder()
        elif choice == '2':
            unzip_brute()
        elif choice == '3':
            deleteSameNameFiles()
        elif choice == '4':
            tagCodeFile()
        elif choice == '5':
            unzip_brute(True)

        if choice != '6':
            if choice in ['1','2','3','4','5']:
                input("\n\nPress enter to continue")
                os.system('cls')
                menu()
                choice = input("\n\n Please enter your option: ")
            else:
                print("\nPlease enter a menu option")
                choice = input("\n\n Please enter your option: ")
