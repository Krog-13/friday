### Smart bot - Friday

---
| Bot realization with webhook, <b>asgi</b> server <em>aiohttp</em>

#### Development mode
* For the https server use <b>ngrok
* <code>ngrok http 8080</code>

#### Prod mode
> For production mode we use architecture aiohttp + nginx with self-signed [certificate](https://core.telegram.org/bots/self-signed),
> and set it in <em>bot</em> and <em>nginx</em> conf

As a server used VDS server with TLS support
- customization features nginx conf <em>(/etc/nginx/sites-enable/friday)</em>
- - listen 8443 ssl;