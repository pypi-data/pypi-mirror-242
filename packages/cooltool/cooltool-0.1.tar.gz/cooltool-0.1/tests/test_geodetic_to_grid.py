from lindvall_tools.geodesy.geodetic_to_grid import geodetic_to_grid

def test_geodetic_to_grid():
    input_var = [
            [(55, 0, 0), (12, 45, 0)],
            [(55, 0, 0), (14, 15, 0)],
            [(57, 0, 0), (12, 45, 0)],
            [(57, 0, 0), (19, 30, 0)],
            [(59, 0, 0), (11, 15, 0)],
            [(59, 0, 0), (19, 30, 0)],
        ]
    result = [
            [6097106.672, 356083.438],
            [6095048.642, 452024.069],
            [6319636.937, 363331.554],
            [6326392.707, 773251.054],
            [6546096.724, 284626.066],
            [6548757.206, 758410.519],
        ]
    for i, var in enumerate(input_var):
        assert geodetic_to_grid(phi=var[0], lam=var[1], ellipsoid='GRS1980', projection='SWEREF99TM') == (result[i][0], result[i][1])
