use std::env;
mod static_analysis;
mod dynamic_analysis;
use crate::static_analysis::static_analysis::*;
use crate::dynamic_analysis::dynamic_analysis::*;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args[1].to_string() == "static" {
        let _s_res = static_options(args).unwrap();
    } else if args[1].to_string() == "dynamic" {
        let _d_res = dynamic_options(args).unwrap();
    } else {
        println!("Invalid option.\nUsage: \ncargo run static|dynamic train|class")
    }
}

#[cfg(test)]
mod test;