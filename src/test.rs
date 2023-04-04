mod test {
    use crate::static_analysis::static_analysis::*;
    #[test]
    fn it_gets_permissions() {
        let result = parse_data_from_apk("train".to_string(),"goodware".to_string()).unwrap();
        assert_eq!(result,1);
    }

    #[test]
    fn it_parses_permissions() {
        let res = parse_permissions("goodware".to_string(),"train".to_string()).unwrap();
        assert_eq!(res,1);
    }

    #[test]
    #[should_panic]
    fn it_fails_to_read_dir() {
        static_data("/bad/path/".to_string(),"goodware".to_string(),"train".to_string()).unwrap();
    }
    
    #[test]
    #[should_panic]
    fn it_fails_init_option() {
        // It fails to identify the options available
        parse_data_from_apk("Invalid".to_string(),"Invalid".to_string()).unwrap();
    }
}