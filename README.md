# built_up
## *python hot_reloader*
  ### *This hot reloader was made to get a nearly similar feel of working in google's flutter dev with hot reloader,  This hot reloader saves your file , reloads its and neglects any errors in your program by tracking the version of your file with no errors. Very appealing while doing app developement with pyqt, kivy, tkinter ,etc.where you won't need to run your program each and every time for even minimal testing of your developement.Make sure that you set the keyboard focus remain in your IDE or the .py file so that your reloader runs or else it pauses until the focus returns.*
###  *The instruction for how to use this program is provided below  and also provided as a function named helper in the program. However the program was set, to run only on linux and the program must be imported and run from a seperate file and that's it you can do your developement while running your program along side with this hot_reloader.*

## **Usage**
### *Incase you have a file names script.py*
*import...*

class x():

    def...
  
        pass
   
    def...
  
        pass

def main():

    run = x()
  
 ### *you should always have a main() function with no arguments through which your program executes and do not call the main function in your program.* 
 ### *Now you get the hot_reloader.py, create a new file some_file.py, and*
 import hot_reloader
 
 filename = 'script.py'     # the file file which you want to run
 
 hot_reloader.re_loader(filename)
 
 ### *The program seems to run only on linux, As for sure the program is set not to run into errors, even if you come across the error, continue to update and debug the errors as the reloader keeps on updating and runs until keyboard interupt. you don't need to get worried about it and running the reloader is simple and if help required, there is a helper function inside the hot_reloader which is same as the above provided instruction for quick reference*
 
 hot_reloader.helper()
  
