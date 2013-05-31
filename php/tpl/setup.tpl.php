<?php

include_once "constants-required.php";
include_once "header.tpl.php";

?>
<h1>Setup</h1>
<h3>Welcome to go-to-bed setup.</h3>
<?php
    print_r($_POST);
    if (!is_writeable(DATA)) {
        ?><div class="error">
            The DATA dir:<?php echo DATA; ?> is not writeable.<br>
            To fix the problem execute: <br>
            <code>$ sudo chown <?php echo getenv('APACHE_RUN_USER'), ':',
                                          getenv('APACHE_RUN_GROUP'), ' ', DATA; ?><br>
                  $ sudo chmod 775 <?php echo DATA; ?> -Rc
            </code><br>
        </div><?php
    } else {
        ?><li class="good">
        The DATA dir:<?php echo DATA; ?> is writeable.
        </li><?php
    }

?>
<p>You need to create your first user.  After it's created you'll be logged in 
   as them, and be able to add more users, and administer the system.</p>
<?php
$buttons = '<input type="submit" value="Create Admin Account" name="submit">';
$actions = '<input type="hidden" name="action" value="Create Admin Account">';
include_once "create.account.form.tpl.php";
include_once "footer.tpl.php";
