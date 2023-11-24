import matplotlib
import cycler

from .colors import RGB, Color, colors

def setColorCycleX():
    n = [5, 11, 29, 21, 15, 39, 6, 34, 9, 27, 20, 38]
    c = []
    for i in n:
        c.append(swatch[i][1].hex_format())
    matplotlib.rcParams['axes.prop_cycle'] = cycler.cycler(color=c)

def setColorCycle(column=3):
    c = []
    for i in range(column, len(swatch), 6):
        c.append(swatch[i][1].hex_format())
    matplotlib.rcParams['axes.prop_cycle'] = cycler.cycler(color=c)

#
# Some default parameters I'd like to use
#

def useTheme(theme='light'):
    matplotlib.rcParams['font.family'] = 'serif'
    matplotlib.rcParams['font.serif'] = ['Arial']
    matplotlib.rcParams['font.sans-serif'] = ['System Font', 'Verdana', 'Arial']
    matplotlib.rcParams['figure.figsize'] = (8, 4)
    matplotlib.rcParams['figure.dpi'] = 108
    matplotlib.rcParams['legend.frameon'] = False
    # matplotlib.rcParams['legend.labelspacing'] = 0.5
    # matplotlib.rcParams['axes.linewidth'] = 0.5
    # matplotlib.rcParams['axes.labelsize'] = 10
    # matplotlib.rcParams['axes.labelpad'] = 4.0
    # matplotlib.rcParams['axes.labelweight'] = 'normal'
    # matplotlib.rcParams['axes.titleweight'] = 'normal'
    # matplotlib.rcParams['axes.titlesize'] = 12
    # matplotlib.rcParams['axes.titlepad'] = 6.0
    # matplotlib.rcParams['axes.formatter.limits'] = [-5, 5]

    if theme == 'light':
        matplotlib.rcParams['figure.facecolor'] = 'white'
        matplotlib.rcParams['axes.facecolor'] = 'white'
        matplotlib.rcParams['axes.edgecolor'] = 'black'
        matplotlib.rcParams['axes.labelcolor'] = 'black'
        matplotlib.rcParams['xtick.color'] = 'black'
        matplotlib.rcParams['ytick.color'] = 'black'
        matplotlib.rcParams['text.color'] = 'black'
        matplotlib.rcParams['legend.facecolor'] = 'white'
        matplotlib.rcParams['legend.edgecolor'] = 'white'
        matplotlib.rcParams['lines.markeredgecolor'] = 'black'
        matplotlib.rcParams['lines.markerfacecolor'] = 'black'
    elif theme == 'dark':
        matplotlib.rcParams['figure.facecolor'] = 'black'
        matplotlib.rcParams['axes.facecolor'] = 'black'
        matplotlib.rcParams['axes.edgecolor'] = 'white'
        matplotlib.rcParams['axes.labelcolor'] = 'white'
        matplotlib.rcParams['xtick.color'] = 'white'
        matplotlib.rcParams['ytick.color'] = 'white'
        matplotlib.rcParams['text.color'] = 'white'
        matplotlib.rcParams['legend.facecolor'] = 'black'
        matplotlib.rcParams['legend.edgecolor'] = 'black'
        matplotlib.rcParams['lines.markeredgecolor'] = 'white'
        matplotlib.rcParams['lines.markerfacecolor'] = 'white'


highlight = [0.85, 0.96, 0]

# Make a list out of it
colorList = list(colors.items())

# The first color palette
idx = [433, 303, 290, 401, 537, 336, 129, 127, 270, 15, 142, 513, 90, 56, 325, 373, 460, 87, 59, 517, 521, 476, 348, 343, 356, 286, 107, 108, 531, 118, 124, 124, 229, 217, 202, 179, 404, 213, 544, 516, 482, 21]

swatch = [colorList[x] for x in idx]
swatchn = [[c[1].red, c[1].green, c[1].blue] for c in swatch]
swatchInHex = [x[1].hex_format() for x in swatch]

idx = [5, 11, 29, 21, 15, 39, 6, 34, 9, 27, 20, 38]
linecolors = [swatchInHex[i] for i in idx]

setColorCycleX()
