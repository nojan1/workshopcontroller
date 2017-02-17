<?php
define("MQTT_HOST", "");
define("MQTT_PORT", "");

require("phpMQTT/phpMQTT.php");

if(isset($_GET["downstairs"] && isset($_GET["upstairs"])){

    $mqtt = new phpMQTT(MQTT_HOST, MQTT_PORT, "Heating Web");
    $response = "";

    if ($mqtt->connect()) {
        $topics['/workshop/heating/confirmation'] = array("qos"=>0, "function"=>"handleConfirmation");
        $mqtt->subscribe($topics,0);

        $command = $_GET["downstairs"] . ";" . $_GET["upstairs"];
        $mqtt->publish("/workshop/heating/setting",$command,0);

        $timeoutTime = new DateTime();
        $timeoutTime->add(new DateInterval("P4S"));

        while($mqtt->proc() && $response == "" && new DateTime() < $timeoutTime){ }

        if($response == ""){
            $response = "Server did not return a reply in time :(";
        }

        $mqtt->close();
    }
}

function handleConfirmation($topic, $msg){
    global response;
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
                    <input type="submit" name="ok" value="Sätt värme">
                </tr>
            </table>
        </form>

        <?php
            if(isset($response)){
                echo "Svar från kommandokö: <i>$response</i>";
            }
        ?>
    </body>
</html>