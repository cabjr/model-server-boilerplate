import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10,  // number of concurrent connections
    duration: '30s',  // test duration (seconds)
};

export default function () {
    let res = http.post('http://localhost:5000/predict', 
    JSON.stringify({
        'model_library': 'tensorflow', 
        'model_name': 'mnist_model', 
        'features': [0, 0, 0,]  // change this for your input data
    }), 
    { headers: { 'Content-Type': 'application/json' } });

    check(res, {
        'status was 200': (r) => r.status == 200,
        'transaction time OK': (r) => r.timings.duration < 200
    });
    sleep(1);
}
