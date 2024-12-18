from moviepy.editor import *
import numpy as np
from app.editing.svg import make_circle, make_text

    
def make_rounded(filename, size, text, font_text, font_size, font_weight, text_color, border, border_color, border_opacity, angle):
    video = VideoFileClip(filename)
    video = video.resize((576, 576))
    make_circle(size=size, 
                text=text, 
                font_text=font_text, 
                font_size=font_size, 
                font_weight=font_weight, 
                text_color=text_color, 
                border=border, 
                border_color=border_color, 
                border_opacity=border_opacity, 
                angle=angle,
                id=filename)

    # bg_image = ColorClip(size=(size, size), color=(255, 255, 255), duration=video.duration)
    image_name = "".join(filename.split("."))[:-1]
    image = ImageClip(f"{image_name}.png").set_duration(video.duration)
    os.remove(f"{image_name}.png")

    filename_out = "".join(filename.split("."))[:-1] + "temp.mp4"
    final = CompositeVideoClip([video.set_position("center", "center"), image.set_position("center", "center")])
    final.write_videofile(
        filename_out,
        codec="libx264",
        fps=60, 
        logger=None)
    

# make_rounded("app/data/another_sample.mp4", 576, 80, "samplesamplesample", 54, (99, 57, 116), (214, 137, 16), 0.7, 135, "228")


def overlay_text(filename, size, offset, text, text_weight, font_family, font_size, text_c, image_name):
    video = VideoFileClip(filename)
    video = video.resize((600, 600))
    make_text(size=size, offset=offset, text=text, text_weight=text_weight, font_family=font_family, font_size=font_size, text_c=text_c, image_name=image_name)

    text = ImageClip(f"{id}.png").set_duration(video.duration)

    filename_out = "".join(filename.split("."))[:-1] + "temp.mp4"
    final = CompositeVideoClip([video.set_position("center", "center"), text.set_position("center", "center")])
    final.write_videofile(
        filename_out,
        codec="libx264",
        fps=60
    )


def make_watermark(filename: str, opacity: float, offsetX: int, offsetY: int, picture_file_path: str) -> None:
    video = VideoFileClip(filename)
    video = video.resize((600, 600))
    image = ImageClip(picture_file_path).set_duration(video.duration).set_opacity(opacity)
    image_y = image.size[1]
    scale = 200 / image_y
    image = image.resize(scale)

    filename_out = "".join(filename.split("."))[:-1] + "temp.mp4"
    position = (video.size[0] // 2 + offsetX - image.size[0] // 2, video.size[1] // 2 + 150 - image.size[1] // 2)
    final = CompositeVideoClip([video, image.set_position(position)], size=(600, 600))
    final.write_videofile(
        filename_out,
        codec="libx264",
        fps=60, 
        logger=None
    )


def make_default_rounded(filename: str) -> None:
    video = VideoFileClip(filename)
    video = video.resize((600, 600))
    filename_out = "".join(filename.split("."))[:-1] + "temp.mp4"
    video.write_videofile(
        filename_out,
        codec="libx264",
        fps=60,
        logger=None
    )
