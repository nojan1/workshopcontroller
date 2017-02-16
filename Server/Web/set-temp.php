<?php
define("MQTT_HOST", "");
define("MQTT_PORT", "");

require("phpMQTT/phpMQTT.php");

$mqtt = new phpMQTT(MQTT_HOST, MQTT_PORT, "Heating Web");

if ($mqtt->connect()) {
	$mqtt->publish("/workshop/heating/setting","",0);
	$mqtt->close();
}

?>

<html>
    <head>
        <title>Set the heating yo</title>
    </head>
    <body>

    </body>
</html>