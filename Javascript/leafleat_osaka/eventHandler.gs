// Google App Script source code
//スプレッドシートID
g_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

// 引数（例：?lati=データ1&long=データ2）
function doGet(e) {

  let result = 'OK';
  do{
    if (e.parameter == undefined) {
        result = 'Error: Parameter undefined';
        break;
    } 
    
    // クエリパラメータ作成
    const queryString = Object.keys(e.parameter)
      .map(key => `${key}=${encodeURIComponent(e.parameter[key])}`)
      .join('&');
      
    // プロパティに記録
    var props = PropertiesService.getScriptProperties();
    props.setProperty("query", queryString);

    // HTML表示
    var html = HtmlService.createTemplateFromFile('index');
    html.col=e.parameter.col;
    return html.evaluate();
  }while(false)
  
  // レスポンスとして結果を返す
  return ContentService.createTextOutput(result);
}

function getScriptURL()
{
    // Full-URL取得
    const baseUrl = ScriptApp.getService().getUrl();

    // フルURLを再構築(From プロパティ)
    var props = PropertiesService.getScriptProperties();
    var value = props.getProperty("query");
    return baseUrl + "?" + value;
}

function getErrorMessage(code)
{
  return "Error: " + code + '.';
}

function getNowDateTime() {
  var now = new Date();
  var timezone = "Asia/Tokyo";

  var date = Utilities.formatDate(now, timezone, "yyyy-MM-dd");
  var time = Utilities.formatDate(now, timezone, "HH:mm:ss");
  var datestr = date + " " + time;

  return datestr;
}

function doSetRecord2(lati, long, col, comment)
{
   // スプレッドシートのIDとシート名を指定
    var ss = SpreadsheetApp.openById(g_ID);
    var sheet = ss.getSheetByName('record');
    
    // 現在時刻の取得
    var datestr = getNowDateTime(); 

    // 引数を新しい行に追加
    sheet.appendRow([datestr, lati, long, col, comment]);
}

function doGetRecordJSON() {
  const sheet = SpreadsheetApp.openById(g_ID).getSheetByName('record');
  const data = sheet.getDataRange().getValues();

  // 1行目をキーとして使用（ヘッダー）
  const headers = data[0];
  let jsonData = [];

  try{
    for (let i = 1; i < data.length; i++) {
      let row = data[i];
      let rowData = {};
      for (let j = 0; j < headers.length; j++) {
        rowData[headers[j]] = row[j];
      }
      jsonData.push(rowData);
    }

    var json = JSON.stringify(jsonData);
    return json;
  } catch (e) {
    Logger.log("エラー:", e);
    throw new Error("サーバー処理中にエラーが発生しました：" + e.message);
  }
}

function doDeleteRecord(){
  const sheet = SpreadsheetApp.openById(g_ID).getSheetByName('record');
  const lastRow = sheet.getLastRow(); // 最終行を取得

  if (lastRow > 1) {
    sheet.deleteRows(2, lastRow - 1); // 2行目から末尾まで削除
  }
}
