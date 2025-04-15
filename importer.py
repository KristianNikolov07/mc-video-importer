import subprocess
import os

video_file_path = "input.mp4"
resource_pack_path = "output"
datapack_path = "functions"
video_name = "test"
namespace = "test"

def ConvertVideo(video_file_path, resource_pack_path):
    subprocess.run('ffmpeg -i ' + video_file_path + ' -vf "fps=20" ' + resource_pack_path + '/%d.png', shell=True)

def GenerateDatapack(resource_pack_path, datapack_path, video_name, namespace):
    total_frames = len(os.listdir(resource_pack_path))
    frames = []
    for i in range(total_frames):
        cam_overlay_path = namespace + ":overlays" + "/" + video_name + "/" + str(i + 1)
        frames.append('execute if score ' + video_name + ' videos matches ' + str(i + 1) + ' run item replace entity @a armor.head with glass[equippable={slot:"head", camera_overlay: "' + cam_overlay_path + '"}]\n')

    os.mkdir(datapack_path + "/" + video_name)
    with open(datapack_path + "/" + video_name + "/play.mcfunction", "w") as f:
        f.write("scoreboard objectives add videos dummy\n")
        f.write("scoreboard players add " + video_name + " event 1\n")
        f.writelines(frames)
        f.write("schedule function " + namespace + ":" + video_name + "/play 1t append")

ConvertVideo(video_file_path, resource_pack_path)

GenerateDatapack(resource_pack_path, datapack_path, video_name, namespace)