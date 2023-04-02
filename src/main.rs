use std::fs;
use std::process::{Command, Stdio};

fn main() {
    println!("Analyzing packages under /data/app/");
    let _s_train = static_training("./data/app/".to_string());
    let _parse_permissions = parse_permissions();
}

fn static_training(dir: String) -> Result<i8, String> {
    let packages = fs::read_dir(dir);
    let mut out_num : i32 = 0;

    let _rw_dir = fs::create_dir("./out/ransomware/");
    let _gw_dir = fs::create_dir("./out/goodware/");

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
        Err("Failed to read directory.".to_string())
    }
}

fn parse_permissions() -> Result<i8, String>{
    let py_call = Command::new("python").arg("src/algorithm/static/static.py").stdout(Stdio::piped())
                                                          .output();
    if py_call.is_ok() {
        println!("Parsed permissions.");
        Ok(1)
    } else {
        Err("Something went wrong.".to_string())
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

    #[test]
    fn it_parses_permissions() {
        let res = parse_permissions().unwrap();
        assert_eq!(res,1);
    }
}
