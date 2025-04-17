import importer
import tkinter
from tkinter import filedialog
from tkinter import messagebox

datapack_path = "output/datapack"
resourcepack_path = "output/resourcepack"
video_path = ""
namespace = ""
video_name = ""


#def select_dp_folder():
#    global datapack_path
#    folder_path = filedialog.askdirectory()
#    if folder_path:
#        datapack_path = folder_path
#        dp_folder_path_label.config(text=datapack_path)

#def select_rp_folder():
#    global resourcepack_path
#    folder_path = filedialog.askdirectory()
#    if folder_path:
#        resourcepack_path = folder_path
#        rp_folder_path_label.config(text=resourcepack_path)

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
        converting_label = tkinter.Label(text="Converting...")
        converting_label.pack()
        importer.SetupOutputDir()
        importer.CreateDatapack(namespace)
        importer.CreateResourcepack(namespace)
        importer.ConvertVideo(video_path, namespace, video_name)
        importer.GenerateFunctions(video_name, namespace)
        converting_label.destroy()
        messagebox.showinfo("MC Video Importer", "Video converted successfully!")
    



top = tkinter.Tk()
top.title("MC Video Importer")
top.resizable(False, False)
top.geometry("400x400")



# dp_folder_select_label = tkinter.Label(text="Please select the folder where you want your datapack to be generated\n(the folder must be empty):")
# dp_folder_select_label.pack()

# dp_folder_select_button = tkinter.Button(text="Select Folder", command=select_dp_folder)
# dp_folder_select_button.pack()

# dp_folder_path_label = tkinter.Label(text="No folder selected")
# dp_folder_path_label.pack()

# rp_folder_select_label = tkinter.Label(text="Please select the folder where you want your resourcepack to be generated\n(the folder must be empty):")
# rp_folder_select_label.pack()

# rp_folder_select_button = tkinter.Button(text="Select Folder", command=select_rp_folder)
# rp_folder_select_button.pack()

# rp_folder_path_label = tkinter.Label(text="No folder selected")
# rp_folder_path_label.pack()

video_select_button = tkinter.Button(text="Select Video", command=select_video)
video_select_button.pack()

video_path_label = tkinter.Label(text="No file selected")
video_path_label.pack()

namespace_input_label = tkinter.Label(text="Namespace:")
namespace_input_label.pack()

namespace_input = tkinter.Entry()
namespace_input.pack()

video_name_input_label = tkinter.Label(text="Video name:")
video_name_input_label.pack()

video_name_input = tkinter.Entry()
video_name_input.pack()

convert_button = tkinter.Button(text="Convert", command=on_convert_press)
convert_button.pack()



top.mainloop()