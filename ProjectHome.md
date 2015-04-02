## OVERVIEW ##

I wanted to be able to copy a snippet of source code from my text editor, convert it into color-coded HTML, and paste that into my blog.  I found some Windows programs for this but I'm a Linux user.  So I wrote my own in Python.

code2blog is a pyGTK front-end to Lorenzo Bettini's excellent command-line utility GNU/Source-Highlight.  The goal of this utility is easy conversion of source code into HTML.  It supports multiple languages and output formats.  You can specify tab size and line numbering.

GNU/Source Highlight supports more options than code2blog offers.  I left php and php3 out of the language list because they didn't work on my system (missing language files).

![http://img143.imageshack.us/img143/3631/screenshotte8.png](http://img143.imageshack.us/img143/3631/screenshotte8.png)

## USAGE ##

code2blog uses two windows; Input and Output.  Put your source in Input, get your markup from Output.

  * **Open**  Loads source from a text file
  * **Paste**  Paste from the sytem clipboard into the Input window.
  * **Clear**  Clears the Input Window

  * **Apply**  Calls GNU/Source Highlight to create the marked up version in the Output Window.  All the output is also selected so you can [Copy](Copy.md) it.

  * **Save**  Save the Output window to a text file
  * **Copy**  Copies from the Output Window to the system clipboard.
  * **Clear**  Clear the Output Window

  * **About**  Show the About Dialog
  * **Quit**  Exit the program

Let's say we're editing a program in our favorite text editor and have a snippet of code we want to blog.  Copy the section to the clipboard, switch to code2blog and click [Paste](Paste.md), [Apply](Apply.md), [Copy](Copy.md).  Then go into your blog and paste it.  For Blogger.com, use the Compose view, not the HTML view.  Yes, I know that seems backwards.


## WARNING ##

The only way to ruin a file is if you don't understand the save option.  This ONLY saves the output window, i.e. the converted output from GNU/Source Highlight.  Please do not save using the name of one of your source files -- code2blog is not meant to be a text a editor.


## REQUIREMENTS ##

  * Python >= 2.4 (http://www.python.org)
  * pyGTK >= 2.6 (http://www.pygtk.org)
  * GNU/Source Highlight >= 2.3 (http://www.gnu.org/software/src-highlite)

My Linux box with a Gnome desktop already had Python + PyGTK.  My distro uses YUM and I was able to install GNU/Source Highlight with:

```
$ su
# yum install source-highlight
```

## QUICK INSTALLATION ##
```
$ cd ~/bin
$ wget http://code2blog.googlecode.com/svn/trunk/code2blog
$ chmod +x code2blog
```

## OTHERFILES ##

I'm including three other files for anyone that would like to modify code2blog:

  * _code2blog.py_ is the same thing as code2blog, except it loads the pyGTK interface from the file _code2blog.glade_.

  * _code2blog.glade_ and _code2blog.gladep_ are the files for the Glade GUI designer (http://glade.gnome.org/).


## TODO ##

I really should add a function to pick the proper source file type when loading files.


## CREDITS ##

Lorenzo Bettini for GNU/Source Highlight.
John Finlay and the pyGTK team for pyGTK which makes this kind of thing silly easy.