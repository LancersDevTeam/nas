## 概要
Slackにピアボーナス機能を実装する.

## 使い方
### nasを送りたい時
**コマンドから送りたいとき**
`/nas! @送りたい相手 メッセージ`
このコマンドはどこからでも行うことができ、相手へのメッセージは専用の部屋に流されます。
botから自分に送られるメッセージも自分にしか見えないようになっているので、心配ないです。

**スタンプから送りたい時**
nasを送りたい相手のメッセージに対して`:eggplant:`スタンプを送ると、nasが送られます。
botや自分に対しては送っても反映されません。スタンプはどの部屋で押しても大丈夫です。
相手への通知は専用の部屋で送られます。


### 自分の残りnasを確認したいとき
`/nas!_st`
残りnasは自分にしか見えないので、どこで確認しても大丈夫です。
一週間に送れるnasは今のところ30に設定しています。

### その週のランキングを確認したいとき
`/nas!_rank`
このコマンドでその週のnasを送られた数のランキングを確認することができます。
現状ではnasが送られた全ての人のランキングを表示するようにしています。
例によって、このコマンドも自分にしか見えないので、どの部屋に送っても大丈夫です。

## スタンプを追加したい時

`stamp_settings.ini`に以下の形式で設定を追加してください。
[送りたいスタンプの名称]
nas_num = 1 #相手に送られるナスの数
confirm_message = "〇〇さんにnasを送ったよ！" #スタンプ送信時に表示されるメッセージ
send_message = "〇〇さんからnasをもらったよ！" #スタンプをもらった時に表示されるメッセージ
reject_message = "今週はもう〇〇さんにはnasを送れないよ！" #nasの上限に達している時、自分に送信されるメッセージ
is_private = 1 #そのスタンプを公開メッセージにするかどうか（1: 個人にしか見えない、0: 全体に公開される）

文章中で使用できる変数
nas_user_id : スタンプを送ったユーザのID
nas_user_name : スタンプを送ったユーザのnickname
receive_user_id : スタンプを送られたユーザのID
receive_user_name : スタンプを送られたユーザのnickname

## 使用技術
- AWS Lambda
- AWS DynamoDB
- AWS API Gateway
- AWS Cloudwatch logs
- Slack API
- Python

### DB構成
**nas**
- tip_user_id : Slackのuser id.primary key
- time_stamp : tipが動作した時刻。日付データでいいかな。
- tip_user_name : tipしたユーザの名前
- receive_user_id : tipされたユーザのuser id
- receive_user_name : tipされたユーザの名前
- tip_type : tipが行われた時の動作にリソース。messegeなのかstampなのか

### Lambdaの環境変数
- NAS_CHANNEL_ID : tip専用部屋のchannel id
- SLACK_BOT_USER_ACCESS_TOKEN : Slackのトークン
- SLACK_OAUTH_ACCESS_TOKEN : Slackのトークン
- TIP_LIMIT : 一週間のtip上限
