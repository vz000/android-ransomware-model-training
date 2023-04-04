pub mod dynamic_analysis {
    pub fn dynamic_options(args: Vec<String>) -> Result<i8, String>{
        if args[2].to_string() == "train" {
            Ok(1)
        } else {
            Err("Invalid".to_string())
        }
    }
}