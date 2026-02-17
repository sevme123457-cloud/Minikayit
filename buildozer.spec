[app]
title = MiniKayit
package.name = minikayit
package.domain = org.sevme
source.dir = .
source.include_exts = py,png,jpg,kv,txt

version = 0.1
requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1