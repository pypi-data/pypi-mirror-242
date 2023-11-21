from moviepy.editor import VideoFileClip

class changementvideo_en_gif:
    def video_to_gif(input_video, output_gif, duree_maximum=10, fps=10):
        #pou chaje video a
        video_chargement = VideoFileClip(input_video)
        video_chargement = video_chargement.subclip(0, min(video_chargement.duration, duree_maximum))
        # Converti video a en gif pandan lap genbe duree a
        video_chargement.write_gif(output_gif, fps=fps)
