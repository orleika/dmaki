<?php

namespace App\Models;

use App\Models\DB;

class Model
{
    protected $table;
    protected $fillable;

    public $data;

    public static function save($data)
    {
        $instance = new static;
        $params = [];

        foreach ($instance->fillable as $column) {
            if (isset($data[$column])) {
                $params[$column] = $data[$column];
            } else {
                return false;
            }
        }
        $implode = function ($glue, $params) {
            return implode($glue, array_keys($params));
        };
        $statement = "INSERT INTO {$instance->table} ({$implode(',', $params)}) VALUES (:{$implode(',:', $params)});";
        $insertedId = DB::insert($statement, $params);

        return self::find($insertedId);
    }

    public static function find($id)
    {
        $instance = new static;

        $statement = "SELECT * FROM {$instance->table} WHERE id = :id LIMIT 1";
        $instance->data = DB::fetch($statement, ['id' => $id]);

        return $instance->data;
    }

    public static function all()
    {
        $instance = new static;

        $statement = "SELECT * FROM {$instance->table}";
        $instance->data = DB::fetchAll($statement, []);

        return $instance->data;
    }

    public static function where($param, $cond)
    {
        $instance = new static;

        $statement = "SELECT * FROM {$instance->table} WHERE {$param} = :cond";
        $instance->data = DB::fetchAll($statement, ['cond' => $cond]);

        return $instance->data;
    }
}
