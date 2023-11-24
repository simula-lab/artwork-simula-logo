# simula-logo



## Getting started

The logo of Simula is not easy to get right. This is a project to automate the generation of the the Penrose-Tiling based logo of simula.
The repository contains tools useful for graphic designers as well as for software developers.

## python-scripts

this folder contains several python scripts. So far the following scripts exists. The usage of the scripts is described in subsequent sections of this README.md file.

### installing the python tool

navigate to the folder `./python-scripts/` then run the command:

`pip3 install .`

this will install the python package `simula-logo-generator` and the command line tool `generate_simula_logo`

### using the `generate_simula_logo` command line tool.

```
% generate_simula_logo -h

usage: generate_simula_logo [-h] [--scale SCALE] [--base-stroke-width BASE_STROKE_WIDTH] [--stroke-colour STROKE_COLOUR] [--tile-opacity TILE_OPACITY] [--Stile-colour STILE_COLOUR] [--Ltile-colour LTILE_COLOUR] [--random-tile-colours]
                            [--svg-output SVG_OUTPUT] [--png-output PNG_OUTPUT]

Generate Simula logo in SVG and PNG formats.

options:
  -h, --help            show this help message and exit
  --scale SCALE         Scale of the logo
  --base-stroke-width BASE_STROKE_WIDTH
                        Base stroke width
  --stroke-colour STROKE_COLOUR
                        Stroke colour
  --tile-opacity TILE_OPACITY
                        Tile opacity: float from 0 (tolally transparent) to 1 (totally opaque)
  --Stile-colour STILE_COLOUR
                        S tile colour
  --Ltile-colour LTILE_COLOUR
                        L tile colour
  --random-tile-colours
                        Use random tile colours
  --svg-output SVG_OUTPUT
                        Output filename for SVG
  --png-output PNG_OUTPUT
                        Output filename for PNG

```

