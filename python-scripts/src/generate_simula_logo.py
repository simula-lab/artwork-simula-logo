import logging
import math
from penrose_p3 import PenroseP3
from btiles import BtileL
# from IPython.display import SVG
import cairosvg

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
                'draw-tiles': True,
        #          'draw-arcs': False,
        #          'reflect-x': True,
        #          'draw-rhombuses': False,
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
        svg = tiling.make_svg()
        # SVG(svg)
        cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to='logo.png')
    except Exception as e:
        logging.error(e)
        raise e    

if __name__=="__main__":
    main()