<?php
    include_once "constants-required.php";

    class DataFile {
        function __construct($filename) {
            
            $this->data = array();
            $this->filename = $filename;
            
            if (file_exists($this->filename)) {
                global $data;
                include_once $this->filename;
                if ($data) {
                    $this->data = $data;
                    unset($data);
                }
            }
        }

        function set_data($name, $value) {
            $this->data["$name"] = $value;
            $this->write();
        }

        function get_data($name) {
            if (isset($this->data["$name"])) {
                return $this->data["$name"];
            }
            return null;
        }

        function write() {
            if (!is_writeable($this->filename)) {
                echo "$this->filename is not writeable";
                exit();
            }
            $fp = fopen($this->filename, "w");
            fputs($fp, "<?php\n");
            fputs($fp, "include_once 'constants-required.php';\n");
            fputs($fp, "global \$data;\n");
            fputs($fp, '$data = '. var_export($this->data, true).";\n");
            fclose($fp);
        }
    }