use rand::Rng;

pub mod shapes;
pub mod color;
pub mod tests;

use color::Color;
use shapes::{circle::Circle, rectangle::Rectangle, shape::Repr, square::SquareFig};

fn main() {
    let mut rng = rand::thread_rng();
    // let N: f64 = rng.gen_range(5.0..50.0); // N = 16 по номеру варианта
    let N: f64 = 16.0;
    let rect: Rectangle = Rectangle::new(Color::new(0, 0, 255), N, N);
    let circle: Circle = Circle::new(Color::new(0, 255, 0), N);
    let square: SquareFig = SquareFig::new(Color::new(255, 0, 0), N);

    println!("{}", rect.repr());
    println!("{}", circle.repr());
    println!("{}", square.repr());
}
