<?php

include_once "constants-required.php";
if (isset($_POST['action']) && $_POST['action'] == 'Login') {
    include_once INC."security.php";
    include_once CLASS_DIR."user.class.php";
    $users = new AllUsers();
    if ($users->confirm_password($_POST['uname'], $_POST['pword'])) {
        $_SESSION['user'] = $_POST['uname'];
        header("Location:".WWW_ROOT);
        exit();
    } else {
        $errors = array('uname' => 'Invalid username or password.');
    }
}
