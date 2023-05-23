
from __future__ import annotations

import datetime
import sys
from abc import abstractmethod
from decimal import Decimal
from enum import Enum
from pikepdf import Page
from typing import (
    TypeVar,
    List
)

from pikepdf import ContentStreamInstruction

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal  # pragma: no cover

import delta_core._core

T = TypeVar('T', bound='Object')
Numeric = TypeVar('Numeric', int, float, Decimal)
Point = List[float]

class PdfMatrix:

    def __init__(self) -> None: ... # Returns Identity Matrix
    def __init__(self, matrix: PdfMatrix) -> None: ...
    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float) -> None: ...
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float

    def translated(self, x: float, y: float) -> PdfMatrix: ...
    def scaled(self, x: float, y: float) -> PdfMatrix: ...
    def rotated(self, angle: float) -> PdfMatrix: ...
    def transform_point(self, x: float, y: float) -> Point: ...
    def get_translation(self) -> list[float]: ...
    def get_rotation(self) -> float: ...
    def get_scale(self) -> list[float]: ...
    def get_skew(self) -> list[float]: ...
    def as_array(self) -> list[float]: ...

    def __mul__(self, other: PdfMatrix) -> PdfMatrix: ...

class TextState:

    def __init__(self) -> None: ...
    graphics_state: GraphicsState
    text_matrix: PdfMatrix
    line_matrix: PdfMatrix
    char_spacing: float
    word_spacing: float
    horizontal_scaling: float
    leading: float
    font: str
    font_size: float
    rendering_mode: int
    rise: float
    knockout: bool

    def rendering_matrix(self) -> PdfMatrix: ...

class GraphicsState:

    def __init__(self) -> None: ...
    CTM: PdfMatrix
    stroke_color_space: str
    fill_color_space: str
    stroke_color: list[float]
    fill_color: list[float]
    stroke_pattern: str
    fill_pattern: str
    text_state: TextState
    line_width: float
    line_cap: int
    line_join: int
    miter_limit: float
    dash_array: list[float]
    dash_phase: float
    rendering_intent: str
    stroke_adjustment: bool
    blend_mode: str
    soft_mask: str
    alpha_constant: float
    alpha_source: bool
    overprint: bool
    overprint_mode: int
    def clone(self) -> GraphicsState: ...

class PathSegment:

    class Type(Enum):
        MOVE_TO = 1
        LINE_TO = 2
        CURVE_TO = 3
        V_CURVE_TO = 4
        Y_CURVE_TO = 5
        CLOSE_PATH = 6

    def __init__(self, type) -> None: ...
    type: Type
    points: list[Point]

class GraphicsObject:

    class Type(Enum):
        Null = 0
        Path = 1
        Text = 2
        Image = 3
        Shading = 4
        InlineImage = 5
        Form = 6

    def __init__(self, type) -> None: ...
    type: Type
    start: int
    end: int
    invisible: bool
    points: list[list[float]]
    graphics_state: GraphicsState
    stroked: bool
    filled: bool
    is_clipping_path: bool
    text: str
    total_adjustment: float
    XObject_key: str
    XObject: any
    def get_bounding_box(self) -> list[float]: ...
    def get_contour(self, tolerance: float = 1.0) -> list[Point]: ...
    def get_path_segments(self) -> list[PathSegment]: ...
    def get_path_instructions(self) -> list[ContentStreamInstruction]: ...
    def is_visible(self) -> bool: ...
    def is_stroked(self) -> bool: ...
    def is_filled(self) -> bool: ...
    def is_clipping_path(self) -> bool: ...
    def get_text(self) -> str: ...
    def get_font_size(self) -> float: ...
    def get_xobject_key(self) -> str: ...
    def get_xobject(self) -> any: ...
    def get_width(self) -> float: ...
    def get_height(self) -> float: ...
    def get_image_width(self) -> float: ...
    def get_image_height(self) -> float: ...
    def get_image_resolution(self) -> list[float]: ...

class MarkedContent:

    def __init__(self) -> None: ...
    start: int
    end: int
    name: str
    tag: str
    properties_key: str
    properties: any
    graphics_objects: list[GraphicsObject]
    marked_contents: list[MarkedContent]
    def is_optional_content(self) -> bool: ...

class ContentObjectBuilder:

    def __init__(self, page: Page) -> None: ...
    graphics_objects: list[GraphicsObject]
    marked_contents: list[MarkedContent]
    page: Page
    def run(self) -> None: ...

class NestPoint:
    def __init__(self, x: int, y: int) -> None: ...
    x: int
    y: int
    def __eq__(self, other: NestPoint) -> bool: ...
    def __ne__(self, other: NestPoint) -> bool: ...

class NestRadians:
    def __init__(self, rads: float) -> None: ...
    @property
    def sin(self) -> float: ...
    @property
    def cos(self) -> float: ...
    def to_degrees(self) -> float: ...

class NestPolygon:
    def __init__(self) -> None: ...
    contour: list[NestPoint]
    holes: list[list[NestPoint]]

class NestBox:
    def __init__(self, center: NestPoint) -> None: ...
    def __init__(self, min: NestPoint, max: NestPoint) -> None: ...
    def __init__(self, width: int, height: int) -> None: ...
    def __init__(self, width: int, height: int, center: NestPoint) -> None: ...
    @staticmethod
    def infinite(center: NestPoint) -> NestBox: ...
    @property
    def min_corner(self) -> NestPoint: ...
    @property
    def max_corner(self) -> NestPoint: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def area(self) -> int: ...
    @property
    def center(self) -> NestPoint: ...

class NestCircle:
    def __init__(self) -> None: ...
    def __init__(self, center: NestPoint, r: float) -> None: ...
    @property
    def center(self) -> NestPoint: ...
    @property
    def radius(self) -> float: ...
    @property
    def area(self) -> int: ...


class NestItem:
    def __init__(self, points: list[NestPoint]) -> None: ...
    @property
    def bin_id(self) -> int: ...
    def is_fixed(self) -> bool: ...
    def mark_as_fixed_in_bin(self, bin_id: int) -> None: ...
    @property
    def priority(self) -> int: ...
    def to_string(self) -> str: ...
    def vertex(self, idx: int) -> NestPoint: ...
    def set_vertex(self, idx: int, v: NestPoint) -> None: ...
    @property
    def area(self) -> int: ...
    def is_contour_convex(self) -> bool: ...
    def is_hole_convex(self) -> bool: ...
    def are_holes_convex(self) -> bool: ...
    @property
    def vertex_count(self) -> int: ...
    @property
    def hole_count(self) -> int: ...
    def is_inside(self, p: NestPoint) -> bool: ...
    def is_inside(self, sh: NestItem) -> bool: ...
    def is_inside(self, box: NestBox) -> bool: ...
    def is_inside(self, circle: NestCircle) -> bool: ...
    @property
    def bounding_box(self) -> NestBox: ...
    @property
    def reference_vertex(self) -> NestPoint: ...
    @property
    def rightmost_top_vertex(self) -> NestPoint: ...
    @property
    def leftmost_bottom_vertex(self) -> NestPoint: ...
    def translate(self, delta: NestPoint) -> None: ...
    @property
    def translation(self) -> NestPoint: ...
    def rotate(self, radians: float) -> None: ...
    @property
    def rotation(self) -> NestRadians: ...
    @property
    def inflation(self) -> int: ...
    def transformed_shape(self) -> NestPolygon: ...
    def reset_transformation(self) -> None: ...

    @staticmethod
    def intersects(sh1: NestItem, sh2: NestItem) -> bool: ...
    @staticmethod
    def touches(sh1: NestItem, sh2: NestItem) -> bool: ...


class NestRectangle(NestItem):
    def __init__(self, width: int, height: int) -> None: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...


class NestInput(List[NestItem]): ...

def nest(input: NestInput, box: NestBox, dist: int = 0) -> int: ...


