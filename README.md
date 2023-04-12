> Note: Still under development, use at your own risk

# aifw!
![DALL·E 2023-04-12 16 04 32 - computer on fire in space, digital art](https://user-images.githubusercontent.com/97220909/231605057-609cddab-2add-4575-840c-4b47a0dd4a9e.png)


An AI powered firewall designed to detect malicious HTTP requests and decide weather to process them or not.

## Python CLI Reference
**Syntax:**
```bash
python -m aifw [-h] [-t | -s target port]
```

- `options`
  - `-s` or `--serve` to start the proxy server
  - `-t` or `--train` to train the model

These options are mutually exclusive

## Training the Models
*Note: Must have python3 installed on local machine and added to PATH*

### With Bash
Call `train.sh`

Example:
```bash
train.sh
```

### With Python Module
Example:
```bash
python3 -m aifw -t
```

## Using the Firewall
There are two main ways to use aifw, as a proxy server and as a middleware for Flask.

### As Flask Middleware
*Note: Model must be trained before starting proxy server*
```python
from aifw import DetectorMiddleware
...
app.wsgi_app = DetectorMiddleware(app.wsgi_app)
...
```

### As Proxy Server
*Note: Must have python installed on local machine and added to PATH*<br>
*Note: Model must be trained before starting proxy server*

#### **With Bash**
Call `proxy.sh` with paramaters `target` and  `port`
- `target` is the proxy destination
  - defaults to `http://localhost:8080`
- `port` is the local port to run the server on
  - defaults to 5000

Example:
```bash
proxy.sh [target] [port]
```

## Known Limitations
- False positives
    - SQL keywords in the query string or body make the model think the request is an attack
        - `/?q=select+an+option`
        - There is no context
    - Javascript keywords trigger the detection regardless of context
        - `/?q=alert+me+of+your+presence`
    - etc.
- Hangs after verifying a POST request

## Future
- [ ] Rework the whole model from the beginning
- [ ] Use NEAT algorithm based on Tensorflow or other popular AI database
- [ ] Consider re-writing parts in Rust, Go, or other languages for performance, being cross-platform, and ease of development
- [ ] Make cross-platform executable with configuration options
- [ ] Docker container for distributed systems?
