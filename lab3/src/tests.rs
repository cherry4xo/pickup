#[cfg(test)]
mod tests {
    use crate::shapes::{circle::Circle, rectangle::Rectangle, shape::Repr, square::SquareFig};
    use crate::color::Color;

    #[test]
    fn rect() {
        let N: f64 = 16.0; // N = 16 по номеру варианта
        let rect: Rectangle = Rectangle::new(Color::new(0, 0, 255), N, N);
        assert_eq!(rect.repr(), String::from("------------\n[Class]: Rectangle\n[Color]: rgb(0 0 255)\n[Length]: 16\n[Width]: 16\n[Square]: 256\n------------"))
    }

    #[test]
    fn circle() {
        let N: f64 = 16.0; // N = 16 по номеру варианта
        let circle: Circle = Circle::new(Color::new(0, 255, 0), N);
        assert_eq!(circle.repr(), String::from("------------\n[Class]: Circle\n[Color]: rgb(0 255 0)\n[Raduis]: 16\n[Square]: 804.247719318987\n------------"))
    }

    #[test]
    fn square() {
        let N: f64 = 16.0; // N = 16 по номеру варианта
        let square: SquareFig = SquareFig::new(Color::new(255, 0, 0), N);
        assert_eq!(square.repr(), String::from("------------\n[Class]: Square\n[Color]: rgb(255 0 0)\n[Length]: 16\n[Square]: 256\n------------"))
    }
}