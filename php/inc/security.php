<?php
include_once "constants-required.php";

if (ini_get('register_globals')) {
    ?><h1>Security issue.</h1><?php
    echo "register_globals is:",ini_get('register_globals'),"<br>";
    ?>
        Turn register_globals off by editing php.ini and changing the line 
        <code>register_globals = On</code> to <code>register_globals = Off</code>
        or add the line "php_flag register_globals off" to .htaccess.
    <?php
    exit();
}

