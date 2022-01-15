from settings import *

def grid_data_load():
    '''Returns sector coordinates (x, y), x range, y range, xcenter, ycenter'''
    # cell pos and corresponding real xy range pos
    grid_data = []
    for grid_row in range(0, N_ROWS):
        ycurrent = grid_row * CELL_SIZE + GRID_ORIGIN[1]
        for grid_col in range(0, N_COLS):
            xcurrent = grid_col * CELL_SIZE + GRID_ORIGIN[0]
            ypos = ycurrent
            for y in range(0, CELL_SIZE):
                xpos = xcurrent
                for x in range(0, CELL_SIZE):
                    sector = (grid_col, grid_row)
                    global_pos = (xpos, ypos)
                    local_pos = (x, y)
                    sector_start = (xcurrent, ycurrent)
                    xrange = (xcurrent, xpos)
                    yrange = (ycurrent, ypos)
                    xcenter = (xpos - (CELL_SIZE / 2) + 1)
                    ycenter = (ypos - (CELL_SIZE / 2) + 1)
                    xpos += 1
                ypos += 1
            grid_data.append([sector, xrange, yrange, xcenter, ycenter])
    return grid_data

def grid_map_pop():
    '''Returns a list holding integers 0'''
    sect_map = []
    for y in range(0, N_ROWS):
        row_list = []
        for x in range(0, N_COLS):
            row_list.append(0)
        sect_map.append(row_list)
    return sect_map