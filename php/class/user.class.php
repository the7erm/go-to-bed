<?php
    include_once "constants-required.php";
    include_once CLASS_DIR."data_file.class.php";

    class AllUsers extends DataFile {
        function __construct() {
            parent::__construct(USER_DATA);
            // call super construct. with filename of users.
            
            $this->salt = 'sdi43p8fhaph4e;fkah&Y&%Ff,qo7hcspd78ch&(1y3=fasd897c'.
                          'asdf8$*CN*CH99`&ac7s;hdcoah7kaUJH7h^ehlca<L>:&348caj';
        }

        public function get_password($name) {
            return $this->get_data($name);
        }

        public function set_password($name, $pword) {
            $this->set_data($name, $pword);
        }

        public function create_user($uname, $pword, $cpword) {
            $result = array(
                'errors' => array(),
                'create' => "FAIL"
            );
            $uname = trim($uname);
            if (!$uname) {
                $result['errors']['uname'] = "You must enter a username.";
            }
            if (!$pword) {
                $result['errors']['pword'] = "You must enter a password.";
            }
            if (!$cpword) {
                $result['errors']['cpword'] = "You must confirm your password.";
            }
            if ($cpword && $pword && $cpword != $pword) {
                $result['errors']['cpword'] = "Passwords do not match.";
            }

            if (isset($this->data["$uname"])) {
                $result['errors']['uname'] = "That user already exists.";
            }

            if ($result['errors']) {
                return $result;
            }

            $hash = $this->do_hash($uname, $pword);
            $this->set_password($uname, $hash);
            $result['create'] = 'OK';

            return $result;
        }

        function do_hash($uname='', $pword='') {
            $salt = $this->salt;
            $parts = array(
                1 => $salt,
                2 => $uname,
                3 => $pword
            );
            $long_salt = $data = "$salt-$uname-$salt-$pword-$salt";

            for($i=0;$i<1000;$i++) {
                foreach ($parts as $k=>$p) {
                    if ($i % $k == 0) {
                        $data = "$data-$p";
                        $get_charcter_at = $i % strlen($p);
                        $i2 = ord($p[$get_charcter_at]);
                        foreach ($parts as $k2=>$p2) {
                            if ($i2 % $k2 == 0) {
                                $data = "$p2-$data-$p2";
                            }
                        }
                    } else {
                        $data = "$salt-$long_salt-$data-$long_salt!!$salt";
                    }
                }
                $data = hash('sha512', $data);
            }
            return $data;
        }

        function confirm_password($uname, $pword) {
            if (!isset($this->data["$uname"])) {
                return false;
            }
            $hash = $this->data["$uname"];
            $hashed_pword = $this->do_hash($uname, $pword);
            return ($hash === $hashed_pword);
        }
    }

