use std::env;
mod static_analysis;
use crate::static_analysis::static_analysis::*;

fn main() {
    let args: Vec<String> = env::args().collect();
    let _res = read_args(args).unwrap();
}

#[cfg(test)]
mod test;