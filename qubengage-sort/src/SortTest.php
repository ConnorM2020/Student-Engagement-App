<?php
require_once __DIR__ . '/functions.inc.php'; 
require_once __DIR__ . '/../vendor/autoload.php';  

use PHPUnit\Framework\TestCase;

class SortTest extends TestCase {
    public function testGetSortedAttendance() {    
        $items = ['Item1', 'Item2', 'Item3'];
        $attendances = [10, 20, 30];
        $expected = [
            ['item' => 'Item3', 'attendance' => 30],
            ['item' => 'Item2', 'attendance' => 20],
            ['item' => 'Item1', 'attendance' => 10],
        ];
        $actual = getSortedAttendance($items, $attendances);
        $this->assertEquals($expected, $actual, "The actual sorted attendances do not match the expected output.");
    }
    
    public function testEmptyInputs() {
        $items = [];
        $attendances = [];
        $expected = [];
        $actual = getSortedAttendance($items, $attendances);
        $this->assertEquals($expected, $actual, "The function should handle empty inputs without error.");
    }
    public function testUnsortedInput() {
        $items = ['Item1', 'Item2', 'Item3', 'Item4'];
        $attendances = [45, 10, 30, 20];
        $expected = [
            ['item' => 'Item1', 'attendance' => 45],
            ['item' => 'Item3', 'attendance' => 30],
            ['item' => 'Item4', 'attendance' => 20],
            ['item' => 'Item2', 'attendance' => 10],
        ];
        $actual = getSortedAttendance($items, $attendances);
        $this->assertEquals($expected, $actual, "The function should correctly sort a completely unsorted input.");
    }

}
