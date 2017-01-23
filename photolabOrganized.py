#Tianyu Li tl1 sectionB

from Tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import tkFileDialog
import math

class Photolab(object):
##############################################    	
# initialize everything   	
##############################################
    #initialize the width and height of the window
    def __init__(self):
        self.width = 1200
        self.height = 700
   
    #initialize everything
    def initAnimation(self):
        self.timerDelay = None
        self.imageWidth = 800
        self.imageHeight = 550
        self.x = self.width/2
        self.y = self.height/2
        self.red = self.green = self.blue = 0
        self.restart = self.cut = self.help = self.instruction = False
        self.level = 10
        self.floodfill = set()
        self.redoList = []
        self.undoList = []
        self.splash = True
        self.galleryP1 = self.galleryP2 = self.gallery1 = self.gallery2 = False
        self.initAnimation2()

    #initialize everything
    def initAnimation2(self):
        self.startColor = self.helpColor = self.exitColor = "yellow"
        self.nextC = self.backC = self.lastC = "yellow"
        self.current = None
        self.galleryColor = "yellow"
        self.gallery1Text = ""
        self.pen = False
        self.red = self.green = self.blue = 0
        self.penList = []
        self.drawn = []
        self.penwidth = 0
        self.initMotion()

    #initialize motion
    def initMotion(self):
        #from 15-112 course note - eventBasedAnimationClass
        self.root.bind("<Key>", lambda event: self.onKeyPressed(event))
        self.root.bind("<Button-1>", lambda event:self.onMousePressed(event))
        self.root.bind("<Motion>", lambda event:self.onMouseMotion(event))
        self.canvas.bind("<B1-Motion>",\
        lambda event: self.leftMouseMoved(event))

    #initialize self.path
    def setPath(self):
        self.path = None

##############################################        
# user interface
##############################################
    #draw background
    def loadBackImage(self):
        #image from www.taopic.com
        self.backpath = "tpImages/photolab.jpg"
        self.backimage = Image.open(self.backpath)
        self.backimage = self.backimage.resize((self.width,self.height),\
                                               Image.ANTIALIAS)
        self.backImage = ImageTk.PhotoImage(self.backimage)
        self.canvas.create_image(self.x, self.y, image=self.backImage)
        
    #draw the splash screen
    def splashScreen(self):
        #draw background
        self.loadBackImage()
        x = self.width/2.0
        y = self.height/5.0
        self.canvas.create_text(x,y,text="PHOTO",font="comicsansme 190 bold",\
                                fill="yellow")
        y1,y2,y3 = y*2.5,y*3.5,y*4.2
        self.canvas.create_text(x,y1,text="LAB",font="comicsansme 220 bold",\
                                fill="yellow")
        text = "by Tianyu Li"
        self.canvas.create_text(x,y2,text=text,font="comicsansme 30 bold",\
                                fill="yellow")
        self.canvas.create_text(x,y3,text="Start",font="comicsansme 80 bold",\
                                fill=self.startColor)
        x1,x2 = x+self.width/2.0/2.0,x-self.width/2.0/2.0
        self.canvas.create_text(x2,y3,text="Help",font="comicsansme 80 bold",\
                                fill=self.helpColor)
        self.canvas.create_text(x1,y3,text="Exit",font="comicsansme 80 bold",\
                                fill=self.exitColor)

    #draw help screen, create texts
    def drawHelp(self):
        self.canvas.create_image(self.x, self.y, image=self.backImage)
        margin = 28
        x = self.width/2
        y = 50
        self.text1 = "In my Photo Lab, you can do interesting\
things to your photo."
        self.text2 = "First of all, you can load a photo. "
        self.text3 = "Just click the button with 'Load Image' on it."
        self.text4 = "You can also edit a specific part of the photo."
        self.text5 = "Just click 'Cut' and follow the instructions."
        self.text6 = "Then you can choose whatever filter you like."
        self.text7 = "And have fun with my Photo Lab!!!"
        self.text8 = "Want to save the funny photo?"
        self.text9 = "Click on 'Save Image' and save it in your computer."
        self.text10 = "More detailed instructions are available inside."
        self.drawHelpScreen(x,y,margin)
        self.drawOpenGallery(x,y,margin)

    #draw an opening to gallery on help screen
    def drawOpenGallery(self,x,y,margin):
        textGallery = "TAKE A LOOK AT MY "
        self.canvas.create_text(x,y+margin*14,text=textGallery,\
                                font="comicsansme 30 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*16,text="GALLERY",font="comicsansme\
                                50 bold underline",fill=self.galleryColor)
        x = self.width/2.0
        y = self.height/5.0
        y3 = y*4.2
        self.canvas.create_text(x,y3,text="Back",\
                                font="comicsansme 80 bold",fill=self.startColor)        

    #print instructions on help screen
    def drawHelpScreen(self,x,y,margin):
        self.canvas.create_text(x,y,text=self.text1,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*2,text=self.text2,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*3,text=self.text3,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*4.5,text=self.text4,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*5.5,text=self.text5,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*7,text=self.text6,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*8,text=self.text7,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*9.5,text=self.text8,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*10.5,text=self.text9,\
                                font="comicsansme 25 bold",fill="yellow")
        self.canvas.create_text(x,y+margin*12,text=self.text10,\
                                font="comicsansme 25 bold",fill="yellow")

    #draw gallery page 1, import the original image
    def drawGalleryPage1(self):
        self.drawGalleryBGFirst()
        x = self.width/4.0/2
        y = self.height/2.0/2
        width = self.width/4.0
        height = self.height/2.0
        margin = 30
        #image from http://tieba.baidu.com/p/1926579178
        self.imageOriJPath = "tpImages/original.jpg"
        self.imageOriJ = Image.open(self.imageOriJPath)
        self.resizeJ(width,height,margin)
        self.oriJ = ImageTk.PhotoImage(self.imageOriJ)
        self.canvas.create_image(x, y, image=self.oriJ)
        self.galleryW, self.galleryH = self.imageOriJ.size
        self.galleryEffect()
        self.showEffectName()

    #resize the original image
    def resizeJ(self,width,height,margin):
        oriWidth, oriHeight = self.imageOriJ.size
        newWidth = int(width-margin)
        newHeight = int(newWidth/float(oriWidth) * oriHeight)
        self.imageOriJ = self.imageOriJ.resize((newWidth, newHeight),\
                                               Image.ANTIALIAS)
        if newHeight > height-margin*2:
            newHeight = int(height-margin*2)
            newWidth = int(newHeight/float(oriHeight) * oriWidth)
        self.imageOriJ = self.imageOriJ.resize((newWidth, newHeight),\
                                               Image.ANTIALIAS)
    #draw modified images to gallery
    def galleryEffect(self):
        x = self.width/4.0/2
        y = self.height/2.0/2
        width = self.galleryW
        height = self.galleryH
        margin = 30
        self.galleryEffect2(x,y,width,height,margin)
        self.galleryEffect3(x,y,width,height,margin)

    #draw modified images to gallery
    #resize every modified image to the size of the original one
    def galleryEffect2(self,x,y,width,height,margin):
        self.imageJBW = Image.open("tpImages/sketch.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.JBW = ImageTk.PhotoImage(self.imageJBW)
        self.canvas.create_image(x+width+margin, y, image=self.JBW)
        self.imageJoilpaint = Image.open("tpImages/oilpaint.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Joilpaint = ImageTk.PhotoImage(self.imageJoilpaint)
        self.canvas.create_image(x+width*2+margin*2, y, image=self.Joilpaint)
        self.imageJblur = Image.open("tpImages/blur.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Jblur = ImageTk.PhotoImage(self.imageJblur)
        self.canvas.create_image(x+width*3+margin*3, y, image=self.Jblur)
        self.imageJgreyscale = Image.open("tpImages/greyscale.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Jgreyscale = ImageTk.PhotoImage(self.imageJgreyscale)
        self.canvas.create_image(x, y+height+margin*2, image=self.Jgreyscale)

    #draw modified images to gallery
    def galleryEffect3(self,x,y,width,height,margin):
        self.imageJmosaic = Image.open("tpImages/mosaic.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Jmosaic = ImageTk.PhotoImage(self.imageJmosaic)
        self.canvas.create_image(x+width+margin, y+height+margin*2,\
                                 image=self.Jmosaic)
        self.imageJmerge = Image.open("tpImages/merge.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Jmerge = ImageTk.PhotoImage(self.imageJmerge)
        self.canvas.create_image(x+width*2+margin*2, y+height+margin*2,\
                                 image=self.Jmerge)
        self.imageJinverting = Image.open("tpImages/inverting.jpg").resize\
                         ((width, height), Image.ANTIALIAS)
        self.Jinverting = ImageTk.PhotoImage(self.imageJinverting)
        self.canvas.create_image(x+width*3+margin*3, y+height+margin*2,\
                                 image=self.Jinverting)
        
    #draw the background of the first page of gallery
    def drawGalleryBGFirst(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="grey50")
        margin = 30
        x = self.width-(self.width-221*4-margin*4)/2
        y1 = self.height/4.0
        font = "comicsansme 20 bold"
        text1 = "Next Page"
        self.canvas.create_text(x,y1,text=text1,font=font,fill=self.nextC)
        text2 = "Go Back"
        y2 = self.height/4.0*3
        self.canvas.create_text(x,y2,text=text2,font=font,fill=self.backC)

    #draw the effect name on the left of the screen
    def showEffectName(self):
        font = "comicsansme 20 bold"
        margin = 30
        x = self.width-(self.width-221*4-margin*4)/2
        y3 = self.y
        self.canvas.create_text(x,y3,text=self.gallery1Text,font=font,\
                                fill="yellow")

    #draw the background of the first page of gallery
    def drawGalleryBGSecond(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="grey50")
        margin = 30
        x = (self.width-221*4-margin*4)/2
        y1 = self.height/4.0
        font = "comicsansme 20 bold"
        text1 = "Last Page"
        self.canvas.create_text(x,y1,text=text1,font=font,\
                                fill=self.lastC)
        text2 = "Go Back"
        y2 = self.height/4.0*3
        self.canvas.create_text(x,y2,text=text2,font=font,fill=self.backC)

    #draw the second page of the gallery
    def drawGalleryPage2(self):
        self.drawGalleryBGSecond()
        margin = 30
        x = (self.width-221*4-margin*4)+250
        y = self.y
        #image from: http://www.360doc.com/content/12/1208/19/10872297_252896830.shtml
        self.imageCity = Image.open("tpImages/city.jpg")
        oriWidth,oriHeight = self.imageCity.size
        self.imageCity = self.imageCity.resize((int(oriWidth/4.5), \
                                                int(oriHeight/4.5)), \
                                               Image.ANTIALIAS)
        self.city = ImageTk.PhotoImage(self.imageCity)
        self.canvas.create_image(x,y,image=self.city)
        width,height = self.imageCity.size
        x2 = x+width/2+250
        self.imagePolar = Image.open("tpImages/polar.jpg").resize\
                          ((400,400),Image.ANTIALIAS)
        self.polar = ImageTk.PhotoImage(self.imagePolar)
        self.canvas.create_image(x2,y,image=self.polar)
        self.showEffectName2()

    #draw the effect name on the left of the screen
    def showEffectName2(self):
        margin = 30
        x = (self.width-221*4-margin*4)/2
        y = self.y
        font = "comicsansme 20 bold"
        self.canvas.create_text(x,y,text=self.gallery1Text,font=font,\
                                fill="yellow")
        font2 = "comicsansme 30 bold"
        text = "You can add more awesomeness to your photo!!!"
        self.canvas.create_text(self.x,self.height-100,text=text,font=font2,\
                                fill="yellow")
        
    #create buttons on the screen part 1
    def createButton(self):
        self.createBackground()
        self.margin,margin,width = 65,30,140
        loadX = margin+width/2
        loadY = margin+margin
        self.canvas.create_rectangle(margin,margin,margin+width,\
                                     self.height-margin,fill="white",width=0)
        #create undo, redo buttons
        recWidth,recHeight = 400,30
        self.canvas.create_rectangle(self.x-recWidth/2,loadY-15-recHeight/2,\
                                     self.x+recWidth/2,loadY-15+recHeight/2,\
                                     fill="white",width=0)
        undo = Button(self.canvas, text="Undo",command=self.undo,width=9)
        self.canvas.create_window(self.x-self.margin*2, loadY-15,window = undo)        
        redo = Button(self.canvas, text="Redo",command=self.redo,width=9)
        self.canvas.create_window(self.x+self.margin*2, loadY-15,window = redo)
        #create help button and exit button
        help = Button(self.canvas, text="Instruction",command=self.Instruction\
                      ,width=9)
        self.canvas.create_window(self.width-100,self.height-100,window = help)        
        exit = Button(self.canvas, text="Exit",command=self.exit,width=9)
        self.canvas.create_window(self.width-100,self.height-50,window = exit)
        gallery = Button(self.canvas, text="Gallery",\
                         command=self.drawGallery,width=9)
        self.canvas.create_window(self.width-100,self.height-150,\
                                  window = gallery)
        #create more buttons
        self.createTools(margin,width,loadX,loadY)
        self.createToolsCon(margin,width,loadX,loadY)
        
    #create tools buttons
    def createTools(self,margin,width,loadX,loadY):
        restart = Button(self.canvas, text="Restart", command=self.Restart,\
                         width=9)
        self.canvas.create_window(self.x, loadY-15,window=restart)
        self.canvas.create_text(loadX, loadY, text="Tool",\
                                font="comicsansme 20 bold")
        loadPicture = Button(self.canvas, text="Upoad Image",\
                             command=self.loadImage,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*.5,\
                                  window=loadPicture)
        save = Button(self.canvas, text="Save Image", \
                      command=self.save,width=9)
        self.canvas.create_window(loadX, loadY+self.margin, window=save)
        cut = Button(self.canvas, text="Cut",command=self.cutImage,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*1.5,window=cut)
        self.canvas.create_text(loadX, loadY+self.margin*2.5, text="Filter",\
                                font="comicsansme 20 bold")
        colorPen = Button(self.canvas, text="Color Pen",command=self.color,\
                          width=9)
        self.canvas.create_window(loadX, loadY+self.margin*2, window=colorPen)
        self.createToolsCon2(margin,width,loadX,loadY)

    #create button part 2, create filter buttons
    def createToolsCon(self,margin,width,loadX,loadY):
        grey = Button(self.canvas, text="Greyscale", command=self.grey,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*6, window=grey)
        vignette = Button(self.canvas, text="Vignette",command=self.vignette,\
                          width=9)
        self.canvas.create_window(loadX, loadY+self.margin*6.5,window=vignette)
        merge = Button(self.canvas, text="Merge",command=self.merge,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*7,window=merge)
        oilpaint = Button(self.canvas, text="Oil Paint ",\
                          command=self.waterColor,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*7.5,window=oilpaint)
        colorfilter = Button(self.canvas, text="Color Filter",\
                             command=self.colorFilter,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*8,window=colorfilter)
        polar = Button(self.canvas, text="Polar",command=self.polarEffect,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*8.5,window=polar)

    #create button part 3, create filter buttons
    def createToolsCon2(self,margin,width,loadX,loadY):
        blur = Button(self.canvas, text="Blur",command=self.blur,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*4.5, window=blur)
        sketch = Button(self.canvas, text="Sketch",\
                        command=self.sketch,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*5, window=sketch)
        mirror = Button(self.canvas, text="Mirror",\
                        command=self.chooseMirror,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*5.5, window=mirror)
        invert = Button(self.canvas, text="Inverting",\
                        command=self.invert,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*3, window=invert)
        bw = Button(self.canvas, text="B/W",\
                    command=self.blackAndWhite,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*3.5, window=bw)
        mosaic = Button(self.canvas, text="Mosaic",\
                        command=self.mosaic,width=9)
        self.canvas.create_window(loadX, loadY+self.margin*4, window=mosaic)        

    #draw background
    def createBackground(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="grey80")
        
    #choose how to flip the given image
    def chooseMirror(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            margin = 150
            x = 950
            y = 50
            horFlip = Button(self.canvas, text="Horizontally Flip",\
                             command=self.mirror, width=12)
            verFlip = Button(self.canvas, text="Vertically Flip",\
                             command=self.verMirror, width=12)
            self.vermirror = self.canvas.create_window(x,y,window=horFlip)
            self.hormirror = self.canvas.create_window(x+margin,y,\
                                                       window=verFlip)
        else: self.noImage()

    #create a canvas for users to select an image to merge with the
    #original image
    def mergeCanvas(self):
        width,height = 300,120
        self.mergeroot = Toplevel()
        self.mergecanvas = Canvas(self.mergeroot, width=width, height=height)
        self.mergecanvas.pack()
        text = "please select an image to be background"
        x,y = width/2,height/3
        self.mergecanvas.create_text(x,y,text=text,font="arial 12 bold")
        browse = Button(self.mergecanvas, text="Browse",\
                        command=self.browseMergeImage)
        xb,yb = x/2,y*2
        self.mergecanvas.create_window(xb, yb, window=browse)
        confirm = Button(self.mergecanvas, text="Confirm",\
                         command=self.confirmMergeImage)
        xc,yc = x+xb,yb
        self.mergecanvas.create_window(xc, yc, window=confirm)
        self.mergecanvas.mainloop()

    #draw instructions
    def drawInstruction(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="grey80")
        x = self.x
        y = 45
        margin = 25
        self.canvas.create_text(x,y,text="INSTRUCTION",\
                                font="comicsansme 40 bold")
        text1 = "Inverting filter gives you negative photograph\
 of your image."
        self.canvas.create_text(x,y+margin*2,text=text1,\
                                font="comicsansme 20")
        text2 = "B/W filter makes your image consist of only black and white."
        self.canvas.create_text(x,y+margin*3.5,text=text2,\
                                font="comicsansme 20")
        self.drawInstruction2(x,y,margin)
        
    #draw instructions part two
    def drawInstruction2(self,x,y,margin):
        text3 = "Mosaic filter adds mosaic effect to your image."
        self.canvas.create_text(x,y+margin*5,text=text3,\
                                font="comicsansme 20")
        text5 = "Blur filter blurs your image."
        self.canvas.create_text(x,y+margin*7.5,text=text5,\
                                font="comicsansme 20")
        text6 = "Sketch filter gives you the sketch version of your image."
        self.canvas.create_text(x,y+margin*9,text=text6,\
                                font="comicsansme 20")
        self.drawInstruction3(x,y,margin)

    #draw instructions part three
    def drawInstruction3(self,x,y,margin):
        text7 = "Mirror filter flips your image.\
 By clicking the buttons on up right conor,"
        text8 = "you can choose to horizantally or vertically flip your image."
        self.canvas.create_text(x,y+margin*10.5,text=text7,\
                                font="comicsansme 20")
        self.canvas.create_text(x,y+margin*11.5,text=text8,\
                                font="comicsansme 20")
        text9 = "Greyscale filter converts your image to black-and-white image."
        self.canvas.create_text(x,y+margin*13,text=text9,\
                                font="comicsansme 20")        
        text10 = "Vignette filter adds vignette effect to your image."
        text11 = "and makes your image focus to be in the center."
        self.canvas.create_text(x,y+margin*14.5,text=text10,\
                                font="comicsansme 20")
        self.canvas.create_text(x,y+margin*15.5,text=text11,\
                                font="comicsansme 20")
        self.drawInstruction4(x,y,margin)

    #draw instructions part four
    def drawInstruction4(self,x,y,margin):
        text12 = "Merge filter merges your image and another selected image."
        self.canvas.create_text(x,y+margin*17,text=text12,\
                                font="comicsansme 20")
        text13 = "Oil Paint filter makes your image look like an oil painting."
        self.canvas.create_text(x,y+margin*18.5,text=text13,\
                                font="comicsansme 20")
        text14 = "Color filter filters one of red, green and blue out \
of your image."
        text15 = "You can choose a color to be filtered out on the \
up right conor."
        self.canvas.create_text(x,y+margin*20,text=text14,\
                                font="comicsansme 20")
        self.canvas.create_text(x,y+margin*21,text=text15,\
                                font="comicsansme 20")
        self.drawInstruction5(x,y,margin)

    #draw instructions part five
    def drawInstruction5(self,x,y,margin):
        text16 = "Polar filter makes a polar using you image."
        text17 = "You can have a polor of your own using polar filter!"
        self.canvas.create_text(x,y+margin*22.5,text=text16,\
                                font="comicsansme 20")
        self.canvas.create_text(x,y+margin*23.5,text=text17,\
                                font="comicsansme 20")
        back = Button(self.canvas, text="Go Back", command=self.goBack)
        x = self.width-100
        y = self.height-100
        self.canvas.create_window(x, y, window=back)

##############################################
# tools
##############################################
    #open gallery from the main window
    def drawGallery(self):
        self.gallery1 = True
        self.redrawAll()
        
    #show users instructions
    def Instruction(self):
        self.instruction = True
        self.redrawAll()

    #close the instruction page
    def goBack(self):
        self.instruction = False
        self.redrawAll()
        
    #exit Photo Lab
    def exit(self):
        self.root.destroy()
        
    #undo the modifications in order
    def undo(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.cut = False
            #if the undoList has more than one element, draw its last element on
            #canvas and append the element to redoList
            if len(self.undoList) > 1:
                self.newImage = ImageTk.PhotoImage(self.undoList[-2])
                self.current = self.canvas.create_image(self.x, self.y,\
                                                        image=self.newImage)
                self.image = self.undoList[-2]
                (self.imawidth, self.imaheight) = self.image.size
                self.redoList.append(self.undoList[-1])
                self.undoList.pop()
        else: self.noImage()

    #redo the modifications in order
    def redo(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.cut = False
            #if the redoList has an element, draw its last element on
            #canvas and append the element to undoList
            if len(self.redoList) > 0:
                self.newImage = ImageTk.PhotoImage(self.redoList[-1])
                self.current = self.canvas.create_image(self.x, self.y,\
                                                        image=self.newImage)
                self.image = self.redoList[-1]
                (self.imawidth, self.imaheight) = self.image.size
                self.undoList.append(self.redoList[-1])
                self.redoList.pop()
        else: self.noImage()
    
    #check if users have loaded an image
    def checkImage(self):
        if self.path != None and self.path != "": return True
        return False
    
    #cut the image
    #draw instructions for cutting image
    def cutImage(self):
        if self.checkImage() or self.current != None:
            self.cut = True
            self.redrawCanvas()
            text = "Press 'Up', 'Down','Left', 'Right'to move the rectangle. \n\
Press 'u', 'd', 'l', 'r' to change the size of the rectangle. \n\
Press 'c' to cut the image."
            x = self.width-200
            y = (self.y-self.imaheight/2)/2
            self.cuttext = self.canvas.create_text(x,y,text=text,\
                                                   font="comicsansme 10 bold")
            self.cutwidth = self.imawidth/2
            self.cutheight = self.imaheight/2
            self.centerx = self.x
            self.centery = self.y
            self.drawCutRectangle()
        else:
            self.noImage()

    #draw the rectangle
    def drawCutRectangle(self):
        self.x0 = self.centerx-self.cutwidth/2
        self.y0 = self.centery-self.cutheight/2
        self.x1 = self.centerx+self.cutwidth/2
        self.y1 = self.centery+self.cutheight/2
        try:self.canvas.delete(self.cutrectangle)
        except:pass
        self.cutrectangle = self.canvas.create_rectangle\
                            (self.x0,self.y0,self.x1,self.y1,width=4)

    #redraw the rectangle with new size
    def drawCutRectangleBigger(self):
        self.cutrectangle = self.canvas.create_rectangle\
                    (self.x0,self.y0,self.x1,self.y1,width=4)

    #delete the orevious rectangle, and draw a new one with new size
    def deleteBiggerRectangle(self):
        self.canvas.delete(self.cutrectangle)
        self.drawCutRectangleBigger()

    #confirm to cut the image
    def cutRectangle(self):
        self.getRGB()
        #create a new image
        newPixels = Image.new("RGB",(self.x1-self.x0,self.y1-self.y0),\
                              "white").load()
        x0 = self.x0-(self.x-(self.imawidth/2))
        y0 = self.y0-(self.y-(self.imaheight/2))
        for i in xrange(self.x1-self.x0):
            for j in xrange(self.y1-self.y0):
                newPixels[i, j] = self.pixels[x0+i, y0+j]
        #change the size of the image to the size cut rectangle
        self.image = Image.new("RGB",(self.x1-self.x0,self.y1-self.y0),"white")
        self.pixels = self.image.load()
        #change the pixels of the image to the pixels of the cut rectangle
        #and create a new image
        for i in xrange(self.x1-self.x0):
            for j in xrange(self.y1-self.y0):
                self.pixels[i, j] = newPixels[i, j]
        (self.imawidth, self.imaheight) = self.image.size
        self.redrawCanvas()
        self.undoList.append(self.image)
        self.newImage = ImageTk.PhotoImage(self.image)
        self.current = self.canvas.create_image(self.x, self.y,\
                                                image=self.newImage)
        self.cut = False
        
    #select an image to merge with the original image
    def browseMergeImage(self):
        #open file dialog for users to select an image to merge with the
        #original image
        self.mergepath = tkFileDialog.askopenfilename()
        try:
            #if users did load an image, get its pixels
            self.mergeimage = Image.open(self.mergepath)
            self.mergeimage = self.mergeimage.resize((self.imawidth,\
                                    self.imaheight),Image.ANTIALIAS)
            self.mergeimage = self.mergeimage.convert("RGB")
            self.pixelsmerge = self.mergeimage.load()
        except: pass

    #close the image selection window
    def confirmMergeImage(self):
        #close the merge image canvas
        self.mergeroot.destroy()
        #resize the image
        self.smallimage = self.mergeimage.resize((int(self.imawidth/3.0),\
                          int(self.imaheight/3.0)),Image.ANTIALIAS)
        self.smallImage = ImageTk.PhotoImage(self.smallimage)
        x = self.width-150
        y = 100
        margin = int(self.imaheight/3.0/2.0)+50
        #draw the image to the canvas
        self.imageMer = self.canvas.create_image(x,y,image=self.smallImage)
        startmerge = Button(self.canvas, text="Start", command=self.startMerge)
        self.startMer = self.canvas.create_window(x,y+margin,\
                                                    window=startmerge)
       
    #redraw the canvas, delete the buttons and scales
    def redrawCanvas(self, mode="normal"):
        self.pen = False
        if mode == "normal": self.canvas.delete(self.current)
        else:
            self.canvas.delete(ALL)
            self.createButton()
        self.newImage = ImageTk.PhotoImage(self.image)
        self.current = self.canvas.create_image(self.x, self.y,\
                                                image=self.newImage)

    #get contours of the objects in the given image
    #Based somewhat loosely on:
    #http://qinxuye.me/article/implement-sketch-and-pencil-with-pil/
    def getContour(self, mode):
        #turn the image to greyscale
        self.grey()
        self.getRGB()
        result = 0
        #get the total number of RGB
        for x in xrange(self.imawidth):
            for y in xrange(self.imaheight):
                (r,g,b) = self.pixels[x,y]
                result += r
        #get the average RGB
        average = result/float(self.imawidth*self.imaheight)
        #max is bigger if the mode is shadow
        if mode == "shadow":max = average/5.0
        if mode == "sketch":max = average/10.0
        for x in xrange(self.imawidth):
            for y in xrange(self.imaheight):
                if x+1<self.imawidth and y+1<self.imaheight:
                    (r,g,b) = self.pixels[x,y]
                    (r2,b2,g2) = self.pixels[x+1,y+1]
                    #change the contour to black
                    #if the difference is bigger than max, change the pixel
                    #to black
                    if abs(r-r2)>max:
                        self.pixels[x,y] = (0,0,0)
                    else:
                        self.pixels[x,y] = (255,255,255)

    #load target image and make it appear on the window in suitable size
    def loadImage(self):
        #check if users select an image
        try:
            if self.restart == False:
                self.path = tkFileDialog.askopenfilename()
            self.image = Image.open(self.path)
            (self.imawidth, self.imaheight) = self.image.size
            #ajust the width and height of the image
            self.loadResize()
            #draw the image on the window
            (self.imawidth, self.imaheight) = self.image.size
            self.oriImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.oriImage)
            self.cut = False
            #reser the undo and redo list
            self.undoList = []
            self.redoList = []
            self.undoList.append(self.image)
            self.redrawCanvas("abnormal")
            self.getRGBcon()
        except:
            if self.current == None: self.noImage()
            else: pass

    #ajust the width and height of the image
    def loadResize(self):
        #resize the given image
        if self.imawidth>self.imageWidth:
            newWidth = self.imageWidth
            newHeight = int((float(newWidth)/self.imawidth)*self.imaheight)
            self.image = self.image.resize((newWidth, newHeight),\
                                            Image.ANTIALIAS)
            (self.imawidth, self.imaheight) = self.image.size 
        if self.imaheight>self.imageHeight:
            newHeight = self.imageHeight
            newWidth = int((float(newHeight)/self.imaheight)*self.imawidth)
            self.image = self.image.resize((newWidth, newHeight),\
                                            Image.ANTIALIAS)

    #tell users if no image is given
    def noImage(self):
        text = "You need to load an image."
        self.canvas.create_text(self.x,self.y,text=text,\
                                font="comicsansme 20 bold")

    #save the modified image
    def save(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            try:
                filename = tkFileDialog.asksaveasfilename()
                self.image.save(filename,"PNG")
            except: pass
        else: self.noImage()

    #restart editing the photo
    def Restart(self):
        if self.checkImage() or self.current != None:
            self.canvas.delete(ALL)
            self.initAnimation()
            self.splash = False
            self.restart = True
            self.createButton()
            self.loadImage()
            self.restart = False
        else:self.noImage()
            
    #get the RGB of every pixel of the image
    def getRGB(self):
        self.image = self.image.convert("RGB")
        self.pixels = self.image.load()

    #get the RGB of every pixel of the image
    def getRGBcon(self):
        self.image = self.image.convert("RGB")
        self.pixelsTwo = self.image.load()        

    #create buttons for users to choose which color filter to choose
    def colorFilter(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            red = Button(self.canvas, text="red",\
                         command=self.colorFilterChosenR)
            self.rfilter = self.canvas.create_window(1100, 50, window = red)
            green = Button(self.canvas, text="green",\
                           command=self.colorFilterChosenG)
            self.gfilter = self.canvas.create_window(1100, 100, window = green)
            blue = Button(self.canvas, text="blue",\
                          command=self.colorFilterChosenB)
            self.bfilter = self.canvas.create_window(1100, 150, window = blue)
        else: self.noImage()

    #red filter
    def colorFilterChosenR(self):
        self.colorFilterChosen("red")

    #green filter
    def colorFilterChosenG(self):
        self.colorFilterChosen("green")

    #blue filter
    def colorFilterChosenB(self):
        self.colorFilterChosen("blue")

    #compute the distance from the pixel to center of the image
    def computeDisToEdge(self, x, y):
        width = abs(self.imawidth/2-x)
        height = abs(self.imaheight/2-y)
        self.distance = (width**2 + height**2)**0.5

    #check the place of the image
    def getImagePlace(self):
        height = (self.height-self.imaheight)/2.0
        width = (self.width-self.imawidth)/2.0
        self.minvalidH = height
        self.maxvalidH = self.height-height
        self.minvalidW = width
        self.maxvalidW = self.width-width

    #make the users draw only on the image
    def isValid(self, i):
        if self.penList[i][0] < self.minvalidW or self.penList[i][0]>\
           self.maxvalidW or self.penList[i][1] < self.minvalidH or\
           self.penList[i][1] > self.maxvalidH:
            return False
        if i>0:
            if self.penList[i-1][0] < self.minvalidW or self.penList[i-1][0]>\
               self.maxvalidW or self.penList[i-1][1] < self.minvalidH or\
               self.penList[i-1][1] > self.maxvalidH:
                return False
        return True

    #set the pen to be able to draw on canvas
    def Pen(self):
        self.pen = True

    #delete the drawing scales and rectangle
    def done(self):
        self.pen = False
        self.redrawCanvas("abnormal")

    #create the color slider
    def colorPressed(self):
        self.redrawCanvas()
        width, height, x0, y0, max = 50, 100, 1100, 30, 255
        self.rectangle = self.canvas.create_rectangle(x0,y0,x0+width,\
                         y0+height,width=0,fill="#%02x%02x%02x" %\
                         (self.red,self.green,self.blue))
        buttonX, buttonY, scaleY = 1160, 150, 40
        margin, marginY = 120, 55
        width = 220
        height = 260
        xR = 1085
        yR = 140
        self.canvas.create_rectangle(xR-width/2,yR-height/2,xR+width/2,\
                                     yR+height/2,fill="white",width=0)
        self.Red = DoubleVar()
        self.Blue = DoubleVar()
        self.Green = DoubleVar()
        self.scaleColorRed = Scale(self.canvas,from_=0,to=max,resolution=\
                                   1,variable=self.Red,orient=HORIZONTAL,\
                                   label="Red",command=self.redScale)
        self.scaleColorGreen = Scale(self.canvas,from_=0,to=max,resolution\
                                     =1,variable=self.Green,orient=HORIZONTAL\
                                     ,label="Green",command=self.greenScale)
        self.scaleColorBlue = Scale(self.canvas,from_=0,to=max,resolution=\
                                    1,variable=self.Blue,orient=HORIZONTAL,\
                                    label="Blue",command=self.blueScale) 
        self.drawScale(buttonX,margin,scaleY,marginY,buttonY)

    #create scales for users to choose color
    def drawScale(self,buttonX,margin,scaleY,marginY,buttonY):         
        self.canvas.create_window(buttonX-margin,scaleY,\
                                  window=self.scaleColorRed)
        self.canvas.create_window(buttonX-margin,scaleY+marginY,\
                                  window=self.scaleColorGreen)
        self.canvas.create_window(buttonX-margin,scaleY+marginY*2,\
                                  window=self.scaleColorBlue)
        getcolor = Button(self.canvas,text="Get Color",\
                          command = self.Pen,width=7)
        self.canvas.create_window(buttonX-15, buttonY, window=getcolor)
        done = Button(self.canvas,text="Done",\
                          command = self.done, width=7)
        self.canvas.create_window(buttonX-15, buttonY+25, window=done)
        penwidth = IntVar()
        width = Scale(self.canvas,from_=1,to=10,\
                      variable=penwidth,orient=HORIZONTAL,command=self.penW,\
                      label="width",length=150)
        self.canvas.create_window(buttonX-.5*margin,scaleY+marginY*3.5,\
                                  window=width)

##############################################
# filters
##############################################
    #taken with minor changes from 15-112 mini lecture
    #http://www.cs.cmu.edu/~112/piazza.html
    #add polar effect to the given image
    def polarEffect(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            size = min(self.imageWidth, self.imageHeight)
            polarIma = Image.new("RGB", (size, size))
            polarPixels = polarIma.load()
            #get pixels as a 2D list of RGB values
            self.getRGB()
            maxAngle = math.pi*2
            maxR = (size**2+size**2)**0.5/2
            for x in xrange(size):
                for y in xrange(size):
                    #get polar x and y coordinates
                    polX = x-size/2
                    polY = size/2-y
                    if polX == 0:
                        if polY<0: angle = 3*math.pi/2
                        else: angle = math.pi/2
                    else:
                        angle = math.atan(float(polY)/polX)
                    if (polX < 0): angle += math.pi
                    if (angle < 0): angle = 2*math.pi + angle
                    radius = (polY**2 + polX**2)**0.5
                    #calculate rectangular coordinates
                    rectX = int(round((self.imawidth - 1) *\
                                      abs(angle/maxAngle)))
                    rectY = int(round((self.imaheight - 1) * (1 - radius/maxR)))
                    polarPixels[x, y] = self.pixels[rectX, rectY]
            self.image = Image.new("RGB", (size, size))
            self.pixels = self.image.load()
            for i in xrange(size):
                for j in xrange(size):
                    self.pixels[i, j] = polarPixels[i, j]
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
            self.imawidth = self.imaheight = size
        else: self.noImage()
                       
    #add vignette effect to the given image
    def vignette(self):
        if self.checkImage() or self.current != None:
            self.getRGB()
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    self.changeVignette(x,y)
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #change the RGB of individual pixel
    def changeVignette(self, x, y):
        factor = 0.5
        dis = min(self.imawidth/2, self.imaheight/2)
        radius = dis/2
        (r, g, b) = self.pixels[x, y]
        #compute the distance from the pixel to the edge of the image
        self.computeDisToEdge(x, y)
        if self.distance>radius:
            diff = self.distance-radius
            newr = int(r-diff*factor-diff*factor)
            newg = int(g-diff*factor-diff*factor)
            newb = int(b-diff*factor-diff*factor)
            if newr<0: newr=0
            if newg<0: newg=0
            if newb<0: newb=0
            self.pixels[x, y] = (newr, newg, newb)        
        
    #loop through the image and filter the color that is chosen
    def colorFilterChosen(self, color):
        self.getRGB()
        for x in xrange(self.imawidth):
            for y in xrange(self.imaheight):
                (r, g, b) = self.pixels[x, y]
                if color == "red": self.redFilter(x,y,g,b)
                if color == "green": self.greenFilter(x,y,r,b)
                if color == "blue": self.blueFilter(x,y,r,g)
        #delete the buttons
        self.canvas.delete(self.rfilter)
        self.canvas.delete(self.gfilter)
        self.canvas.delete(self.bfilter)
        self.undoList.append(self.image)
        self.newImage = ImageTk.PhotoImage(self.image)
        self.current = self.canvas.create_image(self.x, self.y,\
                                                image=self.newImage)

    #change pixel's red to 0, filter red
    def redFilter(self, x, y, g, b):
        self.pixels[x, y] = (0, g, b)

    #change pixel's green to 0, filter green
    def greenFilter(self, x, y, r, b):
        self.pixels[x, y] = (r, 0, b)

    #change pixel's blue to 0, filter blue
    def blueFilter(self, x, y, r, g):
        self.pixels[x, y] = (r, g, 0)
                
    #initialize
    def initFill(self):
        self.redrawCanvas()
        self.drawShadow()
        self.undoList.pop()
        self.undoList.pop()
        self.getRGB()        

    #looping through the image and find similar color in it
    def waterColor(self):
        if self.checkImage() or self.current != None:
            self.initFill()
            step = 30
            for self.i in xrange(0,self.imawidth,step):
                for self.j in xrange(0,self.imaheight,step):
                    #avoiding out of index error
                    self.endx = min(self.imawidth, self.i+step)
                    self.endy = min(self.imaheight, self.j+step)
                    for x in xrange(self.i,self.endx):
                        for y in xrange(self.j,self.endy):
                            if (x,y) not in self.floodfill:
                                self.fill(x,y)
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()
        self.floodfill = set()

    #change the RGB of individual pixel
    def fill(self, x, y):
        r = g = b = 0
        #set colorPixels to an empty list
        self.colorPixels = []                    
        self.colorFill(x,y)
        for i in xrange(len(self.colorPixels)):
            (red,green,blue) = self.pixels\
                               [self.colorPixels[i][0],self.colorPixels[i][1]]
            r += red
            g += green
            b += blue
        #reset RGB
        newr = r/len(self.colorPixels)
        newg = g/len(self.colorPixels)
        newb = b/len(self.colorPixels)
        for i in xrange(len(self.colorPixels)):
            self.pixels[self.colorPixels[i][0],self.colorPixels[i][1]]\
                                                    = (newr,newg,newb)        

    #check adjacent similar color
    #based very loosely on 15112 floodFill
    def colorFill(self,x,y):
        if (x,y) not in self.floodfill:
            self.floodfill.add((x,y))
            self.colorPixels.append((x,y))
            threshold = t = 10
            (r,g,b) = self.pixels[x,y]
            #recursively call colorFill method
            if x+1<self.endx:
                (r1,g1,b1) = self.pixels[x+1,y]
                if abs(r-r1)<t and abs(g-g1)<t and abs(b-b1)<t:
                    if (x+1,y) not in self.floodfill:
                        return self.colorFill(x+1,y)
            if x-1>self.i:
                (r2,g2,b2) = self.pixels[x-1,y]
                if abs(r-r2)<t and abs(g-g2)<t and abs(b-b2)<t:
                    if (x-1,y) not in self.floodfill:
                        return self.colorFill(x-1,y)
            if y+1<self.endy:
                (r3,g3,b3) = self.pixels[x,y+1]
                if abs(r-r3)<t and abs(g-g3)<t and abs(b-b3)<t:
                    if (x,y+1) not in self.floodfill:
                        return self.colorFill(x,y+1)
            if y-1>self.j:
                (r4,g4,b4) = self.pixels[x,y-1]
                if abs(r-r4)<t and abs(g-g4)<t and abs(b-b4)<t:
                    if (x,y-1) not in self.floodfill:
                        return self.colorFill(x,y-1)
        return
                    
    #react to merge pressed
    def merge(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.mergeCanvas()
        else: self.noImage()

    #merge two images
    def startMerge(self):
        self.blackAndWhiteMode("merge")
        self.canvas.delete(self.startMer)
        self.canvas.delete(self.imageMer)

    #change the RGB of the original image
    def mergeOtherImage(self,x,y):
        (newr,newg,newb) = self.pixelsmerge[x,y]
        self.pixels[x,y] = (newr,newg,newb)
        
    #turn the given image to sketch
    def sketch(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.getContour("sketch")
            self.undoList.pop()
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()
        
    #draw contour in the original image
    def drawShadow(self):
        if self.checkImage() or self.current != None:
            self.getRGBcon()
            self.getContour("shadow")
            self.getRGB()
            #draw contour
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    (red, green, blue) = self.pixels[x, y]
                    if red == 0:
                        self.pixelsTwo[x,y] = (0,0,0)
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    self.pixels[x, y] = self.pixelsTwo[x,y]
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #make the given image consists of only black, white and grey
    def grey(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.getRGB()
            #make the RGB of the pixel to the average of the original RGB
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    (r,g,b) = self.pixels[x,y]
                    newr = newg = newb = int((r+g+b)/3.0)
                    self.pixels[x,y] = (newr, newg, newb)
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #vertically flip the given image
    def verMirror(self):
        self.getRGB()
        newPixels = Image.new("RGB",(self.imawidth,self.imaheight),\
                              "white").load()
        for y in xrange(self.imaheight): 
            for x in xrange(self.imawidth):
                newPixels[x,y] = self.pixels[x,self.imaheight-y-1]
        for i in xrange(self.imawidth):
            for j in xrange(self.imaheight):
                self.pixels[i,j]=newPixels[i,j]
        self.undoList.append(self.image)
        self.newImage = ImageTk.PhotoImage(self.image)
        self.current = self.canvas.create_image(self.x, self.y,\
                                                image=self.newImage)
        self.canvas.delete(self.vermirror)
        self.canvas.delete(self.hormirror)

    #horrizontally flip the given image
    def mirror(self):
        self.getRGB()
        newPixels = Image.new("RGB",(self.imawidth,self.imaheight),\
                              "white").load()
        for y in xrange(self.imaheight): 
            for x in xrange(self.imawidth):
                newPixels[x,y] = self.pixels[self.imawidth-x-1,y]
        for i in xrange(self.imawidth):
            for j in xrange(self.imaheight):
                self.pixels[i,j]=newPixels[i,j]
        self.undoList.append(self.image)
        self.newImage = ImageTk.PhotoImage(self.image)
        self.current = self.canvas.create_image(self.x, self.y,\
                                                image=self.newImage)
        self.canvas.delete(self.vermirror)
        self.canvas.delete(self.hormirror)

    #make blur effect on the given image
    #taken with minor changes from 15-112 mini lecture
    #http://www.cs.cmu.edu/~112/piazza.html
    def blur(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.getRGB()
            r = 3
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    self.pixels[x, y] = self.getAverageColor(x,y,r)
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #get average RGB of the given spot
    #taken with minor changes from 15-112 mini lecture
    def getAverageColor(self,x,y,r):
        count = 0
        rTotal,gTotal,bTotal = 0,0,0
        for i in xrange(x-r, x+r):
            for j in xrange(y-r, y+r):
                if i>=0 and i<self.imawidth and j>=0 and j<self.imaheight:
                    (red, green, blue) = self.pixels[i, j]
                    rTotal += red
                    gTotal += green
                    bTotal += blue
                    count = count +1
        newr = int(rTotal/float(count))
        newg = int(gTotal/float(count))
        newb = int(bTotal/float(count))
        return (newr, newg, newb)

    #invert the color of the image
    #draw negative image
    def invert(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.getRGB()
            for x in xrange(self.imawidth):
                for y in xrange(self.imaheight):
                    self.inverter(x,y)
            #draw the modified image to the window
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #taken with minor changes from 15-112 mini lecture
    #http://www.cs.cmu.edu/~112/piazza.html
    def inverter(self,x,y):
        max = 255
        (self.r, self.g, self.b) = self.pixels[x, y]
        newr = max - self.r
        newg = max - self.g
        newb = max - self.b
        self.pixels[x, y] = (newr, newg, newb)
                
    #make the image filled only with black or white
    def blackAndWhiteMode(self,mode):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            result = 0
            self.getRGB()
            #compute the total value of RGB
            for i in xrange(self.imawidth):
                for j in xrange(self.imaheight):
                    (self.r, self.g, self.b) = self.pixels[i, j]
                    result += self.r+self.g+self.b
            #get average value of RGB
            minVal = float(result)/(self.imawidth*self.imaheight*3)
            self.bAndW(mode,minVal)
            #draw the modified image to the window
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()
        
    #modify an image based on the given mode
    def bAndW(self,mode,minVal):
        for x in xrange(self.imawidth):
            for y in xrange(self.imaheight):
                (self.r, self.g, self.b) = self.pixels[x, y]
                if (self.r+self.g+self.b)/3.0 < minVal:
                    if mode == "black":
                        self.black(x,y)
                    if mode == "merge":
                        self.mergeOtherImage(x,y)
                else:
                    self.white(x,y)
                        
    #make the image consists with only black and with
    def blackAndWhite(self):
        self.blackAndWhiteMode('black')

    #make target pixels black
    def black(self, x, y):
        newr = newg = newb = 0
        self.pixels[x, y] = (newr, newg, newb)

    #make target pixels white
    def white(self, x, y):
        newr = newg = newb = 255
        self.pixels[x, y] = (newr, newg, newb)

    #make mosaic
    def mosaic(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.getRGB()
            for x in xrange(0,self.imawidth+self.level,self.level):
                for y in xrange(0,self.imaheight+self.level,self.level):
                    #get the average RGB of a part of the picture
                    self.getAverage(x,y)
            self.undoList.append(self.image)
            self.newImage = ImageTk.PhotoImage(self.image)
            self.current = self.canvas.create_image(self.x, self.y,\
                                                    image=self.newImage)
        else: self.noImage()

    #get the average RGB of a part of the picture
    def getAverage(self,x,y):
        resultr = resultg = resultb = 0
        highX = min(self.imawidth,x+self.level)
        highY = min(self.imaheight,y+self.level)
        if highX != x and highY != y:
            area = (highX-x)*(highY-y)
        else:
            area = self.level**2
        for i in xrange(x,highX):
            for j in xrange(y,highY):
                (self.r, self.g, self.b) = self.pixels[i, j]
                resultr += self.r
                resultg += self.g
                resultb += self.b
        #reset the RGB of a pixel to the average RGB of the whole part
        newr = int(resultr/float(area))
        newg = int(resultg/float(area))
        newb = int(resultb/float(area))
        for hor in xrange(x,highX):
            for ver in xrange(y,highY):                    
                self.pixels[hor, ver] = (newr, newg, newb)

    #show users the color selecting screen
    def color(self):
        if self.checkImage() or self.current != None:
            self.redrawCanvas()
            self.colorPressed()
        else: self.noImage()

    #redraw the rectangle that represents the current color
    def colorRectangle(self):
        width, height, x0, y0, = 50, 100, 1120, 30
        self.rectangle = self.canvas.create_rectangle(x0,y0,x0+width,y0+height,\
            width=0,fill="#%02x%02x%02x" % (self.red,self.green,self.blue))        

    #get the current red portion
    def redScale(self, Red):
        self.red = float(Red)
        self.canvas.delete(self.rectangle)
        self.colorRectangle()
            
    #get the current green portion
    def greenScale(self, Green):
        self.green = float(Green)
        self.canvas.delete(self.rectangle)
        self.colorRectangle()
            
    #get the current blue portion
    def blueScale(self, Blue):
        self.blue = float(Blue)
        self.canvas.delete(self.rectangle)
        self.colorRectangle()

    #set width of the pen
    def penW(self, width):
        self.penwidth = width

    #draw line in regarding of where the mouse moves to
    def drawLine(self):
        self.getImagePlace()
        self.getRGB()
        for i in xrange(len(self.penList)):
            x = self.penList[i][0]
            y = self.penList[i][1]
            x1 = self.penList[i-1][0]
            y1 = self.penList[i-1][1]
            color = "#%02x%02x%02x"% (self.red,self.green,self.blue)
            width = self.penwidth
            if i == 0:
                if (x, y) not in self.drawn and self.isValid(i):
                    self.drawn.append((x, y))
                    self.canvas.create_line(x, y, x, y,fill = color,width=width)
            else:
                if (x1,y1,x,y) not in self.drawn and self.isValid(i)\
                   and abs(x-x1)<30 and abs(y-y1)<30:
                    self.drawn.append((x1,y1,x,y))
                    self.canvas.create_line(x1,y1,x,y,fill = color,width=width)

##############################################
# event-based
##############################################
    #change the size of the cut rectangle
    def onKeyPressed(self,event):
        keysym = ["Down","Up","Right","Left","u","d","l","r"]
        if event.keysym in keysym: self.changeRectangleSize(event)
        if self.cut == True and event.keysym == "c":
            self.canvas.delete(self.cuttext)
            self.canvas.delete(self.cutrectangle)
            self.cutRectangle()

    #change the size of the cut rectangle
    def changeRectangleSize(self,event):
        if self.cut == True:
            if event.keysym == "Down":self.y1 += 5
            elif event.keysym == "Up":self.y0 += 5
            elif event.keysym == "Right":self.x1 += 5
            elif event.keysym == "Left":self.x0 += 5
            self.moveRectangle(event)
            self.checkValid()
            self.deleteBiggerRectangle()
        
    #move the cut rectangle
    def moveRectangle(self,event):
        if event.keysym == "u":
            if self.y0 > self.y-self.imaheight/2:
                self.y1 -= 5
                self.y0 -= 5
        elif event.keysym == "d":
            if self.y1 < self.y+self.imaheight/2:
                self.y1 += 5
                self.y0 += 5
        elif event.keysym == "l":
            if self.x0 > self.x-self.imawidth/2:
                self.x1 -= 5
                self.x0 -= 5
        elif event.keysym == "r":
            if self.x1 < self.x+self.imawidth/2:
                self.x1 += 5
                self.x0 += 5
        self.checkValid()
        self.deleteBiggerRectangle()

    #check if the cut rectangle is within the image
    def checkValid(self):
        if self.y0 < self.y-self.imaheight/2:
            self.y0 = self.y-self.imaheight/2
        if self.y1 > self.y+self.imaheight/2:
            self.y1 = self.y+self.imaheight/2
        if self.x0 < self.x-self.imawidth/2:
            self.x0 = self.x-self.imawidth/2
        if self.x1 > self.x+self.imawidth/2:
            self.x1 = self.x+self.imawidth/2
            
    #react to mouse motion event
    def onMouseMotion(self, event):
        x3 = self.width/2.0-130
        y2 = self.height/5.0*4.2-120
        width = 260
        height = 60
        x,y = event.x,event.y
        textX = self.width/2.0
        textY = self.height/5.0
        x1 = textX+self.width/2.0/2.0
        x2 = textX-self.width/2.0/2.0
        if self.galleryP1 == True or self.galleryP2 == True or\
           self.gallery1 == True or self.gallery2 == True:
            self.MouseMotionGallery(x,y)
        elif self.splash == True:
            self.splashMotion(x,y,textX,textY,x1,x2)
        elif self.help == True:
            self.helpMotion(x,y,x3,y2,width,height,textX,textY)

    #react to mouse motion made in help screen
    def helpMotion(self,x,y,x3,y2,width,height,textX,textY):
        if (x>x3 and x<x3+width) and (y>y2 and y<y2+height):
            self.galleryColor = "red"
            self.startColor = "yellow"
        elif (x>=textX-120 and x<=textX+120) and\
            (y>=textY*3.8 and y<=textY*4.6):
            self.startColor = "red"
            self.galleryColor = "yellow"
        else: self.startColor = self.galleryColor = "yellow"
        self.redrawAll()

    #react to mouse motion made in splash screen
    def splashMotion(self,x,y,textX,textY,x1,x2):
        if (x>=textX-120 and x<=textX+120) and\
            (y>=textY*3.8 and y<=textY*4.6):
            self.startColor = "red"
            self.exitColor = self.helpColor = "yellow"
        elif (x>=x1-120 and x<=x1+120) and (y>=textY*3.8 and y<=textY*4.6):
            self.exitColor = "red"
            self.startColor = self.helpColor = "yellow"
        elif (x>=x2-120 and x<=x2+120) and (y>=textY*3.8 and y<=textY*4.6):
            self.helpColor = "red"
            self.exitColor = self.startColor = "yellow"
        else:
            self.startColor = self.helpColor = self.exitColor = "yellow"
        self.redrawAll()

    #react to mouse motion made in gallery
    def MouseMotionGallery(self,x,y):
        margin = 30
        width = 60
        height = 15
        y1 = self.height/4.0
        y2 = self.height/4.0*3
        if self.galleryP1 == True or self.gallery1 == True:
            x0 = self.width-(self.width-221*4-margin*4)/2
            xtext = self.width/4.0/2
            ytext = self.height/2.0/2
            self.mouseMotionG1(x,y,xtext,ytext,margin)
            if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
                self.nextC = "red"
                self.backC = "yellow"
            elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
                self.nextC = "yellow"
                self.backC = "red"
            else: self.nextC = self.backC = "yellow"
        if self.galleryP2 == True or self.gallery2 == True:
            x0 = (self.width-221*4-margin*4)/2
            widthImage,heightImage = self.imageCity.size
            x1 = (self.width-221*4-margin*4)+250
            x2 = x1+widthImage/2+250
            y3 = self.y
            self.mouseMotionG2(x,y,width,height,x0,x1,x2,\
                               widthImage,heightImage,y1,y2,y3)
        self.redrawAll()

    #mouse motion made in gallery page 2
    def mouseMotionG2(self,x,y,width,height,x0,x1,x2,widthImage,\
                      heightImage,y1,y2,y3):
        if x>x1-widthImage/2 and x<x1+widthImage/2\
            and y>y3-heightImage/2 and y<y3+heightImage/2:
            self.gallery1Text = "Original Image"
        elif x>x2-200 and x<x2+200 and y>y3-200 and y<y3+200:
            self.gallery1Text = "Polar Effect"
        else: self.gallery1Text = ""
        if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
            self.lastC = "red"
            self.backC = "yellow"
        elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
            self.lastC = "yellow"
            self.backC = "red"
        else: self.backC = self.lastC = "yellow"

    #mouse motion made in gallery page 1
    def mouseMotionG1(self,x,y,xtext,ytext,margin):
        if x>xtext-self.galleryW/2 and x<xtext+self.galleryW/2 and\
            y>ytext-self.galleryH/2 and y<ytext+self.galleryH/2:
            self.gallery1Text = "Original Image"
        elif x>xtext+self.galleryW*.5+margin and x<xtext+\
            self.galleryW*1.5+margin and y>ytext-self.galleryH/2\
            and y<ytext+self.galleryH/2:
            self.gallery1Text = "Sketch Effect"
        elif x>xtext+self.galleryW*1.5+margin*2 and x<xtext+\
            self.galleryW*2.5+margin*2 and y>ytext-self.galleryH/2\
            and y<ytext+self.galleryH/2:
            self.gallery1Text = "Oil Painting"
        elif x>xtext+self.galleryW*2.5+margin*3 and x<xtext+\
            self.galleryW*3.5+margin*3 and y>ytext-self.galleryH/2\
            and y<ytext+self.galleryH/2:
            self.gallery1Text = "Blur Effect"
        elif x>xtext-self.galleryW/2 and x<xtext+self.galleryW/2 and\
            y>ytext+self.galleryH*.5+margin*2 and \
            y<ytext+self.galleryH*1.5+margin*2:
            self.gallery1Text = "Greyscale Effect"
        elif x>xtext+self.galleryW*.5+margin and x<xtext+\
            self.galleryW*1.5+margin and y>ytext+self.galleryH*.5+margin*2\
            and y<ytext+self.galleryH*1.5+margin*2:
            self.gallery1Text = "Mosaic Effect"
        elif x>xtext+self.galleryW*1.5+margin*2 and x<xtext+\
            self.galleryW*2.5+margin*2 and y>ytext+self.galleryH*.5+margin*2\
            and y<ytext+self.galleryH*1.5+margin*2:
            self.gallery1Text = "Merge Effect"
        elif x>xtext+self.galleryW*2.5+margin*3 and x<xtext+\
            self.galleryW*3.5+margin*3 and y>ytext+self.galleryH*.5+margin*2\
            and y<ytext+self.galleryH*1.5+margin*2:
            self.gallery1Text = "Inverting Effect"
        else: self.gallery1Text = ""
            
    #react to mouse pressed event
    def onMousePressed(self,event):
        x,y = event.x,event.y
        textX = self.width/2.0
        textY = self.height/5.0
        x1 = textX+self.width/2.0/2.0
        x2 = textX-self.width/2.0/2.0
        x3 = self.width/2.0-130
        y2 = self.height/5.0*4.2-120
        width = 260
        height = 60
        if self.galleryP1 == True or self.galleryP2 == True or\
           self.gallery1 == True or self.gallery2 == True:
            self.mousePressedGallery(x,y)
        elif self.splash == True:
            self.splashPressed(textX,textY,x1,x2,x,y)
        elif self.help == True:
            self.helpPressed(width,height,textX,textY,x3,y2,x,y)

    #react to mouse pressed event made in help screen
    def helpPressed(self,width,height,textX,textY,x3,y2,x,y):
        if (x>=textX-120 and x<=textX+120) and\
            (y>=textY*3.8 and y<=textY*4.6):
            self.help = False
            self.splash = True
            self.redrawAll()
        elif (x>x3 and x<x3+width) and (y>y2 and y<y2+height):
            self.help = False
            self.galleryP1 = True
            self.redrawAll()

    #react to mouse pressed event made in splash screen
    def splashPressed(self,textX,textY,x1,x2,x,y):
        if (x>=textX-120 and x<=textX+120) and\
            (y>=textY*3.8 and y<=textY*4.6):
            self.splash = False
            self.redrawAll()
        elif (x>=x1-120 and x<=x1+120) and (y>=textY*3.8 and y<=textY*4.6):
            self.root.destroy()
        elif (x>=x2-120 and x<=x2+120) and (y>=textY*3.8 and y<=textY*4.6):
            self.help = True
            self.splash = False
            self.redrawAll()

    #react to mouse pressed event made in gallery
    def mousePressedGallery(self,x,y):
        margin = 30
        width = 60
        height = 15
        y1 = self.height/4.0
        y2 = self.height/4.0*3
        if self.galleryP1 == True or self.galleryP2 == True:
            self.gallerP12Pressed(margin,width,height,y1,y2,x,y)
        elif self.gallery1 == True or self.gallery2 == True:
            self.galler12Pressed(margin,width,height,y1,y2,x,y)
        self.redrawAll()

    #react to mouse pressed event made in gallery
    def galler12Pressed(self,margin,width,height,y1,y2,x,y):
        if self.gallery1 == True:
            x0 = self.width-(self.width-221*4-margin*4)/2
            if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
                self.gallery1 = False
                self.gallery2 = True 
            elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
                self.gallery1 = False
        elif self.gallery2 == True:
            x0 = (self.width-221*4-margin*4)/2
            if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
                self.gallery1 = True
                self.gallery2 = False 
            elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
                self.gallery2 = False            

    #react to mouse pressed event made in gallery
    def gallerP12Pressed(self,margin,width,height,y1,y2,x,y):
        if self.galleryP1 == True:
            x0 = self.width-(self.width-221*4-margin*4)/2
            if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
                self.galleryP1 = False
                self.galleryP2 = True
            elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
                self.galleryP1 = False
                self.help = True
        elif self.galleryP2 == True:
            x0 = (self.width-221*4-margin*4)/2
            if (x>x0-width and x<x0+width) and (y>y1-height and y<y1+height):
                self.galleryP1 = True
                self.galleryP2 = False 
            elif (x>x0-width and x<x0+width) and (y>y2-height and y<y2+height):
                self.galleryP2 = False
                self.help = True

    #react to mouse move event
    def leftMouseMoved(self, event):
        if self.pen == True:
            #http://www.cs.cmu.edu/~112/notes/notes-event-based-programming.html
            ctrl  = ((event.state & 0x0004) != 0)#verbatim from 15-112 course note
            shift = ((event.state & 0x0001) != 0)#verbatim from 15-112 course note
            x, y = event.x, event.y
            self.penList.append((x,y))
            self.drawLine()
        
    #redraw everything
    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.splash == True:self.splashScreen()
        elif self.help == True:self.drawHelp()
        elif self.instruction == True:self.drawInstruction()
        elif self.galleryP1 == True:self.drawGalleryPage1()
        elif self.galleryP2 == True:self.drawGalleryPage2()
        elif self.gallery1 == True:self.drawGalleryPage1()
        elif self.gallery2 == True:self.drawGalleryPage2()
        else:
            self.createButton()
            try:
                self.newImage = ImageTk.PhotoImage(self.image)
                self.current = self.canvas.create_image(self.x, self.y,\
                                                        image=self.newImage)
            except:pass

    #have fun
    def run(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.initAnimation()
        self.redrawAll()
        self.setPath()
        self.root.mainloop()

Photolab().run()

#Test Functions

    
