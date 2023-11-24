import logging
import math
from penrose_p3 import PenroseP3
from btiles import BtileL
from PIL import Image
import argparse
import cairosvg


def generate_simula_logo_svg(scale=100, base_stroke_width=0.02, stroke_colour='#000', tile_opacity=0, Stile_colour="#fff", Ltile_colour="#fff", random_tile_colours=False):
    try:
        ngen = 3
        config = {
            'width': '100%', 
            'height': '100%',
            'stroke-colour': stroke_colour,
            'base-stroke-width': base_stroke_width,
            'margin': 1.05,
            'tile-opacity': 0,
            'Stile-colour': Stile_colour,
            'Ltile-colour': Ltile_colour,
            'random-tile-colours': random_tile_colours,
            'rotate': 3*math.pi/2,
            'reflect-x': True
        }       
        tiling = PenroseP3(scale, ngen, config) 
        psi = (math.sqrt(5) - 1) / 2
        theta = 2*math.pi / 5
        rot = math.cos(theta) + 1j*math.sin(theta)
        xOffset = 0
        A = -scale/2 + 0j + xOffset
        B = scale/2 * rot + xOffset
        C = scale/2 / psi + 0j + xOffset
        tiling.set_initial_tiles([BtileL(A, B, C)])
        tiling.make_tiling()
        del tiling.elements[14:]
        del tiling.elements[8:10]
        del tiling.elements[0:2]
        svg_text = tiling.make_svg()
        return svg_text
    except Exception as e:
        logging.error(e)
        raise e

def autocrop_image_with_transparency(input_path, output_path):
    with Image.open(input_path) as image:
        # Convert the image to RGBA if it's not already in that mode
        image = image.convert("RGBA")

        # Get the bounding box of the non-transparent part of the image
        bbox = image.getbbox()

        # Crop the image to the bounding box
        if bbox:
            cropped_image = image.crop(bbox)
            cropped_image.save(output_path)

def main():
    try:
        parser = argparse.ArgumentParser(description="Generate Simula logo in SVG and PNG formats.")
        parser.add_argument("--scale", type=int, default=200, help="Scale of the logo")
        parser.add_argument("--base-stroke-width", type=float, default=0.02, help="Base stroke width")
        parser.add_argument("--stroke-colour", default="#000", help="Stroke colour")
        parser.add_argument("--tile-opacity", type=float, default=0, help="Tile opacity: float from 0 (tolally transparent) to 1 (totally opaque)")
        parser.add_argument("--Stile-colour", default="#fff", help="S tile colour")
        parser.add_argument("--Ltile-colour", default="#fff", help="L tile colour")
        parser.add_argument("--random-tile-colours", action='store_true', help="Use random tile colours")
        parser.add_argument("--svg-output", default="simula-logo.svg", help="Output filename for SVG")
        parser.add_argument("--png-output", default="simula-logo.png", help="Output filename for PNG")

        args = parser.parse_args()

        # A simple example starting with a BL tile
        scale = 200
        svg_text = generate_simula_logo_svg(scale, base_stroke_width=0.02, stroke_colour='#000', tile_opacity=0, Stile_colour='#fff', Ltile_colour='#fff', random_tile_colours=False)
        with open(args.svg_output, 'w') as f:
            f.write(svg_text)        
        cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), write_to=args.png_output, output_height=1080,output_width=1080)
        autocrop_image_with_transparency(args.png_output, args.png_output)

    except Exception as e:
        logging.error(e)
        raise e    

if __name__=="__main__":
    main()