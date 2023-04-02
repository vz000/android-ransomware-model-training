use std::fs;
use std::process::{Command, Stdio};

fn main() {
    println!("Analyzing packages under /data/app/");
    let _s_train = static_training("./data/app/".to_string());

}

pub fn static_training(dir: String) -> Result<i8, String> {
    let packages = fs::read_dir(dir);
    let mut out_num : i32 = 0;

    if packages.is_ok() {
        for package in packages.unwrap() {
            let apk = package.unwrap().path().display().to_string();
            println!("Reading {}",apk);
            let aapt_output = Command::new("aapt").arg("dump").arg("permissions").arg(apk)
                                        .stdout(Stdio::piped()).output().expect("aapt was not found.");
            let parsed_output = String::from_utf8_lossy(&aapt_output.stdout).to_string();
            let file_name = format!("./out/aaptOut{}.txt", out_num);
            let _result = fs::write(file_name, &parsed_output);
    
            out_num += 1;
        };
        Ok(1)
    } else {
        Err("Failed to read directory".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn it_gets_permissions() {
        let result = static_training("./data/app/".to_string()).unwrap();
        assert_eq!(result,1);
    }

    #[test]
    #[should_panic]
    fn it_fails_to_read_dir() {
        static_training("/bad/path/".to_string()).unwrap();
    }
}
