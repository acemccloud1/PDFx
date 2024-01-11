# PDFx - A metaphorical Swiss-Knife for PDF files.

### Description
This is a very minimalistic utility that helps you extract (all/range), merge, covert (to PNG), encrypt, decrypt and compress PDF files. You can also use the pyinstaller module to create a portable executable file (*.exe) from this and use it on any Windows machine.

### PyInstaller Command
pyinstaller --icon "PDFx.ico" -n PDFx --version-file ".\file_version_info.txt" --windowed --clean --onefile -w main.py

### Embedding the icons
https://pythonassets.com/posts/window-icon-in-tk-tkinter/#packing-icons-into-an-executable-file
