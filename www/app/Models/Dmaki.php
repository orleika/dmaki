<?php

namespace App\Models;

class Dmaki extends Model {
    protected $table = 'wnet';

    protected $fillable = [
        'word',
        'layer',
        'pos',
        'parent_id',
    ];
}
