import subprocess
import os
import json

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
        '    "pack_format": 57,\n' \
        '    "supported_formats": [57, 71]'
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
        '    "pack_format": 41,\n' \
        '    "supported_formats": [41, 63]\n' \
        '  }\n' \
        '}')
    os.makedirs(resourcepack_path + "/assets", exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace, exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace + "/textures", exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace + "/textures/overlays", exist_ok=True)
    os.makedirs(resourcepack_path + "/assets/" + namespace + "/sounds", exist_ok=True)

def ConvertVideo(video_file_path, namespace, video_name):
    output_folder_path = resourcepack_path + "/assets/" + namespace + "/textures/overlays/" + video_name
    os.makedirs(output_folder_path, exist_ok=True)
    subprocess.run('ffmpeg -i ' + video_file_path + ' -vf "fps=20" ' + output_folder_path + '/%d.png', shell=True)

def ExportSound(video_file_path, namespace, video_name):
    output_path = resourcepack_path + "/assets/" + namespace + "/sounds/" + video_name
    subprocess.run('ffmpeg -i ' + video_file_path + ' -vn -acodec libvorbis ' + output_path + '.ogg', shell=True)

def GenerateSoundsJson(namespace, video_name):
    file_path = resourcepack_path + "/assets/" + namespace + "/sounds.json"
    sounds_json = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            sounds_json = json.load(f)
        
    sounds_json[video_name] = {
        "sounds":[
            namespace + ":" + video_name
        ]
    }

    with open(file_path, "w") as f:
        json.dump(sounds_json, f, indent=4)

def GenerateFunctions(video_name, namespace):
    video_frames_path = resourcepack_path + "/assets/" + namespace + "/textures/overlays/" + video_name
    functions_output_path =  datapack_path + "/data/" + namespace + "/function"
    total_frames = len(os.listdir(video_frames_path))
    frames = []
    for i in range(total_frames):
        cam_overlay_path = namespace + ":overlays" + "/" + video_name + "/" + str(i + 1)
        frames.append('execute if score ' + video_name + ' videos matches ' + str(i + 1) + ' run item replace entity @a[tag=watches_' + video_name + '] armor.head with glass[equippable={slot:"head", camera_overlay: "' + cam_overlay_path + '"}]\n')

    os.makedirs(functions_output_path + "/" + video_name, exist_ok=True)

    #show_frames.mcfunction
    with open(functions_output_path + "/" + video_name + "/show_frames.mcfunction", "w") as f:
        f.write("scoreboard players add " + video_name + " videos 1\n")
        f.writelines(frames)
        f.write('execute if score ' + video_name + ' videos matches ' + str(total_frames + 1) + ' run item replace entity @a[tag=watches_' + video_name + '] armor.head with air\n')
        f.write('execute if score ' + video_name + ' videos matches ' + str(total_frames + 1) + ' run tag @a[tag=watches_' + video_name + '] remove watches_' + video_name + '\n')
        f.write("execute if score " + video_name + " videos matches .." + str(total_frames + 1) + " run schedule function " + namespace + ":" + video_name + "/show_frames 1t append")
    
    #play.mcfunction
    with open(functions_output_path + "/" + video_name + "/play.mcfunction", "w") as f:
        f.write("tag @s add watches_" + video_name + "\n")
        f.write("playsound " + namespace + ":" + video_name + " master @s ~ ~ ~ \n")
        f.write("scoreboard objectives add videos dummy\n")
        f.write("scoreboard players reset " + video_name + " videos\n")
        f.write("function " + namespace + ":" + video_name + "/show_frames\n")

    #stop.mcfunction
    with open(functions_output_path + "/" + video_name + "/stop.mcfunction", "w") as f:
        f.write("scoreboard players set " + video_name + " videos " + str(total_frames) + "\n")
        f.write('item replace entity @a[tag=watches_' + video_name + '] armor.head with air\n')
        f.write("stopsound @a[tag=watches_" + video_name + "]\n")
        f.write("tag @a[tag=watches_" + video_name + "] remove watches_" + video_name)