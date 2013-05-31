<?php
    define('CONSTANTS_INCLUDED', true);

    define('DOCUMENT_ROOT',dirname($_SERVER['SCRIPT_FILENAME'])."/");
    define('WWW_ROOT', dirname($_SERVER["SCRIPT_NAME"])."/");

    define('TPL', DOCUMENT_ROOT.'tpl/');
    define('DATA', DOCUMENT_ROOT.'data/');
    define('USER_DATA', DATA.'users.data.php');
    define('CHILD_DATA', DATA.'children.data.php');

    define('INC', DOCUMENT_ROOT.'inc/');
    define('CONTROLLER', DOCUMENT_ROOT.'controller/');
    define('CLASS_DIR', DOCUMENT_ROOT.'class/');

    define('JS', WWW_ROOT.'js/');
    define('CSS', WWW_ROOT.'css/');
    define('IMAGES', WWW_ROOT.'images/');
