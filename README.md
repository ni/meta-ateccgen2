# meta-ateccgen2

This layer provides support for the NI ATE Core Configurations Gen 2 distribution. The NI ATE Core Configurations Gen 2 distribution supplies a operating system that runs on NI ATE Core Configurations Gen 2 targets, and provides the flexibility and customization benefits of a Linux system.

About NI ATE Core Configurations
------------------------
To learn about NI ATE Core Configurations, visit [NI ATE Core Configurations].

Building the Layer
-----------

To build the meta-ateccgen2 layer, follow the instructions available on [Github].

llama.cpp
-----------

Both the minimal and proprietary images include the CPU-only llama.cpp tools
`llama-cli`, `llama-server`, and `llama-quantize`, pinned to upstream build b5046.
No model weights are bundled, and the server is not started automatically.
Provide a GGUF model with a license and memory footprint suitable for the target.

Build the image in the configured Yocto build environment:

```sh
bitbake ateccgen2-proprietary-image
```

On the target, run inference with a model stored on persistent storage:

```sh
llama-cli -m /path/to/model.gguf -p "Hello" -n 64 -c 2048
llama-server -m /path/to/model.gguf --host 127.0.0.1 --port 8080 -c 2048
```

Contact
----
Email [licensing@ni.com]

[NI ATE Core Configurations]:https://www.ni.com/en-us/shop/electronic-test-instrumentation/what-is-ate-core-configurations.html
[Github]:https://www.github.com/ni/ateccgen2-manifest
[licensing@ni.com]:mailto:licensing@ni.com
