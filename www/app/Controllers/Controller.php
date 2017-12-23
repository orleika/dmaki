<?php

namespace App\Controllers;

use App\Models;

abstract class Controller
{
    protected $request;
    protected $response;
    protected $service;
    protected $app;

    public function __construct($request, $response, $service, $app)
    {
        $this->request = $request;
        $this->response = $response;
        $this->service = $service;
        $this->app = $app;
    }
}
