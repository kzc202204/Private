// Expressをrequire
var app = require('express')();
// httpモジュールをrequire
var http = require('http').Server(app);
var io = require('socket.io')(http);

// ディレクトリでindex.htmlをリク・レス
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Socket.IOをコネクト
io.on('connection', function(socket){
  console.log('a user connected (%s)', socket.request.connection.remoteAddress);
  // メッセージ処理
  socket.on('chat msg', function(msg){
    io.emit('chat res', msg);
  });
});

// ポートを3000番
http.listen(3000, function(){
  console.log('listening on *:3000');
});

