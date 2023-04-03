use std::fs;
use std::env;
use std::path::Path;
use std::process::{Command, Stdio};

fn main() {
    let args: Vec<String> = env::args().collect();
    let res = train_option(args[1].clone(),args[2].clone()).unwrap();
    if res == 1 {
        let _m_res = static_model();
    } else {
        println!("test");
    }
}

fn train_option(option: String, data_type: String) -> Result<i8, String> {
    if option == "train" || option == "class" && data_type == "nslf" || data_type == "slf" {
        if option == "train" {
            let in_folder = format!("./data/{}/static/",data_type);
            println!("Analyzing packages under /data/{}/static/",data_type);
            let s_train = static_data(in_folder, data_type).unwrap();
            let parse_permissions = parse_permissions(s_train);
                if parse_permissions.is_ok() {
                    Ok(1)
                } else {
                    Err("An error occurred while parsing permissions.".to_string())
            }
        } else {
            Ok(2)
        }
    } else {
        Err("Option not available".to_string())
    }
}

fn static_data(dir: String, out_dir: String) -> Result<String, String> {
    let packages = fs::read_dir(dir);
    let mut out_num : i32 = 0;
    let new_dir: String;
    if out_dir == "nslf" {
        let _rw_dir = fs::create_dir("./out/ransomware/");
        new_dir = "ransomware".to_string();
    } else {
        let _gw_dir = fs::create_dir("./out/goodware/");
        new_dir = "goodware".to_string();
    }

    if packages.is_ok() {
        for package in packages.unwrap() {
            let apk = package.unwrap().path().display().to_string();
            println!("Reading {}",apk);
            let aapt_output = Command::new("aapt").arg("dump").arg("permissions").arg(apk)
                                        .stdout(Stdio::piped()).output().expect("aapt was not found.");
            let parsed_output = String::from_utf8_lossy(&aapt_output.stdout).to_string();
            let file_name = format!("./out/{}/aaptOut{}.txt",new_dir,out_num);
            let _result = fs::write(file_name, &parsed_output);
    
            out_num += 1;
        };
        Ok(new_dir)
    } else {
        Err("Failed to read directory.".to_string())
    }
}

fn parse_permissions(data_type: String) -> Result<i8, String>{
    let py_call = Command::new("python").arg("src/algorithm/static/static.py").arg("-1").arg(data_type)
        .stdout(Stdio::piped()).output();  

    if py_call.is_ok() {
        println!("Parsed permissions.");
        Ok(1)
    } else {
        Err("Something went wrong.".to_string())
    }
}

fn static_model() -> Result<i8,String>{
    if Path::new("./out/ransomware/").exists() && Path::new("./out/goodware/").exists() {
        let py_call = Command::new("python").arg("src/algorithm/static/static.py").arg("0").arg("ransomware")
                                                .stdout(Stdio::piped()).output();
        if py_call.is_ok() {
            println!("Detectors were generated");
            Ok(1)
        } else {
            Err("Something went wrong".to_string())
        }
    } else {
        Err("Both ransomware and goodware data must be available.".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn it_gets_permissions() {
        // Uses default input "/data/app" for static training.
        let result = train_option("train".to_string(),"slf".to_string()).unwrap();
        assert_eq!(result,1);
    }

    #[test]
    fn it_parses_permissions() {
        let res = parse_permissions("goodware".to_string()).unwrap();
        assert_eq!(res,1);
    }

    #[test]
    #[should_panic]
    fn it_fails_to_read_dir() {
        static_data("/bad/path/".to_string(),"slf".to_string()).unwrap();
    }
    
    #[test]
    #[should_panic]
    fn it_fails_init_option() {
        // It fails to identify the options available
        train_option("Invalid".to_string(),"Invalid".to_string()).unwrap();
    }
}
