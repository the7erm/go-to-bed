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
    }