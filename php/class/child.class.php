<?php
    include_once "constants-required.php";
    include_once CLASS_DIR."data_file.class.php";

    class AllChildren extends DataFile {
        function __construct() {
            parent::__construct(CHILD_DATA);
        }

        function set_child($name, $key, $value) {
            if (!isset($this->data["$name"]["$key"])) {
                $this->data["$name"] = array(
                    "$key" => $value
                );
            } else {
                $this->data["$name"]["$key"] = $value;
            }
            $this->write();
        }

        function create_child($name) {
            if (!$name) {
                return;
            }
            $result = array(
                'errors' => array(),
                'status' => 'FAIL'
            );
            if (isset($this->data["$name"])) {
                $result['errors']["$name"] = 'A child by that name already exists';
                return $result;
            }
            $this->data["$name"] = array();
            $this->write();
            $result['status'] = 'OK';
            return $result;
        }

        function set_restriction($name, $when, $start, $end, $message='') {
            if (!$name) {
                return;
            }
            $this->data["$name"]["$when"] = array(
                'start' => $start,
                'end' => $end, 
                'message' => $message
            );
            $this->write();
        }
    }

