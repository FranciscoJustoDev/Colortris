from settings import *

def sector_load():
    '''Returns a list -> tuple ->sector coordinates, tuple -> x range, tuple -> y range'''
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
                    xcenter = (xpos - (GRIDSTEP / 2))
                    ycenter = (ypos - (GRIDSTEP / 2))
                    xpos += 1
                ypos += 1
            sector_data.append([sector, xrange, yrange, xcenter, ycenter])
    return sector_data

def sector_map_pop():
    '''Returns a list holding integers 0'''
    sect_map = []
    for y in range(0, N_ROWS):
        row_list = []
        for x in range(0, N_COLS):
            row_list.append(0)
        sect_map.append(row_list)
    return sect_map