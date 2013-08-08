<?php

session_start();

include_once 'constants.php';
include_once INC.'security.php';
include_once INC.'common.php';

if (isset($_GET['msg_for'])) {
    if (0 === strpos($_SERVER['REMOTE_ADDR'], '10.1.') || 
        0 === strpos($_SERVER['REMOTE_ADDR'], '192.168.')) {
        include_once CLASS_DIR."child.class.php";
        $children = new AllChildren();
        $name = $_GET['msg_for'];
        $children->message_recieved($name, $_GET['id']);
    } else {
        header('HTTP/1.0 403 Forbidden');
    }
    exit();
}

if (isset($_GET['status'])) {
    if (0 === strpos($_SERVER['REMOTE_ADDR'], '10.1.') || 
        0 === strpos($_SERVER['REMOTE_ADDR'], '192.168.')) {
        include_once CLASS_DIR."child.class.php";
        $children = new AllChildren();
        header('Content-Type: application/json');
        echo json_encode($children->data["{$_GET['status']}"]);
    } else {
        header('HTTP/1.0 403 Forbidden');
    }
    exit();
}

if (!file_exists(USER_DATA)) {
    include_once CONTROLLER."setup.controller.php";
    include_once TPL."setup.tpl.php";
    exit();
}

if (!isset($_SESSION['user'])) {
    include_once CONTROLLER."login.controller.php";
    include_once TPL."login.tpl.php";
    exit();
}


include_once CONTROLLER."admin.controller.php";
include_once TPL."admin.tpl.php";


