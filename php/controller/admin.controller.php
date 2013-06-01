<?php
    include_once 'constants-required.php';
    include_once CLASS_DIR."user.class.php";
    include_once CLASS_DIR."child.class.php";

    $children = new AllChildren();

    if (isset($_POST['action'])) {
        if ($_POST['action'] == 'Create Child Account') {
            $children->create_child($_POST['cname']);
        }
        if ($_POST['action'] == 'Create Admin Account') {

        }
        if ($_POST['action'] == 'Apply Child Data' || 
            $_POST['action'] == 'Create Child Account') {
            foreach ($_POST['times'] as $when=>$time) {
                $cname = $_POST['cname'];
                $children->set_restriction($cname, 
                                           $when,
                                           $time['start'],
                                           $time['end'],
                                           $time['message']);
            }
        }
        if ($_POST['action'] == 'send_message') {
            foreach ($_POST['message'] as $name=>$message) {
                if ($name != 'all') {
                    $children->send_message($name, $message);
                } else {
                    foreach ($children->data as $child_name=>$child) {
                        $children->send_message($child_name, $message);
                    }
                }
            }
        }
        if ($_POST['action'] == 'save_reminder') {
            foreach ($_POST['reminder'] as $name=>$messages) {
                foreach ($messages as $id=>$msg_info) {
                    if ($name != 'all') {
                        $children->set_reminder($name, $msg_info['cron'],
                                                $msg_info['message'],
                                                $msg_info['logout'],
                                                $msg_info['full_screen'],
                                                $id);
                    } else {
                        foreach ($children->data as $child_name=>$child) {
                            $children->set_reminder($child_name, 
                                                    $msg_info['cron'],
                                                    $msg_info['message'],
                                                    $msg_info['logout'],
                                                    $msg_info['full_screen'],
                                                    $id);
                        }
                    }
                    
                }
            }
        }

        if ($_POST['action'] == 'save_grounded') {
            foreach ($_POST['grounded'] as $name=>$data) {
                if ($name != 'all') {
                    $children->set_grounded($name, $data['until'], $data['message']);
                }
            }
        }
    }