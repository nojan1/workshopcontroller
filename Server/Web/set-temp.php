<?php
define("MQTT_HOST", "127.0.0.1");
define("MQTT_PORT", "7000");

require("phpMQTT/phpMQTT.php");

if(isset($_GET["downstairs"]) && isset($_GET["upstairs"])){

    $mqtt = new phpMQTT(MQTT_HOST, MQTT_PORT, "Heating Web");
    $response = "";

    if ($mqtt->connect()) {
        $topics['/workshop/heating/confirmation'] = array("qos"=>0, "function"=>"handleConfirmation");
        $mqtt->subscribe($topics,0);

        $command = $_GET["downstairs"] . ";" . $_GET["upstairs"];
        $mqtt->publish("/workshop/heating/setting",$command,0);

        $timeoutTime = new DateTime();
        $timeoutTime->add(new DateInterval("PT4S"));

        while($mqtt->proc() && $response == "" && new DateTime() < $timeoutTime){ }

        if($response == ""){
            $response = "Server did not return a reply in time :(";
        }

        $mqtt->close();
    }
}

function handleConfirmation($topic, $msg){
    global $response;
    $response = $msg;
}
?>

<html>
    <head>
        <title>Set the heating yo</title>
    </head>
    <body>
        <form method="get">
            <table>
                <tr>
                    <td>
                        <b>Nere</b><br/>
                        <input name="downstairs" type="text" value="15">
                    </td>
                    <td>
                        <b>Uppe</b><br/>
                        <input name="upstairs" type="text" value="10">
                    </td>
                </tr>
                <tr>
                    <td>
                        <input type="submit" name="ok" value="Sätt värme">
                    </td>
                </tr>
            </table>
        </form>

        <?php
            if(!empty($response)){
                echo "Svar från kommandokö: <i>$response</i>";
            }
        ?>
    </body>
</html>