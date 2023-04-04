use std::fs;
use std::path::Path;
use std::process::{Command, Stdio};

pub mod static_analysis {
    use crate::static_analysis::Command;
    use crate::static_analysis::Stdio;
    use crate::static_analysis::Path;
    use crate::static_analysis::fs;

    pub fn read_args(args: Vec<String>) -> Result<i8, String> {
        if args[1].to_string() == "train" {
            let types = vec!["ransomware","goodware"];
            for apk_type in types {
                let _res = parse_data_from_apk(args[1].to_string(), apk_type.to_string());
            }
            let m_res = static_model();
            if m_res.is_ok() {
                Ok(1)
            } else {
                Err("Error in read args.".to_string())
            }
        } else if args[1].to_string() == "class" {
            let types = vec!["ransomware"]; // Goodware can be added to this vector.
            for apk_type in types {
                let _res = parse_data_from_apk(args[1].to_string(), apk_type.to_string());
                let _m_res = classify(apk_type.to_string());
            }
            Ok(1)
        } else {
            Err("Invalid option".to_string())
        }
    }
    
    pub fn parse_data_from_apk(option: String, data_type: String) -> Result<i8, String> {
        if option == "train" || option == "class" && data_type == "ransomware" || data_type == "goodware" {
                let in_folder = format!("./data/{}/static/{}/",data_type,option);
                println!("Analyzing packages under /data/{}/static/{}/",data_type,option);
                let s_train = static_data(in_folder, data_type, option.clone()).unwrap();
                let parse_permissions = parse_permissions(s_train, option.clone());
                    if parse_permissions.is_ok() {
                        Ok(1)
                    } else {
                        Err("An error occurred while parsing permissions.".to_string())
                    }
        } else {
            Err("Option not available".to_string())
        }
    }
    
    pub fn static_data(dir: String, out_dir: String, phase: String) -> Result<String, String> {
        let packages = fs::read_dir(dir);
        let mut out_num : i32 = 0;
        let new_dir: String;
        if out_dir == "ransomware" {
            let _rw_dir = fs::create_dir("./out/ransomware/");
            let subdir_name = format!("./out/ransomware/static/{}",phase);
            let _rw_subdir = fs::create_dir(subdir_name);
            new_dir = "ransomware".to_string();
        } else {
            let _gw_dir = fs::create_dir("./out/goodware/");
            let subdir_name = format!("./out/goodware/static/{}",phase);
            let _gw_subdir = fs::create_dir(subdir_name);
            new_dir = "goodware".to_string();
        }
    
        if packages.is_ok() {
            for package in packages.unwrap() {
                let apk = package.unwrap().path().display().to_string();
                println!("Reading {}",apk);
                let aapt_output = Command::new("aapt").arg("dump").arg("permissions").arg(apk)
                                            .stdout(Stdio::piped()).output().expect("aapt was not found.");
                let parsed_output = String::from_utf8_lossy(&aapt_output.stdout).to_string();
                let file_name = format!("./out/{}/static/{}/aaptOut{}.txt",new_dir,phase,out_num);
                let _result = fs::write(file_name, &parsed_output);
        
                out_num += 1;
            };
            Ok(new_dir)
        } else {
            Err("Failed to read directory.".to_string())
        }
    }
    
    pub fn parse_permissions(data_type: String, phase: String) -> Result<i8, String>{
        let py_call = Command::new("python").arg("src/algorithm/static/static.py").arg("-1").arg(data_type)
                                            .arg(phase).stdout(Stdio::piped()).output();  
    
        if py_call.is_ok() {
            println!("Parsed permissions.");
            Ok(1)
        } else {
            Err("Error parsing permissions.".to_string())
        }
    }
    
    pub fn static_model() -> Result<i8,String> {
        if Path::new("./out/ransomware/static/").exists() && Path::new("./out/goodware/static/").exists() {
            let py_call = Command::new("python").arg("src/algorithm/static/static.py").arg("0").arg("ransomware")
                                                    .arg("train").stdout(Stdio::piped()).output();
            if py_call.is_ok() {
                println!("Detectors were generated");
                Ok(1)
            } else {
                Err("Error training model".to_string())
            }
        } else {
            Err("Both ransomware and goodware data must be available.".to_string())
        }
    }
    
    pub fn classify(data_type: String) -> Result<i8,String> {
        let py_call = Command::new("python").arg("src/algorithm/static/static.py").arg("2").arg(data_type).arg("class").stdout(Stdio::piped()).output();  
    
        if py_call.is_ok() {
            println!("Data classified.");
            Ok(1)
        } else {
            Err("Something went wrong.".to_string())
        }
    }
}