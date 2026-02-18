

# Describes the colors in ARGB format to assign to each cell status depending on the simulation type
colorsets = {
    'brian': {
        0: 0xffffffff,
        1: 0xff00ff00,
        10: 0xff000000
    },
    'conway': {
        0: 0xffffffff,
        1: 0xff000000,
        10: 0xff000000
    }
}


presets = {
    'R-pentomino': [
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]
    ],
    'B-heptomino': [
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [0, 1, 0, 0]
    ],

}