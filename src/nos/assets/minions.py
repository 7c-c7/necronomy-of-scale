from pathlib import Path

import nos.assets as assets

# Skeleton Archer, a basic enemy.
SKELETON_ARCHER = assets.AnimatedAsset(
    path=Path("assets/Skeleton_Archer.png"),
    tile_size=(32, 34),
    static_tile=(2, 0),
    animation_tiles={
        "idle": [(0, 0), (1, 0)],
        "celebrating": [(1, 0), (3, 0)],
        "standing": [(2, 0)],
        "walking": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "attacking": [(3, 0), (0, 0), (0, 1), (1, 0)],
        "dead": [(2, 1)],
    },
    frame_duration={"idle": 40, "celebrating": 40, "walking": 40, "attacking": 40},
    colorkey=(255, 0, 255),
)

# Skeleton Swordsman, an even basic-er enemy.
SKELETON_SWORDSMAN = assets.AnimatedAsset(
    path=Path("assets/Skeleton_Swordsman.png"),
    tile_size=(32, 32),
    static_tile=(1, 0),
    animation_tiles={
        "idle": [(0, 0), (2, 0)],
        "celebrating": [(1, 0), (0, 1)],
        "standing": [(2, 0)],
        "walking": [(0, 0), (1, 0), (2, 0), (0, 1)],
        "attacking": [(1, 0), (0, 1), (1, 1), (0, 0), (2, 0)],
        "dead": [(2, 1)],
    },
    frame_duration={"idle": 40, "celebrating": 40, "walking": 40, "attacking": 40},
    colorkey=(255, 0, 255),
)
