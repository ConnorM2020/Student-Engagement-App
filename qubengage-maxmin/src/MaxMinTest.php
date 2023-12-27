<?php
require_once __DIR__ . '/functions.inc.php'; 
require_once __DIR__ . '/vendor/autoload.php';

use PHPUnit\Framework\TestCase;

class MaxMinTest extends TestCase {
    public function testNormalCase() {
        $items = ["Item1", "Item2", "Item3"];
        $attendances = [30, 50, 40];
        $expected = ["Item2 - 50", "Item1 - 30"]; // Max, Min
        $this->assertEquals($expected, getMaxMin($items, $attendances));
    }
    public function testEmptyArrays() {
        $items = [];
        $attendances = [];
        $expected = [null, null];
        $this->assertEquals($expected, getMaxMin($items, $attendances));
    }
    public function testValidArray() {
        $items = ["Item1", "Item2", "Item3", "Item4"];
        $attendances = [10, 20, 15, 25];
        $expected = ["Item4 - 25", "Item1 - 10"]; // Max, Min
        $result = getMaxMin($items, $attendances);
        $this->assertEquals($expected, $result);
    }

    public function testInValidArray() {
        $items = ["Item1", "Item2", "Item3", "Item4"];
        $attendances = [6, 32, 4, 13];
        $expected = ["Item2 - 32", "Item3 - 4"]; // Max, Min
        $result = getMaxMin($items, $attendances);
        $this->assertEquals($expected, $result);
    }
}
?>
