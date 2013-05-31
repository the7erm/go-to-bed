<?php
    include_once 'constants-required.php';
    if (!isset($errors)) {
        $errors = array();
    }
?>
<form method="post">
    <table border="1" cellspacing="0">
        <tr>
            <td>Child's name</td>
            <td colspan="3">
                <input type="text" name="cname" placeholder="Enter Child's name" value="<?php 
                    if (isset($_POST['cname'])) {
                        eent($_POST['cname']);
                    }
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
                <input  class='time' type="text" name="time[school_night][start]" value="21:00"><br>
                <small>starts</small>
            </td>
            <td>
                <input  class='time' type="text" name="time[school_night][end]" value="06:00"><br>
                <small>ends</small>
            </td>
            <td>
                <textarea name="time[school_night][message]">Time for bed</textarea>
            </td>
        </tr>
        <tr>
            <td>
                Weekends<br>
                <small>(Fri-Sat)</small>
            </td>
            <td>
                <input  class='time' type="text" name="time[weekend][start]" value="22:00"><br>
                <small>starts</small>
            </td>
            <td>
                <input  class='time' type="text" name="time[weekend][end]" value="06:00"><br>
                <small>ends</small>
            </td>
            <td>
                <textarea name="time[school_night][message]">Time for bed</textarea>
            </td>
        </tr>
        <tr>
            <td colspan="4"><?php echo $buttons, $actions;?></td>
        </tr>
    </table>
</form>
<script type="text/javascript">
  $(function() {
    $(".time").timepicker({ 'step': 15 });
  });
</script>