use std::f64::consts::PI;
use super::shape::{Figure, Square, Repr, SquareResult};
use crate::color::Color;

pub struct Circle {
    figure: Figure,
    radius: f64,
    color: Color
}

impl Circle {
    pub fn new(color: Color, radius: f64) -> Self {
        Circle { figure: Figure::new(), radius: radius, color: color }
    }
}

impl Square for Circle {
    fn get_square(&self) -> SquareResult {
        let square: f64 = PI * self.radius * self.radius;
        SquareResult::Ok(square)
    }
}

impl Repr for Circle {
    fn repr(&self) -> String {
        format!("------------\n[Class]: Circle\n[Color]: {}\n[Raduis]: {}\n[Square]: {}\n------------",
                self.color.get_color(), self.radius, self.get_square())
    }
}