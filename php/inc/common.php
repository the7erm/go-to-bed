<?php
    function error_div($errors, $key) {
        if (isset($errors["$key"])) {
            ?><div class='error'><?php echo htmlentities($errors["$key"]); ?></div><?php
        }
    }

    function ent($data) {
        if (is_array($data) || is_object($data)) {
            return '<pre>'.htmlentities(print_r($data, true), ENT_QUOTES).'</pre>';
        }
        return htmlentities($data, ENT_QUOTES);
    }

    function eent($data) {
        echo ent($data);
    }
    