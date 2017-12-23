<?php

namespace App\Models;

class Dmaki extends Model {
    protected $table = 'dmaki';

    protected $fillable = [
        'word',
        'layer',
        'type',
        'parent_id',
    ];
}
