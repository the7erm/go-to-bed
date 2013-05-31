<?php
    include_once 'constants-required.php';
    if (!isset($errors)) {
        $errors = array();
    }
?>
<form method="post">
    <table border="1" cellspacing="0">
        <tr>
            <td>Username</td>
            <td>
                <input type="text" name="uname"<?php 
                    if (isset($_POST['uname'])) {
                        echo ' value="',ent($_POST['uname']),'"';
                    }
                ?>><?php
                error_div($errors, 'uname');
                ?>
            </td>
        </tr>
        <tr>
            <td>Password</td>
            <td>
                <input type="password" name="pword"><?php
                    error_div($errors, 'pword');
                ?>
            </td>
        </tr>
        <tr>
            <td>Confirm Password</td>
            <td>
                <input type="password" name="cpword"><?php
                    error_div($errors, 'cpword');
                    echo $actions;
                ?>
                
            </td>
        </tr>
        <tr>
            <td colspan="2"><?php echo $buttons; ?></td>
        </tr>
    </table>
</form>