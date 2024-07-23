from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import font as tkFont
from PIL import ImageTk, Image
from stegano import lsb
from stegano import exifHeader as aaa
from subprocess import Popen
import os

# Global variable to keep track of the main window
main = None

def encode():
    global main
    if main:
        main.withdraw()  # Hide the main window

    enc = Toplevel()
    enc.attributes("-fullscreen", True)

    screen_width = enc.winfo_screenwidth()
    screen_height = enc.winfo_screenheight()

    try:
        bg_image = Image.open("bg2.JPG")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(bg_image)
        label1 = Label(enc, image=img)
        label1.image = img  # Keep a reference to avoid garbage collection
        label1.pack(fill=BOTH, expand=YES)
    except FileNotFoundError:
        enc.configure(bg="white")

    fontl = tkFont.Font(family='Algerian', size=32)

    LabelTitle = Label(enc, text="ENCODE", bg="blue", fg="white", width=20)
    LabelTitle['font'] = fontl
    LabelTitle.place(relx=0.6, rely=0.1)

    def back():
        enc.destroy()
        if main:
            main.deiconify()  # Show the main window again

    Buttonback = Button(enc, text="Back", command=back)
    Buttonback.place(relx=0.7, rely=0.85, height=31, width=94)

    def openfile():
        global fileopen
        global imagee

        fileopen = askopenfilename(initialdir="/Desktop", title="Select file",
                                   filetypes=(("jpeg png files", ".jpg *.png"), ("all files", ".*")))
        imagee = Image.open(fileopen)
        imagee = imagee.resize((300, 300), Image.Resampling.LANCZOS)
        imagee = ImageTk.PhotoImage(imagee)

        Labelpath = Label(enc, text=fileopen)
        Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)
        Labeling = Label(enc, image=imagee)
        Labeling.image = imagee  # Keep a reference to avoid garbage collection
        Labeling.place(relx=0.7, rely=0.3)

        secimg = StringVar()
        radiol = Radiobutton(enc, text='jpeg', value='jpeg', variable=secimg)
        radiol.place(relx=0.7, rely=0.57)
        radio2 = Radiobutton(enc, text='png', value='png', variable=secimg)
        radio2.place(relx=0.8, rely=0.57)

        Labell = Label(enc, text="Enter message")
        Labell.place(relx=0.6, rely=0.6, height=21, width=104)
        entrysecmes = Text(enc, wrap=WORD)
        entrysecmes.place(relx=0.7, rely=0.6, relheight=0.15, relwidth=0.25)

        Label2 = Label(enc, text="File Name")
        Label2.place(relx=0.6, rely=0.80, height=21, width=104)
        entrysave = Entry(enc)
        entrysave.place(relx=0.7, rely=0.80, relheight=0.05, relwidth=0.25)

        def encode_image():
            message = entrysecmes.get("1.0", END).strip()
            if secimg.get() == "jpeg":
                inimage = fileopen
                response = messagebox.askyesno("Popup", "Do you want to encode?")
                if response == 1:
                    aaa.hide(inimage, entrysave.get() + ".jpg", message)
                    messagebox.showinfo("Popup", f"Successfully encoded to {entrysave.get()}.jpeg")
                else:
                    messagebox.showwarning("Popup", "Unsuccessful")
            elif secimg.get() == "png":
                inimage = fileopen
                response = messagebox.askyesno("Popup", "Do you want to encode?")
                if response == 1:
                    lsb.hide(inimage, message=message).save(entrysave.get() + '.png')
                    messagebox.showinfo("Popup", f"Successfully encoded to {entrysave.get()}.png")
                else:
                    messagebox.showwarning("Popup", "Unsuccessful")

        Button2 = Button(enc, text="Encode", command=encode_image)
        Button2.place(relx=0.7, rely=0.9, height=31, width=94)

    Button2 = Button(enc, text="Open File", command=openfile)
    Button2.place(relx=0.7, rely=0.2, height=31, width=94)

    enc.mainloop()

def decode():
    global main
    if main:
        main.withdraw()  # Hide the main window

    dec = Toplevel()
    dec.attributes("-fullscreen", True)

    screen_width = dec.winfo_screenwidth()
    screen_height = dec.winfo_screenheight()

    try:
        bg_image = Image.open("bg2.JPG")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(bg_image)
        label1 = Label(dec, image=img)
        label1.image = img  # Keep a reference to avoid garbage collection
        label1.pack(fill=BOTH, expand=YES)
    except FileNotFoundError:
        dec.configure(bg="white")

    fontl = tkFont.Font(family='Algerian', size=32)

    LabelTitle = Label(dec, text="DECODE", bg="blue", fg="white", width=20)
    LabelTitle['font'] = fontl
    LabelTitle.place(relx=0.6, rely=0.1)

    secimg = StringVar()
    radiol = Radiobutton(dec, text='jpeg', value='jpeg', variable=secimg)
    radiol.place(relx=0.7, rely=0.57)
    radio2 = Radiobutton(dec, text='png', value='png', variable=secimg)
    radio2.place(relx=0.8, rely=0.57)

    def openfile():
        global fileopen
        global imagee

        fileopen = askopenfilename(initialdir="/Desktop", title="Select file",
                                   filetypes=(("jpeg png files", ".jpg *.png"), ("all files", ".*")))
        imagee = Image.open(fileopen)
        imagee = imagee.resize((300, 300), Image.Resampling.LANCZOS)
        imagee = ImageTk.PhotoImage(imagee)

        Labelpath = Label(dec, text=fileopen)
        Labelpath.place(relx=0.6, rely=0.25, height=21, width=450)
        Labeling = Label(dec, image=imagee)
        Labeling.image = imagee  # Keep a reference to avoid garbage collection
        Labeling.place(relx=0.7, rely=0.3)

    def decode_image():
        try:
            if secimg.get() == "png":
                message = lsb.reveal(fileopen)
            elif secimg.get() == "jpeg":
                message = aaa.reveal(fileopen)
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {e}")
            return
        
        if not message:
            messagebox.showwarning("Warning", "No message found in the image")
            return
        
        decoded_message = Text(dec, wrap=WORD)
        decoded_message.insert(INSERT, message)
        decoded_message.configure(state=DISABLED)
        decoded_message.place(relx=0.7, rely=0.7, relheight=0.15, relwidth=0.25)

    Button2 = Button(dec, text="Open File", command=openfile)
    Button2.place(relx=0.7, rely=0.2, height=31, width=94)

    Button2 = Button(dec, text="DECODE", command=decode_image)
    Button2.place(relx=0.7, rely=0.8, height=31, width=94)

    def back():
        dec.destroy()
        if main:
            main.deiconify()  # Show the main window again

    Buttonback = Button(dec, text="Back", command=back)
    Buttonback.place(relx=0.7, rely=0.88, height=31, width=94)  # Adjusted placement for spacing

    dec.mainloop()

def init_main_window():
    global main
    main = Tk()
    main.title('Enc & Dec Panel')
    main.attributes("-fullscreen", True)

    fontl = tkFont.Font(family='Algerian', size=32)

    # Check if the background image exists
    bg_image_path = "bg1.JPG"
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()

    if not os.path.exists(bg_image_path):
        messagebox.showerror("Error", f"Background image '{bg_image_path}' not found. Using default background color.")
        main.configure(bg="white")
    else:
        # Load and resize the background image
        bg1_image = Image.open(bg_image_path)
        bg1_image = bg1_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        image1 = ImageTk.PhotoImage(bg1_image)
        label = Label(main, text="", image=image1)
        label.image = image1  # Keep a reference to avoid garbage collection
        label.pack(fill=BOTH, expand=YES)

    LabelTitle = Label(main, text="IMAGE STEGANOGRAPHY", bg="green", fg="white", width=22)
    LabelTitle['font'] = fontl
    LabelTitle.place(relx=0.32, rely=0.1)

    encbutton = Button(main, text='Encode', fg="white", bg="black", width=15, command=encode)
    encbutton['font'] = fontl
    encbutton.place(relx=0.36, rely=0.3)

    decbutton = Button(main, text='Decode', fg="white", bg="black", width=15, command=decode)
    decbutton['font'] = fontl
    decbutton.place(relx=0.36, rely=0.5)

    





    ButtonExit = Button(main, text="EXIT", fg="white",bg="red", width=10, command=exit)
    ButtonExit['font'] = fontl
    ButtonExit.place(relx=0.4, rely=0.7)

    main.mainloop()

init_main_window()