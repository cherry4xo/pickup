pub struct Color {
    r: u8,
    g: u8,
    b: u8,
}

impl Color {
    pub fn new(r: u8, g: u8, b: u8) -> Self {
        Color { r: r, g: g, b: b }
    }

    pub fn get_color(&self) -> String {
        format!("rgb({} {} {})", self.r, self.g, self.b)
    }
}