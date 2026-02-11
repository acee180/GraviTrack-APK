[app]

# App title
title = GraviTrack

# Package name
package.name = gravitrack

# Package domain (reverse domain notation)
package.domain = org.gravitrack

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 1.0

# Application requirements
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

# Application permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,VIBRATE

# Application icon (optional - create a 512x512 PNG)
#icon.filename = %(source.dir)s/icon.png

# Supported orientations
orientation = portrait

# Android API to use
android.api = 31

# Minimum API your app will support
android.minapi = 21

# Android SDK version to use
android.sdk = 31

# Android NDK version to use
android.ndk = 25b

# Android NDK directory (leave blank for auto-detection)
android.ndk_path = 

# Android SDK directory (leave blank for auto-detection)
android.sdk_path = 

# p4a (python-for-android) fork to use
p4a.fork = kivy

# p4a branch to use
p4a.branch = master

# The log level of the application
log_level = 2

# Application will be fullscreen
fullscreen = 0

# Presplash background color
#android.presplash_color = #FFFFFF

# Adaptive icon (optional)
#android.adaptive_icon.foreground = %(source.dir)s/data/icon_fg.png
#android.adaptive_icon.background = #ffffff

# Gradle dependencies
android.gradle_dependencies = 

# Add Java compilation options
android.add_compile_options = 

# Copy libraries
android.add_libs_armeabi_v7a = 
android.add_libs_arm64_v8a = 

# Blacklist of non-existing files
android.whitelist = 

[buildozer]

# Display warning if buildozer is run as root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Binary directory
bin_dir = ./bin

# Log level
log_level = 2
