use std::borrow::Borrow;

use super::shape::{Figure, Square, SquareResult, Repr};
use crate::color::Color;

pub struct Rectangle {
    figure: Figure,
    color: Color,
    length: f64,
    width: f64,
}

impl Rectangle {
    pub fn new(color: Color, length: f64, width: f64) -> Self {
        Rectangle { figure: Figure::new(), color: color, length: length, width: width }
    }

    pub fn get_length(&self) -> f64 {
        self.length
    }

    pub fn get_width(&self) -> f64 {
        self.width
    }

    pub fn get_color(&self) -> String {
        self.color.get_color()
    }
}

impl Square for Rectangle {
    fn get_square(&self) -> SquareResult {
        let square: f64 = self.length * self.width;
        SquareResult::Ok(square)
    }
}

impl Repr for Rectangle {
    fn repr(&self) -> String {
        format!("------------\n[Class]: Rectangle\n[Color]: {}\n[Length]: {}\n[Width]: {}\n[Square]: {}\n------------",
                self.color.get_color(), self.length, self.width, self.get_square())
    }
}