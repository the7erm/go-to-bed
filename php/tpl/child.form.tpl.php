<?php
    include_once 'constants-required.php';

    ?>
    
      <h3><?php 
        eent($name);
      ?></h3>
      <div>
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
                            eent($times['school_night']['start']);
                        ?>"><br>
                        <small>starts</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[school_night][end]" value="<?php 
                            eent($times['school_night']['end']);
                        ?>"><br>
                        <small>ends</small>
                    </td>
                    <td>
                        <textarea name="times[school_night][message]"><?php 
                            eent($times['school_night']['message']);
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
                            eent($times['weekend']['start']);
                        ?>"><br>
                        <small>starts</small>
                    </td>
                    <td>
                        <input  class='time' type="text" name="times[weekend][end]" value="<?php 
                            eent($times['weekend']['end']);
                        ?>"><br>
                        <small>ends</small>
                    </td>
                    <td>
                        <textarea name="times[weekend][message]"><?php 
                            eent($times['weekend']['message']);
                        ?></textarea>
                    </td>
                </tr>
                <tr>
                    <td colspan="4"><?php echo $buttons, $actions;?></td>
                </tr>
            </table>
        </form>
      </div>
    
