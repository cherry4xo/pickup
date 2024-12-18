use std::fmt;

pub enum SquareResult {
    AbstractMethod,
    Ok(f64)
}

impl fmt::Display for SquareResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SquareResult::AbstractMethod => write!(f, "Abstract method"),
            SquareResult::Ok(value) => write!(f, "{value}")
        }
    }
}

pub struct Figure { }

impl Figure {
    pub fn new() -> Self {
        Figure {}
    }
}

pub trait Repr {
    fn repr(&self) -> String;
}

pub trait Square {
    fn get_square(&self) -> SquareResult;
}

impl Square for Figure {
    fn get_square(&self) -> SquareResult {
        SquareResult::AbstractMethod
    }
}

impl Repr for Figure {
    fn repr(&self) -> String {
        String::from("------------\n[Figure] abstract struct\n------------")
    }
}