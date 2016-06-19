<p>Тест проверки подключения MySQL</p>

<?php
$mysqli = new mysqli("localhost", "USERNAME", "PASSWORD", "BASENAME");

/* check connection */
if (mysqli_connect_errno()) {
    printf("<p>Ошибка подключения: %s\n</p>", mysqli_connect_error());
    exit();
}

printf("<p>Информация: %s\n</p>", $mysqli->host_info);

/* close connection */
$mysqli->close();
?>
