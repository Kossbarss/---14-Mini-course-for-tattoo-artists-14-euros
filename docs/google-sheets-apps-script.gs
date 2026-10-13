/**
 * Приймач заявок з попапа лендингу → рядок у Google-таблиці.
 *
 * Налаштування (5 хвилин):
 * 1. Створіть Google-таблицю → Розширення → Apps Script → вставте цей код → Зберегти.
 * 2. Розгорнути → Нове розгортання → тип «Веб-застосунок».
 *    Виконувати від імені: «Я». Хто має доступ: «Усі».
 * 3. Скопіюйте URL виду https://script.google.com/macros/s/AKfy.../exec
 *    і вставте в config.js → formEndpoint.
 * Після змін у коді потрібно робити «Нове розгортання» (URL залишається тим самим при «Керувати розгортаннями → Редагувати»).
 */
var SHEET_NAME = 'Заявки';
var HEADERS = ['Дата', 'Email', 'Телефон', 'Мова', 'Кнопка', 'utm_source', 'utm_medium', 'utm_campaign', 'Сторінка'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var data = {};
    try { data = JSON.parse(e.postData.contents); } catch (err) {}
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) {
      sh.appendRow(HEADERS);
      sh.setFrozenRows(1);
    }
    sh.appendRow([
      new Date(), clean(data.email), clean(data.phone), clean(data.lang), clean(data.source),
      clean(data.utm_source), clean(data.utm_medium), clean(data.utm_campaign), clean(data.page)
    ]);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

// Обрізає довжину й нейтралізує формули (=, +, -, @), щоб у таблиці не виконувався введений текст.
function clean(v) {
  var s = String(v == null ? '' : v).slice(0, 200);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
