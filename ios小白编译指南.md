# ios 小白编译指南

# 更新你的 mac os到最新版本。

## 关于mac系统的bug
APPID 账号最好关闭双重验证，不然mac的bug会导致无处输入验证码。

APPID 账号如果关联支付宝支付，会无法升级系统。在 app-store 界面也无法修改支付方式，需要到 itunes 里设置账户支付方式。

# 一定要使用 git clone 方式拉代码

# ios platform 编译bug：
执行 ` make iframework BUILDTYPE=Release `，死活提示找不到 toolchan.cmake 文件。
```
mkdir -p build/ios
(cd build/ios && cmake -G Xcode ../.. \
		-DCMAKE_TOOLCHAIN_FILE=../../platform/ios/toolchain.cmake \
		-DMBGL_PLATFORM=ios \
		-DMASON_PLATFORM=ios)
CMake Error at /usr/local/Cellar/cmake/3.10.3/share/cmake/Modules/CMakeDetermineSystem.cmake:100 (message):
  Could not find toolchain file: ../../platform/ios/toolchain.cmake
Call Stack (most recent call first):
  CMakeLists.txt:2 (project)
```
不知道何方bug，只好把 toolchain.cmake 改成绝对路径，手敲 cmake 命令：
```
cmake -G Xcode ../.. -DCMAKE_TOOLCHAIN_FILE=/Users/xx/mapbox/mapbox-gl-native/platform/ios/toolchain.cmake -DMBGL_PLATFORM=ios -DMASON_PLATFORM=ios
```
