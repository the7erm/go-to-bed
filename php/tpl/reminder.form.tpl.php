<form method="post">
    <table>
        <?php
        /*
            $this->data["$name"]["reminders"]["$id"] = array(
                'when' => $when,
                'message' => $message
            );
        */
        
        ?>
        <tr>
            <td>
                <?php
                    $elm_id = ent(preg_replace('/(\W)/', '-', $name.'-'.$id));
                ?>
                <input type="text" class="cron" id="<?php echo $elm_id; ?>-cron" name="reminder[<?php 
                    eent($name);
                ?>][<?php eent($id); ?>][cron]" 
                       value='<?php eent($reminder['cron']); ?>' placeholder="Cron event"><br>
                <textarea class="reminder" name="reminder[<?php 
                    eent($name);
                ?>][<?php eent($id); ?>][message]" placeholder="Enter Mesage to be displayed"><?php 
                    eent($reminder['message']); 
                ?></textarea><br>
                <?php 
                    $key = 'logout';
                    $elm_name = "reminder[".ent($name)."][".ent($id)."][$key]";
                    $label = "Log them out during event.";
                    include TPL."reminder.checkbox.tpl.php";
                ?>
                <br>
                <?php 
                    $key = 'full_screen';
                    $elm_name = "reminder[".ent($name)."][".ent($id)."][$key]";
                    $label = "Display the message fullscreen.";
                    include TPL."reminder.checkbox.tpl.php";
                ?>
            </td>
        </tr>
        <tr>
            <td>
                <input type="submit" value="Save">
                <input type="hidden" name="action" value="save_reminder">
            </td>
        </tr>
    </table>
</form>
