import subprocess
import os

datapack_path = "output/datapack"
resourcepack_path = "output/resourcepack"

def SetupOutputDir():
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/datapack", exist_ok=True)
    os.makedirs("output/resourcepack", exist_ok=True)

def CreateDatapack(namespace):
    with open(datapack_path + "/pack.mcmeta", "w") as f:
        f.write('{\n' \
        '  "pack": {\n' \
        '    "description": "MC Video Importer",\n' \
        '    "pack_format": 18,\n' \
        '    "supported_formats": [18, 46]'
        '  }\n' \
        '}')
    os.makedirs(datapack_path + "/data", exist_ok=True)
    os.makedirs(datapack_path + "/data/" + namespace, exist_ok=True)
    os.makedirs(datapack_path + "/data/" + namespace + "/function", exist_ok=True)

def CreateResourcepack(namespace):
    with open(resourcepack_path + "/pack.mcmeta", "w") as f:
        f.write('{\n' \
        '  "pack": {\n' \
        '    "description": "MC Video Importer",\n' \
        '    "pack_format": 18,\n' \
        '    "supported_formats": [18, 46]\n' \
        '  }\n' \
        '}')
    os.makedirs(resourcepack_path + "/assets", exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace, exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace + "/textures", exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace + "/textures/overlays", exist_ok=True)

def ConvertVideo(video_file_path, namespace, video_name):
    output_folder_path = resourcepack_path + "/assets/" + namespace + "/textures/overlays/" + video_name
    os.makedirs(output_folder_path, exist_ok=True)
    subprocess.run('ffmpeg -i ' + video_file_path + ' -vf "fps=20" ' + output_folder_path + '/%d.png', shell=True)

def GenerateFunctions(video_name, namespace):
    video_frames_path = resourcepack_path + "/assets/" + namespace + "/textures/overlays/" + video_name
    functions_output_path =  datapack_path + "/data/" + namespace + "/function"
    total_frames = len(os.listdir(video_frames_path))
    frames = []
    for i in range(total_frames):
        cam_overlay_path = namespace + ":overlays" + "/" + video_name + "/" + str(i + 1)
        frames.append('execute if score ' + video_name + ' videos matches ' + str(i + 1) + ' run item replace entity @p armor.head with glass[equippable={slot:"head", camera_overlay: "' + cam_overlay_path + '"}]\n')

    os.makedirs(functions_output_path + "/" + video_name, exist_ok=True)
    with open(functions_output_path + "/" + video_name + "/show_frames.mcfunction", "w") as f:
        f.write("scoreboard players add " + video_name + " videos 1\n")
        f.writelines(frames)
        f.write('execute if score ' + video_name + ' videos matches ' + str(total_frames + 1) + ' run item replace entity @p armor.head with air\n')
        f.write("execute if score testvid videos matches .." + str(total_frames + 1) + " run schedule function " + namespace + ":" + video_name + "/show_frames 1t append")
    
    with open(functions_output_path + "/" + video_name + "/play.mcfunction", "w") as f:
        f.write("scoreboard objectives add videos dummy\n")
        f.write("scoreboard players reset " + video_name + " videos\n")
        f.write("function " + namespace + ":" + video_name + "/show_frames\n")

    with open(functions_output_path + "/" + video_name + "/stop.mcfunction", "w") as f:
        f.write("scoreboard players set " + video_name + " videos " + str(total_frames))