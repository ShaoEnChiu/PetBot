# PetBot(寵物 Line 機器人)

## 目的
使用 Line 機器人來控制寵物照護相關 IoT 裝置

## 使用者發送訊息控制 IoT 裝置
Line 機器人端 -> IoT 平台端 -> IoT 裝置端

## IoT 裝置回應訊息至使用者
IoT 裝置端 -> IoT 平台端 -> Line 機器人端

## IoT 裝置端
- LinkIt Smart 7688 開發板
- Python 讀/寫感測器資訊至雲端
- Arduino 讀/寫感測器

## IoT平台端
- 中華電信 IoT 智慧聯網大平台 納管感測器資訊
 
## Line 機器人端
- Heroku 提供 Https Webhook 介接 Line Bot
- Python 處理商業邏輯及讀寫 IoT 平台感測器資訊
- Line Bot 提供聊天 API 接口
