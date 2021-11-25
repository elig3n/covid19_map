<?php
    $date = $_GET['date'];
    $f_date = '';
    for ($i = 0; $i < strlen($date); $i++)
        if($date[$i] != '-')
            $f_date .= $date[$i];
    $output = exec("python GenerateMap.py {$f_date}");
    if($output == "404")
        header('Location:' . '404.html', true);
    else
        header('Location:' . "{$output}", true);
?>