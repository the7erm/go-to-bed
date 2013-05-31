<?php
    include_once "constants-required.php";
    $errors = array();

    if (isset($_POST['action']) && $_POST['action'] == 'Create Admin Account') {
        include_once INC."security.php";
        include_once CLASS_DIR."user.class.php";
        $users = new AllUsers();
        $result = $users->create_user($_POST['uname'], $_POST['pword'], 
                                      $_POST['cpword']);

        $errors = $result['errors'];
        if (!$result['errors']) {
            $_SESSION['user'] = $_POST['uname'];
            header("Location:".WWW_ROOT);
            exit();
        }
    }
    
