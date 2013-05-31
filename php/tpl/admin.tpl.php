<?php
    include_once 'constants-required.php';

    include_once "header.tpl.php";

    ?>
    <div id="tabs">
      <ul>
        <li><a href="#tabs-1">Children</a></li>
        <li><a href="#tabs-2">Add Admin</a></li>
        <li><a href="#tabs-3">Add Child</a></li>
      </ul>
      <div id="tabs-1">
        <div id="accordion">
        <?php
            $buttons = '<input type="submit" value="Apply" name="submit">';

            foreach ($children->data as $name=>$times) {
                $actions = '<input type="hidden" name="action" value="Apply Child Data">
                            <input type="hidden" name="old_name" value="'.ent($name).'">';
                include TPL."child.form.tpl.php";
            }
        ?>
        </div>
      </div>
      <div id="tabs-2">
        <?php 
            $buttons = '<input type="submit" value="Create Admin Account" name="submit">';
            $actions = '<input type="hidden" name="action" value="Create Admin Account">';
            include_once TPL."create.account.form.tpl.php"; 
        ?>
      </div>
      <div id="tabs-3">
        <?php 
            $buttons = '<input type="submit" value="Create Child Account" name="submit">';
            $actions = '<input type="hidden" name="action" value="Create Child Account">';
            include_once TPL."create.child.form.tpl.php";
        ?>
      </div>
    </div>
    <script type="text/javascript">
      $(function() {
        $( "#tabs" ).tabs();
        $( "#accordion" ).accordion();
      });
    </script>
    <?php
    eent($_POST);
    include_once "footer.tpl.php";