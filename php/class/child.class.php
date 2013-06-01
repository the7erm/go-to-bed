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
            $result = array(
                'errors' => array(),
                'status' => 'FAIL'
            );

            if (!$name) {
                $result['errors']['uname'] = "No name";
                return $result;
            }
            
            if (isset($this->data["$name"])) {
                $result['errors']["$name"] = 'A child by that name already exists';
                return $result;
            }
            $this->data["$name"] = array(
                'restriction' => array(),
                'messages' => array(),
                'reminders' => array()
            );
            $this->write();
            $result['status'] = 'OK';
            return $result;
        }

        function set_restriction($name, $when, $start, $end, $message='') {
            if (!$name) {
                return;
            }

            if (!isset($this->data["$name"])) {
                return;
            }

            if (!isset($this->data["$name"]['restriction'])) {
                $this->data["$name"]['restriction'] = array();
            }

            if (!isset($this->data["$name"]['restriction']["$when"])) {
                $this->data["$name"]['restriction']["$when"] = array();
            }

            $this->data["$name"]["restriction"]["$when"] = array(
                'start' => $start,
                'end' => $end, 
                'message' => $message
            );

            $this->write();
        }

        function send_message($name, $message) {
            if (!isset($this->data["$name"])) {
                return;
            }
            if (!isset($this->data["$name"]['messages'])) {
                $this->data["$name"]['messages'] = array();
            }
            $id = date('r').'-'.rand();
            $this->data["$name"]["messages"]["$id"] = $message;
            $this->write();
        }

        function message_recieved($name, $id) {
            unset($this->data["$name"]["messages"]["$id"]);
            $this->write();
        }

        function set_reminder($name, $cron, $message, $logout, $full_screen, $id='') {
            if (!isset($this->data["$name"])) {
                return;
            }
            if (!isset($this->data["$name"]['reminders'])) {
                $this->data["$name"]['reminders'] = array();
            }
            if (!$id || $id == 'new') {
                $id = date('r').'-'.rand();
            }
            $this->data["$name"]["reminders"]["$id"] = array(
                'cron' => $cron,
                'message' => $message,
                'logout' => (bool)$logout,
                'full_screen' => (bool)$full_screen
            );
            $this->write();
        }

        function set_grounded($name, $until, $message) {
            if (!isset($this->data["$name"]['grounded'])) {
                $this->data["$name"]['grounded'] = array();
            }
            $this->data["$name"]["grounded"] = array(
                'until' => $until,
                'message' => $message
            );
            $this->write();
        }

    }

