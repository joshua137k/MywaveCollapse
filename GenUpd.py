NUM_PARTS = 4
DIM = 50
tasks = []
for i in range(NUM_PARTS):
    for j in range(NUM_PARTS):
        start_x = i * (DIM // NUM_PARTS)
        end_x = (i + 1) * (DIM // NUM_PARTS)
        start_y = j * (DIM // NUM_PARTS)
        end_y = (j + 1) * (DIM // NUM_PARTS)
        print(f"update_matrix_part(grid, {start_x}, {end_x}, {start_y}, {end_y})")