<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");
require('functions.inc.php');

$output = array(
	"error" => false,
	"items" => "",
	"attendance" => 0,
	"max_item" => "",
	"min_item" => ""
);
$item_1 = $_REQUEST['item_1'];
$item_2 = $_REQUEST['item_2'];
$item_3 = $_REQUEST['item_3'];
$item_4 = $_REQUEST['item_4'];
$attendance_1 = $_REQUEST['attendance_1'];
$attendance_2 = $_REQUEST['attendance_2'];
$attendance_3 = $_REQUEST['attendance_3'];
$attendance_4 = $_REQUEST['attendance_4'];
$items = array($item_1,$item_2,$item_3,$item_4);
$attendances = array($attendance_1,$attendance_2,$attendance_3,$attendance_4);
if (empty($attendance_1) || empty($attendance_2) || 
    empty($attendance_3) || empty($attendance_4) ||
    !is_numeric($attendance_1) || !is_numeric($attendance_2) || 
    !is_numeric($attendance_3) || !is_numeric($attendance_4)) {
    $output['error'] = true;
    $output['message'] = 'Invalid input. Please enter only numeric values for attendance fields.';
    echo json_encode($output);
    exit();
}
// reassign into each array itemy
$items = array($item_1, $item_2, $item_3, $item_4);
$attendances = array($attendance_1, $attendance_2, $attendance_3, $attendance_4);

$max_min_items = getMaxMin($items, $attendances);

$output['items']=$items;
$output['attendance']=$attendances;
$output['max_item']=$max_min_items[0];
$output['min_item']=$max_min_items[1];

echo json_encode($output);
exit();
