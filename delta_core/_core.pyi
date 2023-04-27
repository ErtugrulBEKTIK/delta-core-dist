
from __future__ import annotations

import datetime
import sys
from abc import abstractmethod
from decimal import Decimal
from enum import Enum
from pikepdf import Page
from typing import (
    TypeVar,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal  # pragma: no cover

import delta_core._core

T = TypeVar('T', bound='Object')
Numeric = TypeVar('Numeric', int, float, Decimal)


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
    def transform_point(self, x: float, y: float) -> list[float]: ...
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

"""
 py::class_<Point>(m, "Point", "2D Point")
      .def(py::init<int, int>(), py::arg("x"), py::arg("y"))
      //.def_property_readonly("x", &Point::X)
      .def_property_readonly("x", [](const Point& p) { return p.X; })
      .def_property_readonly("y", [](const Point& p) { return p.Y; })
      .def(
          "__repr__",
          [](const Point& p) {
            std::string r("Point(");
            r += boost::lexical_cast<std::string>(p.X);
            r += ", ";
            r += boost::lexical_cast<std::string>(p.Y);
            r += ")";
            return r;
          }
      )
      .def("__eq__", [](const Point& p, const Point& q) { return p == q; });

"""

class NestPoint:

    def __init__(self) -> None: ...
    def __init__(self, x: int, y: int) -> None: ...
    x: int
    y: int
    def __eq__(self, other: NestPoint) -> bool: ...
    def __repr__(self) -> str: ...

class NestRadians:
    def __init__(self, rads: float) -> None: ...
    def sin(self) -> float: ...
    def cos(self) -> float: ...
    def to_degrees(self) -> float: ...

class NestBox:
    def __init__(self, x: int, y: int) -> None: ...


class NestItem:
    def __init__(self, points: list[NestPoint]) -> None: ...
    def translation(self) -> NestPoint: ...
    def rotation(self) -> NestRadians: ...


def nest(input: list[NestItem], box: NestBox) -> any: ...


