
<input type="checkbox" value="1" 
       name="<?php echo $elm_name; ?>" 
       id="<?php echo $elm_id; ?>-<?php echo $key; ?>"
       <?php 
            if ($reminder["$key"]) {
                echo ' checked';
            }
       ?>>
<label for="<?php echo $elm_id; ?>-full_screen">Log them out during event.</label>
