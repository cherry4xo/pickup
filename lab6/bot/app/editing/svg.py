import os
from svgwrite import Drawing
from svgwrite.shapes import Ellipse
from svgwrite.path import Path
from svgwrite.text import TextPath, Text
from math import pi, cos, sin, radians, degrees


# def make_circle(size: int, 
#                 border: int, 
#                 text: str, 
#                 font_size:int, 
#                 round_c, 
#                 text_c, 
#                 round_opacity: float, 
#                 angle: int, 
#                 id: str):
#     dwg = Drawing(f"{id}.svg", (size, size))
#     text = text + "‎"

#     c = size // 2
#     r = (size - border) // 2
#     angle = radians(angle) - pi / 2
#     ellipse = Ellipse(center=(c, c), 
#                       r=(r, r), 
#                       stroke=f"rgb({round_c[0]}, {round_c[1]}, {round_c[2]})", 
#                       fill_opacity=0, 
#                       stroke_width=f"{border}",
#                       opacity=round_opacity)

#     dwg.add(ellipse)
    
#     border *= 0.75
#     r_path = size // 2 - border 
#     center = size // 2
#     text_length = 2 * pi * r_path
    
#     path_form = f"""M {center * (1 - cos(angle)) + border * cos(angle)} {center * (1 - sin(angle)) + border * sin(angle)}
#                     A {r_path} {r_path} 0 1 1 {center * (1 - cos(angle + pi)) + border * cos(angle + pi)} {center * (1 - sin(angle + pi)) + border * sin(angle + pi)}
#                     M {center * (1 - cos(angle + pi)) + border * cos(angle + pi)} {center * (1 - sin(angle + pi)) + border * sin(angle + pi)}
#                     A {r_path} {r_path} 0 1 1 {center * (1 - cos(angle)) + border * cos(angle)} {center * (1 - sin(angle)) + border * sin(angle)}
#                 """

#     path = Path(path_form, fill_opacity=0)

#     dwg.add(path)

#     text = Text(text="", 
#                 fill=f"rgb({text_c[0]}, {text_c[1]}, {text_c[2]})", 
#                 style=f"font-size:{font_size}px; font-family:Arial",
#                 textLength=text_length,
#                 lengthAdjust="spacing")
#     text.add(TextPath(path=path, 
#                       text=text, 
#                       method='align', 
#                       spacing='exact'))
#     dwg.add(text)
#     dwg.save()
#     os.system(f"inkscape {id}.svg -o {id}.png")
#     os.remove(f"{id}.svg")


def make_circle(size: int, 
                text: str,
                font_text: str,
                font_size: int,
                font_weight: int,
                text_color: str,
                border: int,
                border_color: str,
                border_opacity: float,
                angle: int,
                id: str):
    image_name = "".join(id.split("."))[:-1]
    dwg = Drawing(f"{image_name}.svg", (size, size))
    text = text + "‎"

    c = size // 2
    r = (size - border) // 2
    angle = radians(angle) - pi / 2
    ellipse = Ellipse(center=(c, c), 
                      r=(r, r), 
                      stroke=border_color, 
                      fill_opacity=0, 
                      stroke_width=f"{border}",
                      opacity=border_opacity)

    dwg.add(ellipse)
    
    border *= 0.75
    r_path = size // 2 - border 
    center = size // 2
    text_length = 2 * pi * r_path
    
    path_form = f"""M {center * (1 - cos(angle)) + border * cos(angle)} {center * (1 - sin(angle)) + border * sin(angle)}
                    A {r_path} {r_path} 0 1 1 {center * (1 - cos(angle + pi)) + border * cos(angle + pi)} {center * (1 - sin(angle + pi)) + border * sin(angle + pi)}
                    M {center * (1 - cos(angle + pi)) + border * cos(angle + pi)} {center * (1 - sin(angle + pi)) + border * sin(angle + pi)}
                    A {r_path} {r_path} 0 1 1 {center * (1 - cos(angle)) + border * cos(angle)} {center * (1 - sin(angle)) + border * sin(angle)}
                """

    path = Path(path_form, fill_opacity=0)

    dwg.add(path)

    text_obj = Text(text="", 
                fill=text_color, 
                style=f"font-size:{font_size}px; font-family:{font_text}; font-weight:{font_weight}",)
                # textLength=text_length,)
                # lengthAdjust="spacing")
    text_obj.add(TextPath(path=path, 
                      text=text, 
                      method='align', ))
                    #   spacing='exact'))
    dwg.add(text_obj)
    dwg.save()
    
    os.system(f"inkscape {image_name}.svg -o {image_name}.png")
    os.remove(f"{image_name}.svg")


# make_circle(800, 50, "sample sample", 50, (99, 57, 116), (214, 137, 16), 0.7, 90, id="another_try")

# make_circle(600, "SAMPLE SAMPLE SAMPLE", "Arial", 40, 100, "rgb(0, 0, 0)", 50, "rgb(255, 255, 255)", 0.5, 90, "another try")


def make_text(size: int, offset: int, text: str, text_weight: int, font_family: str, font_size: int, text_c: tuple, image_name: str):
    dwg = Drawing(f"{id}.svg", size=(size, size), debug=True)

    dwg.add(Text(text=text, 
                 fill=f"rgb({text_c[0]}, {text_c[1]}, {text_c[2]})", 
                 x=[size//2],
                 y=[size//2 + offset],
                 style=f"font-size:{font_size}px; font-family:{font_family}; text-weight:{text_weight}",
                 text_anchor="middle"))
    
    dwg.save()
    os.system(f"inkscape {image_name}.svg -o {image_name}.png")
    os.remove(f"{image_name}.svg")


# make_text(576, 50, "sample sample sample", 32, (255, 255, 255), "1337")
    
