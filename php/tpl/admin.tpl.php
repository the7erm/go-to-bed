<?php
    include_once 'constants-required.php';
    include_once "header.tpl.php";
    ?>
    <div id="loading">Loading ...</div>
    <?php
      flush();
      ob_flush();
    ?>
    <div id="tabs" style="display:none;">
      <ul>
        <li><a href="#tabs-1">Children</a></li>
        <li><a href="#tabs-2">Add Admin</a></li>
        <li><a href="#tabs-3">Add Child</a></li>
      </ul>
      <div id="tabs-1">
        <div id="accordion" style="display:none;">
          <h3>All</h3>
          <div>
            <form method="post">
              <table>
                  <tr>
                      <td>
                          <textarea name="message[all]" 
                              placeholder="Send all the children a message."></textarea>
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
          </div>
          <?php
              $buttons = '<input type="submit" value="Apply" name="submit">';
              foreach ($children->data as $name=>$child_data) {
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
    <?php
      ob_flush();
    ?>
    <script type="text/javascript">
      $(function() {
        $("#tabs").tabs();
        
        
        $("#accordion").accordion({collapsible: true, heightStyle: "content"});
        $('.date').datepicker();
        
        $('.cron').each(function(obj){
          var _this = $(this),
              id = _this.prop('id');
          if (!id) {
              return;
          }
          $("#"+id).jqCron({
              enabled_minute: true,
              multiple_dom: true,
              multiple_month: true,
              multiple_mins: true,
              multiple_dow: true,
              multiple_time_hours: true,
              multiple_time_minutes: true,
              default_period: 'week',
              no_reset_button: false,
              lang: 'en'
          });
        });
        $("#tabs").show('fast', function(){
          $("#accordion").show('fast');
        });
        $("#loading").hide();
      });
    </script>
    <?php
    if (isset($_POST['pword'])) {
      $_POST['pword'] = '***';
    }
    if (isset($_POST['cpword'])) {
      $_POST['cpword'] = '***';
    }
    // eent($_POST);
    include_once "footer.tpl.php";
