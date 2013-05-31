<?php

include_once "constants-required.php";

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <script type="text/javascript" src="<?php echo JS; ?>jquery-timepicker/jquery.timepicker.js"></script>
    <link rel="stylesheet" type="text/css" href="<?php echo JS; ?>jquery-timepicker/jquery.timepicker.css" />
    <?php
        if (isset($addional_scripts)) {
            foreach ($addional_scripts as $script) {
                ?>
                <script type="text/javascript" src="<?php
                    echo $script;
                ?>"></script><?php echo "\n";
            }
        }
    ?>
    <style>
        @font-face {
            font-family: FreeSans;
            src: url('<?php echo CSS; ?>FreeSans.ttf');
            font-family: FreeSansBold;
            src: url('<?php echo CSS; ?>FreeSansBold.ttf');
        }
        body {
            font-family: FreeSans !important;
        }
        .error {
            color:red;
            font-weight:bold;
        }

        .good {
            color: green;
            font-weight:bold;
        }

        td {
            vertical-align: top;
        }
    
        .cron td {
            background: #EEE;
        }
        .cron > .float-left {
            background: #eee;
            margin:3px;
        }
        .day-wrapper {
            min-width:50px;
            float:left;
        }

        .min-wrapper {
            float:left;
        }

        .hour-wrapper {
            float: left;
        }

        input[type=checkbox]:checked + label {
           font-weight: bold;
        }

        input[type=checkbox] + label {
            
            
        }
        input[type=checkbox] {
            padding: 5px;
            margin-bottom:12px;
        }

        .month label {
            min-width: 60px;
        }

        .float-left {
            float:left;
        }
        .float-right {
            float:right;
        }
        .date {
            width:100px;
        }
        .time {
            width:100px;
        }
    </style>
</head>
<body>
