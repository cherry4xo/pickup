use std::fs::File;
use std::io::{ErrorKind, Read};

fn main() {
    let path: String = String::from("text.txt");
    let mut file = File::open(&path).expect("File should be included in this project");
    let mut file_str = String::new();
    let _ = file.read_to_string(&mut file_str);
    println!("{}", file_str);
}