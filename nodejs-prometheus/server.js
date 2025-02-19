const express = require('express');
const client = require('prom-client');

const app = express();

let collectDefaultMetrics = client.collectDefaultMetrics;
const register = new client.Registry();
//let register = new client.Registry();


// Create custom metrics
const customCounter = new client.Counter({
    name: "my_custom_counter",
    help: "Custom counter for my application",
});

// Create custom metrics
const userCounter = new client.Counter({
    name: "my_user_counter",
    help: "User counter for my application",
});

// Create custom metrics
const fileCounter = new client.Counter({
    name: "my_file_counter",
    help: "File counter for my application",
});

// Add your custom metric to the registry
register.registerMetric(customCounter);
register.registerMetric(userCounter);
register.registerMetric(fileCounter);

client.collectDefaultMetrics({
    app: 'node-application-monitoring-app',
    prefix: 'node_',
    timeout: 10000,
    gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5],
    register
});
// Create a route to expose /
app.get('/', (req, res) => {
    customCounter.inc();
 userCounter.inc();
 fileCounter.inc();
 console.log(register.metrics());
 res.send("test");
});

// Create a route to expose metrics
app.get('/metrics', async (req, res) => {
    res.setHeader('Content-Type', register.contentType);
    res.send(await register.metrics());
});

app.listen(8080, () => {
    console.log("Server is running on port 8080");
});