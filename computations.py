from settings import *

def sector_load():
    '''Returns a list -> with each sectors coordinates and x y range'''
    sector_data = []
    for grid_row in range(0, N_ROWS):
        ycurrent = grid_row * GRIDSTEP
        for grid_col in range(0, N_COLS):
            xcurrent = grid_col * GRIDSTEP
            ypos = ycurrent
            for y in range(0, GRIDSTEP):
                xpos = xcurrent
                for x in range(0, GRIDSTEP):
                    sector = (grid_col, grid_row)
                    global_pos = (xpos, ypos)
                    local_pos = (x, y)
                    sector_start = (xcurrent, ycurrent)
                    xrange = (xcurrent, xpos)
                    yrange = (ycurrent, ypos)
                    xpos += 1
                ypos += 1
            sector_data.append([sector, xrange, yrange])
    return sector_data

def sector_map_pop():
    sect_map = []
    for y in range(0, N_COLS):
        for x in range(0, N_ROWS):
            sect_map.append([0])
    return sect_map

def sector_anchors():
    spawns = []
    x = GRIDSTEP / 2
    for n in range(0, N_COLS):
        spawns.append(int(x))
        x += GRIDSTEP
    return spawns