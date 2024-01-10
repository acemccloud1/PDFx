from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import fitz         # Install using 'pip install pymupdf'
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from base64 import b64decode
import os
from time import sleep


# Encode the PNG files into byte-data so there's no need to package any additional data files into the EXE
small_icon_data = fr"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAHYcAAB2HAGnwnjqAAAAB3RJTUUH5AscDR4M+THKpQAABBtJREFUWMO9l29olVUcxz+/8zzbddlK0W01ERRNySTS9DpMJwlColC0ab3MCrKoF5GZCL4tX/QiISOhF71I042ZkBAp9sdQdIgthTRo/V0tsyl4hbl773O+vXiezbl87jNx6weXe+45v/P7fs/3/H7nnGtkWP613QAh0jxgKfJzQdORGpGmgoR0EakX1IN0BnTYnPUo8nTu3FgxvlUG3wNQC9rkvTZ47xudKXAGSPEHjWyXkE6DtnkuHHbU07nzxVQMl6UAsF5i6/SptdPXLZsTLJzVkOVfBVoC2uWoX5DlnEog//oeKEUAi4PAhc+ums+W1iVsWddE/d13ICkr9kykpzJErqCADMtVB8BkJAZiMvQXy5QjZe3eoN2V5RCmDdgQC4LIiw8OneXsLxfp7r1MX6EfMyBThGwLKw0mGEUzK/cV+sufdnbjTMNlM6B6tHJkEshvbk/6VCUJSQbsAPYZ5sPAJRnvSdbfALwF1KUBnHx3o2NDc26oWlARiGzxsZhAfst+8B7MpoFakJYB9cMWGSUzE8wh3QXUALVp4CXvIrqWrwE2DU0UP4M+0smmLzHzsQLOPYj0HrD0duQcaZIJrBFoHta9ArQaeB5x0IFNAd4EHhlL8AxrADaDr3PAKmDl/wQ83BYBjzqMpcR7mWG3XnMGV0BpOVKDWOmA/NguLMk12W/5aRe+Qba6gvM8B8wYA7xhbStGcqdzYfTq+2u/eBi5FRVmzwqJEyILo7fs3YFcEJ2bWF0Krp8FN96IJqkmLPW+sOjs5TX3/bQGb8+Bggqh7w2BASCX5uHFqZmTCtv2tH5eF7pyc/IOsBjYj7iKvSHl8MxB1gjKrKoQ6AFmpaz8jxmTC1vb1n/2GJF7hSioumHlshEkuJFQtv3tgB/SRsvefbKv9fA9RMHLQNVoIt6inXeIE/+hm/yqcv68C6Im4gtnrE0YXzvgK+Cfm3lUB96AyeMADvArsN+BnQD23szDLK6rcSLQjvyZEHwJ2E78emkB7hwnwEErAgeBd7BQYef2J8m/0fEn8BLwITCX5Kk2IYyO493yChl9CXgb6EtRym7S/zvYMcwuW/54urw6tx5wIRZ9jHzr9dIbXoYqgO9AuoJkcUn6hK93SEfBtdnCI6lyVHySjcJqgWcSysmaq0ADg+MOaKsU4HYJDOoFrhqmPA4T58PFDrhyalQzw4pBfRgRlK9m4wtyjVDXAuEk8ANQ6AKVM6em/i+w+9shuCbgGFA5khmU+uDqt1C8EH8rKgPfZR3Jo9mCvcADwEZgQgoDiArQswNcDZQuXcPYhWx3VvDMQ0bnWgBqQGuRnkZ+MagBqXrEjVhE/i8UnSZOvANAvy04cnsEhoh8/wRADmk2aAHS7LjtI6QfkbpBXch3gw3YQ4dGFfdfY/jYXn71xiAAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTEtMjhUMTM6MzA6MTErMDA6MDDKzDL3AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTExLTI4VDEzOjMwOjExKzAwOjAwu5GKSwAAACB0RVh0c29mdHdhcmUAaHR0cHM6Ly9pbWFnZW1hZ2ljay5vcme8zx2dAAAAGHRFWHRUaHVtYjo6RG9jdW1lbnQ6OlBhZ2VzADGn/7svAAAAGHRFWHRUaHVtYjo6SW1hZ2U6OkhlaWdodAA1MTKPjVOBAAAAF3RFWHRUaHVtYjo6SW1hZ2U6OldpZHRoADUxMhx8A9wAAAAZdEVYdFRodW1iOjpNaW1ldHlwZQBpbWFnZS9wbmc/slZOAAAAF3RFWHRUaHVtYjo6TVRpbWUAMTYwNjU3MDIxMe6q0kMAAAATdEVYdFRodW1iOjpTaXplADE2NzY1QkJSwMbRAAAAR3RFWHRUaHVtYjo6VVJJAGZpbGU6Ly8uL3VwbG9hZHMvNTYvQk9EQ0o5cS8yNjk5L3B5dGhvbl9sb2dvX2ljb25fMTY4ODg2LnBuZ0bGbXgAAAAASUVORK5CYII="
large_icon_data = fr"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"


def main():
    root = Tk()
    app = Window(root)
    root.mainloop()


class Window():
    def __init__(self, master):
        self.master = master
        self.master.title("PDFx - A metaphorical Swiss-Knife for PDF files")
        self.master.geometry('700x400')

        # Embed the encoded byte-data of the PNG files into the main program directly
        small_icon = PhotoImage(data=b64decode(small_icon_data))
        large_icon = PhotoImage(data=b64decode(large_icon_data))
        self.master.iconphoto(False, large_icon, small_icon)

        self.RadioFrame = LabelFrame(self.master, text="Functions", width=250, height=150)
        self.RadioFrame.place(x=10, y=10)

        self.InfoFrame = LabelFrame(self.master, text="AppInfo", width=250, height=150)
        self.InfoFrame.place(x=10, y=320)

        Options = {
            "Clean Slate": "cleanslate",
            "Extract All": "extractall",
            "Extract Range": "extractrange",
            "Merge": "merge",
            "Convert to PNG": "pdf2png",
            "Encrypt": "encrypt",
            "Decrypt": "decrypt",
            "Compress": "compress",
        }

        selection = StringVar()
        selection.set("cleanslate")

        for text, value in Options.items():
            Radiobutton(self.RadioFrame, text=text, variable=selection, value=value, command=lambda: Clicked(selection.get())).pack(anchor=W)

        Label(self.InfoFrame, text=f"Creator: Unmesh Patil\nLanguage: Python\nVersion: 24.01.04", wraplength=400, justify=LEFT).pack(anchor=W)


        def clear_canvas():
            try:
                self.MainFrame.destroy()
            except AttributeError:
                pass


        def Clicked(variable):
            # Extract all pages from a PDF file
            if selection.get() == "extractall":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Extract All Pages", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for extraction.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                def extractall():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        fileext = str(p.suffix)
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        Label(frame, text=f"Output Directory:- {outputdir}", bg="lime", fg="black", wraplength=400, justify=LEFT).grid(row=6, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        # Extract all pages of the PDF file
                        input_pdf = PdfReader(filepath)
                        # Decrypt if the PDF is encrypted
                        if input_pdf.is_encrypted:
                            password = str(passtext.get())
                            input_pdf.decrypt(password)
                        # Begin page extraction
                        for i, page in enumerate(input_pdf.pages):
                            output = PdfWriter()
                            output.add_page(page)
                            extracted_filepath = fr"{outputdir}\{filename_only}_{i+1}{fileext}"
                            with open(extracted_filepath, "wb") as output_stream:
                                output.write(output_stream)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Password (if PDF is encrypted):", wraplength=400, justify=LEFT).grid(row=2, column=0)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=2, column=1)
                Button(frame, text="Select File", command=lambda: extractall()).grid(row=3, column=0, padx=10, pady=10, columnspan=2)

            # Extract specific pages/range from a PDF file
            elif selection.get() == "extractrange":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Extract Custom Range", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for extraction.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                Label(frame, text="Password (if PDF is encrypted):", wraplength=400, justify=LEFT).grid(row=1, column=0)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=1, column=1)
                Label(frame, text="Step# 1 --> Start Page#", wraplength=400, justify=LEFT).grid(row=2, column=0)
                e1 = Entry(frame, width=10)
                e1.grid(row=2, column=1)
                e1.insert(0, "2")
                Label(frame, text="Step# 2 --> End Page#", wraplength=400, justify=LEFT).grid(row=3, column=0)
                e2 = Entry(frame, width=10)
                e2.grid(row=3, column=1)
                e2.insert(0, "3")
                def extractrange():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        fileext = str(p.suffix)
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, sticky='w', columnspan=3)
                        Label(frame, text=f"Output Directory:- {outputdir}", wraplength=400, justify=LEFT).grid(row=6, column=0, sticky='w', columnspan=3)
                        # Extract the pages from the give range
                        input_pdf = PdfReader(filepath)
                        # Decrypt if the PDF is encrypted
                        if input_pdf.is_encrypted:
                            password = str(passtext.get())
                            input_pdf.decrypt(password)
                        # Begin page extraction
                        output = PdfWriter()
                        rangestart = int(e1.get())
                        rangeend = int(e2.get())
                        for i in range(rangestart, (rangeend + 1)):
                            output.add_page(input_pdf.pages[i-1])
                        extracted_filepath = fr"{outputdir}\{filename_only}_{rangestart}-{rangeend}{fileext}"
                        with open(extracted_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        Label(frame, text=f"Extracted File:- {extracted_filepath}", bg="lime", fg="black").grid(row=7, column=0, columnspan=3, sticky='w', padx=10, pady=10)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Step# 3 --> ", wraplength=400, justify=LEFT).grid(row=4, column=0)
                Button(frame, text="Select File", command=lambda: extractrange()).grid(row=4, column=1, padx=5, pady=5)

            # Merge multiple PDF files
            elif selection.get() == "merge":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Merge PDF", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="IMP:- Password-Protected PDF files are *NOT* supported for merge operation! Please unencrypt them before merging.", fg='Red', wraplength=475, justify=LEFT).grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=5)
                Label(frame, text="NOTE:- The selected files will be sorted in an ascending order before merging, so please name them in the order you want them merged.", fg='OrangeRed', wraplength=475, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)
                Label(frame, text="TIP:- Prefix the filenames with numericals (1, 2 etc.) to enforce the order sequence.", fg='MediumSeaGreen', wraplength=475, justify=LEFT).grid(row=2, column=0, columnspan=2, sticky='w', padx=10, pady=5)
                def mergeall():
                    try:
                        # Fetch the folder-path
                        filepath_tuple = filedialog.askopenfilenames(initialdir="/", title="Select files", filetypes=[("PDF files", "*.pdf")])
                        filepath = filepath_tuple[0].replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        Label(frame, text=f"Output Directory:- {outputdir}", wraplength=475, justify=LEFT).grid(row=6, column=0, sticky='w')
                        # Merge all the PDF files in the directory
                        output = PdfMerger()
                        for i, filepath in enumerate(filepath_tuple):
                            newpath = filepath_tuple[i].replace('/', '\\')
                            file = PdfReader(newpath)
                            output.append(file)
                        merged_filepath = fr"{outputdir}\PDFx_Merged.pdf"
                        with open(merged_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        Label(frame, text=f"Merged File:- {merged_filepath}", bg="lime", fg="black", wraplength=475, justify=LEFT).grid(row=7, column=0, sticky='w', padx=5, pady=5)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Button(frame, text="Select Files", command=lambda: mergeall()).grid(row=3, column=0, padx=10, pady=10, columnspan=2)

            # Convert all pages of a PDF file into PNG files
            elif selection.get() == "pdf2png":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Extract All Pages As PNG", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for extraction.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                def extractpng():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        Label(frame, text=fr"Output Directory:- {outputdir}", bg="lime", fg="black", wraplength=400, justify=LEFT).grid(row=6, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        # Extract all pages of the PDF file
                        input_pdf = PdfReader(filepath)
                        # Decrypt if the PDF is encrypted
                        if input_pdf.is_encrypted:
                            password = str(passtext.get())
                            input_pdf.decrypt(password)
                        # Create a copy of the file; reqd as input for fitz
                        output = PdfWriter()
                        for i, page in enumerate(input_pdf.pages):
                            output.add_page(page)
                        extracted_filepath = fr"{outputdir}\PDF2PNG.pdf"
                        with open(extracted_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        pdf_path = os.path.abspath(extracted_filepath)
                        # Begin pdf page to image conversion
                        doc = fitz.open(pdf_path)
                        for i in range(len(doc)):
                            page = doc.load_page(i)
                            pix = page.get_pixmap(dpi=150)
                            output = fr"{outputdir}\{filename_only}_{i+1}.png"
                            pix.save(output)
                        doc.close()
                        os.remove(extracted_filepath)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Password (if PDF is encrypted):", wraplength=400, justify=LEFT).grid(row=2, column=0)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=2, column=1)
                Label(frame, text="IMP:- This may take a while. Please be patient.....", fg='Red', wraplength=400, justify=LEFT, font='Helvetica 11 bold').grid(row=3, column=0, columnspan=2, padx=15, pady=15)
                Button(frame, text="Select File", command=lambda: extractpng()).grid(row=4, column=0, padx=10, pady=10, columnspan=2)

            # Decrypt a PDF file
            elif selection.get() == "decrypt":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Decrypt PDF", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for decryption.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                def decrypt():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        # Extract all pages of the PDF file
                        input_pdf = PdfReader(filepath)
                        if not input_pdf.is_encrypted:
                            raise Exception("The PDF is not encrypted!")
                        # Decrypt the encrypted PDF
                        password = str(passtext.get())
                        input_pdf.decrypt(password)
                        # Create a copy of the file; reqd as input for fitz
                        output = PdfWriter()
                        for i, page in enumerate(input_pdf.pages):
                            output.add_page(page)
                        unencrypted_filepath = fr"{outputdir}\{filename_only}_Unencrypted.pdf"
                        with open(unencrypted_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        Label(frame, text=f"Unencrypted File:- {unencrypted_filepath}", bg="lime", fg="black", wraplength=475, justify=LEFT).grid(row=7, column=0, sticky='w', padx=5, pady=5)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Password for decrypting PDF:", wraplength=400, justify=LEFT).grid(row=2, column=0)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=2, column=1)
                Button(frame, text="Select File", command=lambda: decrypt()).grid(row=4, column=0, padx=10, pady=10, columnspan=2)

            # Encrypt a PDF file
            elif selection.get() == "encrypt":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Encrypt PDF", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for encryption.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                def encrypt():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        # Extract all pages of the PDF file
                        input_pdf = PdfReader(filepath)
                        if input_pdf.is_encrypted:
                            raise Exception("The PDF is already encrypted!")
                        # Create a copy of the file; reqd as input for fitz
                        output = PdfWriter()
                        for i, page in enumerate(input_pdf.pages):
                            output.add_page(page)
                        # Encrypt the unencrypted PDF
                        password = str(passtext.get())
                        output.encrypt(password)
                        encrypted_filepath = fr"{outputdir}\{filename_only}_Encrypted.pdf"
                        with open(encrypted_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        Label(frame, text=f"Encrypted File:- {encrypted_filepath}", bg="lime", fg="black", wraplength=475, justify=LEFT).grid(row=7, column=0, sticky='w', padx=5, pady=5)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Password for encrypting PDF:", wraplength=400, justify=LEFT).grid(row=2, column=0)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=2, column=1)
                Button(frame, text="Select File", command=lambda: encrypt()).grid(row=4, column=0, padx=10, pady=10, columnspan=2)

            # Compress a PDF file
            elif selection.get() == "compress":
                clear_canvas()
                self.MainFrame = LabelFrame(self.master, text="Compress PDF", width=250, height=150)
                self.MainFrame.place(x=165, y=10)
                frame = self.MainFrame
                Label(frame, text="NOTE:- You may select only one file at a time for compression.", fg='OrangeRed', wraplength=400, justify=LEFT).grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
                def compress():
                    try:
                        # Fetch the filepath
                        absfilepath = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("PDF files", "*.pdf")])
                        filepath = absfilepath.replace('/', '\\')
                        p = Path(filepath)
                        outputdir = str(p.parent)
                        filename_only = str(p.name).split('.')[0]
                        Label(frame, text=f"Selected File:- {filepath}", wraplength=400, justify=LEFT).grid(row=5, column=0, columnspan=3, sticky='w', padx=5, pady=5)
                        # Extract all pages of the PDF file
                        input_pdf = PdfReader(filepath)
                        if input_pdf.is_encrypted:
                            password = str(passtext.get())
                            input_pdf.decrypt(password)
                        # Create a copy of the file; reqd as input for fitz
                        output = PdfWriter()
                        for i, page in enumerate(input_pdf.pages):
                            # page.compress_content_streams()         #<-- This is CPU intensive!
                            output.add_page(page)
                        # Compress the PDF
                        output.add_metadata(input_pdf.metadata)
                        compressed_filepath = fr"{outputdir}\{filename_only}_Compressed.pdf"
                        with open(compressed_filepath, "wb") as output_stream:
                            output.write(output_stream)
                        Label(frame, text=f"Compressed File:- {compressed_filepath}", bg="lime", fg="black", wraplength=475, justify=LEFT).grid(row=7, column=0, sticky='w', padx=5, pady=5)
                        messagebox.showinfo(title="Success", message="Task completed successfully.")
                    except Exception as e:
                        messagebox.showerror(title="ERROR", message=fr"Error:- {e}")
                Label(frame, text="Password (if PDF is encrypted):", wraplength=400, justify=LEFT).grid(row=2, column=0)
                Label(frame, text="IMP:- Compression works only if the input file is inflated or has duplicated objects.", fg='Red', wraplength=400, justify=LEFT, font='TkTextFont 10 bold').grid(row=3, column=0, columnspan=2, padx=15, pady=15)
                passtext = Entry(frame, show="*", width=15)
                passtext.grid(row=2, column=1)
                Button(frame, text="Select File", command=lambda: compress()).grid(row=4, column=0, padx=10, pady=10, columnspan=2)


            # Compress a PDF file
            elif selection.get() == "cleanslate":
                clear_canvas()


# Run the main program; 'root.mainloop()'
if __name__ == '__main__':
    main()
