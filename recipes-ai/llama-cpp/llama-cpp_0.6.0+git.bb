SUMMARY = "CPU-based LLM inference with llama.cpp"
DESCRIPTION = "llama.cpp command-line inference, HTTP server, and GGUF quantization tools"
HOMEPAGE = "https://github.com/ggml-org/llama.cpp"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=223b26b3c1143120c87e2b13111d3e99"

SRC_URI = "git://github.com/ggml-org/llama.cpp.git;protocol=https;nobranch=1"
SRCREV = "fcac19079f3f2985fe74ed845f0880e7e9a8030a"

S = "${WORKDIR}/git"

inherit cmake

EXTRA_OECMAKE = " \
    -DBUILD_SHARED_LIBS=OFF \
    -DGGML_NATIVE=OFF \
    -DGGML_OPENMP=OFF \
    -DGGML_LLAMAFILE=OFF \
    -DGGML_BLAS=OFF \
    -DGGML_CUDA=OFF \
    -DGGML_VULKAN=OFF \
    -DGGML_OPENCL=OFF \
    -DLLAMA_OPENSSL=OFF \
    -DLLAMA_USE_PREBUILT_UI=OFF \
    -DLLAMA_BUILD_UI=OFF \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_TOOLS=ON \
    -DLLAMA_BUILD_EXAMPLES=ON \
    -DLLAMA_BUILD_SERVER=ON \
"

OECMAKE_TARGET_COMPILE = "llama-cli llama-server llama-quantize"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/bin/llama-cli ${D}${bindir}/llama-cli
    install -m 0755 ${B}/bin/llama-server ${D}${bindir}/llama-server
    install -m 0755 ${B}/bin/llama-quantize ${D}${bindir}/llama-quantize
}