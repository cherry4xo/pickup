use super::shape::{SquareResult, Repr};
use crate::shapes::rectangle::Rectangle;
use crate::color::Color;
use crate::shapes::shape::Square;

pub struct SquareFig {
    rectangle: Rectangle
}

impl SquareFig {
    pub fn new(color: Color, length: f64) -> Self {
        let rect = Rectangle::new(color, length, length);
        SquareFig { rectangle: rect }
    }
}

impl Square for SquareFig {
    fn get_square(&self) -> SquareResult {
        let square: f64 = self.rectangle.get_length() * self.rectangle.get_width();
        SquareResult::Ok(square)
    }
}

impl Repr for SquareFig {
    fn repr(&self) -> String {
        format!("------------\n[Class]: Square\n[Color]: {}\n[Length]: {}\n[Square]: {}\n------------",
                self.rectangle.get_color(), self.rectangle.get_length(), self.get_square())
    }
}