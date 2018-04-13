<?php

/**
 * Configuration for database connection
 *
 */

$host       = "35.196.250.112" 
$username   = "root";
$password   = "";
$dbname     = "test";
$dsn        = "mysql:host=$host;dbname=$dbname";
$options    = array(
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
              );
