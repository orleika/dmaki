<?php
require_once __DIR__ . '/../vendor/autoload.php';

$klein = new \Klein\Klein();

$request = \Klein\Request::createFromGlobals();
$uri = $request->server()->get('REQUEST_URI');
$request->server()->set('REQUEST_URI', substr($uri, strlen($_ENV['APP_PATH'])));

try {
    App\Models\DB::connect();
} catch (PDOException $e) {
    header('Content-Type: appliaction/json; charset=UTF-8', true, 500);
    die(json_encode(['error' => $e]));
}

$klein->respond(function ($request, $response, $service, $app) use ($klein) {
    $klein->onError(function ($klein, $err_msg) {
        $klein->service()->flash($err_msg);
    });
    $service->layout('../app/Views/layouts/base.phtml');
    $service->appPath = $_ENV['APP_PATH'];
});

$klein->onHttpError(function ($code, $router) {
    switch ($code) {
        case 404:
            $router->service()->render('../app/Views/404.phtml');
            break;
        default:
            $router->response()->body('Oh no, a bad error happened that caused a '. $code);
    }
});

$klein->respond('GET', '/', function ($request, $response, $service, $app) {
    $service->render('../app/Views/index.phtml');
});

$klein->respond('GET', '/dmaki.json', function ($request, $response, $service, $app) {
    $controller_class = 'App\Controllers\DmakiController';
    $controller = new $controller_class($request, $response, $service, $app);
    $controller->index();
});

$klein->dispatch($request);
