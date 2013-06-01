<?php
    include_once 'constants-required.php';

    ?>
    
      <h3><?php 
        eent($name);
      ?></h3>
      <div>
        <h2>Send a Message</h2>
        <form method="post">
            <table>
                <tr>
                    <td>
                        <textarea name="message[<?php eent($name); ?>]" 
                            placeholder="Send <?php eent($name); ?> a message."></textarea>
                    </td>
                </tr>
                <tr>
                    <td align="right">
                        <input type="submit" value="Send Message">
                        <input type="hidden" name="action" value="send_message">
                    </td>
                </tr>
            </table>
        </form>
        <br />
        <form method="post">
            <table border="1" cellspacing="0">
                <tr>
                    <td>Child's name</td>
                    <td colspan="3">
                        <input type="text" name="cname" placeholder="Enter Child's name" value="<?php 
                            eent($name);
                        ?>"><?php
                        error_div($errors, 'cname');
                        ?>
                    </td>
                </tr>
                <tr>
                    <td>
                        School nights<br>
                        <small>(Sun-Thu)</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[school_night][start]" value="<?php 
                            eent($child_data['restriction']['school_night']['start']);
                        ?>"><br>
                        <small>starts</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[school_night][end]" value="<?php 
                            eent($child_data['restriction']['school_night']['end']);
                        ?>"><br>
                        <small>ends</small>
                    </td>
                    <td>
                        <textarea name="times[school_night][message]"><?php 
                            eent($child_data['restriction']['school_night']['message']);
                        ?></textarea>
                    </td>
                </tr>
                <tr>
                    <td>
                        Weekends<br>
                        <small>(Fri-Sat)</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[weekend][start]" value="<?php 
                            eent($child_data['restriction']['weekend']['start']);
                        ?>"><br>
                        <small>starts</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[weekend][end]" value="<?php 
                            eent($child_data['restriction']['weekend']['end']);
                        ?>"><br>
                        <small>ends</small>
                    </td>
                    <td>
                        <textarea name="times[weekend][message]"><?php 
                            eent($child_data['restriction']['weekend']['message']);
                        ?></textarea>
                    </td>
                </tr>
                <tr>
                    <td colspan="4"><?php echo $buttons, $actions;?></td>
                </tr>
            </table>
        </form>
        <h2>Reminders</h2>
        <?php 
            foreach($child_data['reminders'] as $id=>$reminder) {
                include TPL."reminder.form.tpl.php";
                ?><br><?php
            }
            $id = 'new';
            $reminder = array();
            include TPL."reminder.form.tpl.php";
        ?>
        <h2>Grounded</h2>
        <form method="post">
            <input type="text" class='date' 
                   name="grounded[<?php eent($name); ?>][until][date]" placeholder="End Date"
                   value="<?php eent($child_data['grounded']['until']['date']); ?>">
            <input type="text" class='time' name="grounded[<?php eent($name); ?>][until][time]" 
                   placeholder="End Time"
                   value="<?php eent($child_data['grounded']['until']['time']); ?>"><br>
            <textarea name="grounded[<?php eent($name); ?>][message]" 
                      placeholder="Enter reason why they are grounded."><?php 
                      eent($child_data['grounded']['message']);
            ?></textarea><br>
            <input type="submit" value="Save">
            <input type="hidden" name="action" value="save_grounded">
        </form>
      </div>