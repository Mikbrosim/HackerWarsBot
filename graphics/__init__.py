import tkinter as tk
import os

class Window:
    def __init__(self):
        self.root = tk.Tk()

        self.overlay = False

        self.graphics = Graphics(self)
        self.eventManager = EventManager(self)

    @property
    def overlay(self):
        return self._overlay

    @overlay.setter
    def overlay(self,value):
        if isinstance(value, bool):
            self.overlay = value * 7 # The 7 stands for 2**3-1

        elif isinstance(value, int):
            self._overlay = value

            binary = [int(x) for x in bin(value+8)[2:]] # The 8 stands for 2**3
            self.root.attributes('-topmost',binary[-1])
            self.root.attributes('-transparentcolor','white' if binary[-2] else '')
            self.root.overrideredirect(binary[-3])

        else:
            print("NOT BOOL ERROR")

    @property
    def windowTitle(self):
        return self._windowTitle

    @windowTitle.setter
    def windowTitle(self,value):
        if isinstance(value, str):
            self._windowTitle = value
            self.root.title(value)
        else:
            print("NOT STRING ERROR")

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self,value):
        if isinstance(value, bool):
            self._fullscreen = value
            self.root.attributes('-fullscreen',value)
        else:
            print("NOT BOOL ERROR")

    @property
    def icon(self):
        return self._fullscreen

    @icon.setter
    def icon(self,value):
        if isinstance(value, str) and value.endswith(".ico") and os.path.isfile(value):
            self._icon = value
            self.root.iconbitmap(value)
        else:
            print("NO ICON ERROR")

    @property
    def geometry(self):
        posX,posY,sizeX,sizeY = self.root.winfo_x(), self.root.winfo_y(), self.root.winfo_width(), self.root.winfo_height()
        return tuple(map(int,(posX,posY,sizeX,sizeY)))

    @geometry.setter
    def geometry(self,value):
        if isinstance(value, tuple) and len(value) == 4:
            value = tuple(map(round,value))
            posX,posY,sizeX,sizeY = value
            self.root.geometry(str(sizeX) + "x" + str(sizeY) + "+" + str(posX) + "+" + str(posY))
            self.root.update_idletasks()
        else:
            print("NOT TUPLE ERROR")

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()


class Graphics:
    def __init__(self,window):
        self.root = window.root
        self.canvas = tk.Canvas(self.root,bg = "white", bd = -2)

        self.widthPos = self.canvas.winfo_screenwidth()
        self.heightPos = self.canvas.winfo_screenheight()

        self.buttons = []
        self.checkboxs = []
        self.labels = []

        #print(self.widthPos,self.heightPos)

    def update(self):
        try:
            self.root.update()
            self.root.update_idletasks()
        except tk.TclError:
            exit()

    def pack(self):
        self.canvas.pack(expand = 'yes', fill = 'both')

    def clear(self):
        del self.buttons[:]
        del self.checkboxs[:]
        self.canvas.delete("all")

        if hasattr(self, 'oldLabels'):
            #labels = self.oldLabels[:]
            for i in range(len(self.oldLabels)):
                label = self.oldLabels.pop()
                label.destroy()
                label.forget()


        self.oldLabels = self.labels[:]
        self.labels = []

    def stop(self):
        self.root.destroy()

    def createLine(self, x1, y1, x2, y2, width = 2, fill = "black", ratio = 0):
        if ratio == 0:
            widthPos = self.widthPos
            heightPos = self.heightPos
        if ratio == 1:
            widthPos = self.widthPos
            heightPos = self.widthPos
        if ratio == 2:
            widthPos = self.heightPos
            heightPos = self.heightPos
        return self.canvas.create_line(x1*widthPos,y1*heightPos,x2*widthPos,y2*heightPos, width = width, fill = fill)

    def createBox(self, x1, y1, x2, y2, width = 2, fill = None, outline = "black", hoverColor = None):
        self.canvas.create_rectangle(x1*self.widthPos,y1*self.heightPos,x2*self.widthPos,y2*self.heightPos, width = width, fill = fill, outline = outline, activefill = hoverColor)
        return (x1, y1, x2, y2)

    def createImage(self, x, y, img):
        photo = tk.PhotoImage(file=img)
        photoLabel = tk.Label(image=photo,bd=0)
        photoLabel.place(x=x*self.widthPos,y=y*self.heightPos)
        photoLabel.image = photo
        self.labels.append(photoLabel)

    def createWindow(self, window, x1, y1, x2, y2, width = 0, outline = "black"):
        self.canvas.create_window(x1*self.widthPos-(-width//2), y1*self.heightPos-(-width//2), window=window, width=(x2-x1)*self.widthPos-width, height=(y2-y1)*self.heightPos-width, anchor="nw")
        if width != 0:
            self.createBox(x1, y1, x2, y2, width = width, outline = outline)

    class Text:
        def __init__(self, graphics, x, y, color = "black", scale = 1, text = "", font = "Times", allign = "center", width = 0):
            self.graphics = graphics
            self.x = x
            self.y = y
            self.color = color
            self.scale = scale
            self.text = text
            self.font = font
            self.allign = allign
            self.width = width

            self.draw()

        def draw(self):
            self.label = self.graphics.canvas.create_text(self.x*self.graphics.widthPos, self.y*self.graphics.heightPos, fill = self.color, text = self.text, font = self.font + " " + str(int(self.scale*self.graphics.widthPos//100)), anchor = self.allign, width = self.width*self.graphics.widthPos)

        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            self._text = value
            if hasattr(self, "label"):
                self.graphics.canvas.itemconfig(self.label, text=self._text)

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            self._color = value
            if hasattr(self, "label"):
                self.graphics.canvas.itemconfig(self.label, fill=self._color)

    class _BaseGraphic:
        def __init__(self, graphics, x1, y1, x2, y2, scale = 1, text = "", font = "Times"):
            self.graphics = graphics
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.scale = scale
            self.text = text
            self.font = font

    class _BaseBorder(_BaseGraphic):
        def __init__(self, graphics, x1, y1, x2, y2, scale = 1, text = "", font = "Times", width = 2, outline = "black", backgroundColor = None):
            super().__init__(graphics, x1, y1, x2, y2, scale, text, font)
            self.width = width
            self.outline = outline
            self.backgroundColor = backgroundColor

    class InputField(_BaseBorder):
        def __init__(self, graphics, x1, y1, x2, y2, scale = 1, text = "", font = "Times", width = 2, outline = "black", backgroundColor = None):
            super().__init__(graphics, x1, y1, x2, y2, scale, text, font, width, outline, backgroundColor)
            self.draw()

        def draw(self):
            self.inputField = tk.Entry(self.graphics.canvas, font = self.font + " " + str(int(self.scale*self.graphics.widthPos//100)), bd=0, bg = self.backgroundColor)
            self.inputField.insert(0, self._text)
            self.graphics.createWindow(self.inputField, self.x1, self.y1, self.x2, self.y2, self.width, self.outline)

        @property
        def text(self):
            if hasattr(self, "inputField"):
                self._text = self.inputField.get()
            return self._text

        @text.setter
        def text(self, value):
            self._text = value
            if hasattr(self, "inputField"):
                self.inputField.delete(0, tk.END)
                self.inputField.insert(0, self._text)

    class TextField(_BaseBorder):
        def __init__(self, graphics, x1, y1, x2, y2, scale = 1, text = "", font = "Times", width = 2, outline = "black", backgroundColor = None):
            super().__init__(graphics, x1, y1, x2, y2, scale, text, font, width, outline, backgroundColor)
            self.draw()

        def draw(self):
            self.textField = tk.Text(self.graphics.canvas, font = self.font + " " + str(int(self.scale*self.graphics.widthPos//100)), bd=0, bg = self.backgroundColor)
            self.textField.insert(tk.INSERT, self._text)
            self.graphics.createWindow(self.textField, self.x1, self.y1, self.x2, self.y2, self.width, self.outline)

        @property
        def text(self):
            if hasattr(self, "textField"):
                self._text = self.textField.get('1.0','end-1c')
            return self._text

        @text.setter
        def text(self, value):
            self._text = value
            if hasattr(self, "textField"):
                self.textField.delete('1.0','end-1c')
                self.textField.insert('1.0', self._text)

    class CheckBox(_BaseBorder):
        def __init__(self, graphics, x1, y1, x2, y2, width = 2, outline = "black", scale = 1, text = "", font = "Times", value = False, colors = ["red","green"], func = lambda value: value):
            super().__init__(graphics, x1, y1, x2, y2, scale, text, font, width, outline)
            self._value = value
            self.colors = colors

            self.graphics.checkboxs.append(self)

            self.func = func

            self.draw()

        def draw(self):
            self.graphics.createBox(self.x1, self.y1, self.x2, self.y2, width = self.width, outline = self.outline, fill = self.colors[self.value])
            self.graphics.Text(self.graphics,(self.x1+self.x2)/2, (self.y1+self.y2)/2, scale = self.scale, font = self.font, text = self.text)

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            self._value = value
            self.draw()


    class Button(_BaseBorder):
        def __init__(self, graphics, x1, y1, x2, y2, text, func, width = 2, font = "Times", fill = None, outline = "black", hoverColor = None, scale = 1):
            super().__init__(graphics, x1, y1, x2, y2, scale, text, font, width, outline)
            self.func = func
            self.hoverColor = hoverColor
            self.fill = fill

            self.graphics.buttons.append(self)

            self.draw()

        def draw(self):
            self.graphics.createBox(self.x1, self.y1, self.x2, self.y2, width = self.width, outline = self.outline, fill = self.fill, hoverColor = self.hoverColor)
            self.graphics.Text(self.graphics,(self.x1+self.x2)/2, (self.y1+self.y2)/2, color = self.fill, text = self.text, scale = self.scale)

    def backgroundColor(self, color):
        self.canvas.configure(bg=color)

class EventManager:
    def __init__(self,window):
        self.graphics = window.graphics
        self.canvas = self.graphics.canvas
        self.root = self.graphics.root

        self.setup()
        self.graphics.pack()

    def setup(self):
        self.canvas.bind("<Button-1>", self.leftClick)
        self.canvas.bind("<Button-2>", self.middleClick)
        self.canvas.bind("<Button-3>", self.rightClick)
        self.root.bind("<Escape>",self.escape)

    def leftClick(self,event):
        pos = (event.x/self.graphics.widthPos, event.y/self.graphics.heightPos)
        self.buttonChecker(pos)
        self.checkboxChecker(pos)
        #print("left",pos)

    def rightClick(self, event):
        pos = (event.x,event.y)
        #print("right",pos)
        pass

    def middleClick(self, event):
        pos = (event.x,event.y)
        #print("middle",pos)
        pass

    def escape(self, event):
        #print(event)
        self.graphics.stop()

    def buttonChecker(self, pos):
        for button in self.graphics.buttons:
            if (button.x1 < pos[0] < button.x2 and button.y1 < pos[1] < button.y2):
                button.func()
                return True
        else:
            return False

    def checkboxChecker(self, pos):
        for box in self.graphics.checkboxs:
            if (box.x1 < pos[0] < box.x2 and box.y1 < pos[1] < box.y2):
                box.value = not box.value
                box.func(box.value)
                return True
        else:
            return False

if __name__ == "__main__":
    def B1():
        print("B1")
    def B2():
        print("B2")

    window = Window()

    window.windowTitle = "Test1!!!"
    window.fullscreen = False
    window.icon = "favicon.ico"
    window.geometry = (0,0,1600,900)

    graphics = window.graphics
    graphics.createBox(0.1,0.1,0.2,0.2,5)
    graphics.createBox(0.3,0.3,0.4,0.4,5)
    graphics.Text(graphics,0.35,0.35,text="Fish",scale = 1)
    graphics.Button(graphics,0.2,0.2,0.3,0.3,"B1",B1,5)
    graphics.Button(graphics,0.4,0.4,0.5,0.5,"B2",B2,5)
    graphics.createBox(0.6,0.6,0.7,0.7,fill=None,outline="black",width=10,hoverColor="red")

    while True:
        print(window.geometry)
        graphics.update()
