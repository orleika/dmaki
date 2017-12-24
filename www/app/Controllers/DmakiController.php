<?php

namespace App\Controllers;

use App\Models;
use Klein\Exceptions\ValidationException;

class DmakiController extends Controller
{
    private static function random()
    {
        return mt_rand() / mt_getrandmax();
    }

    private static function circle_random($layer = 1)
    {
        $c = 100;
        $r0 = ($layer - 1) * $c;
        $rr = $layer * $c;
        while(true) {
            $x = floor(self::random() * $layer * $c * 2) - $c * $layer;
            $y = floor(self::random() * $layer * $c * 2) - $c * $layer;
            $r = $x * $x + $y * $y;
            if ($r0 * $r0 <= $r && $r < $rr * $rr) {
                return [$x, $y];
            }
        }
    }

    private static function parent_word($id, $d) {
        foreach($d as $dd) {
            if ($d->id === $id) {
                return $d->word;
            }
        }
    }

    private static function children_words($id, $d)
    {
        return array_fillter($d, function($dd) use ($id) {
            return $d->id === $id;
        });
    }

    public function index()
    {
        $dmaki = Models\dmaki::all();
        $nodes = array_map(function($d) use ($dmaki) {
            $point = self::circle_random($d->layer);
            return [
                'id' => "n{$d->id}",
                'label' => "$d->word",
                'x' => $point[0],
                'y' => $point[1],
                'size' => 5 / ($d->layer * 0.5),
            ];
        }, $dmaki);
        $edges = [];
        foreach($dmaki as $i => $d) {
            $edges[] = [
                'id' => "e{$i}",
                'source' => "n{$d->parent_id}",
                'target' => "n{$d->id}",
            ];
        }

        return $this->response->code(200)->json([
            'nodes' => $nodes,
            'edges' => $edges,
        ])->send();
    }
}
