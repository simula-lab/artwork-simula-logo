import logging
import math
from penrose_p3 import PenroseP3
from btiles import BtileL
# from IPython.display import SVG
import cairosvg
from PIL import Image

def main():
    try:
        # A simple example starting with a BL tile
        scale = 100

        ngen = 3

        config = {'width': '100%', 'height': '100%',
                'stroke-colour': '#000',
                'base-stroke-width': 0.02,
                'margin': 1.05,
                #'tile-opacity': 0,
        #          'random-tile-colours': True,
                'Stile-colour': '#fff',
                'Ltile-colour': '#fff',
        #          'Aarc-colour': '#f00',
        #          'Carc-colour': '#00f',
                # 'draw-tiles': True,
        #          'draw-arcs': False,
        #          'reflect-x': True,
                #  'draw-rhombuses': False,
                 'rotate': math.pi/2,
        #          'flip-y': False, 
        #          'flip-x': False,
        }        
        tiling = PenroseP3(scale, ngen, config)
        psi = (math.sqrt(5) - 1) / 2
        theta = 2*math.pi / 5
        rot = math.cos(theta) + 1j*math.sin(theta)
        xOffset = -50
        A = -scale/2 + 0j + xOffset
        B = scale/2 * rot + xOffset
        C = scale/2 / psi + 0j + xOffset

        tiling.set_initial_tiles([BtileL(A, B, C)])
        tiling.make_tiling()
        del tiling.elements[14:]
        del tiling.elements[8:10]
        del tiling.elements[0:2]
        svg_text = tiling.make_svg()
        with open('simula-logo.svg', 'w') as f:
            f.write(svg_text)

        cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), write_to='simula-logo.png', output_height=540,output_width=1080)
        autocrop_image_with_transparency('simula-logo.png', 'simula-logo.png')

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

if __name__=="__main__":
    main()