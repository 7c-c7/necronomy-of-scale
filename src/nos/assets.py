from __future__ import annotations

import dataclasses

import pygame as pg
from pathlib import Path

import nos
from nos import config


def load_asset(path: Path) -> pg.Surface:
    img = pg.image.load(path)
    img.set_colorkey((0, 0, 0))
    return img.convert_alpha()


def load_assets(paths: list[Path]) -> list[pg.Surface]:
    return [load_asset(path) for path in paths]


def load_directory(directory: Path) -> list[pg.Surface]:
    """
    Load all assets in a directory. Directory must contain only image files.
    Parameters
    ----------
    directory : Path
        The directory containing the image files.

    Returns
    -------
    list[pg.Surface]: the images loaded from the directory.
    """
    return load_assets([directory / file for file in directory.iterdir()])


@dataclasses.dataclass
class Asset:
    path: Path = None
    spritesheet: pg.Surface = None
    tile_size: tuple[int, int] = None
    scale: float | tuple[float, float] = (1, 1)
    static_tile: tuple[int, int] = (0, 0)
    offset: tuple[int, int] = (0, 0)
    colorkey: tuple[int, int, int] = (0, 0, 0)
    """
    Attributes
    ----------
    path : Path
        The path to the image file.
    spritesheet : pg.Surface
        The image file.
    tile_size : tuple[int, int]
        The size of the tiles in the spritesheet.
    scale : float | tuple[float, float]
        The scale to apply to images from the spritesheet.
    static_tile : tuple[int, int]
        The tile to use as the static image, in tile indices (default is (0, 0)).
    offset : tuple[int, int]
        The offset of the (0, 0) tile from the top left corner of the spritesheet.
    colorkey : tuple[int, int, int]
        The color to use as the transparency mask for the spritesheet.
    """

    def __post_init__(self):
        if not self.path and not self.spritesheet:
            raise ValueError("Either path or image must be provided.")
        if self.path and self.spritesheet:
            raise ValueError("Only one of path or image must be provided.")
        if self.path:
            self.spritesheet = pg.image.load(self.path)
            self.spritesheet.set_colorkey(self.colorkey)
        self.scale: tuple[float, float] = (
            self.scale if isinstance(self.scale, tuple) else (self.scale, self.scale)
        )

    def load(self) -> None:
        self.spritesheet = self.spritesheet.convert_alpha()
        self.tile_size = self.tile_size or self.spritesheet.get_size()
        if self.scale != (1.0, 1.0):
            self.spritesheet = pg.transform.scale(
                self.spritesheet,
                (
                    int(self.spritesheet.size[0] * self.scale[0]),
                    int(self.spritesheet.size[1] * self.scale[1]),
                ),
            )
            self.tile_size = (
                int(self.tile_size[0] * self.scale[0]),
                int(self.tile_size[1] * self.scale[1]),
            )
            self.offset = (
                int(self.offset[0] * self.scale[0]),
                int(self.offset[1] * self.scale[1]),
            )

    def rect_from_tile(self, tile: tuple[int, int]) -> pg.Rect:
        x, y = (
            self.offset[0] + tile[0] * self.tile_size[0],
            self.offset[1] + tile[1] * self.tile_size[1],
        )
        return pg.Rect((x, y), self.tile_size)

    def tile_from_coordinates(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        x, y = coordinates
        return x // self.tile_size[0], y // self.tile_size[1]

    def get_tile(self, tile: tuple[int, int]) -> pg.Surface:
        return self.spritesheet.subsurface(self.rect_from_tile(tile))

    @property
    def image(self) -> pg.Surface:
        return self.get_tile(self.static_tile)

    @classmethod
    def stack(
        cls,
        assets: list[Asset],
        tiles: list[tuple[int, int]] = None,
        offsets: list[tuple[int, int]] = None,
        scale: float | tuple[float, float] = (1, 1),
    ) -> Asset:
        offsets = offsets or [(0, 0) for _ in assets]
        tiles = tiles or [asset.static_tile for asset in assets]
        size = (
            max(asset.get_tile(tile).size[0] for asset, tile in zip(assets, tiles)),
            max(asset.get_tile(tile).size[1] for asset, tile in zip(assets, tiles)),
        )
        spritesheet = pg.Surface(size, pg.SRCALPHA)
        for asset, offset in zip(assets, offsets):
            spritesheet.blit(asset.get_tile(asset.static_tile), offset)
        return Asset(
            spritesheet=spritesheet,
            tile_size=size,
            scale=scale,
        )


@dataclasses.dataclass
class AnimatedAsset(Asset):
    animation_tiles: dict[str, list[tuple[int, int]]] = dataclasses.field(
        default_factory=dict
    )
    frame_duration: int | dict[str, int | list[int]] = 5
    loop: bool | dict[str, bool] = True
    animations: dict[str, nos.Animation] = dataclasses.field(
        init=False, default_factory=dict
    )

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.loop, bool):
            self.loop = {state: self.loop for state in self.animation_tiles}
        if isinstance(self.frame_duration, int):
            self.frame_duration = {
                state: self.frame_duration for state in self.animation_tiles
            }
        for state in self.animation_tiles:
            if state not in self.loop:
                self.loop[state] = True
            if state not in self.frame_duration:
                self.frame_duration[state] = 5
        for state, tiles in self.animation_tiles.items():
            if isinstance(self.frame_duration[state], int):
                self.frame_duration[state] = [self.frame_duration[state] for _ in tiles]
            if not len(self.frame_duration[state]) == len(tiles):
                raise ValueError(
                    f"Specific frame durations for {state} must be given for each tile."
                )

    def load(self) -> None:
        super().load()
        self.animations = {
            state: nos.Animation(
                images=[self.get_tile(tile) for tile in tiles],
                img_duration=self.frame_duration[state],
                loop=self.loop[state],
            )
            for state, tiles in self.animation_tiles.items()
        }


DESKTOP = Asset(
    Path("assets/desktop.png"),
)

# Manifest, the main page.
MANIFEST_SPRITESHEET_POSITION_OFFSET = (176, 1040)
MANIFEST_SPRITESHEET_PAGE_SIZE = (592, 464)
PAGES = pg.image.load("assets/pages.png")
BORDERS = pg.image.load("assets/borders.png")
manifest_page = Asset(
    spritesheet=PAGES,
    tile_size=MANIFEST_SPRITESHEET_PAGE_SIZE,
    offset=MANIFEST_SPRITESHEET_POSITION_OFFSET,
)
manifest_border = Asset(
    spritesheet=BORDERS,
    tile_size=MANIFEST_SPRITESHEET_PAGE_SIZE,
    offset=MANIFEST_SPRITESHEET_POSITION_OFFSET,
)
MANIFEST = Asset.stack(
    [manifest_page, manifest_border],
    scale=(
        config.GAME["manifest"]["width"] / MANIFEST_SPRITESHEET_PAGE_SIZE[0],
        config.GAME["manifest"]["height"] / MANIFEST_SPRITESHEET_PAGE_SIZE[1],
    ),
)

# Card, what most things of importance will be displayed on.
CARD_SPRITESHEET_POSITION_OFFSET = (1927, 1445)
CARD_SPRITESHEET_SIZE = (74, 21)
CARD_SCALE = config.GAME["card"]["height"] / CARD_SPRITESHEET_SIZE[1]
card_page = Asset(
    spritesheet=PAGES,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SPRITESHEET_POSITION_OFFSET,
)
card_border = Asset(
    spritesheet=BORDERS,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SPRITESHEET_POSITION_OFFSET,
)
CARD = Asset.stack([card_page, card_border], scale=CARD_SCALE)
CARD_SELECT_BORDER_OFFSET = (1927, 1478)
CARD_SELECT_BORDER = Asset(
    spritesheet=BORDERS,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SELECT_BORDER_OFFSET,
    scale=CARD_SCALE,
)

# Skeleton Archer, a basic enemy.
SKELETON_ARCHER = AnimatedAsset(
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
SKELETON_SWORDSMAN = AnimatedAsset(
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


def load_all() -> None:
    """
    load all assets and optimize for use.
    """
    for maybe_asset in globals().values():
        if isinstance(maybe_asset, Asset):
            maybe_asset.load()


def clean_up() -> None:
    """
    Remove all construction assets to save memory.
    """
    for maybe_asset in globals().values():
        if not isinstance(maybe_asset, Asset):
            del maybe_asset


def initialize():
    load_all()
    clean_up()
