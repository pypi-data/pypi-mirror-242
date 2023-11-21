from durevideo import videoduree
from videogif import changementvideo_en_gif

inputla = "C:\\Users\\barbara\\Desktop\\videotogiffy\\video\\WIN.mp4"
inputla1 = inputla.replace(".mp4", "")

if videoduree.dure(inputla) <= 10:
    changementvideo_en_gif.video_to_gif(f"{inputla}", f"{inputla1}.gif", fps=10)
else:
    print("video a pa dwe dire plis ke 10s tandiske videow la dire", videoduree.dure(inputla), "s")
