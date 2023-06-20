TARGET_CC_ARCH += "${LDFLAGS}"

DEPENDS += " protobuf-native protobuf grpc grpc-native libgpiod "

inherit cmake
