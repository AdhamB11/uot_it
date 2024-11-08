const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const ADMIN_USER_ID =1088297869; // استبدل هذا بمعرفك الحقيقي

// إعداد البوت باستخدام التوكن
const bot = new TelegramBot('7809146187:AAH5aL7EQeeC2lI_oe6FlihqdlZIZg9VjQU', { polling: true });
const userNumbersFile = "user_numbers.txt";

// وظيفة للتحقق من الرقم
function isValidNumber(number) {
  return number.length === 10 && /^\d+$/.test(number) && ["180", "181"].includes(number.slice(3, 6));
}

// بدء المحادثة
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "مرحبًا! من فضلك، أدخل رقم القيد الخاص بك.");
});

// معالجة رقم المستخدم
bot.on('message', (msg) => {
  const number = msg.text;
  const userId = msg.from.id;

  if (isValidNumber(number)) {
    let userNumbers = [];

    try {
      userNumbers = fs.readFileSync(userNumbersFile, 'utf8').trim().split('\n').map(line => line.split(','));
    } catch (error) {
      // إذا كان الملف غير موجود، نتابع العمل
    }

    const exists = userNumbers.some(entry => entry[0] === number && entry[1] !== String(userId));
    if (exists) {
      return bot.sendMessage(msg.chat.id, "هذا الرقم مستخدم من قبل مستخدم آخر.");
    }

    fs.appendFileSync(userNumbersFile, `${number},${userId}\n`);
    bot.sendMessage(msg.chat.id, `تم إضافة الرقم: ${number}`);
    showButtons(msg.chat.id);
  } else {
    bot.sendMessage(msg.chat.id, "رقم القيد غير صحيح. تأكد من أنه مكون من 10 أرقام وأن الأرقام الرابعة والخامسة والسادسة هي 180 أو 181.");
  }
});

// عرض الأرقام المخزنة للمسؤول
bot.onText(/\/list_numbers/, (msg) => {
  if (msg.from.id === ADMIN_USER_ID) {
    try {
      const userNumbers = fs.readFileSync(userNumbersFile, 'utf8').trim();
      bot.sendMessage(msg.chat.id, userNumbers ? الأرقام المستخدمة:\n${userNumbers} : "لا توجد أرقام مستخدمة.");
    } catch (error) {
      bot.sendMessage(msg.chat.id, "لم يتم العثور على ملف الأرقام.");
    }
  } else {
    bot.sendMessage(msg.chat.id, "ليس لديك إذن لاستخدام هذا الأمر.");
  }
});

// إظهار الأزرار
function showButtons(chatId) {
  const options = {
    reply_markup: {
      inline_keyboard: [
        [{ text: "مقدمة في البرمجة", callback_data: 'intro_programming' }],
        [{ text: "البرمجة الشيئية", callback_data: 'object_oriented' }],
        [{ text: "معمارية الحاسوب", callback_data: 'computer_architecture' }],
        [{ text: "تراكيب البيانات", callback_data: 'data_structures' }],
        [{ text: "مقدمة في قواعد البيانات", callback_data: 'db_intro' }],
        [{ text: "التحليل العددي", callback_data: 'numerical_analysis' }]
      ]
    }
  };
  bot.sendMessage(chatId, "اختر درسًا:", options);
}

// معالجة الأزرار
bot.on('callback_query', (query) => {
  bot.answerCallbackQuery(query.id, { text: You selected: ${query.data} });
});