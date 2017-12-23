<?php

namespace App\Models;

use PDO;

class DB
{
    private static $instance;

    private $dbh;

    public static function getInstance()
    {
        static $instance = null;
        if ($instance === null) {
            $instance = new self();
        }
        return $instance;
    }

    public static function connect()
    {
        $dsn = "mysql:host={$_ENV['MYSQL_HOST']};dbname={$_ENV['MYSQL_DATABASE']};charset=utf8";
        $user = $_ENV['MYSQL_USER'];
        $password = $_ENV['MYSQL_PASSWORD'];
        $dbh = new PDO($dsn, $user, $password);
        $dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        self::getInstance()->dbh = $dbh;
    }

    public static function fetch($statement, $params)
    {
        $stmt = self::getInstance()->dbh->prepare($statement);
        $stmt->execute(self::convertArray($params));
        return $stmt->fetch(PDO::FETCH_OBJ);
    }

    public static function fetchAll($statement, $params)
    {
        $stmt = self::getInstance()->dbh->prepare($statement);
        $stmt->execute(self::convertArray($params));
        return $stmt->fetchAll(PDO::FETCH_CLASS);
    }

    public static function insert($statement, $params)
    {
        $instance = self::getInstance();
        $stmt = $instance->dbh->prepare($statement);
        $stmt->execute(self::convertArray($params));
        return $instance->dbh->lastInsertId();
    }

    private static function convertArray($params)
    {
        if ($params != null) {
            if (!is_array($params)) {
                return array($params);
            } elseif (array_diff_key($params, array_keys(array_keys($params)))) {
                return array_values($params);
            }
        }
        return $params;
    }
}
