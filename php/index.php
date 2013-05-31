<?php

session_start();

include_once 'constants.php';
include_once INC.'security.php';
include_once INC.'common.php';

if (isset($_GET['status'])) {
    include_once CLASS_DIR."child.class.php";
    $children = new AllChildren();
    echo json_encode($children->data["{$_GET['status']}"]);
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


