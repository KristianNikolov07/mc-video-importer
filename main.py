import importer
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

datapack_path = "output/datapack"
resourcepack_path = "output/resourcepack"
video_path = ""
namespace = ""
video_name = ""

def select_video():
    global video_path
    _video_path = filedialog.askopenfilename()
    if _video_path:
        video_path = _video_path
        video_path_label.config(text=video_path)

def on_convert_press():
    namespace = namespace_input.get()
    video_name = video_name_input.get()
    if video_path and video_name and namespace:
        converting_label = ttk.Label(text="Converting...")
        converting_label.pack()
        importer.SetupOutputDir()
        importer.CreateDatapack(namespace)
        importer.CreateResourcepack(namespace)
        
        importer.ConvertVideo(video_path, namespace, video_name)
        importer.ExportSound(video_path, namespace, video_name)
        importer.GenerateSoundsJson(namespace, video_name)
        importer.GenerateFunctions(video_name, namespace)
        converting_label.destroy()
        messagebox.showinfo("MC Video Importer", "Video converted successfully!")
    



top = tkinter.Tk()
top.title("MC Video Importer")
top.resizable(False, False)
top.geometry("400x400")

video_select_button = ttk.Button(text="Select Video", command=select_video)
video_select_button.pack(pady=(10,0))

video_path_label = ttk.Label(text="No file selected")
video_path_label.pack()

namespace_input_label = ttk.Label(text="Namespace:")
namespace_input_label.pack(pady=(10, 0))

namespace_input = ttk.Entry()
namespace_input.pack()

video_name_input_label = ttk.Label(text="Video name:")
video_name_input_label.pack(pady=(10, 0))

video_name_input = ttk.Entry()
video_name_input.pack()

convert_button = ttk.Button(text="Convert", command=on_convert_press)
convert_button.pack(pady=10)



top.mainloop()